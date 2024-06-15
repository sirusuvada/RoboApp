import asyncio
from bleak import BleakClient,BleakError
import streamlit as st

# UUIDs for the BLE service and characteristics
SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
CHARACTERISTIC_UUID_RX = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

# Replace this with your ESP32's MAC address
DEVICE_ADDRESS = "AE3E8C07-584F-76DE-5522-F8ABCAFC0030"

async def send_command(command):
    try:
        async with BleakClient(DEVICE_ADDRESS) as client:
            if client.is_connected:
                print(f"Connected to {DEVICE_ADDRESS}")
                command_str = str(command).encode()
                await client.write_gatt_char(CHARACTERISTIC_UUID_RX, command_str, response=True)
                print(f"Sent command: {command}")
            else:
                st.write("Failed to connect to the device")
    except BleakError as e:
        st.write(f" {e}. ")

async def main(command):
    await send_command(command)

def run_asyncio_task(command):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(command))
    loop.close()

# Use run_asyncio_task to run the async code
if(st.button('hi')):
   run_asyncio_task(3)
