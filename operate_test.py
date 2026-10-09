from robomation import *
import time

hamster_s = HamsterS()          # 자동 탐색
hamster_s.set_wheel_speed('both', 30) # 양쪽 바퀴 속도 30으로 → 앞으로 출발
time.sleep(2) # 2초 기다림 (그동안 계속 전진)
hamster_s.set_wheel_speed('both', 0) # 양쪽 바퀴 속도 0으로 → 정지