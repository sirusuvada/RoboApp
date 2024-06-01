import streamlit as st
from bleak import BleakScanner, BleakClient

# Streamlit UI
st.title("BLE Device Interaction")

# Scan for nearby BLE devices
st.write("Scanning for nearby BLE devices...")
devices = BleakScanner.discover()

# Display list of discovered devices
device_names = [device.name for device in devices]
selected_device = st.selectbox("Select a device:", device_names)

# Connect to selected device
client = BleakClient(selected_device)

if st.button("Connect"):
    st.write(f"Connecting to {selected_device}...")
    connected = await client.connect()
    if connected:
        st.write("Connected to device.")

        # Example: Read data from a characteristic
        data = await client.read_gatt_char("0000XXXX-0000-1000-8000-00805f9b34fb")
        st.write("Data:", data)

        # Example: Write data to a characteristic
        # await client.write_gatt_char("0000XXXX-0000-1000-8000-00805f9b34fb", b"Hello")

    else:
        st.write("Failed to connect to device.")

# Disconnect from device when finished
if st.button("Disconnect"):
    await client.disconnect()
    st.write("Disconnected from device.")
