"""A starting point for a new module or command
"""

import argparse
import configparser
import logging
from typing import Dict, Any


# some ideas for the future:
#   added config param to append a date to the logfile name

_CONFIG_FILE = "template.ini"  # replace with actual module name
_LOG_FILE = "template.log"  # replace with actual module name
_CONSOLE_LEVEL = logging.INFO
_FILE_LEVEL = logging.INFO

_logger = logging.getLogger(__name__)  # pylint: disable=C0103


def load_config_file(base_config: dict) -> configparser.ConfigParser:
    """Load the configuration file and initialize any variables

    Args:
        base_config (dict): the default configuration values

    Returns:
        configparser.ConfigParser: the config_parser object in case you want to
        use it for saving the configuration
    """
    parser = configparser.ConfigParser()
    parser.read(_CONFIG_FILE)
    # set variables from config
    if "logging" in parser:
        logging_config = parser["logging"]
        base_config["console_log_level"] = int(
            logging_config.get(
                "console_log_level", str(base_config["console_log_level"])
            )
        )
        base_config["logfile_log_level"] = int(
            logging_config.get(
                "logfile_log_level", str(base_config["logfile_log_level"])
            )
        )
        base_config["logfile_name"] = logging_config.get(
            "logfile_name", base_config["logfile_name"]
        )
    return parser


def update_config_file(parser: configparser.ConfigParser) -> None:
    """Save the configuration file. A later version of this should take in any
    non global variables as a parameter

    Args:
        parser (configparser.ConfigParser): the config parser object

    Raises:
        ValueError: if the parser is None
    """
    if not parser:
        raise ValueError("update_config_file called before load_config_file")
    # config_parser['Login Parameters']['refresh_token'] = token_dict['refresh_token']
    with open(_CONFIG_FILE, "w", encoding="UTF-8") as configfile:
        parser.write(configfile)


def initialize_logging(
    logfile_name: str, console_log_level: int, logfile_log_level: int
) -> None:
    """Initialize logging settings

    Args:
        logfile_name (str): the file name to save the file log to, use None to not save a log file
        console_log_level (int): the logging level for console log messages
        logfile_log_level (int): the logging level for file log messages
    """
    _logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(name)s - %(asctime)s (%(levelname)s): %(message)s")
    formatter.datefmt = "%Y-%m-%d %H:%M:%S %z"
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_log_level)
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)
    if logfile_name:
        file_handler = logging.FileHandler(logfile_name)
        file_handler.setLevel(logfile_log_level)
        file_handler.setFormatter(formatter)
        _logger.addHandler(file_handler)


def main() -> None:
    """put the business logic here when run from the command line"""
    pass  # pylint: disable=W0107


# when run as a script, do initialization
if __name__ == "__main__":
    config: Dict[str, Any] = {
        "logfile_name": _LOG_FILE,
        "console_log_level": _CONSOLE_LEVEL,
        "logfile_log_level": _FILE_LEVEL,
    }
    config_parser = load_config_file(config)

    # command-line arguments override config file settings
    arg_parser = argparse.ArgumentParser(description="do something interesting.")
    arg_parser.add_argument("--verbose", "-v", action="store_true", dest="verbose")
    arg_parser.add_argument(
        "--verbose_log", "-V", action="store_true", dest="verbose_log"
    )
    ns = arg_parser.parse_args()
    if ns.verbose:
        config["console_log_level"] = logging.DEBUG
    if ns.verbose_log:
        config["logfile_log_level"] = logging.DEBUG

    initialize_logging(
        config["logfile_name"], config["console_log_level"], config["logfile_log_level"]
    )
    main()
