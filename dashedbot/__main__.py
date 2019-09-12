from os import environ

from discord.ext import commands

from dashedbot import monetary, presence, scores

bot = commands.Bot(command_prefix='$',
                   description='a custom bot for my server')

bot.add_cog(scores.Scores())
bot.add_cog(monetary.Apartments(bot))
bot.add_cog(presence.Presence(bot))

bot.run(environ['DISCORD_BOT_TOKEN'])
