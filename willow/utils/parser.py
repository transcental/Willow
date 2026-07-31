from willow.commands import COMMANDS
from willow.commands import HELP_MESSAGE
from willow.config import config
from willow.utils.signal import SignalApi


async def parse_command(client: SignalApi, envelope: dict):
    """
    Parse the command from the message and call the appropriate handler.
    """
    data = envelope.get("dataMessage", {})
    message = data.get("message")
    command_name = message.split()[0][
        len(config.signal.prefix) :
    ]  # Remove prefix and get command name

    for command in COMMANDS:
        if command.name == command_name:
            await command.handler(client, envelope)
            return

    quote_timestamp = data.get("timestamp")
    quote_author = envelope.get("source")

    # If no command matched, send a message back to the user
    group_id = client.create_group_id(data.get("groupInfo", {}).get("groupId"))

    if group_id:
        await client.send_message(
            recipient=group_id,
            message=f"Unknown command: {command_name}.\n{HELP_MESSAGE}",
            quote_author=quote_author,
            quote_timestamp=quote_timestamp,
            quote_message=message,
        )
