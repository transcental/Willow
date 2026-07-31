async def boop_command(client, envelope):
    """
    Handle the w/boop command.
    """
    data = envelope.get("dataMessage", {})
    internal_group_id = data.get("groupInfo", {}).get("groupId")
    group_id = client.create_group_id(internal_group_id)
    quote_message = data.get("message")
    quote_timestamp = data.get("timestamp")
    quote_author = envelope.get("source")

    # await send_heartbeat(f"Boop command received from {quote_author} in group {group_id}\nquote: {quote_message}\nquote_timestamp: {quote_timestamp}\nquote_author: {quote_author}", client)

    await client.send_message(
        recipient=group_id,
        message="*boop*",
        quote_message=quote_message,
        quote_author=quote_author,
        quote_timestamp=quote_timestamp,
    )
