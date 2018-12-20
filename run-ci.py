import argparse
import os
import sys

import ci.cpp


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    subparsers.add_parser("clean-conan-cache")

    build_parser = subparsers.add_parser("deploy")
    build_parser.add_argument(
        "--profile", action="append", dest="profiles", required=True
    )
    build_parser.add_argument("--user", default="tanker")
    build_parser.add_argument("--ref", required=True)
    build_parser.add_argument("--native-commit-hash", dest="native_commit_hash")

    args = parser.parse_args()

    ci.cpp.update_conan_config(sys.platform.lower())
    if args.command == "clean-conan-cache":
        ci.cpp.clean_conan_cache()
    elif args.command == "deploy":
        native_commit_hash = os.environ.get("SDK_NATIVE_COMMIT_HASH")
        channel, version = args.ref.split("/")
        deployer = ci.cpp.Deployer(
            channel=channel,
            version=version,
            profiles=args.profiles, user=args.user,
        )
        deployer.build(
            upload=True,
            native_commit_hash=native_commit_hash,
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
