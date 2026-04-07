"""A starting point for a new module or command"""

import argparse
import configparser
import logging
from typing import Any

# some ideas for the future:
#   added config param to append a date to the logfile name

_CONFIG_FILE = "template.ini"  # replace with actual module name
_LOG_FILE = "template.log"  # replace with actual module name
_CONSOLE_LEVEL = logging.INFO
_FILE_LEVEL = logging.INFO

_logger = logging.getLogger(__name__)


def load_config_file(base_config: dict[str, Any]) -> configparser.ConfigParser:
    """Load the configuration file and initialize any variables.

    Args:
        base_config: the default configuration values, mutated in place with
            values from the config file.

    Returns:
        The ConfigParser object, in case you want to use it for saving config.
    """
    parser = configparser.ConfigParser()
    parser.read(_CONFIG_FILE, encoding="UTF-8")
    if "logging" in parser:
        logging_config = parser["logging"]
        base_config["console_log_level"] = int(
            logging_config.get("console_log_level", str(base_config["console_log_level"]))
        )
        base_config["logfile_log_level"] = int(
            logging_config.get("logfile_log_level", str(base_config["logfile_log_level"]))
        )
        base_config["logfile_name"] = logging_config.get(
            "logfile_name", base_config["logfile_name"]
        )
    return parser


def update_config_file(parser: configparser.ConfigParser | None) -> None:
    """Save the configuration file.

    Args:
        parser: the ConfigParser object returned by load_config_file.

    Raises:
        ValueError: if parser is None.
    """
    if parser is None:
        raise ValueError("update_config_file called before load_config_file")
    with open(_CONFIG_FILE, "w", encoding="UTF-8") as configfile:
        parser.write(configfile)


def initialize_logging(
    logfile_name: str | None, console_log_level: int, logfile_log_level: int
) -> None:
    """Initialize logging settings.

    Calling this more than once replaces existing handlers, preventing duplicate
    log lines if cli() is invoked multiple times in the same process.

    Args:
        logfile_name: file name to save the log to; pass None to skip file logging.
            For production services consider structlog for structured/JSON logging.
        console_log_level: logging level for console output.
        logfile_log_level: logging level for file output.
    """
    for handler in _logger.handlers:
        handler.close()
    _logger.handlers.clear()
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


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        argv: argument list; defaults to sys.argv. Pass an explicit list for testing.

    Returns:
        Namespace with parsed arguments.
    """
    arg_parser = argparse.ArgumentParser(description="do something interesting.")
    arg_parser.add_argument("--verbose", "-v", action="store_true", dest="verbose")
    arg_parser.add_argument("--verbose_log", "-V", action="store_true", dest="verbose_log")
    return arg_parser.parse_args(argv)


def main() -> None:
    """Put the business logic here when run from the command line."""
    pass


def cli() -> None:
    """Entry point for the installed console script.

    Loads config, parses CLI arguments, initializes logging, then calls main().
    """
    config: dict[str, Any] = {
        "logfile_name": _LOG_FILE,
        "console_log_level": _CONSOLE_LEVEL,
        "logfile_log_level": _FILE_LEVEL,
    }
    load_config_file(config)

    # command-line arguments override config file settings
    ns = parse_args()
    if ns.verbose:
        config["console_log_level"] = logging.DEBUG
    if ns.verbose_log:
        config["logfile_log_level"] = logging.DEBUG

    initialize_logging(
        config["logfile_name"], config["console_log_level"], config["logfile_log_level"]
    )
    main()


if __name__ == "__main__":
    cli()
