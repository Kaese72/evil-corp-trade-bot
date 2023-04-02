"""Script file for evilbot"""
import argparse
import os
from evilbot.discordbot import run_bot
from evilbot.gcpintegration.sheets import spreadsheet_api

PARSER = argparse.ArgumentParser(
    "evilbot",
    description="discord bot for interacting with a Ev1l corp spreadsheet backend",
)
PARSER.add_argument(
    "--discord-bot-token",
    dest="discord_bot_token",
    type=str,
    default=os.environ.get("DISCORD_BOT_TOKEN"),
)
PARSER.add_argument(
    "--gcp-credentials-file",
    dest="gcp_credentials_file",
    type=str,
    default=os.environ.get("GCP_CREDENTIALS_FILE") or "credentials.json",
)
PARSER.add_argument(
    "--gcp-sheet-id",
    dest="gcp_sheet_id",
    type=str,
    default=os.environ.get("GCP_SHEET_ID"),
)

ARGS = PARSER.parse_args()
run_bot(
    token=ARGS.discord_bot_token,
    sheet_wrapper=spreadsheet_api(
        ARGS.gcp_credentials_file,
        sheet_id=ARGS.gcp_sheet_id,
    ),
)
