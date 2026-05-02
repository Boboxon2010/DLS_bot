import cv2
import numpy as np
from ppadb.client import Client as AdbClient

def connect_device():
    # LDPlayer odatda 5554, 5556 yoki 5558 portlarida ishlaydi
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    
    if len(devices) == 0:
        print("LDPlayer topilmadi! ADB yoqilganini tekshiring.")
        return None
    
    device = devices[0]
    print(f"Ulandi: {device.serial}")
    return device

def get_screen(device):
    # Ekran rasmini olish
    image_bytes = device.screencap()
    image_array = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return frame

# Tekshirish
device = connect_device()
if device:
    frame = get_screen(device)
    cv2.imshow("LDPlayer Ekrani", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
