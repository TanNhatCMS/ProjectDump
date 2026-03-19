import sys
import os
import argparse
from aggregator import aggregate_code
from constants import TEXT_VI, TEXT_EN


def main():
    print("🚀 PROJECTDUMP")
    print("=" * 40)

    # Select language
    lang = input("🌐 Select language (en/vi): ").strip().lower()
    text = TEXT_EN if lang == "en" else TEXT_VI


    # Argument parsing
    parser = argparse.ArgumentParser(description="PROJECTDUMP - Aggregate project source files")
    parser.add_argument("path", nargs="?", help=text["input_project_path"], default=os.getcwd())
    parser.add_argument(
        "--include-text", "-t",
        action="store_true",
        help="Include .txt and .md files"
    )
    args = parser.parse_args()

    project_path = os.path.abspath(args.path)
    include_text = args.include_text

    success = aggregate_code(project_path, text, include_text=include_text)

    if success:
        print(text["done"])
    else:
        print(text["error"])
        sys.exit(1)


if __name__ == "__main__":
    main()