import json
import os
import time
from urllib.parse import quote
from typing import Literal

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class PUBGStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("PUBG_API_KEY")
        self.base_url = "https://api.pubg.com/shards"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/vnd.api+json"
        }
        self.current_season = None
        self.main_color = 0xD4AC0D

        base_path = os.path.dirname(os.path.abspath(__file__))
        self.cache_file = os.path.join(base_path, "..", "tracking.json")

        # 봇 시작 시 시즌 정보 로드
        self.bot.loop.create_task(self.load_current_season())

    async def load_current_season(self):
        """API를 통해 현재 활성화된 시즌 ID를 자동으로 가져옵니다."""
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{self.base_url}/steam/seasons"
                async with session.get(url, headers=self.headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        seasons = data.get('data', [])
                        for season in seasons:
                            if season['attributes'].get('isCurrentSeason'):
                                self.current_season = season['id']
                                print(f"✅ PUBG 현재 시즌 로드 완료: {self.current_season}")
                                return
                        if seasons:
                            self.current_season = seasons[-1]['id']
        except Exception as e:
            print(f"❌ PUBG 시즌 정보 로드 중 오류: {e}")

    async def fetch_pubg_data(self, platform, nickname):
        if not self.current_season:
            await self.load_current_season()
            if not self.current_season:
                return {"error": "시즌 정보를 불러올 수 없습니다."}
        async with aiohttp.ClientSession() as session:
            # 1. Player ID 조회
            player_url = f"{self.base_url}/{platform}/players?filter[playerNames]={quote(nickname)}"
            async with session.get(player_url, headers=self.headers) as resp:
                if resp.status == 404:
                    return {"error": "플레이어를 찾을 수 없습니다."}
                if resp.status != 200:
                    return {"error": f"API 오류 ({resp.status})"}
                player_json = await resp.json()
                player_id = player_json['data'][0]['id']

            # 2. Season Stats 조회
            stats_url = f"{self.base_url}/{platform}/players/{player_id}/seasons/{self.current_season}"
            async with session.get(stats_url, headers=self.headers) as resp:
                if resp.status != 200:
                    return {"error": "전적 데이터를 가져올 수 없습니다."}
                stats_json = await resp.json()
            
            modes = stats_json['data']['attributes']['gameModeStats']

            # 1. 사용 가능한 모든 스쿼드 모드 후보군 정의
            # 순서대로 확인하며 플레이 기록(roundsPlayed)이 있는 것을 선택
            possible_modes = ['squad', 'squad-fpp', 'solo', 'solo-fpp', 'duo', 'duo-fpp']
            squad = {}
            
            for mode in possible_modes:
                data = modes.get(mode, {})
                if data and data.get('roundsPlayed', 0) > 0:
                    squad = data
                    break # 기록이 있는 첫 번째 모드를 선택

            if not squad or squad.get('roundsPlayed', 0) == 0:
                return {"error": "이번 시즌 플레이 기록이 없습니다. (일반 매치 기준)"}
            
            rounds = squad['roundsPlayed']
            wins = squad['wins']
            kills = squad['kills']
            damage = squad['damageDealt']
            return {
                "nickname": nickname,
                "platform": platform,
                "adr": round(damage / rounds, 1),
                "kd": round(kills / (rounds - wins) if (rounds - wins) > 0 else kills, 2),
                "win_rate": round((wins / rounds) * 100, 1),
                "top10": round((squad['top10s'] / rounds) * 100, 1),
                "rounds": rounds
            }

    @app_commands.command(name="pubg", description="배틀그라운드 플레이어의 시즌 전적을 조회합니다.")
    @app_commands.describe(
        platform="플랫폼 선택 (기본: Steam)",
        nickname="조회할 플레이어의 닉네임",
        refresh="실시간 데이터 강제 갱신 여부"
    )
    async def pubg_stats(
        self, 
        interaction: discord.Interaction, 
        platform: Literal["steam", "kakao"] = "steam",
        nickname: str = None,
        refresh: bool = False
    ):
        await interaction.response.defer() # API 응답 대기를 위해 먼저 지연 응답

        cache_key = f"pubg {platform}:{nickname.lower().replace(' ', '')}"
        
        # 캐시 로드
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except:
            cache = {}

        current_time = time.time()
        data = None
        footer_text = ""

        # 캐시 확인
        if not refresh and cache_key in cache:
            if current_time - cache[cache_key]['timestamp'] < 1800:
                data = cache[cache_key]['data']
                footer_text = "캐시 데이터 사용 중"

        if data is None:
            data = await self.fetch_pubg_data(platform, nickname)
            
            if "error" in data:
                return await interaction.followup.send(f"❌ {data['error']}")

            # 캐시 저장
            cache[cache_key] = {"timestamp": current_time, "data": data}
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(cache, f, ensure_ascii=False, indent=4)
            footer_text = "실시간 데이터 업데이트 완료"

        # 임베드 구성
        embed = discord.Embed(
            title=f"🔫 PUBG 전적: {data['nickname']}",
            color=self.main_color
        )
        embed.add_field(name="플랫폼", value=platform.upper(), inline=True)
        embed.add_field(name="플레이 횟수", value=f"{data['rounds']}회", inline=True)
        embed.add_field(name="평균 딜량 (ADR)", value=f"**{data['adr']}**", inline=True)
        embed.add_field(name="킬데스 (K/D)", value=f"**{data['kd']}**", inline=True)
        embed.add_field(name="승률", value=f"{data['win_rate']}%", inline=True)
        embed.add_field(name="TOP 10", value=f"{data['top10']}%", inline=True)

        dak_url = f"https://dak.gg/pubg/profile/{platform}/{quote(data['nickname'])}"
        embed.add_field(
            name="🔗 상세 전적 (DAK.GG)",
            value=f"[클릭하여 이동]({dak_url})",
            inline=False
        )
        embed.set_footer(text=footer_text)
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(PUBGStats(bot))