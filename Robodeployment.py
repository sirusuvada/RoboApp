import streamlit as st
import pygatt

st.title("ESP32 BLE Communication")

if 'adapter' not in st.session_state:
    st.session_state.adapter = None
    st.session_state.device = None

st.header("Connect to ESP32")

selected_device = st.text_input("Enter the MAC Address of the ESP32")

if st.button("Connect"):
    if not selected_device:
        st.error("Please enter a MAC address.")
    else:
        if not st.session_state.adapter:
            st.session_state.adapter = pygatt.GATTToolBackend()
            st.session_state.adapter.start()

        try:
            device = st.session_state.adapter.connect(selected_device, address_type=pygatt.BLEAddressType.random)
            st.session_state.device = device
            st.success(f"Connected to ESP32 with MAC Address: {selected_device}")
        except pygatt.exceptions.NotConnectedError:
            st.error("Failed to connect. Make sure the MAC address is correct and the device is in range.")

if st.session_state.device:
    device = st.session_state.device

    st.header("Send Data to ESP32")
    user_input = st.text_input("Enter data to send")

    if st.button("Send"):
        try:
            device.char_write("YOUR_CHARACTERISTIC_UUID", bytearray(user_input, 'utf-8'))
            st.success(f"Sent: {user_input}")
        except pygatt.exceptions.BLEError as e:
            st.error(f"Failed to send data: {e}")

    st.header("Read Data from ESP32")
    if st.button("Read"):
        try:
            data = device.char_read("YOUR_CHARACTERISTIC_UUID")
            st.write(f"Received: {data.decode('utf-8')}")
        except pygatt.exceptions.BLEError as e:
            st.error(f"Failed to read data: {e}")

    if st.button("Disconnect"):
        device.disconnect()
        st.session_state.device = None
        st.success("Disconnected")

st.sidebar.header("About")
st.sidebar.info(
    "This app allows you to communicate with an ESP32 device over a Bluetooth Low Energy (BLE) connection. "
    "Use the options to connect, send data, and read data."
)
