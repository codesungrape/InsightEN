"""
Provides a preconfigured logger instance for use across the application.

This module sets up a root logger with a console handler and a standardized
log message format. Other modules can import `log` from here to ensure
consistent logging behavior.
"""

import logging
import sys


def setup_logger():
    """
    Configures the root logger for the application.
    """
    # get the root logger - top-level lgoger
    logger = logging.getLogger()

    # Set the minimum level of messages to be processed
    # DEBUG is the lowest, so it will capture everything
    logger.setLevel(logging.DEBUG)

    # Create a formatter to define the log message format
    # This format includes timestamp, log level, module name, and the message.
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Create a handler to send log messages to the console
    # In Python, handlers determine where log messages go (console, file, network etc.)
    # sys.stdout ensures it goes to the standard output stream
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)  # Set level for this specific handler
    console_handler.setFormatter(formatter)

    # Optional- so edited out right now:
    # Create a handler to send log messages to a file
    # file_handler = logging.FileHandler('app.log')
    # file_handler.setLevel(logging.INFO)  # log only INFO and above to the file
    # file_handler.setFormatter(formatter)

    # Add the handlers to the root logger
    # Avoid adding handlers if they already exist
    if console_handler not in logger.handlers:
        logger.addHandler(console_handler)

    # if file_handler not in logger.handlers:
    #      logger.addHandler(file_handler)

    return logger


# Create a logger instance to be imported by other modules
log = setup_logger()
