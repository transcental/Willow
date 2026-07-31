from willow.config import config
from willow.utils.parser import parse_command
from willow.utils.signal import SignalApi


async def receive_messages(client: SignalApi):
    """
    Receive messages from the Signal API and call the callback function for each message.
    """
    for envelope in await client.receive_messages():
        if envelope:
            message = envelope.get("envelope", {}).get("dataMessage", {})
            content = message.get("message")
            if content:
                if content.startswith(config.signal.prefix):
                    await parse_command(client, envelope.get("envelope", {}))
