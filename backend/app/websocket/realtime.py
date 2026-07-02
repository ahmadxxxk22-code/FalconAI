from fastapi import WebSocket, WebSocketDisconnect
from app.services.signal_engine import SignalEngine
import asyncio


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send(self, websocket: WebSocket, message: dict):
        await websocket.send_json(message)


manager = ConnectionManager()
engine = SignalEngine()


async def stream_signals(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            signal = engine.analyze_market(
                symbol="BTCUSDT",
                timeframe="1m"
            )

            await manager.send(websocket, signal)

            await asyncio.sleep(5)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
