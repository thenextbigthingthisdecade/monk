import argparse


def setup() -> tuple[str, str]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-log",
        "--loglevel",
        default="warning",
        help="Provide logging level. Example --loglevel debug, default=warning",
    )
    parser.add_argument(
        "-file",
        "--filePath",
        default="sample.mnk",
        help="Provide the path to the file to be compiled, default='sample.mnk'",
    )
    args = parser.parse_args()
    return args.loglevel.upper(), args.filePath


level, file_path = setup()
