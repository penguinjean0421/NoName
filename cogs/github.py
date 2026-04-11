import discord
from discord import app_commands
from discord.ext import commands
from typing import List

class Github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.github_data = {
            "2358006": {
                "title": "📂 과제 아카이브",
                "description": "과제는 여기에 모아뒀어요.",
                "aliases": ["과제", "레포트", "이삼오팔공공육", "2358006"]
            },
            "penguinjean0421": {
                "title": "📂 penguinjean's Github",
                "description": "수업시간에 심심해서 Slave를 탄생 시킨 사람의 깃허브",
                "aliases": ["penguinjean", "jean", "펭귄진", "펭귄청바지"]
            },
        }

    # --- 공통 임베드 송신 로직 ---
    async def send_github_embed(self, interaction: discord.Interaction, name: str):
        data = self.github_data[name]

        embed = discord.Embed(
            title=data['title'],
            description=data['description'],
            color=0x2b3137
        )
        embed.add_field(name="👤 GitHub ID", value=f"`{name}`", inline=True)
        embed.add_field(
            name="🔗 Link",
            value=f"[저장소 방문하기](https://github.com/{name})",
            inline=True
        )

        embed.set_thumbnail(
            url="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
        )
        embed.set_footer(
            text=f"요청자: {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )

        await interaction.response.send_message(embed=embed)

    # --- 슬래시 명령어 ---
    @app_commands.command(name="github", description="등록된 GitHub 저장소 정보를 조회합니다.")
    @app_commands.describe(keyword="조회할 키워드를 입력하거나 선택하세요. (예: 과제, 펭귄진)")
    async def github_search(self, interaction: discord.Interaction, keyword: str):
        target_name = None
        clean_text = keyword.lower().replace(" ", "")

        for key, info in self.github_data.items():
            if clean_text == key.lower() or clean_text in info["aliases"]:
                target_name = key
                break

        if target_name:
            await self.send_github_embed(interaction, target_name)
        else:
            embed = discord.Embed(
                description=f"🔍 '{keyword}'에 해당하는 정보를 찾을 수 없습니다.",
                color=0xE74C3C
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    # --- 자동 완성(Autocomplete) 로직 ---
    @github_search.autocomplete('keyword')
    async def github_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        choices = []
        for key, info in self.github_data.items():
            for alias in [key] + info["aliases"]:
                if current.lower() in alias.lower():
                    choices.append(app_commands.Choice(name=alias, value=alias))
                    break
        
        return choices[:25]

async def setup(bot: commands.Bot):
    await bot.add_cog(Github(bot))