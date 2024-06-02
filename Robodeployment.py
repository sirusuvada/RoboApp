import bluetooth
import streamlit as st

target_name = "ESP32-BLE"
target_address = None
def fin():
    nearby_devices = bluetooth.discover_devices()
    
    for addr, name in nearby_devices:
        if target_name == name:
            target_address = addr
            break
    
    if target_address is not None:
        st.write("Found target Bluetooth device with address:")
    else:
        st.write("Could not find target Bluetooth device.")
if st.button('Say hello'):
    fin()
