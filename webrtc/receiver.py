import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription

async def consume_media(pc):
    while True:
        # Access and process media
        for track in pc.getTracks():
            if track.kind == "video":
                frame = await track.recv()
                process_frame(frame)

async def run(pc, offer):
    await pc.setRemoteDescription(offer)

    # Here you can add your own tracks or media processing if needed

    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)
    return pc.localDescription

async def main():
    pc = RTCPeerConnection()
    offer = ...  # Get the offer from the remote peer

    answer = await run(pc, offer)
    # Send the answer back to the remote peer

    # Consume incoming media
    await consume_media(pc)

asyncio.run(main())
