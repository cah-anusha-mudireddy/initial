import argparse
import logging

from cardinal_validation_toolkit import FileResult, LineError, validate_path


def file_description(result: FileResult) -> str:
    detail = f" ({result.file_type}, {result.schema_version})" if result.file_type else ""
    return f"'{result.file_path}'{detail}"


def line_description(error: LineError) -> str:
    line = str(error.line_number).rjust(6, ' ')
    column = str(error.column_number).rjust(3, ' ')
    return f"line {line}, column {column} ({error.column_name})"


def main():
    parser = argparse.ArgumentParser("cardinal_validation_toolkit", description="Validate Cardinal CSV Files")
    parser.add_argument("--target-path", "-t", required=True, help="file or directory to validate")
    parser.add_argument("--recursive", "-r", action="store_true", help="scan all subdirectories recursively")
    args = vars(parser.parse_known_args()[0])

    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler()])

    try:
        results = validate_path(args["target_path"], args["recursive"])
        file_total = 0
        file_error_total = 0
        line_error_total = 0

        for result in results:
            file_total += 1

            if result.file_error:
                file_error_total += 1
                logging.error(f"file {file_description(result)}: {result.file_error}")
            else:
                logging.info(f"validating file {file_description(result)}...")
                line_error_inital = line_error_total

                for error in result.line_errors:
                    line_error_total += 1
                    logging.error(f"{line_description(error)}: {error.message}")

                if line_error_total > line_error_inital:
                    file_error_total += 1

        logging.info(f"{file_total - file_error_total} files passed validation")

        if file_error_total > 0 or line_error_total > 0:
            logging.error(f"{line_error_total} errors in {file_error_total} files")
            exit(1)
    except Exception as e:
        logging.error("uncaught exception:")
        logging.error(e)
        exit(1)


if __name__ == "__main__":
    main()
