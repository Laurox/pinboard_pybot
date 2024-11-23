# pinboard_pybot 📌

A simple Discord bot that allows you to react to messages with a 📌 `:pushpin:` emoji and sends the pinned message to a
pre-configured channel using an impersonation webhook.

---

## Requirements

- **Python**: 3.12 or later
- **Dependencies**: Install from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Usage

### 1. Configuration:

Create a `config.toml` file in the root directory with the following structure:

```toml
prefix = "!"
description = "lorem ipsum"
owner_id = 123
[api_tokens]
discord = "BOT_API_KEY"
```

Replace `BOT_API_KEY` with your bot's token, available from
the [Discord Developer Portal](https://discord.com/developers/applications).

### 2. Run the Bot:

Start the bot using the following command. If no config file path is provided, the default `config.toml` will be used:

```bash
python bot.py [config-file]
```

---

## Development

### Code Formatting

This project uses [Ruff](https://docs.astral.sh/ruff/) for formatting. Install Ruff to ensure code
consistency:

```bash
pip install ruff
```

To check for issues, run:

```bash
ruff check .
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.