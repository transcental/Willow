from dataclasses import dataclass
from types import FunctionType

from willow.commands.boop import boop_command
from willow.config import config


@dataclass
class Command:
    name: str
    description: str
    handler: FunctionType


COMMANDS = [
    Command(
        name="boop",
        description="Send a boop message.",
        handler=boop_command,
    ),
    Command(
        name="help",
        description="List all available commands.",
        handler=lambda client, envelope: client.send_message(
            recipient=client.create_group_id(
                envelope.get("dataMessage", {}).get("groupInfo", {}).get("groupId")
            ),
            message="\n".join(
                [
                    f"`{config.signal.prefix}{cmd.name}`: {cmd.description}"
                    for cmd in COMMANDS
                ]
            ),
            quote_message=envelope.get("dataMessage", {}).get("message"),
            quote_author=envelope.get("source"),
            quote_timestamp=envelope.get("dataMessage", {}).get("timestamp"),
        ),
    ),
]

HELP_MESSAGE = "\n".join(
    [f"`{config.signal.prefix}{cmd.name}`: {cmd.description}" for cmd in COMMANDS]
)
