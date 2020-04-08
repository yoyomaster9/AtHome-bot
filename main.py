import discord
from discord.ext import commands, tasks
import discordtoken
import time
import asyncio
from datetime import datetime
import Krypto
import data

BOT_PREFIX = ('@')

client = commands.Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return
    else:
        await client.process_commands(message)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Mathnasium@Home'))
    print('Logged in as ' + client.user.name)
    print('---------------------')
    for g in client.guilds:
        print('Logged into {}'.format(g))


@client.command(description = 'Checks to see if the bot is responsive',
                help = 'Responds with Pong!',
                brief = 'Responds with Pong!')
async def ping(ctx):
    await ctx.send('Pong!')


@client.command(description = 'Solves any and all krypto problems!\n Works with both fraction and non-fraction krypto.',
                brief = 'Solves krypto problems',
                help = '''Replace n1, n2, ... with your numbers, and T with the target number. Type out fractions as a/b.
                          For example, @krypto 1/2, 3, 4, 5, 6, 1 will return (( 1/2 - 3 ) * 4 ) + ( 5 + 6 ) = 1.
                          NOTE: Sometimes the solver will lag behind if there is no solution.''',
                usage = 'n1, n2, n3, n4, n5, T')
async def krypto(ctx):
    s = ctx.message.content[8:]
    solution = Krypto.Main(s)
    if solution == False:
        await ctx.send('I couldn\'t find a solution!')
    else:
        await ctx.send('Here is your solution!\n{}'.format(solution))


@client.command(brief = 'Logs out of all servers.',
                description  = 'Logs out of all servers.\nONLY FOR ADMIN USE!')
async def logout(ctx):
    if ctx.author.id in data.admins:
        await ctx.send('Logging out!!')
        await client.logout()
    else:
        await ctx.send('You\'re not a developer!')

async def notifications():
    await client.wait_until_ready()



client.loop.create_task(notifications())
client.run(discordtoken.token)
