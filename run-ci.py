import argparse
import os
import sys

import ci.cpp


def make_sub_parser(subparsers, name):
    parser = subparsers.add_parser(name)
    parser.add_argument(
        "--profile", action="append", dest="profiles", required=True
    )
    parser.add_argument("--user", default="tanker")
    parser.add_argument("--ref", required=True)
    return parser


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    subparsers.add_parser("clean-conan-cache")

    build_parser = make_sub_parser(subparsers, "build")
    deploy_parser = make_sub_parser(subparsers, "deploy")

    args = parser.parse_args()
    command = args.command

    ci.cpp.update_conan_config(sys.platform.lower())
    ci.cpp.set_build_env()
    if command == "clean-conan-cache":
        ci.cpp.clean_conan_cache()
    elif command in ("build", "deploy"):
        native_commit_hash = os.environ.get("SDK_NATIVE_COMMIT_HASH")
        channel, version = args.ref.split("/")
        deployer = ci.cpp.Deployer(
            channel=channel,
            version=version,
            profiles=args.profiles, user=args.user,
        )
        should_upload = (command == "deploy")
        deployer.build(
            upload=should_upload,
            native_commit_hash=native_commit_hash,
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
