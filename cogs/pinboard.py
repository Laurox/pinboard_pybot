import discord

from discord.ext.commands import Cog, command, Context

from utils.impersonate_webhook import ImpersonateWebhook


class Pinboard(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pinboard_channel = bot.config.PINBOARD_CHANNEL

    @Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji != "📌" or user.bot:
            return

        message = reaction.message
        webhook = ImpersonateWebhook(
            self.bot, channel_id=self.pinboard_channel, name="pinboard-hook"
        )

        await webhook.impersonate_message(message)

    @command()
    async def pinboard(self, ctx: Context, channel: discord.TextChannel):
        """'!pinboard [channel]' sets the channel where the pins will be posted"""
        self.pinboard_channel = channel.id
        await ctx.send(f"Pinboard channel set to {channel.mention}.")


async def setup(bot):
    await bot.add_cog(Pinboard(bot))
