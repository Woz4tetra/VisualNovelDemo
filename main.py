import argparse
import os
from typing import cast

from game.command_line_args import CommandLineArgs
from game.runner import Runner


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("story", type=str, help="The story to run")
    parser.add_argument(
        "--log-level", type=str, default="debug", help="The log level to use"
    )
    args = parser.parse_args()

    if os.path.exists(args.story):
        args.story = os.path.abspath(args.story)

    Runner(cast(CommandLineArgs, args)).run()


if __name__ == "__main__":
    main()
