import discord
from discord.ext import commands

from dashedbot.utils import get_logger, read_json, write_json

logger = get_logger('dashedbot.scores')


class Scores(commands.Cog):
    '''handles the coins each user has'''

    VALUE = 5

    def __init__(self):
        '''loads the initial state from disk'''
        self._scores = read_json('scores.json')

    @commands.Cog.listener()
    async def on_message(self, message):
        '''gives certain number of currency per word to a person
        in a guild context'''
        if not message.guild:
            return
        s = str(message.author.id)
        n = self.VALUE * len(message.content.split())
        self[s] = self[s] + n
        logger.debug('added %d to %s', n, s)
        self.save()

    @commands.command()
    async def coins(self, ctx):
        '''gives the caller info on their current balance'''
        s = str(ctx.author.id)
        await ctx.send('{0.mention} has {1} coin(s)'.format(ctx.author, self[s]))

    @commands.command()
    async def pay(self, ctx, member: discord.Member, amt: int):
        '''transfers an amount to the pinged user'''
        (f, t) = map(str, (ctx.author.id, member.id))
        logger.debug('transfering %d from %s to %s', amt, f, t)
        a = self[f]
        b = self[t]
        if amt > a:
            await ctx.send('insufficient funds')
        else:
            self[f] = a - amt
            self[t] = b + amt
            self.save()

    def __getitem__(self, key: str):
        return self._scores.get(key, 500)

    def __setitem__(self, key: str, val: int):
        self._scores[key] = val

    def save(self):
        '''persist to disk'''
        write_json(self._scores, name='scores.json')
