import discord
from discord.ext import commands
import config
import cogs

BOT_PREFIX = ('@')

bot = commands.Bot(command_prefix=BOT_PREFIX)
for x in commands.Cog.__subclasses__():
    bot.add_cog(x(bot))

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name='Mathnasium@Home'))
    print('Logged in as ' + bot.user.name)
    print('---------------------')
    for g in bot.guilds:
        print('Logged into {}'.format(g))
        if not discord.utils.get(g.roles, name = 'InClassroom'):
            await g.create_role(name = 'InClassroom', color = discord.Color(0x06ffea), mentionable = True, hoist = True)
        r = discord.utils.get(g.roles, name = 'InClassroom')
        for m in r.members:
            await m.remove_roles(r)
        classroom = discord.utils.get(g.voice_channels, name = 'Classroom')
        if classroom:
            for m in classroom.members:
                await m.add_roles(r)

@bot.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == bot.user:
        return
        
    # Otherwise process command
    else:
        await bot.process_commands(message)

bot.run(config.token)
