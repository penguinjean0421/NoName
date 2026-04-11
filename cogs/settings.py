import json
import os
from typing import Literal, Optional

import discord
from discord import app_commands
from discord.ext import commands

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.config_file = os.path.join(base_path, "..", "config.json")
        self.server_configs = {}
        self.load_config()

    def load_config(self):
        """설정 파일(JSON) 로드"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.server_configs = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.server_configs = {}
        else:
            self.server_configs = {}

    def save_config(self):
        """설정 파일 저장"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.server_configs, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"파일 저장 중 오류 발생: {e}")

    def get_server_data(self, guild: discord.Guild):
        """서버 데이터 초기화 및 반환"""
        gid = str(guild.id)
        if gid not in self.server_configs:
            self.server_configs[gid] = {
                "server_name": guild.name,
                "owner_id": guild.owner_id,
                "owner_name": str(guild.owner),
                "log_channel_id": None,
                "punish_log_channel_id": None,
                "command_channel_id": None,
                "ticket_panel_channel_id": None,
                "ticket_panel_msg_id": None,
                "ticket_count": 0
            }
        else:
            keys = ["ticket_panel_channel_id", "ticket_panel_msg_id", "ticket_count"]
            for key in keys:
                if key not in self.server_configs[gid]:
                    self.server_configs[gid][key] = 0 if "count" in key else None
            self.server_configs[gid]["server_name"] = guild.name
        self.save_config()
        return self.server_configs[gid]

    # --- 슬래시 명령어 ---

    @app_commands.command(name="set", description="서버의 각종 로그 및 티켓 채널을 설정합니다.")
    @app_commands.describe(
        target="설정할 항목을 선택하세요.",
        channel="항목을 설정할 채널을 지정하세요. (미지정 시 현재 채널)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def set_command(
        self, 
        interaction: discord.Interaction, 
        target: Literal["log", "punish", "bot", "ticket"], 
        channel: Optional[discord.TextChannel] = None
    ):
        key_map = {
            "log": "log_channel_id",
            "bot": "command_channel_id",
            "punish": "punish_log_channel_id",
            "ticket": "ticket_panel_channel_id"
        }

        target_channel = channel or interaction.channel
        gid = str(interaction.guild.id)
        self.get_server_data(interaction.guild)

        self.server_configs[gid][key_map[target]] = target_channel.id
        
        # 기본 성공 임베드
        embed = discord.Embed(
            description=f"✅ **{target.upper()}** 채널이 {target_channel.mention}로 설정되었습니다.",
            color=0x2ECC71
        )

        # 티켓 전용 로직
        if target == "ticket":
            ticket_cog = self.bot.get_cog('Ticket')
            if ticket_cog:
                # 패널 생성은 시간이 걸릴 수 있으므로 defer 고려 가능하나 일단 직행
                panel_msg = await ticket_cog.send_ticket_panel(target_channel)
                if panel_msg:
                    self.server_configs[gid]["ticket_panel_msg_id"] = panel_msg.id
                    embed.description = f"✅ 티켓 패널이 {target_channel.mention}에 생성되었습니다.\n(ID: {panel_msg.id})"
                else:
                    return await interaction.response.send_message("❌ 티켓 메시지 생성 실패", ephemeral=True)
            else:
                return await interaction.response.send_message("❌ Ticket 시스템을 찾을 수 없습니다.", ephemeral=True)

        self.save_config()
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="reset", description="서버 설정을 초기화하거나 특정 채널 설정을 제거합니다.")
    @app_commands.describe(target="초기화할 항목을 선택하세요.")
    @app_commands.checks.has_permissions(administrator=True)
    async def reset_command(
        self, 
        interaction: discord.Interaction, 
        target: Literal["log", "punish", "bot", "ticket", "all"]
    ):
        gid = str(interaction.guild.id)
        key_map = {
            "log": "log_channel_id",
            "bot": "command_channel_id",
            "punish": "punish_log_channel_id",
            "ticket": "ticket_panel_channel_id"
        }

        if target == "all":
            await self.delete_ticket_panel(interaction.guild)
            self.server_configs.pop(gid, None)
            embed = discord.Embed(description="✅ 모든 설정이 초기화되었습니다.", color=0xE74C3C)
        else:
            if target == "ticket":
                await self.delete_ticket_panel(interaction.guild)

            if gid in self.server_configs:
                self.server_configs[gid][key_map[target]] = None
                if target == "ticket":
                    self.server_configs[gid]["ticket_panel_msg_id"] = None
                embed = discord.Embed(
                    description=f"✅ **{target.upper()}** 설정 및 패널이 제거되었습니다.",
                    color=0x95A5A6
                )
            else:
                return await interaction.response.send_message("❌ 설정된 데이터가 없습니다.", ephemeral=True)

        self.save_config()
        await interaction.response.send_message(embed=embed)

    async def delete_ticket_panel(self, guild: discord.Guild):
        """저장된 티켓 패널 메시지를 삭제"""
        gid = str(guild.id)
        config = self.server_configs.get(gid)
        if not config:
            return

        msg_id = config.get("ticket_panel_msg_id")
        chn_id = config.get("ticket_panel_channel_id")

        if msg_id and chn_id:
            channel = self.bot.get_channel(chn_id) or await self.bot.fetch_channel(chn_id)
            if channel:
                try:
                    msg = await channel.fetch_message(msg_id)
                    await msg.delete()
                except:
                    pass

async def setup(bot):
    await bot.add_cog(Settings(bot))