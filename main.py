import discord
from discord.ext import commands, tasks
import discordtoken
import time
import asyncio
from datetime import datetime
import Krypto
import config
import datetime
import random
from googletrans import Translator


# Checks to see if s contains any of the words in kws
def kwCheck(s, kws):
    for x in kws:
        if x in s:
            return True
    return False

def roll(s): # Simulates rolls of the form #d#+#d#..
    l = []
    s = s.lower()
    for i in s.split('+'):
        if 'd' in i:
            try:
                if i[0] == 'd':
                    i = '1' + i
            except:
                i = '1' + i
            [n, max] = [int(x) for x in i.split('d')]
            for j in range(n):
                l.append(random.randint(1, max))
        else:
            l.append(int(i))
    return l

BOT_PREFIX = ('@')

client = commands.Bot(command_prefix=BOT_PREFIX)
translator = Translator()


@client.event
async def on_message(message):
    # We do not want the bot to reply to itself
    if message.author == client.user:
        return

    # The Whitney check
    elif message.author.id == config.WhitneyID and 'hav ' in message.content.lower():
        # unicode for :regional_indicator_e:
        await message.add_reaction('\U0001F1EA')

    elif 'thanks' in message.content.lower() or 'thnaks' in message.content.lower():
        e = discord.utils.get(message.guild.emojis, name = 'thnaks')
        await message.add_reaction(e)

    elif translator.detect(message.content).lang == 'fr':
        msg = translator.translate(message.content).text
        await message.channel.send('I believe you meant this?\n```{}```'.format(msg))

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
        if not discord.utils.get(g.roles, name = 'InClassroom'):
            await g.create_role(name = 'InClassroom', color = discord.Color(0x06ffea), mentionable = True, hoist = True)
        r = discord.utils.get(g.roles, name = 'InClassroom')
        for m in r.members:
            await m.remove_roles(r)
        classroom = discord.utils.get(g.voice_channels, name = 'Classroom')
        if classroom:
            for m in classroom.members:
                await m.add_roles(r)

        print('Logged into {}'.format(g))

@client.command(description = 'Checks to see if the bot is responsive',
                help = 'Responds with Pong!',
                brief = 'Responds with Pong!')
async def ping(ctx):
    await ctx.send('Pong! {}ms'.format(round(client.latency*1000, 1)))


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
    if ctx.author.id in config.admins:
        for g in client.guilds:
            r = discord.utils.get(g.roles, name = 'InClassroom')
            for m in r.members:
                await m.remove_roles(r)
        await ctx.send('Logging out!!')
        await client.logout()
    else:
        await ctx.send('You\'re not a developer!')

@client.command(description = 'Rolls a die at random.',
                help = 'Rolls a die at random. Can add extra dice or mods by doing\'d20 + 2d4 + 1\'')
async def roll(ctx, arg*):
    s = ''.join(arg)
    r = sum(roll(s))
    await ctx.send('You rolled a {}!'.format(r))

@client.command(description = 'Returns information on the bot.',
                brief = 'Returns information on the bot.')
async def about(ctx):
    with open('about.txt', 'r') as file:
        s = ''.join(file.readlines())
        await ctx.send(s)

async def notifications():
    await client.wait_until_ready()
    channel = client.get_channel(config.notificationChannelID)
    while not client.is_closed():
        now = datetime.datetime.strftime(datetime.datetime.now(), '%A %H:%M')
        if now in config.workoutPlanTime:
            await channel.send('Hey {InClassroom}! Please don\'t forget to fill out the student\'s workout plans! Thank you!'.format(InClassroom = discord.utils.get(channel.guild.roles, name = 'InClassroom').mention))
        elif now in config.wobTime:
            await channel.send('Hey {InClassroom}! We\'re about halfway through this session. If you haven\'t quite moved to WOB yet, please consider doing it soon!'.format(InClassroom = discord.utils.get(channel.guild.roles, name = 'InClassroom').mention))
        await asyncio.sleep(60)


client.loop.create_task(notifications())
client.run(discordtoken.token)
