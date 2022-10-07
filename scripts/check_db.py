"""
Description: Get summary stats on daily brief database log.
Author: Haley Hunter-Zinck
Date: 2022-10-04
"""

import sys
import logging
import argparse
import time
import sqlite3


def create_cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check a daily-brief database.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "file_db", type=str, help="path to file containing sqlite database"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="activate verbose logging output",
    )

    return parser


def main() -> int:
    """Print summary statistics on the database."""

    tic = time.time()

    parser = create_cli()
    args = parser.parse_args()

    conn = sqlite3.connect(args.file_db)
    cur = conn.cursor()

    statement = "SELECT COUNT(*) FROM log"
    cur.execute(statement)
    n_log_entry = cur.fetchall()[0][0]
    print(f"Number of log entries: {n_log_entry}")

    n_run = 1
    statement = f"SELECT run FROM log ORDER BY rowid DESC LIMIT {n_run}"
    cur.execute(statement)
    run = cur.fetchall()[0][0]
    print(f"Last run: {run}")

    cur.close()
    conn.close()

    logging.info(f"Runtime: {round(time.time() - tic)} s")

    return 0


if __name__ == "__main__":
    sys.exit(main())
