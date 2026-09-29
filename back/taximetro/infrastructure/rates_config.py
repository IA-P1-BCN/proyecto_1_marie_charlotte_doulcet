import configparser
from taximetro.domain.rates import Rates

RATES_SECTION = "rates"
RATE_KEYS = ("stopped_rate", "moving_rate")

def load_rates(path="config.ini"):
    parser = configparser.ConfigParser()
    if not parser.read(path):
        raise ValueError(f"Config file not found: {path}")

    try:
        values = {key: parser.getfloat(RATES_SECTION, key) for key in RATE_KEYS}
        return Rates(**values)
    except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as exc:
        raise ValueError(f"Invalid or missing rate configuration in {path}: {exc}") from exc

def save_rates(rates, path="config.ini"):
    parser = configparser.ConfigParser()
    parser.read(path)
    if not parser.has_section(RATES_SECTION):
        parser.add_section(RATES_SECTION)
    for key, value in rates.to_dict().items():
        parser.set(RATES_SECTION, key, str(value))

    with open(path, "w") as f:
        parser.write(f)
