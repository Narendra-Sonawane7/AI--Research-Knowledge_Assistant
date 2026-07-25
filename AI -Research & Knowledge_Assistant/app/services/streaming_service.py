import asyncio


class StreamingService:

    @staticmethod
    async def stream_text(text):

        words = text.split()

        for word in words:

            yield word + " "

            await asyncio.sleep(0.05)