import asyncio
from bleak import BleakClient, BleakScanner

SERVICE_UUID = "0000FFF0-0000-1000-8000-00805F9B34FB"
CHARACTERISTIC_UUID = "0000FFF1-0000-1000-8000-00805F9B34FB"
OUTPUT_FILE = "received_audio.wav"

audio_buffer = bytearray()

async def main():
    print("Scanning for devices...")
    devices = await BleakScanner.discover()

    for device in devices:
        if device.name and "XIAO_S3_SENSE" in device.name:
            print(f"Found device: {device.name} ({device.address})")
            async with BleakClient(device.address) as client:
                print("Connected to XIAO S3")

                def callback(sender, data):
                    global audio_buffer
                    audio_buffer.extend(data)
                    print(f"Received {len(data)} bytes")

                # Start notifications and receive data
                await client.start_notify(CHARACTERISTIC_UUID, callback)
                await asyncio.sleep(180)  # Wait longer for the full recording and transmission
                await client.stop_notify(CHARACTERISTIC_UUID)

                # Save received data to WAV file
                if audio_buffer:
                    with open(OUTPUT_FILE, "wb") as f:
                        f.write(audio_buffer)
                    print(f"Audio saved to {OUTPUT_FILE}")
                else:
                    print("No audio data received.")
            break
    else:
        print("Device not found.")

if __name__ == "__main__":
    asyncio.run(main())
