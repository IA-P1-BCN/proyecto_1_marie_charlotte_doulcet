import configparser

RATES_SECTION = "rates"
RATE_KEYS = ("stopped_rate", "moving_rate")

def load_rates(path="config.ini"):
    parser = configparser.ConfigParser()
    if not parser.read(path):
        raise ValueError(f"Config file not found: {path}")

    try: 
        rates = {key: parser.getfloat(RATES_SECTION, key) for key in RATE_KEYS}
    except(configparser.NoSectionError, configparser.NoOptionError, ValueError) as exc:
        raise ValueError (f"Invalid or missing rate configuration in {path}: {exc}") from exc 

    for key, value in rates.items():
        if value <= 0:
            raise ValueError(f"Invalid value for {key}: must be positive")

    return rates 

def save_rates(rates, path="config.ini"):
    for key, value in rates.items():
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            raise ValueError(f"Invalid value for {key}: must be a positive number")

    parser = configparser.ConfigParser()
    parser.read(path)
    if not parser.has_section(RATES_SECTION):
        parser.add_section(RATES_SECTION)
    for key, value in rates.items():
        parser.set(RATES_SECTION, key, str(value))

    with open(path, "w") as f:
        parser.write(f)

            