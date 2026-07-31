import base64
import logging

from aiohttp import ClientSession

from willow.config import config


async def send_heartbeat(message, client: "SignalApi", level=logging.INFO):
    logging.log(level, f"Heartbeat: {message}")
    await client.send_message(recipient=config.signal.log_group, message=message)


class SignalApi:
    def __init__(
        self, number: str, api_key: str, base_url: str, session: ClientSession
    ):
        self.number = number
        self.api_key = api_key
        self.base_url = base_url
        self.http = session

    async def api_test(self) -> bool:
        async with self.http.get(
            f"{self.base_url}/v1/health",
            headers={"Authorization": f"Bearer {self.api_key}"},
        ) as resp:
            if resp.status != 204:
                return False
            return True

    def create_group_id(self, group_id: str) -> str:
        return f"group.{base64.b64encode(group_id.encode('ascii')).decode('ascii')}"

    async def send_message(
        self,
        recipient: str,
        message: str,
        quote_message: str | None = None,
        quote_author: str | None = None,
        quote_timestamp: int | None = None,
    ) -> int:
        body = {
            "recipients": [recipient],
            "message": message,
            "number": self.number,
            "text_mode": "styled",
        }
        if quote_author and quote_timestamp:
            body["quote_author"] = quote_author
            body["quote_timestamp"] = quote_timestamp
            if quote_message:
                body["quote_message"] = quote_message
        async with self.http.post(
            f"{self.base_url}/v2/send",
            json=body,
            headers={"Authorization": f"Bearer {self.api_key}"},
        ) as resp:
            if resp.status != 201 and not (
                resp.status == 400 and "Failed to send" in await resp.text()
            ):
                raise Exception(
                    f"Failed to send message: {resp.status} {await resp.text()}"
                )
            else:
                res = await resp.json()
                ts = res.get("timestamp")
                if not ts:
                    await send_heartbeat(
                        f"Failed to get timestamp from response: {res}", client=self
                    )
                return ts

    async def receive_messages(self) -> list[dict]:
        """
        Receive messages from the Signal API.
        """
        async with self.http.get(
            f"{self.base_url}/v1/receive/{self.number}?ignore_stories=true&ignore_avatars=true&ignore_stickers=true",
            headers={"Authorization": f"Bearer {self.api_key}"},
        ) as resp:
            if resp.status != 200:
                raise Exception(
                    f"Failed to receive messages: {resp.status} {await resp.text()}"
                )
            else:
                try:
                    res = await resp.json(content_type=None)
                    # await send_heartbeat(
                    #     f"Received {len(res)} ({type(res)}) messages\n{res}",
                    #     client=self,
                    # )
                    return res
                except Exception as e:
                    await send_heartbeat(
                        f"Failed to parse JSON response: {e}\n{resp}",
                        client=self,
                    )
                    return []
