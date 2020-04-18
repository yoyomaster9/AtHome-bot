import discord
from discord.ext import commands, tasks
import discordtoken
import time
import asyncio
from datetime import datetime
import Krypto
import data
import datetime
import random


# Checks to see if s contains any of the words in kws
def kwCheck(s, kws):
    for x in kws:
        if x in s:
            return True
    return False

BOT_PREFIX = ('@')

client = commands.Bot(command_prefix=BOT_PREFIX)


@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

    # Check if there's a tech issue
    elif kwCheck(message.content.lower(), ['issue', 'connection', 'gateway', 'trouble','problem', 'help', '502']) and random.random() > .5:
        msg = random.choice([
        'Have you tried refreshing it?',
        'Maybe refresh your page?',
        'Refreshing usually fixes this!',
        'Many people had this issue! Refreshing usually fixed it.',
        'Sometimes ConexED has issues with this. Maybe try refrshing?',
        'Just keep refrshing the page. Usually that fixes things!'
        ])
        await message.channel.send(msg)

    # Otherwise process command
    else:
        await client.process_commands(message)

@client.event
async def on_voice_state_update(member, vsbefore, vsafter):
    # vsbefore and vsafter are voice states
    r = discord.utils.get(member.guild.roles, name = 'InClassroom')
    vc = discord.utils.get(member.guild.voice_channels, name = 'Classroom')
    if vsafter.channel == vc:
        await member.add_roles(r)
    elif vsafter.channel == None:
        await member.remove_roles(r)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='Mathnasium@Home'))
    print('Logged in as ' + client.user.name)
    print('---------------------')
    for g in client.guilds:
        print('Logged into {}'.format(g))
        if not discord.utils.get(g.roles, name = 'InClassroom'):
            await g.create_role(name = 'InClassroom', color = discord.Color(0x06ffea), mentionable = True, hoist = True)

        r = discord.utils.get(g.roles, name = 'InClassroom')
        classroom = discord.utils.get(g.voice_channels, name = 'Classroom')
        if classroom:
            for m in classroom.members:
                await m.add_roles(r)


@client.command(description = 'Checks to see if the bot is responsive',
                help = 'Responds with Pong!',
                brief = 'Responds with Pong!')
async def ping(ctx):
    await ctx.send('Pong! {}ms'.format(round(bot.latency*1000, 1)))


@client.command(description = 'Solves any and all krypto problems!\n Works with both fraction and non-fraction krypto.',
                brief = 'Solves krypto problems.',
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


@client.command(brief = 'Logs out of all servers. ADMIN ONLY',
                description  = 'Logs out of all servers.\nONLY FOR ADMIN USE!')
async def logout(ctx):
    if ctx.author.id in data.admins:
        await ctx.send('Logging out!!')
        await client.logout()
    else:
        await ctx.send('You\'re not a developer!')

@client.command(description = 'Returns information on the bot.',
                brief = 'Returns information on the bot.')
async def about(ctx):
    with open('about.txt', 'r') as file:
        s = ''.join(file.readlines())
        await ctx.send(s)

async def notifications():
    await client.wait_until_ready()
    channel = client.get_channel(data.notificationChannelID)
    while not client.is_closed():
        now = datetime.datetime.strftime(datetime.datetime.now(), '%A %H:%M')
        if now in data.clockInTime:
            await channel.send('Hello @InClassroom! Quick reminder to clock in today!')
        elif now in data.clockOutTime:
            await channel.send('Hello @InClassroom! Quick reminder to clock out today! Also, don\'t forget to wrap up your Workout Plans!')
        elif now in data.workoutPlanTime:
            await channel.send('Hey @InClassroom! Don\'t forget to fill out the student\'s workout plans!')
        await asyncio.sleep(60)


client.loop.create_task(notifications())
client.run(discordtoken.token)
