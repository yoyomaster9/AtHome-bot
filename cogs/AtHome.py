from discord.ext import commands
import Krypto
import config
from googletrans import Translator
translator = Translator()

# Checks to see if s contains any of the words in kws
def kwCheck(s, kws):
    for x in kws:
        if x in s:
            return True
    return False


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


        # WORK ON THIS

        # # The Whitney check
        # elif message.author.id == config.WhitneyID and 'hav ' in message.content.lower():
        #     # unicode for :regional_indicator_e:
        #     await message.add_reaction('\U0001F1EA')
        #
        # elif 'thanks' in message.content.lower() or 'thnaks' in message.content.lower():
        #     e = discord.utils.get(message.guild.emojis, name = 'thnaks')
        #     await message.add_reaction(e)
        #
        # elif translator.detect(message.content).lang == 'fr':
        #     msg = translator.translate(message.content).text
        #     await message.channel.send('I believe you meant this?\n```{}```'.format(msg))
