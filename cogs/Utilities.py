from discord.ext import commands
import config
import discord

class Utilties(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description = 'Checks to see if the bot is responsive',
                    help = 'Responds with Pong!',
                    brief = 'Responds with Pong!')
    async def ping(self, ctx):
        await ctx.send('Pong! {}ms'.format(round(self.bot.latency*1000, 1)))

    @commands.command(brief = 'Logs out of all servers. ADMIN ONLY',
                    description  = 'Logs out of all servers.\nONLY FOR ADMIN USE!')
    async def logout(self, ctx):
        if ctx.author.id in config.admins:
            for g in self.bot.guilds:
                r = discord.utils.get(g.roles, name = 'InClassroom')
                for m in r.members:
                    await m.remove_roles(r)
            await ctx.send('Logging out!!')
            await self.bot.logout()
        else:
            await ctx.send('You\'re not a developer!')

    @commands.command(description = 'Returns information on the bot.',
                    brief = 'Returns information on the bot.')
    async def about(ctx):
        with open('about.txt', 'r') as file:
            s = ''.join(file.readlines())
            await ctx.send(s)
