from functools import reduce
from os import environ

import discord
from discord.ext import commands


def non_bots(guild: discord.Guild):
    return tuple(filter(lambda m: not m.bot, guild.members))


async def set_presence(bot: discord.Client, n: int):
    version = environ['HASH']
    g = discord.Game('with {0} users. version r{1}'.format(n, version))
    await bot.change_presence(status=discord.Status.online, activity=g)


class Presence(commands.Cog):
    '''Maintains our presence'''

    def __init__(self, bot):
        '''sets state'''
        self.bot = bot
        self.n = -1

    @commands.Cog.listener()
    async def on_ready(self):
        '''set n to the number of non-bots in all guilds'''
        self.n = reduce(lambda acc, g: acc +
                        len(non_bots(g)), self.bot.guilds, 0)
        await set_presence(self.bot, self.n)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''if not a bot update presence'''
        if not member.bot:
            self.n += 1
            await set_presence(self.bot, self.n)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        '''if not a bot then remove 1 from our count'''
        if not member.bot:
            self.n -= 1
            await set_presence(self.bot, self.n)
