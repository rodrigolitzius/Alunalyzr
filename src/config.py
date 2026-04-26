import tomllib

def ler_config():
    with open("./config.toml", "rb") as file:
        config = tomllib.load(file)

    return config

config = ler_config()
