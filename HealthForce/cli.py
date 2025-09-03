import argparse
import asyncio
from linkedin import run_linkedin_extractor
from textracter import run_textract_extractor


def main():
    parser = argparse.ArgumentParser(prog="healthforce_test_project")
    subparsers = parser.add_subparsers(dest="command")

    # LinkedIn
    li_parser = subparsers.add_parser("linkedin", help="Extract LinkedIn posts")
    li_parser.add_argument("--profile-url", required=True, help="LinkedIn profile URL")
    li_parser.add_argument(
        "--min-posts", type=int, default=5, help="Minimum posts to fetch"
    )

    # Textract
    tx_parser = subparsers.add_parser("textract", help="Extract docs with AWS Textract")
    tx_parser.add_argument(
        "--invoice-path", required=True, help="Path to invoice image"
    )
    tx_parser.add_argument(
        "--rx-path", required=True, help="Path to Italian prescription image"
    )

    args = parser.parse_args()

    if args.command == "linkedin":
        asyncio.run(run_linkedin_extractor(args.profile_url, args.min_posts))
    elif args.command == "textract":
        run_textract_extractor(args.invoice_path, args.rx_path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
