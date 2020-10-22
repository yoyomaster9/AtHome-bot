from discord.ext import commands
import Krypto

class Krypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description = 'Solves any and all krypto problems!\n Works with both fraction and non-fraction krypto.',
                    brief = 'Solves krypto problems.',
                    help = '''Replace n1, n2, ... with your numbers, and T with the target number. Type out fractions as a/b.
                              For example, @krypto 1/2, 3, 4, 5, 6, 1 will return (( 1/2 - 3 ) * 4 ) + ( 5 + 6 ) = 1.
                              NOTE: Sometimes the solver will lag behind if there is no solution.''',
                    usage = 'n1, n2, n3, n4, n5, T')
    async def krypto(self, ctx):
        s = ctx.message.content[8:]
        solution = Krypto.Main(s)
        if solution == False:
            await ctx.send('I couldn\'t find a solution!')
        else:
            await ctx.send('Here is your solution!\n{}'.format(solution))
