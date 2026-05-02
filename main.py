import cv2
import numpy as np
from ppadb.client import Client as AdbClient
import time
import math
import random

class DLSBot:
    def __init__(self):
        self.client = AdbClient(host="127.0.0.1", port=5037)
        self.devices = self.client.devices()
        self.device = self.devices[0]

        # Koordinatalar (1014x569 rasm asosida)
        self.JOY_CENTER = (120, 460)
        self.BTN_A = (935, 475) # Hard Kick
        self.BTN_B = (800, 500) # Low Kick / Pressure
        
        # To'p shabloni
        self.ball_template = cv2.imread('ball.png', 0)

    def get_screen(self):
        sreencap = self.device.screencap()
        return cv2.imdecode(np.frombuffer(sreencap, np.uint8), cv2.IMREAD_COLOR)

    def find_ball(self, screen):
        gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(gray, self.ball_template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.6: # 60% o'xshashlik
            w, h = self.ball_template.shape[::-1]
            return (max_loc[0] + w//2, max_loc[1] + h//2)
        return None

    def move_joystick(self, tx, ty, duration=200):
        sx, sy = self.JOY_CENTER
        # Tasodifiy zig-zag qo'shish (Aldab o'tish uchun)
        tx += random.randint(-10, 10)
        ty += random.randint(-10, 10)
        
        angle = math.atan2(ty - sy, tx - sx)
        ex = int(sx + 80 * math.cos(angle))
        ey = int(sy + 80 * math.sin(angle))
        self.device.shell(f"input swipe {sx} {sy} {ex} {ey} {duration}")

    def tap(self, x, y):
        self.device.shell(f"input tap {x} {y}")

    def play(self):
        print("Bot o'yinni boshladi...")
        while True:
            frame = self.get_screen()
            ball = self.find_ball(frame)

            if ball:
                bx, by = ball
                print(f"To'p koordinatasi: {bx}, {by}")

                # 1. Agar to'p raqib darvozasi oldida bo'lsa (O'ng tomonda)
                if bx > 750:
                    print("GOL URISH IMKONIYATI!")
                    self.move_joystick(bx, by, 100)
                    self.tap(*self.BTN_A) # Zarba!
                
                # 2. To'pni quvib yurish
                else:
                    self.move_joystick(bx, by, 150)
                    # Himoya uchun vaqti-vaqti bilan B ni bosib turadi
                    if random.random() > 0.7:
                        self.tap(*self.BTN_B)
            else:
                # To'p yo'qolsa, oldinga (o'ngga) qarab yur
                self.move_joystick(900, 300, 200)

            time.sleep(0.05) # Tezlikni oshirish uchun kichik tanaffus

if __name__ == "__main__":
    bot = DLSBot()
    bot.play()
