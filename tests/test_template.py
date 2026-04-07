import configparser
import logging
from collections.abc import Generator
from pathlib import Path

import pytest
from pytest_mock import MockerFixture

import template
from template import (
    initialize_logging,
    load_config_file,
    main,
    parse_args,
    update_config_file,
)


@pytest.fixture(autouse=True)
def reset_logger() -> Generator[None, None, None]:
    """Remove any handlers added to _logger between tests."""
    yield
    template._logger.handlers.clear()


# ---------------------------------------------------------------------------
# load_config_file
# ---------------------------------------------------------------------------


class TestLoadConfigFile:
    def test_defaults_preserved_when_no_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)  # no .ini present
        config = {
            "console_log_level": logging.INFO,
            "logfile_log_level": logging.INFO,
            "logfile_name": "test.log",
        }
        load_config_file(config)
        assert config["console_log_level"] == logging.INFO
        assert config["logfile_log_level"] == logging.INFO
        assert config["logfile_name"] == "test.log"

    def test_config_overrides_console_log_level(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ini = tmp_path / "template.ini"
        ini.write_text("[logging]\nconsole_log_level = 10\n")
        monkeypatch.chdir(tmp_path)
        config = {
            "console_log_level": logging.INFO,
            "logfile_log_level": logging.INFO,
            "logfile_name": "test.log",
        }
        load_config_file(config)
        assert config["console_log_level"] == logging.DEBUG  # 10

    def test_config_overrides_logfile_name(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        ini = tmp_path / "template.ini"
        ini.write_text("[logging]\nlogfile_name = custom.log\n")
        monkeypatch.chdir(tmp_path)
        config = {
            "console_log_level": logging.INFO,
            "logfile_log_level": logging.INFO,
            "logfile_name": "default.log",
        }
        load_config_file(config)
        assert config["logfile_name"] == "custom.log"

    def test_returns_config_parser(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        config = {
            "console_log_level": logging.INFO,
            "logfile_log_level": logging.INFO,
            "logfile_name": "test.log",
        }
        result = load_config_file(config)
        assert isinstance(result, configparser.ConfigParser)


# ---------------------------------------------------------------------------
# update_config_file
# ---------------------------------------------------------------------------


class TestUpdateConfigFile:
    def test_raises_on_none_parser(self) -> None:
        with pytest.raises(ValueError, match="update_config_file called before load_config_file"):
            update_config_file(None)

    def test_writes_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        parser = configparser.ConfigParser()
        parser["logging"] = {"console_log_level": "20"}
        update_config_file(parser)

        written = configparser.ConfigParser()
        written.read(tmp_path / "template.ini")
        assert written["logging"]["console_log_level"] == "20"


# ---------------------------------------------------------------------------
# initialize_logging
# ---------------------------------------------------------------------------


class TestInitializeLogging:
    def test_adds_console_handler(self) -> None:
        initialize_logging(None, logging.INFO, logging.DEBUG)
        handler_types = [type(h) for h in template._logger.handlers]
        assert logging.StreamHandler in handler_types

    def test_no_file_handler_when_logfile_none(self) -> None:
        initialize_logging(None, logging.INFO, logging.DEBUG)
        for h in template._logger.handlers:
            assert not isinstance(h, logging.FileHandler)

    def test_adds_file_handler_when_logfile_given(
        self, tmp_path: Path, mocker: MockerFixture
    ) -> None:
        mocker.patch("logging.FileHandler", return_value=logging.NullHandler())
        initialize_logging(str(tmp_path / "test.log"), logging.INFO, logging.DEBUG)
        assert len(template._logger.handlers) == 2

    def test_logger_level_set_to_debug(self) -> None:
        initialize_logging(None, logging.INFO, logging.DEBUG)
        assert template._logger.level == logging.DEBUG

    def test_console_handler_level(self) -> None:
        initialize_logging(None, logging.WARNING, logging.DEBUG)
        stream_handlers = [h for h in template._logger.handlers if type(h) is logging.StreamHandler]
        assert stream_handlers[0].level == logging.WARNING


# ---------------------------------------------------------------------------
# parse_args
# ---------------------------------------------------------------------------


class TestParseArgs:
    def test_defaults_are_false(self) -> None:
        ns = parse_args([])
        assert ns.verbose is False
        assert ns.verbose_log is False

    def test_short_verbose_flag(self) -> None:
        ns = parse_args(["-v"])
        assert ns.verbose is True
        assert ns.verbose_log is False

    def test_short_verbose_log_flag(self) -> None:
        ns = parse_args(["-V"])
        assert ns.verbose is False
        assert ns.verbose_log is True

    def test_both_flags(self) -> None:
        ns = parse_args(["-v", "-V"])
        assert ns.verbose is True
        assert ns.verbose_log is True

    def test_long_verbose_flag(self) -> None:
        ns = parse_args(["--verbose"])
        assert ns.verbose is True

    def test_long_verbose_log_flag(self) -> None:
        ns = parse_args(["--verbose_log"])
        assert ns.verbose_log is True


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


class TestMain:
    def test_main_runs_without_error(self) -> None:
        main()  # should not raise
