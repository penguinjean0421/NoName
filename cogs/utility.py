from discord.ext import commands
import random

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 멤버들 인스타
        self.insta_links = {
            'aespa' : 'aespa_offical',  
            'karina' : 'katarinabluu',
            'giselle' : 'aerichandesu',
            'winter' : 'imwinter',
            'ningning' : 'imnotningning'
        }

    # 제시된 것중에 하나 선택
    @commands.command(name="choose")
    async def choose(ctx, *options) : 
        print('입력중')
        if len (options) < 2 :
            await ctx.send ("최소 2개이상의 선택지를 제시해라 좀.")
        else :
            select = random.choice(options)
            await ctx.send(f'{select}')

    # 멤버들 인스타와 팀 구호 
    @commands.command(name="aespa", aliases=['에스파'])
    async def aespa(self, ctx):
        await ctx.send('Be my æ')
        await ctx.send('Be my æ')

    @commands.command(name="karina", aliases=['카리나'])
    async def karina(self, ctx):
        await ctx.send(self.insta_links['karina'])

    @commands.command(name="giselle", aliases=['지젤'])
    async def giselle(self, ctx):
        await ctx.send(self.insta_links['giselle'])

    @commands.command(name="winter", aliases=['윈터'])
    async def winter(self, ctx):
        await ctx.send(self.insta_links['winter'])

    @commands.command(name="ningning", aliases=['닝닝'])
    async def ningning(self, ctx):
        await ctx.send(self.insta_links['ningning'])

async def setup(bot):
    await bot.add_cog(Utility(bot))