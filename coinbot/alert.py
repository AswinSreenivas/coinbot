"""Send text messages using Twilio."""
import os
from typing import List
from typing import Optional

import click
from twilio.rest import Client


def text_alert(all_values: bool, msg: str, recipients: List[str], from_number: str) -> None:
    """Send a text message alert."""
    twilio_client = get_twilio_client()
    send_text_msg(twilio_client, recipients, from_number, msg)


def get_from_number() -> Optional[str]:
    """Read the Twilio from number from the environment."""
    return os.environ.get("TWILIO_FROM")


def get_twilio_client() -> Client:
    """Get a Twilio client."""
    return Client(os.environ.get("TWILIO_ACCOUNT_SID"), os.environ.get("TWILIO_AUTH_TOKEN"))


def get_phone_numbers() -> Optional[list[str]]:
    """Get the phone numbers to send text messages to."""
    # print("ALERT RECIPIENTS:", os.environ.get("ALERT_RECIPIENTS"))
    nums = os.environ.get("ALERT_RECIPIENTS")
    return nums.split(",") if nums is not None else None


def send_text_msg(client: Client, recipients: list[str], from_number: str, msg: str) -> None:
    """Send a text message to the recipients."""
    click.echo("Alert sent!")
    for num in recipients:
        client.messages.create(
            to=num,
            from_=from_number,
            body=msg,
        )
