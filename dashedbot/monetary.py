from datetime import datetime, timedelta

from discord.ext import commands

from dashedbot.utils import get_logger, read_json, write_json, map_values


class Apartments(commands.Cog):
    '''handles renting out apartments'''

    CATEGORY = 4
    PRICE = 300

    def __init__(self, bot):
        '''loads our state from JSON'''
        self._state = map_values(lambda ts: datetime.fromtimestamp(ts),
                                 read_json('apartments.json'))
        self._bot = bot

    def __getitem__(self, key: str):
        return self._state[key]

    def __setitem__(self, key: str, val: datetime):
        self._state[key] = val

    def save(self):
        write_json(map_values(lambda dt: dt.timestamp(), self._state),
                   name='apartments.json')

    @commands.command()
    async def rent(self, ctx, *, name=None):
        '''Rents out an apartment with optional name else uses your nick'''
        if ctx.guild:  # assumes one guild
            name = name or ctx.author.display_name.replace(' ', '-')
            category = ctx.guild.categories[self.CATEGORY]
            s = str(ctx.author.id)
            scores = self._bot.get_cog('Scores')
            if not scores:
                raise RuntimeError('WTF')
            elif self.PRICE > scores[s]:
                await ctx.send('{0.mention}: insufficient funds'.format(ctx.author))
            else:
                scores[s] = scores[s] - self.PRICE
                scores.save()
                await category.create_text_channel(name, reason='rented out by {0.id}'.format(ctx.author))
                self[s] = datetime.now() + timedelta(days=30)
                self.save()

    @commands.command()
    async def due(self, ctx, *, id: str):
        '''tells when an id's rent is due'''
        await ctx.send('{0}\'s rent is due {1}'.format(id, self[str(ctx.author.id)]))

    @commands.command()
    async def renew(self, ctx):
        '''add 30 more days to the lease'''
        id = str(ctx.author.id)
        scores = self._bot.get_cog('Scores')
        if id in self._state and scores:
            if self.PRICE > scores[id]:
                await ctx.send('{0.mention}: insufficient funds'.format(ctx.author))
            else:
                scores[id] -= self.PRICE
                scores.save()
                self[id] += timedelta(days=30)
