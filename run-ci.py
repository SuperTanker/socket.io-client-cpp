import argparse
import sys

import ci.cpp


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    build_parser = subparsers.add_parser("deploy")
    build_parser.add_argument(
        "--profile", action="append", dest="profiles", required=True
    )
    build_parser.add_argument("--user", default="tanker")
    build_parser.add_argument("--build-only", action="store_false", dest="upload")
    build_parser.add_argument("--ref", required=True)

    args = parser.parse_args()

    ci.cpp.update_conan_config(sys.platform.lower())
    if args.command == "deploy":
        channel, version = args.ref.split("/")
        deployer = ci.cpp.Deployer(
            channel=channel,
            version=version,
            profiles=args.profiles, user=args.user,
        )
        deployer.build()
        if args.upload:
            deployer.upload()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
