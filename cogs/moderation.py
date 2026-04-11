import asyncio
import re
from datetime import timedelta
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def parse_time(self, time_str: str):
        """시간 문자열(s, m, h, d)을 초 단위 정수로 변환"""
        if not time_str:
            return None
        if time_str.isdigit():
            return int(time_str)
        match = re.match(r"(\d+)([smhd])", time_str.lower())
        if not match:
            return None
        amount, unit = int(match.group(1)), match.group(2)
        unit_map = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        return amount * unit_map[unit]

    # --- 처벌(Sanction) 명령어 ---

    @app_commands.command(name="mute", description="음성 채널에서 대상의 마이크를 차단합니다.")
    @app_commands.describe(member="차단할 멤버", time="차단 시간 (예: 10m, 1h / 미입력 시 무기한)")
    @app_commands.checks.has_permissions(administrator=True)
    async def server_mute(self, interaction: discord.Interaction, member: discord.Member, time: Optional[str] = None):
        if not member.voice:
            return await interaction.response.send_message("❌ 대상이 음성 채널에 있지 않습니다.", ephemeral=True)

        seconds = self.parse_time(time) if time else None
        await member.edit(mute=True, reason=f"실행자: {interaction.user} ({time or '무기한'})")

        embed = discord.Embed(description=f"🔇 {member.mention} 마이크 차단 ({time or '무기한'})", color=0xE74C3C)
        await interaction.response.send_message(embed=embed)
        logger = self.bot.get_cog('Logger')
        if logger: await logger.send_log(interaction.guild, embed, type="punish")

        if seconds:
            await asyncio.sleep(seconds)
            if member.voice:
                await member.edit(mute=False)
                unmute_embed = discord.Embed(
                    description=f"🔊 {member.mention} 뮤트 해제 (시간 종료)",
                    color=0x2ECC71
                )
                if logger: await logger.send_log(interaction.guild, unmute_embed, type="punish")

    @app_commands.command(name="unmute", description="음성 채널 마이크 차단을 해제합니다.")
    @app_commands.checks.has_permissions(administrator=True)
    async def server_unmute(self, interaction: discord.Interaction, member: discord.Member):
        if not member.voice:
            return await interaction.response.send_message("❌ 대상이 음성 채널에 있지 않습니다.", ephemeral=True)

        await member.edit(mute=False)
        embed = discord.Embed(description=f"🔊 {member.mention} 마이크 차단 해제", color=0x2ECC71)
        await interaction.response.send_message(embed=embed)
        logger = self.bot.get_cog('Logger')
        if logger: await logger.send_log(interaction.guild, embed, type="punish")

    @app_commands.command(name="deafen", description="음성 채널에서 대상의 헤드셋(소리)을 차단합니다.")
    @app_commands.describe(member="차단할 멤버", time="차단 시간 (예: 10m, 1h / 미입력 시 무기한)")
    @app_commands.checks.has_permissions(administrator=True)
    async def server_deafen(self, interaction: discord.Interaction, member: discord.Member, time: Optional[str] = None):
        if not member.voice:
            return await interaction.response.send_message("❌ 대상이 음성 채널에 있지 않습니다.", ephemeral=True)

        seconds = self.parse_time(time) if time else None
        await member.edit(deafen=True, reason=f"실행자: {interaction.user} ({time or '무기한'})")

        embed = discord.Embed(description=f"🔇 {member.mention} 헤드셋 차단 ({time or '무기한'})", color=0xE74C3C)
        await interaction.response.send_message(embed=embed)
        logger = self.bot.get_cog('Logger')
        if logger: await logger.send_log(interaction.guild, embed, type="punish")

        if seconds:
            await asyncio.sleep(seconds)
            if member.voice:
                await member.edit(deafen=False)
                log_embed = discord.Embed(
                    description=f"🔊 {member.mention} 헤드셋 차단 해제 (시간 종료)",
                    color=0x2ECC71
                )
                if logger: await logger.send_log(interaction.guild, log_embed, type="punish")

    @app_commands.command(name="undeafen", description="음성 채널 헤드셋 차단을 해제합니다.")
    @app_commands.describe(member="해제할 멤버")
    @app_commands.checks.has_permissions(administrator=True)
    async def server_undeafen(self, interaction: discord.Interaction, member: discord.Member):
        if not member.voice:
            return await interaction.response.send_message("❌ 대상이 음성 채널에 있지 않습니다.", ephemeral=True)

        await member.edit(deafen=False)
        embed = discord.Embed(description=f"🔊 {member.mention} 헤드셋 차단 해제", color=0x2ECC71)
        await interaction.response.send_message(embed=embed)
        
        logger = self.bot.get_cog('Logger')
        if logger: await logger.send_log(interaction.guild, embed, type="punish")

    @app_commands.command(name="vckick", description="음성 채널에서 멤버를 강제 퇴장시킵니다.")
    @app_commands.describe(member="퇴장시킬 멤버", reason="퇴장 사유")
    @app_commands.checks.has_permissions(administrator=True)
    async def server_vckick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "사유 없음"):
        if not member.voice:
            return await interaction.response.send_message("❌ 대상이 음성 채널에 있지 않습니다.", ephemeral=True)

        await member.move_to(None, reason=f"실행자: {interaction.user} | {reason}")
        embed = discord.Embed(
            title="👟 음성 강제 퇴장",
            description=f"{member.mention} 퇴장됨\n사유: {reason}",
            color=0xE74C3C
        )
        await interaction.response.send_message(embed=embed)
        logger = self.bot.get_cog('Logger')
        if logger: await logger.send_log(interaction.guild, embed, type="punish")

    @app_commands.command(name="timeout", description="멤버에게 타임아웃(채팅 금지)을 적용합니다.")
    @app_commands.describe(member="대상 멤버", time="시간 (예: 10m, 1h)", reason="사유")
    @app_commands.checks.has_permissions(administrator=True)
    async def server_timeout(self, interaction: discord.Interaction, member: discord.Member, time: str, reason: str = "사유 없음"):
        seconds = self.parse_time(time)
        if not seconds:
            return await interaction.response.send_message("❌ 올바른 시간 형식을 입력하세요. (예: 10m, 1h, 1d)", ephemeral=True)

        try:
            await member.timeout(timedelta(seconds=seconds), reason=f"실행자: {interaction.user} | {reason}")
            embed = discord.Embed(
                title="⏳ 타임아웃",
                description=f"{member.mention} ({time})\n사유: {reason}",
                color=0xE74C3C
            )
            await interaction.response.send_message(embed=embed)
            logger = self.bot.get_cog('Logger')
            if logger: await logger.send_log(interaction.guild, embed, type="punish")
        except Exception as e:
            await interaction.response.send_message(f"❌ 오류 발생: {e}", ephemeral=True)

    @app_commands.command(name="untimeout", description="멤버의 타임아웃을 해제합니다.")
    @app_commands.checks.has_permissions(administrator=True)
    async def server_untimeout(self, interaction: discord.Interaction, member: discord.Member, reason: str = "관리자에 의한 해제"):
        if not member.timed_out_until:
            return await interaction.response.send_message(f"❌ {member.mention} 님은 현재 타임아웃 상태가 아닙니다.", ephemeral=True)

        try:
            await member.timeout(None, reason=f"실행자: {interaction.user} | {reason}")
            embed = discord.Embed(
                title="✅ 타임아웃 해제",
                description=f"{member.mention} 님의 타임아웃이 해제되었습니다.",
                color=0x2ECC71
            )
            await interaction.response.send_message(embed=embed)
            
            logger = self.bot.get_cog('Logger')
            if logger: await logger.send_log(interaction.guild, embed, type="punish")
        except Exception as e:
            await interaction.response.send_message(f"❌ 오류 발생: {e}", ephemeral=True)

    @app_commands.command(name="kick", description="멤버를 서버에서 추방합니다.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def server_kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "사유 없음"):
        try:
            await member.kick(reason=f"실행자: {interaction.user} | {reason}")
            embed = discord.Embed(title="👞 추방 완료", description=f"{member.mention} 추방됨\n사유: {reason}", color=0xE74C3C)
            await interaction.response.send_message(embed=embed)
            logger = self.bot.get_cog('Logger')
            if logger: await logger.send_log(interaction.guild, embed, type="punish")
        except Exception as e:
            await interaction.response.send_message(f"❌ 권한이 부족하거나 오류가 발생했습니다: {e}", ephemeral=True)

    @app_commands.command(name="ban", description="멤버를 서버에서 차단합니다.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def server_ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "사유 없음"):
        try:
            await member.ban(reason=f"실행자: {interaction.user} | {reason}", delete_message_seconds=86400)
            embed = discord.Embed(title="🚫 차단 완료", description=f"{member.mention} 차단됨\n사유: {reason}", color=0xE74C3C)
            await interaction.response.send_message(embed=embed)
            
            logger = self.bot.get_cog('Logger')
            if logger: await logger.send_log(interaction.guild, embed, type="punish")
        except Exception as e:
            await interaction.response.send_message(f"❌ 오류 발생: {e}", ephemeral=True)

    @app_commands.command(name="unban", description="서버 차단을 해제합니다.")
    @app_commands.describe(user_id="차단 해제할 유저의 ID")
    @app_commands.checks.has_permissions(ban_members=True)
    async def server_unban(self, interaction: discord.Interaction, user_id: str):
        async for entry in interaction.guild.bans():
            if str(entry.user.id) == user_id:
                await interaction.guild.unban(entry.user)
                embed = discord.Embed(title="✅ 차단 해제", description=f"{entry.user} (ID: {user_id}) 해제됨", color=0x2ECC71)
                await interaction.response.send_message(embed=embed)
                logger = self.bot.get_cog('Logger')
                if logger: await logger.send_log(interaction.guild, embed, type="punish")
                return
        
        await interaction.response.send_message("❌ 차단 목록에서 해당 ID를 찾을 수 없습니다.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Moderation(bot))