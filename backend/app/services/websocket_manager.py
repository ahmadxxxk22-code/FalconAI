import asyncio
import json
import websockets


class WebSocketManager:

    def __init__(self):
        self.connections = {}

    async def connect_binance(self, symbol="btcusdt"):

        url = (
            f"wss://stream.binance.com:9443/ws/"
            f"{symbol.lower()}@kline_1m"
        )

        async with websockets.connect(url) as websocket:

            self.connections[symbol] = websocket

            while True:

                message = await websocket.recv()

                data = json.loads(message)

                yield data

    async def close(self, symbol):

        if symbol in self.connections:

            await self.connections[symbol].close()

            del self.connections[symbol]

    async def close_all(self):

        for websocket in self.connections.values():

            await websocket.close()

        self.connections.clear()
