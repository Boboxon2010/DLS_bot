from ppadb.client import Client as AdbClient
import cv2
import numpy as np

def test_connection():
    # ADBga ulanish
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    
    if len(devices) == 0:
        print("XATO: LDPlayer topilmadi! ADB Debugni yoqing.")
        return

    device = devices[0]
    print(f"Muvaffaqiyatli ulandi: {device.serial}")

    # Skrinshot olish testi
    print("Ekran rasmga olinmoqda...")
    screenshot = device.screencap()
    img = cv2.imdecode(np.frombuffer(screenshot, np.uint8), cv2.IMREAD_COLOR)
    
    # Rasmni ko'rsatish
    cv2.imshow("Bot nima ko'rayapti?", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_connection()
