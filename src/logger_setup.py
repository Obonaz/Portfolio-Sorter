import logging
import os

# Default log file path can be defined here or passed as an argument
DEFAULT_LOG_FILE = 'logs/sorting_app.log'
LOGGER_NAME = "FileSorterApp"

def setup_logging(log_file_path: str = DEFAULT_LOG_FILE, level: int = logging.INFO) -> logging.Logger:
    """
    Configures and returns a logger instance for the application.

    Args:
        log_file_path: The full path to the log file.
        level: The logging level for the logger and handlers.

    Returns:
        A configured logging.Logger instance.
    """
    logger = logging.getLogger(LOGGER_NAME)

    # Prevent adding handlers multiple times if this function is called more than once
    if logger.handlers:
        # Logger is already configured (e.g., if setup_logging was called previously)
        # You might want to check if configuration is identical or update it,
        # but for now, simply returning the existing logger is fine.
        return logger

    logger.setLevel(level)

    # Ensure the log directory exists
    log_dir = os.path.dirname(log_file_path)
    if log_dir: # Ensure log_dir is not an empty string (e.g. if log_file_path is just 'app.log')
        os.makedirs(log_dir, exist_ok=True)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create File Handler
    try:
        file_handler = logging.FileHandler(log_file_path, mode='a') # 'a' for append
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        # Fallback to console logging if file handler fails
        print(f"Error setting up file handler for logging: {e}. Logging to console only.")


    # Create Console Handler (recommended for development)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG) # Or use the same 'level' as the file handler
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logger.info(f"Logger '{LOGGER_NAME}' configured. Logging to file: {log_file_path}")

    return logger

if __name__ == '__main__':
    # Example usage:
    # Call setup once at the beginning of your application
    logger1 = setup_logging(level=logging.DEBUG)
    logger1.debug("This is a debug message from logger1.")
    logger1.info("This is an info message from logger1.")
    logger1.warning("This is a warning message from logger1.")
    logger1.error("This is an error message from logger1.")

    # Demonstrate getting the logger instance elsewhere
    # (it will be the same instance with the same handlers)
    logger2 = logging.getLogger(LOGGER_NAME)
    logger2.info("This is an info message from logger2, using the same logger instance.")

    # Test that handlers are not duplicated
    logger3 = setup_logging() # Calling setup_logging again
    logger3.info("This is an info message from logger3 after calling setup_logging again. Should not have duplicate handlers.")

    print(f"Logger '{logger1.name}' has {len(logger1.handlers)} handlers.")
    assert len(logger1.handlers) == 2 # Or 1 if file handler failed
    print(f"Logger '{logger2.name}' has {len(logger2.handlers)} handlers.")
    assert len(logger2.handlers) == 2 # Or 1
    print(f"Logger '{logger3.name}' has {len(logger3.handlers)} handlers.")
    assert len(logger3.handlers) == 2 # Or 1

    # Test logging to a different file
    custom_log_file = 'logs/custom_test_log.log'
    if os.path.exists(custom_log_file):
        os.remove(custom_log_file)

    # Need to reset for testing a different configuration.
    # This is tricky because getLogger returns the same logger instance.
    # For a true reset, we'd need to remove handlers or use a different logger name.
    # For this test, we'll rely on the fact that our setup_logging guard
    # prevents re-adding handlers to the *same* logger if called multiple times.
    # To test a *new* file, we'd typically do this with a different logger name or by
    # clearing handlers of the existing logger first.
    
    # Let's try a simple way to test a new file by removing previous handlers for LOGGER_NAME
    # This is more for testing the setup function itself rather than typical app usage.
    existing_logger = logging.getLogger(LOGGER_NAME)
    if existing_logger.handlers:
        existing_logger.handlers = [] # Clear handlers for re-configuration for this test

    logger_custom_file = setup_logging(log_file_path=custom_log_file, level=logging.INFO)
    logger_custom_file.info(f"This message should go to '{custom_log_file}'.")

    if os.path.exists(custom_log_file):
        with open(custom_log_file, 'r') as f:
            content = f.read()
            assert f"This message should go to '{custom_log_file}'." in content
            print(f"Message successfully logged to '{custom_log_file}'.")
        os.remove(custom_log_file) # Clean up
    else:
        print(f"Error: Custom log file '{custom_log_file}' was not created.")

    print("Logger setup tests completed.")
