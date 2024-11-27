CREATE TABLE IF NOT EXISTS config
(
    guild_id     INTEGER NOT NULL,
    config_key   VARCHAR(31),
    config_value VARCHAR(255),
    PRIMARY KEY (guild_id, config_key)
);

CREATE TABLE IF NOT EXISTS pin_log
(
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    guild_id   INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    message_id INTEGER NOT NULL,
    user_id    INTEGER NOT NULL
);
