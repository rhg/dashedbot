from functools import reduce
from subprocess import check_output
from os import environ

import discord
from discord.ext import commands


def get_version(root: str) -> str:
    return check_output(["git", "rev-parse", "HEAD"], cwd=root)


def non_bots(guild: discord.Guild):
    return tuple(filter(lambda m: not m.bot, guild.members))


class Presence(commands.Cog):
    '''Maintains our presence'''

    def __init__(self, bot):
        '''sets state'''
        self.bot = bot
        self.n = -1
        root = environ.get('ROOT', False)
        self._version = get_version(root) if root else 'unknown'

    @commands.Cog.listener()
    async def on_ready(self):
        '''set n to the number of non-bots in all guilds'''
        self.n = reduce(lambda acc, g: acc +
                        len(non_bots(g)), self.bot.guilds, 0)
        await self.set_presence()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''if not a bot update presence'''
        if not member.bot:
            self.n += 1
            await self.set_presence()

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        '''if not a bot then remove 1 from our count'''
        if not member.bot:
            self.n -= 1
            await self.set_presence()

    async def set_presence(self):
        game = discord.Game('with {0} users. version r{1}'.format(
            self.n, self._version.upper()))
        await self.bot.change_presence(status=discord.Status.online, activity=game)
