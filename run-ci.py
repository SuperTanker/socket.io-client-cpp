import argparse
import sys

import ci.cpp


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="subcommands", dest="command")

    clean_cache_parser = subparsers.add_parser("clean-conan-cache")

    build_parser = subparsers.add_parser("deploy")
    build_parser.add_argument(
        "--profile", action="append", dest="profiles", required=True
    )
    build_parser.add_argument("--user", default="tanker")
    build_parser.add_argument("--build-only", action="store_false", dest="upload")
    build_parser.add_argument("--ref", required=True)
    build_parser.add_argument("--native-commit-hash", dest="native_commit_hash")

    args = parser.parse_args()

    ci.cpp.update_conan_config(sys.platform.lower())
    if args.command == "clean-conan-cache":
        ci.cpp.clean_conan_cache()
    elif args.command == "deploy":
        if args.upload and not args.native_commit_hash:
            sys.exit("--native-commit-hash must be passed when uploading")
        if not args.upload and args.native_commit_hash:
            sys.exit("--native-commit-hash cannot be used with --build-only")
        channel, version = args.ref.split("/")
        deployer = ci.cpp.Deployer(
            channel=channel,
            version=version,
            profiles=args.profiles, user=args.user,
        )
        deployer.build(
            upload=args.upload,
            native_commit_hash=args.native_commit_hash,
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
