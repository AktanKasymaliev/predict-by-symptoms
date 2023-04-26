from configparser import ConfigParser, NoOptionError, NoSectionError
import os

def get_config(config: ConfigParser, section: str, name: str, default=None) -> str:
    try:
        output = config.get(section, name)
    except (NoOptionError, NoSectionError):
        output = default
    return output

def config() -> None:
    config_parse = ConfigParser()
    config_parse.read("settings.ini")
    DATABASE = "DATABASE"
    SYSTEM = "SYSTEM"
    EMAIL = "EMAIL"

    #DATABASE
    os.environ.setdefault("DATABASE_NAME", get_config(config_parse, DATABASE, "NAME"))
    os.environ.setdefault("DATABASE_USER", get_config(config_parse, DATABASE, "USER"))
    os.environ.setdefault("DATABASE_PASSWORD", get_config(config_parse, DATABASE, "PASSWORD"))
    os.environ.setdefault("DATABASE_HOST", get_config(config_parse, DATABASE, "HOST"))
    os.environ.setdefault("DATABASE_PORT", get_config(config_parse, DATABASE, "PORT"))
    
    #SYSTEM
    os.environ.setdefault("DJANGO_DEBUG", get_config(config_parse, SYSTEM, "DJANGO_DEBUG", "False"))
    os.environ.setdefault("DJANGO_KEY", get_config(config_parse, SYSTEM, "DJANGO_KEY", "super_secret_key"))
    os.environ.setdefault("ADMIN_USERNAME", get_config(config_parse, SYSTEM, "ADMIN_USERNAME", "admin"))
    os.environ.setdefault("ADMIN_PASSWORD", get_config(config_parse, SYSTEM, "ADMIN_PASSWORD", "admin"))