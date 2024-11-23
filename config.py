import toml


class Config:
    PINBOARD_CHANNEL = 1309661580924944526

    def __init__(self, config_file: str):
        try:
            self.config = toml.load(config_file)
        except FileNotFoundError as ex:
            print(f"Config file <{config_file}> not found: {ex}")
        except (TypeError, toml.TomlDecodeError) as ex:
            print(f"Config file is invalid: {ex}")

        self.prefix = str(self.config["prefix"])
        self.description = str(self.config["description"])
        self.owner_id = int(self.config["owner_id"])
        self.token = str(self.config["api_tokens"]["discord"])
