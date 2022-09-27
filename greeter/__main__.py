import sys
import logging
import argparse
import time
import math

from . import greeter


def create_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Print a greeting.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(help="Choose task", dest="task")

    parser.add_argument("name", metavar="name", type=str, help="your name")
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="activate verbose logging output",
    )

    parser_hello = subparsers.add_parser(
        "hello",
        help="Say hello",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_bye = subparsers.add_parser(
        "bye", help="Say bye", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser_hello.add_argument(
        "--time_of_day",
        "-t",
        choices=["morning", "afternoon", "evening"],
        default="morning",
        help="Specify time of the day",
    )
    parser_bye.add_argument(
        "--friend",
        "-f",
        type=str,
        default="fulana",
        help="Say bye to a friend in addition to yourself",
    )

    return parser


def main() -> int:
    """{description of what main does}"""

    tic = time.time()

    parser = create_cli()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)

    obj = greeter.Greeter(args.name)

    if args.task == "hello":

        logging.info("saying hello...")
        obj.say_hello(time_of_day=args.time_of_day)

    elif args.task == "bye":

        logging.info("saying bye...")
        obj.say_bye(friend=args.friend)

    toc = time.time()
    runtime = round(toc - tic)
    if runtime < 60:
        logging.info(f"Runtime: {runtime} s")
    else:
        runtime_min = math.floor(runtime / 60)
        runtime_sec = runtime - (runtime_min * 60)
        logging.info(f"Runtime: {runtime_min} min and {runtime_sec} sec")

    return 0


if __name__ == "__main__":
    sys.exit(main())
