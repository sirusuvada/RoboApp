import streamlit as st
import asyncio
from bleak import BleakClient

# UUIDs for the BLE service and characteristics
SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
CHARACTERISTIC_UUID_RX = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

# Replace this with your ESP32's MAC address
DEVICE_ADDRESS = "AE3E8C07-584F-76DE-5522-F8ABCAFC0030"

async def send_command(command):
    async with BleakClient(DEVICE_ADDRESS) as client:
        if client.is_connected:
            if command == 1:
                await client.write_gatt_char(CHARACTERISTIC_UUID_RX, b"1", response=True)
            elif command == 0:
                await client.write_gatt_char(CHARACTERISTIC_UUID_RX, b"0", response=True)
        else:
            st.write("Failed to connect to the device")

if st.button('Glow your LED'):
    asyncio.run(send_command(1))
    st.write('Your LED glows')

if st.button('Turn off your LED'):
    asyncio.run(send_command(0))
    st.write('Your LED turns off')
