import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# 토큰 가져오기
load_dotenv()
BOT_TOKEN = os.getenv(f'BOT_TOKEN', None)
if BOT_TOKEN is None :
    print('로드 실패')
else :
    print('로드 성공')  

# 봇 커맨드 설정
intents = discord.Intents.default()
intents.message_content = True
bot_command_prefix = "æ"
bot = commands.Bot(bot_command_prefix, intents = intents, help_command=None)

@bot.event
# 봇 상태 설정
async def on_ready(): 
    print(f'{bot.user.name} 봇이 온라인이 되었습니다!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("penguinjæn Online"))

bot.run(BOT_TOKEN)