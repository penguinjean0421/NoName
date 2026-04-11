import os
import re
import time
import json
from urllib.parse import quote
from typing import Literal

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

class LOLStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("RIOT_API_KEY")
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.cache_file = os.path.join(base_path, "..", "tracking.json")

        # 플랫폼 및 지역 매핑
        self.platform_alias = {
            'kr': 'kr', 'jp': 'jp1', 'na': 'na1', 'euw': 'euw1', 'eune': 'eun1',
            'br': 'br1', 'lan': 'la1', 'las': 'la2', 'tr': 'tr1', 'ru': 'ru',
            'oc': 'oc1', 'ph': 'ph2', 'sg': 'sg2', 'th': 'th2', 'vn': 'vn2'
        }
        self.region_map = {
            'kr': 'asia', 'jp1': 'asia',
            'na1': 'americas', 'br1': 'americas', 'la1': 'americas', 'la2': 'americas',
            'euw1': 'europe', 'eun1': 'europe', 'tr1': 'europe', 'ru': 'europe',
            'oc1': 'sea', 'ph2': 'sea', 'sg2': 'sea', 'th2': 'sea', 'vn2': 'sea'
        }

        if not os.path.exists(self.cache_file):
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump({}, f)

        if not self.clean_cache_task.is_running():
            self.clean_cache_task.start()

    @tasks.loop(minutes=10)
    async def clean_cache_task(self):
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            current_time = time.time()
            new_data = {k: v for k, v in data.items() if current_time - v['timestamp'] < 1800}
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"캐시 정리 중 오류 발생: {e}")

    async def fetch_riot_data(self, platform, name, tag):
        routing = self.region_map.get(platform, 'asia')
        headers = {"X-Riot-Token": self.api_key}
        async with aiohttp.ClientSession() as session:

            # 1. Account-V1: PUUID 획득
            acc_url = (
                f"https://{routing}.api.riotgames.com/riot/account/v1/"
                f"accounts/by-riot-id/{quote(name)}/{quote(tag)}"
            )
            async with session.get(acc_url, headers=headers) as resp:
                if resp.status != 200:
                    return None
                acc_data = await resp.json()
                puuid = acc_data['puuid']

            # 2. Summoner-V4: 레벨 정보
            sum_url = f"https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
            async with session.get(sum_url, headers=headers) as resp:
                if resp.status != 200:
                    return None
                sum_data = await resp.json()

            # 3. League-V4: 랭크 정보
            league_url = f"https://{platform}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
            async with session.get(league_url, headers=headers) as resp:
                if resp.status != 200:
                    return None
                league_data = await resp.json()

            res = {
                "level": sum_data.get('summonerLevel', 0),
                "icon": sum_data.get('profileIconId', 1),
                "solo": {"tier": "Unranked", "lp": 0, "w": 0, "l": 0},
                "flex": {"tier": "Unranked", "lp": 0, "w": 0, "l": 0}
            }
            for entry in league_data:
                info = {
                    "tier": f"{entry['tier']} {entry['rank']}",
                    "lp": entry['leaguePoints'],
                    "w": entry['wins'],
                    "l": entry['losses']
                }
                if entry['queueType'] == 'RANKED_SOLO_5x5':
                    res['solo'] = info
                elif entry['queueType'] == 'RANKED_FLEX_SR':
                    res['flex'] = info
            return res

    @app_commands.command(name="lol", description="리그 오브 레전드 소환사의 전적을 조회합니다.")
    @app_commands.describe(
        region="조회할 서버 지역 (기본: KR)",
        summoner_id="소환사명#태그 입력 (예: Hide on bush#KR1)",
        refresh="실시간 데이터 강제 갱신 여부"
    )
    async def lol_stats(
        self, 
        interaction: discord.Interaction, 
        region: Literal["kr", "na", "euw", "jp", "br"] = "kr",
        summoner_id: str=None, 
        refresh: bool = False
    ):
        # 1. 입력값 검증
        if "#" not in summoner_id:
            return await interaction.response.send_message("❌ 정확한 ID 형식이 아닙니다. `이름#태그` 형태로 입력해주세요.", ephemeral=True)

        await interaction.response.defer() # API 호출을 위한 대기 처리

        platform = self.platform_alias.get(region, region)
        cache_key = f"lol {platform}:{summoner_id.replace(' ', '').lower()}"
        
        # 2. 캐시 로드
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except:
            cache = {}

        current_time = time.time()
        data = None
        footer_text = ""

        # 캐시 확인 (갱신 요청이 아니고 25분 이내 데이터일 때)
        if not refresh and cache_key in cache:
            if current_time - cache[cache_key]['timestamp'] < 1500:
                data = cache[cache_key]['data']
                footer_text = "캐시 데이터 사용 중"

        # 3. 실시간 데이터 가져오기
        if data is None:
            try:
                name, tag = summoner_id.rsplit("#", 1)
                data = await self.fetch_riot_data(platform, name.strip(), tag.strip())
            except Exception as e:
                print(f"LoL API 오류: {e}")
                data = None

            if not data:
                return await interaction.followup.send("❌ 소환사를 찾을 수 없습니다. 이름과 태그를 다시 확인해주세요.")

            # 신규 데이터 캐시 저장
            cache[cache_key] = {"timestamp": current_time, "data": data}
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=4)
            footer_text = "실시간 데이터 업데이트 완료"

        # 4. 임베드 구성
        opgg_region = re.sub(r'\d+', '', platform)
        encoded_id = quote(summoner_id.replace('#', '-'))
        opgg_url = f"https://www.op.gg/summoners/{opgg_region}/{encoded_id}"

        embed = discord.Embed(title=f"🎮 [{region.upper()}] {summoner_id} (Lv.{data['level']})", color=0x1ABC9C)
        embed.set_thumbnail(url=f"https://ddragon.leagueoflegends.com/cdn/14.6.1/img/profileicon/{data['icon']}.png")

        # 랭크 정보 필드 추가 함수
        def add_rank_field(name, stats, emoji):
            total = stats['w'] + stats['l']
            wr = round(stats['w'] / total * 100, 1) if total > 0 else 0
            val = f"**{stats['tier']}**\n{stats['lp']} LP\n{stats['w']}승 {stats['l']}패 ({wr}%)"
            embed.add_field(name=f"{emoji} {name}", value=val, inline=True)

        add_rank_field("솔로 랭크", data['solo'], "🏆")
        add_rank_field("자유 랭크", data['flex'], "⚔️")
        
        embed.add_field(name="🔗 자세한 전적 (OP.GG)", value=f"[전적 보러가기]({opgg_url})", inline=False)
        embed.set_footer(text=footer_text)
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LOLStats(bot))