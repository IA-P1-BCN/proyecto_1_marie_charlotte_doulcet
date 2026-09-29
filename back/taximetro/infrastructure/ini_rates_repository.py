import configparser
from taximetro.domain.rates import Rates
from taximetro.domain.rates_repository import RatesRepository

SECTION = "rates"
KEYS = ("stopped_rate", "moving_rate")


class IniRatesRepository(RatesRepository):
    """Default rates stored in config.ini (tracked in git, no secrets)."""

    def __init__(self, path="config.ini"):
        self.path = path

    def load(self):
        parser = configparser.ConfigParser()
        if not parser.read(self.path):
            raise ValueError(f"Config file not found: {self.path}")
        try:
            return Rates(**{key: parser.getfloat(SECTION, key) for key in KEYS})
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as exc:
            raise ValueError(f"Invalid or missing rate configuration in {self.path}: {exc}") from exc

    def save(self, rates):
        parser = configparser.ConfigParser()
        parser.read(self.path)
        if not parser.has_section(SECTION):
            parser.add_section(SECTION)
        for key, value in rates.to_dict().items():
            parser.set(SECTION, key, str(value))
        with open(self.path, "w") as f:
            parser.write(f)
