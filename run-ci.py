import argparse
from path import Path

import ci.cpp


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    subparsers.add_parser("build")
    subparsers.add_parser("deploy")

    args = parser.parse_args()
    command = args.command

    ci.cpp.update_conan_config()
    should_upload = command == "deploy"
    ci.cpp.set_home_isolation()
    ci.cpp.build_recipe(Path.getcwd(), upload=should_upload, conan_reference=None)


if __name__ == "__main__":
    main()
