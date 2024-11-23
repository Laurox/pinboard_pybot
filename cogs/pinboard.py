import discord

from discord.ext.commands import Cog, command, Context


class Pinboard(Cog):

    def __init__(self, bot):
        self.bot = bot
        self.pinboard_channel = bot.config.PINBOARD_CHANNEL

    @Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji != "📌" or user.bot:
            return

        message = reaction.message
        if self.pinboard_channel:
            channel = self.bot.get_channel(self.pinboard_channel)
            if not channel:
                print(f"error getting channel <{self.pinboard_channel}>")
                pass

            # Retrieve or create the appropriate webhook
            guild_webhooks: list[discord.Webhook] = await channel.webhooks()
            webhooks_filtered: list[discord.Webhook] = [w for w in guild_webhooks if
                                                        str(channel.id) in w.name]
            if not webhooks_filtered:
                webhook: discord.Webhook = await channel.create_webhook(name=f'pinboard-hook-{channel.id}')
            else:
                webhook: discord.Webhook = webhooks_filtered[0]

            # todo: refactor this and test with multiple accounts and message types
            # Prepare content and attachments
            files = [await attachment.to_file() for attachment in message.attachments]
            content = message.content if message.content else None  # Ensure content isn't empty

            payload = {
                "content": content if files else message.content,
                "username": message.author.display_name,
                "avatar_url": message.author.display_avatar.url if message.author.display_avatar else None,
            }

            # None, is not allowed in files, so we have to add it manually
            if files:
                payload["files"] = files

            await webhook.send(**payload)

    @command()
    async def pinboard(self, ctx: Context, channel: discord.TextChannel):
        """'!pinboard [channel]' sets the channel where the pins will be posted"""
        self.pinboard_channel = channel.id
        await ctx.send(f"Pinboard channel set to {channel.mention}.")


async def setup(bot):
    await bot.add_cog(Pinboard(bot))
