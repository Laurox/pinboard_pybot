import discord


class ImpersonateWebhook:
    def __init__(self, bot, channel_id, name):
        self.bot = bot
        self.channel_id = channel_id
        self.name = name
        self.channel = self.bot.get_channel(self.channel_id)

        if not self.channel:
            raise ValueError(f"Unable to find channel <{channel_id}>")

    async def _get_or_create_webhook(self) -> discord.Webhook:
        existing_webhooks: list[discord.Webhook] = await self.channel.webhooks()

        for webhook in existing_webhooks:
            if webhook.name == f"{self.name}-{self.channel.id}":
                return webhook

        return await self.channel.create_webhook(name=f"{self.name}-{self.channel.id}")

    async def impersonate_message(self, message: discord.Message):
        webhook = await self._get_or_create_webhook()

        # download attachments - if any - and save them for re-sending
        # we could opt to only send the cdn url, if rate limit becomes a problem
        files = [await attachment.to_file() for attachment in message.attachments]

        payload = {
            "content": message.content or "",
            "username": message.author.display_name,
            "avatar_url": (
                message.author.display_avatar.url
                if message.author.display_avatar
                else None
            ),
        }

        if files:
            payload["files"] = files

        await webhook.send(**payload)
