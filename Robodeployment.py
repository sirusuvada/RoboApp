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
            print(f"Connected to {DEVICE_ADDRESS}")
            command_str = str(command).encode()
            await client.write_gatt_char(CHARACTERISTIC_UUID_RX, command_str, response=True)
            print(f"Sent command: {command}")
        else:
            st.write("Failed to connect to the device")

async def main(command):
    await send_command(command)

def run_asyncio_task(command):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(command))
    loop.close()

async def automate_with_face():
    # Load the pre-trained face cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Initialize variables
    frame_count = 0
    avg_area = 0
    direction = "Unknown"

    # Function to detect and draw rectangles around faces
    async def detect_faces(frame):
        nonlocal frame_count, avg_area, direction

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Draw rectangle around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Calculate rectangle area
            area = w * h
            st.write(area)
            # Update average area
            avg_area = (avg_area * frame_count + area) / (frame_count + 1)
            

            # If rectangle area is more than 100*100 pixels
            if area > 100 * 100:
                frame_count += 1
                # If 10 frames passed, update direction and reset frame count and average area
                if frame_count == 10:
                    if x<frame.shape[1]//4 or x+w>(3*frame.shape[1])//4:
                        direction = "Left" if x < frame.shape[1] // 4 else "Right"
                        # Send command based on direction
                        if direction == "Left":
                            await send_command(2)
                        else:
                            await send_command(3)
                    elif avg_area < 20000 and x>frame.shape[1]//4 and x<(3*frame.shape[1])//4:
                        await send_command(1)
                    elif avg_area >60000 and x>frame.shape[1]//4 and x<(3*frame.shape[1])//4:
                        await send_command(4)
                    else:
                        direction = "Not finding humans"
                    frame_count = 0
                    avg_area = 0
            else:
                await send_command(-1)

        # Convert frame to JPEG format
        _, jpeg = cv2.imencode('.jpg', frame)
        display(Image(data=jpeg.tobytes()))

    # Open webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Detect faces in the frame
        frame = cv2.flip(frame, 1)

        # Run face detection asynchronously
        await detect_faces(frame)

        # Stop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam
    cap.release()

if st.button('Move forward'):
    # run_asyncio_task(1)
    send_command(1)
    st.write('Your robo move forward')

if st.button('Move backward'):
    run_asyncio_task(4)
    st.write('Your robo move backward')
    
if st.button('Move left'):
    run_asyncio_task(2)
    st.write('Your robo move left')
    
if st.button('Move right'):
    run_asyncio_task(3)
    st.write('Your robo move right')
    
if st.button('Stop'):
    run_asyncio_task(-1)
    st.write('Your robo stopped')

if st.button('Automate with face for forward and backward'):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(automate_with_face())
    loop.close()
if st.button('stop the face algorithm'):
    cv2.VideoCapture(0).release()
