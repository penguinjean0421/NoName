import json
import os
import time

import aiohttp
import discord
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
                # steam 샤드를 기준으로 시즌 목록 조회
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
                            print(f"⚠️ 현재 시즌 태그를 찾지 못해 마지막 시즌으로 설정: {self.current_season}")
                    else:
                        print(f"❌ PUBG 시즌 로드 실패 (Status: {resp.status})")
        except Exception as e:
            print(f"❌ 시즌 정보를 가져오는 중 오류 발생: {e}")

    @commands.command(name="pubg")
    async def pubg_stats(self, ctx, plat_or_nick: str, *, nickname: str = None, mode: str = "squad"):
        valid_platforms = ["steam", "kakao", "psn", "xbox", "stadia"]

        if plat_or_nick.lower() in valid_platforms:
            platform = plat_or_nick.lower()
            target_nick = nickname
        else:
            platform = "steam"
            target_nick = f"{plat_or_nick} {nickname if nickname else ''}".strip()
        dak_url = f"https://dak.gg/pubg/profile/{platform}/{target_nick}"
        
        if not target_nick:
            embed = discord.Embed(
                description="💡 사용법: `!pubg 닉네임` 또는 `!pubg kakao 닉네임`",
                color=0x95A5A6
            )
            return await ctx.send(embed=embed)

        async with aiohttp.ClientSession() as session:
            try:
                # 1. 플레이어 ID 조회
                player_url = f"{self.base_url}/{platform}/players?filter[playerNames]={target_nick}"
                async with session.get(player_url, headers=self.headers) as resp:
                    if resp.status != 200:
                        await ctx.send(f"[{platform.upper()}] **{nickname}**님을 찾을 수 없습니다. (에러 {resp.status})")
                        return
                    player_data = await resp.json()
                    player_id = player_data['data'][0]['id']

                # 2. 전적 데이터 조회 (Lifetime)
                stats_url = f"{self.base_url}/{platform}/players/{player_id}/seasons/lifetime"
                async with session.get(stats_url, headers=self.headers) as resp:
                    if resp.status != 200:
                        await ctx.send("전적 데이터를 불러오는 데 실패했습니다.")
                        return
                    stats_data = await resp.json()

                # 3. 데이터 파싱
                game_stats = stats_data['data']['attributes']['gameModeStats'].get(mode.lower(), {})
                
                if not game_stats or game_stats.get('roundsPlayed', 0) == 0:
                    await ctx.send(f"**{nickname}**님의 `{mode}` 모드 데이터가 존재하지 않습니다.")
                    return

                kills = game_stats.get('kills', 0)
                wins = game_stats.get('wins', 0)
                rounds = game_stats.get('roundsPlayed', 0)
                damage = game_stats.get('damageDealt', 0)
                
                kd = round(kills / (rounds - wins), 2) if (rounds - wins) > 0 else kills
                avg_dmg = int(damage / rounds)

                # 4. Embed 생성
                embed = discord.Embed(title=f"PUBG 전적: {target_nick}", color=0xF1C40F)
                embed.add_field(name="플랫폼", value=platform.upper(), inline=True)
                embed.add_field(name="모드", value=mode.upper(), inline=True)
                embed.add_field(name="판수", value=f"{rounds}회", inline=True)
                embed.add_field(name="승리", value=f"{wins}회", inline=True)
                embed.add_field(name="K/D", value=f"**{kd}**", inline=True)
                embed.add_field(name="평균 딜량", value=f"{avg_dmg}", inline=True)
                embed.add_field(name="🔗 상세 전적 (DAK.GG)", value=f"[클릭하여 이동]({dak_url})", inline=False)
                embed.set_footer(text=f"{platform.upper()} / Lifetime Stats")

                await ctx.send(embed=embed)

            except Exception as e:
                print(f"[Cog Error] {e}")
                await ctx.send("전적 조회 중 오류가 발생했습니다.")

# 이 함수가 있어야 main.py에서 로드할 수 있습니다.
async def setup(bot):
    await bot.add_cog(PUBGStats(bot))