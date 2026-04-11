import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional, Literal

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_data = {
            "welcome": {
                "name": "Slave",
                "greeting": "서버에 초대해 주셔서 감사합니다!\n",
                "summary": "즐거운 서버 활동을 돕기 위한 주요 명령어들을 안내해 드립니다.\n",
            },
        }

        self.credit_data = {
            "credit": {
                "bot_name": "Slave",
                "developer": "penguinjean0421",
                "illustrator": "aram",
                "supporter": "목대 겜소과 친목 디코",
            },
        }

    # --- 공통 임베드 생성 메서드 (재사용 가능) ---

    def create_welcome_embed(self) -> discord.Embed:
        data = self.help_data["welcome"]
        embed = discord.Embed(
            title=f"👋 {data['name']} 입니다.",
            description=f"{data['greeting']}{data['summary']}",
            color=0x5d2b90
        )
        embed.add_field(name="🆔 명령어 방식", value="`모든 명령어는 슬래시(/)를 사용합니다.`", inline=False)
        embed.add_field(name="📖 도움말", value="`/help`, `/help 카테고리:관리자`", inline=True)
        embed.add_field(name="✨ 유틸리티", value="`/choose`, `/menu`", inline=True)
        embed.add_field(name="🎮 게임 전적", value="`/lol`, `/pubg`", inline=True)
        embed.add_field(name="⚙️ 서버 관리", value="상세 명령어는 `/help 카테고리:관리자` 참고", inline=False)
        embed.add_field(name="📚 과제도움", value="`/github`", inline=False)
        embed.add_field(
            name="💻 소스보기",
            value=f"[`GitHub Repository`](https://github.com/{self.credit_data['credit']['developer']}/{data['name']})",
            inline=False
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text="상세 도움말은 /help를 입력하세요.")
        return embed

    def create_admin_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title="🛠️ 서버 관리자 명령어 가이드",
            description="서버 관리 권한이 있는 멤버만 사용 가능한 명령어입니다.",
            color=0xE74C3C
        )
        embed.add_field(
            name="🔇 음성 제재",
            value="`/mute`, `/unmute`, `/vckick`",
            inline=True
        )
        embed.add_field(
            name="🔨 서버 제재",
            value="`/timeout`, `/kick`, `/ban`, `/unban`",
            inline=True
        )
        embed.add_field(
            name="⚙️ 시스템 설정",
            value="`/set`, `/reset`",
            inline=True
        )
        embed.add_field(
            name="🎫 티켓 시스템",
            value="`/open`, `/close`, `/answer`", 
            inline=False,
        )
        embed.set_footer(text="시간 단위: s(초), m(분), h(시간), d(일) | 예: 10m, 1d")
        return embed

    # --- 이벤트 리스너 ---

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        # Settings 또는 Logger Cog에서 채널 가져오기 시도
        system_cog = self.bot.get_cog('Settings') or self.bot.get_cog('Logger')
        channel = None
        if system_cog and hasattr(system_cog, 'get_log_channel'):
            channel = system_cog.get_log_channel(guild)
            
        target = channel or guild.system_channel
        if target and target.permissions_for(guild.me).send_messages:
            await target.send(embed=self.create_welcome_embed())

    # --- 슬래시 명령어 ---

    @app_commands.command(name="help", description="봇의 사용 방법 및 명령어 목록을 확인합니다.")
    @app_commands.describe(카테고리="조회할 도움말 카테고리를 선택하세요.")
    async def help_slash(
        self, 
        interaction: discord.Interaction, 
        카테고리: Optional[Literal["일반", "관리자"]] = "일반"
    ):
        if 카테고리 == "관리자":
            # 관리자 권한 확인 (선택 사항)
            if not interaction.user.guild_permissions.administrator:
                return await interaction.response.send_message("❌ 관리자 도움말은 관리자만 열람할 수 있습니다.", ephemeral=True)
            embed = self.create_admin_embed()
        else:
            embed = self.create_welcome_embed()
            
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="credit", description="봇 개발진 및 도움을 주신 분들을 확인합니다.")
    async def credit_slash(self, interaction: discord.Interaction):
        data = self.credit_data["credit"]
        embed = discord.Embed(
            title=f"Thanks for using {data['bot_name']}",
            description=f"{data['bot_name']}를 함께 만들어주신 분들입니다.",
            color=0x5d2b90
        )
        embed.add_field(
            name="👤 Developer",
            value=f"[@{data['developer']}](https://github.com/{data['developer']})",
            inline=True
        )
        embed.add_field(name="🎨 Illustrator", value=f"@{data['illustrator']}", inline=True)
        embed.add_field(name="🤝 Supporter", value=data['supporter'], inline=False)
        embed.add_field(
            name="🔗 Source Code",
            value=f"[GitHub Repository](https://github.com/{data['developer']}/{data['bot_name']})",
            inline=False
        )
        embed.add_field(name="📧 Contact", value=f"`{data['developer']}@gmail.com`", inline=False)

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=f"© 2026 {data['developer']} All rights reserved.")

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Information(bot))
    
    
        # 0x5d2b90 0x007acc