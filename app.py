import argparse
import os
import logging
import sys

# Add src to Python path to allow direct import of modules from src
# This is often needed when running a script from the project root
# that imports from a subdirectory like 'src'.
# A more robust solution might involve setting PYTHONPATH environment variable
# or using a proper package structure (e.g., setup.py).
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

try:
    from main_sorter import process_files
    from logger_setup import setup_logging, LOGGER_NAME
except ImportError as e:
    print(f"Error importing necessary modules. Ensure 'src' directory is accessible and contains required files: {e}")
    # If these core modules are missing, the app cannot run.
    # No logger is available yet, so direct print is used.
    sys.exit(1)


if __name__ == "__main__":
    # 1. Setup Logging (as early as possible)
    # If logger_setup itself fails, it might print to console.
    try:
        setup_logging() # Configures root logger and handlers
        logger = logging.getLogger(LOGGER_NAME) # Get the specific app logger
    except Exception as e:
        # Fallback if logging setup fails catastrophically
        print(f"Critical error during logging setup: {e}. Exiting.", file=sys.stderr)
        sys.exit(1)

    # 2. Argument Parsing
    parser = argparse.ArgumentParser(description="Sorts document files from a source directory into categorized subfolders in a target directory.")
    parser.add_argument("source_dir", help="Source directory containing files to sort.")
    parser.add_argument("target_dir", help="Target directory where categorized subfolders will be created.")
    
    args = parser.parse_args()

    # 3. Input Validation
    logger.info(f"Application invoked with Source: '{args.source_dir}', Target: '{args.target_dir}'")

    if not os.path.isdir(args.source_dir):
        error_msg = f"Source directory '{args.source_dir}' does not exist or is not a directory."
        print(error_msg, file=sys.stderr)
        logger.critical(error_msg)
        sys.exit(1)

    if os.path.abspath(args.source_dir) == os.path.abspath(args.target_dir):
        error_msg = "Source and target directories cannot be the same. This could lead to data loss or unexpected behavior."
        print(error_msg, file=sys.stderr)
        logger.critical(error_msg)
        sys.exit(1)
    
    # Note: main_sorter.py already handles creation of target_dir if it doesn't exist
    # and logs a warning. If it fails to create, it logs an error and returns.
    # So, we don't need to explicitly create args.target_dir here, but we could add
    # a check for writability if desired, though that can be complex.

    # 4. Run the Sorting Process
    print(f"Starting file sorting process from '{args.source_dir}' to '{args.target_dir}'...")
    logger.info(f"Initiating file processing from source: {args.source_dir} to target: {args.target_dir}")

    try:
        process_files(args.source_dir, args.target_dir)
        success_msg = "File sorting process completed successfully."
        print(success_msg)
        logger.info(success_msg)
    except KeyboardInterrupt:
        interruption_msg = "\nSorting process interrupted by user. Exiting."
        print(interruption_msg)
        logger.warning("Sorting process interrupted by user.")
        sys.exit(130)  # Standard exit code for Ctrl+C
    except FileNotFoundError as e: # Should ideally be caught within process_files or its callees
        error_msg = f"Error: A file or directory was not found: {e}. Please ensure all paths are correct."
        print(error_msg, file=sys.stderr)
        logger.critical(f"Critical path error: {e}", exc_info=True)
        sys.exit(1)
    except Exception as e:
        error_msg = f"An unexpected error occurred: {e}"
        print(error_msg, file=sys.stderr)
        # exc_info=True will log the full stack trace for unexpected errors
        logger.critical(f"An unexpected critical error occurred: {e}", exc_info=True)
        sys.exit(1)
