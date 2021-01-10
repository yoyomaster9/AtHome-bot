from discord.ext import commands
import discord
import Krypto
import config


class AtHome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener() #not sure if this works
    async def on_voice_state_update(self, member, vsbefore, vsafter):
        # vsbefore and vsafter are voice states
        r = discord.utils.get(member.guild.roles, name = 'InClassroom')
        vc = discord.utils.get(member.guild.voice_channels, name = 'Classroom')
        if vsafter.channel == vc:
            await member.add_roles(r)
        elif vsafter.channel == None:
            await member.remove_roles(r)


    @commands.Cog.listener()
    async def on_message(self, message):
        # We do not want the bot to reply to itself
        if message.author == self.bot.user:
            return

        # The Whitney check
        elif message.author.id == 685907947699961932 and 'hav ' in message.content.lower():
            # unicode for :regional_indicator_e:
            await message.add_reaction('\U0001F1EA')

        elif 'thanks' in message.content.lower() or 'thnaks' in message.content.lower():
            e = discord.utils.get(message.guild.emojis, name = 'thnaks')
            await message.add_reaction(e)
