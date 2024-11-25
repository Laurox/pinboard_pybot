CREATE TABLE IF NOT EXISTS config
(
    guild_id     INTEGER NOT NULL,
    config_key   VARCHAR(31),
    config_value VARCHAR(255),
    PRIMARY KEY (guild_id, config_key)
);