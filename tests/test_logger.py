import pytest
from unittest.mock import patch, MagicMock
from storm.common.services.logger import Logger
import logging
import colorlog

@pytest.fixture
def logger():
    """Fixture to create a logger instance for testing."""
    return Logger("TestLogger")

def test_logger_info(logger):
    """Test info level logging."""
    with patch('logging.Logger.info') as mock_info:
        logger.info("Test info message")
        mock_info.assert_called_once_with("Test info message")

def test_logger_with_context(logger):
    """Test logging with context."""
    with patch('logging.Logger.info') as mock_info:
        logger.set_context({"request_id": "12345", "user_id": "67890"})
        logger.info("Test context message")
        mock_info.assert_called_once_with("request_id=12345 user_id=67890 Test context message")

def test_logger_debug(logger):
    """Test debug level logging."""
    with patch('logging.Logger.debug') as mock_debug:
        logger.debug("Test debug message")
        mock_debug.assert_called_once_with("Test debug message")

def test_logger_warning(logger):
    """Test warning level logging."""
    with patch('logging.Logger.warning') as mock_warning:
        logger.warning("Test warning message")
        mock_warning.assert_called_once_with("Test warning message")

def test_logger_error(logger):
    """Test error level logging."""
    with patch('logging.Logger.error') as mock_error:
        logger.error("Test error message")
        mock_error.assert_called_once_with("Test error message")

def test_logger_critical(logger):
    """Test critical level logging."""
    with patch('logging.Logger.critical') as mock_critical:
        logger.critical("Test critical message")
        mock_critical.assert_called_once_with("Test critical message")

def test_logger_no_context(logger):
    """Test logging without context to ensure it handles no context correctly."""
    with patch('logging.Logger.info') as mock_info:
        logger.info("Test message without context")
        mock_info.assert_called_once_with("Test message without context")


def test_logger_color_formatting(logger):
    """Test that the console handler uses color formatting."""
    stream_handler = next(handler for handler in logger.logger.handlers if isinstance(handler, logging.StreamHandler))
    assert isinstance(stream_handler.formatter, colorlog.ColoredFormatter)
