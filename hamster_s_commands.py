# =============================================================
#  햄스터 S 파이썬 명령어 모음 (robomation 패키지)
# -------------------------------------------------------------
#  설치:   python -m pip install -U robomation
#  실행:   python hamster_s_commands.py
#  중지:   Ctrl + C
#
#  카테고리별로 함수가 나뉘어 있습니다.
#  맨 아래 RUN 목록에서 실행하고 싶은 것만 남기고 실행하세요.
#  (전부 한꺼번에 돌리면 로봇이 계속 움직이니 책상 위에서는 주의!)
#  출처: https://github.com/RobomationLAB/Robomation_Python/wiki/HamsterS
# =============================================================

from robomation import *
import time


# -------------------------------------------------------------
# 0. 연결하기
# -------------------------------------------------------------
hamster_s = HamsterS()                       # 자동 탐색으로 연결
# hamster_s = HamsterS('COM3')               # 포트 지정 (아두이노와 같이 쓸 때 권장)
# hamster_s = HamsterS(0, address='D9:4B:8B:A4:E1:67')  # 제품 고유 주소 지정
#
# 로봇 2대 이상: 번호를 다르게 + 주소 지정
# hamster_s1 = HamsterS(0, address='D9:4B:8B:A4:E1:67')
# hamster_s2 = HamsterS(1, address='AA:BB:CC:DD:EE:FF')
#
# 고유 주소는 연결 시 출력되는 메시지에서 확인:
#   HamsterS[0] Connected: COM3 D9:4B:8B:A4:E1:67


# -------------------------------------------------------------
# 1. 이동 · 회전
#    wait=True(기본): 동작이 끝날 때까지 다음 줄로 안 넘어감
#    wait=False      : 바로 다음 줄 실행
# -------------------------------------------------------------
def demo_move():
    # 바퀴 속도 설정: 'left' / 'right' / 'both', -100 ~ 100 (0 = 정지, 음수 = 후진)
    hamster_s.set_wheel_speed('both', 30)
    time.sleep(1)
    hamster_s.set_wheel_speed('left', 30)    # 왼쪽만 → 오른쪽으로 돎
    hamster_s.set_wheel_speed('right', -30)  # 오른쪽 후진 → 제자리 회전
    time.sleep(1)

    # 현재 속도에 값 더하기 (-200 ~ 200)
    hamster_s.set_wheel_speed('both', 20)
    hamster_s.change_wheel_speed('both', 10) # 20 → 30
    time.sleep(1)

    # 멈추기
    hamster_s.stop()

    # 거리만큼 이동: 단위 'cm'(기본) / 'mm' / 'inch'
    hamster_s.move_distance(10, 'cm')

    # 시간(초)만큼 이동
    hamster_s.move_time(1)

    # 제자리 회전: 'left' / 'right', 각도(도)
    hamster_s.turn_degree('left', 90)
    hamster_s.turn_degree('right', 90)

    # 바퀴가 움직이는 중인지 확인 (True / False)
    hamster_s.move_time(2, wait=False)
    while hamster_s.wheel_moving():
        print('이동 중...')
        time.sleep(0.5)

    # 현재 바퀴 속도 읽기
    print('왼쪽 바퀴 속도:', hamster_s.wheel_speed('left'))


def demo_grid():
    # 말판 위에서 한 칸 이동 / 90도 회전
    hamster_s.grid_move()
    hamster_s.grid_turn('left')              # 'left' / 'right'
    hamster_s.grid_move()


def demo_pen():
    # 펜 홀더에 펜을 꽂고 사용
    # 기준점 중심 회전
    #   base: 'left_pen' / 'right_pen' / 'left_wheel' / 'right_wheel'
    #   direction: 'forward' / 'backward'
    hamster_s.pivot('left_pen', 'forward', 90)

    # 원 그리기
    #   base: 'left_pen' / 'right_pen'
    #   direction: 'left_forward' / 'left_backward' / 'right_forward' / 'right_backward'
    #   (각도, 반지름, 단위 'cm'/'mm'/'inch')
    hamster_s.pivot_circle('left_pen', 'left_forward', 360, 5, 'cm')


# -------------------------------------------------------------
# 2. 선 따라가기 (검은 선 위에 놓고 실행)
# -------------------------------------------------------------
def demo_line():
    hamster_s.set_trace_speed(5)             # 속도 1 ~ 10
    hamster_s.set_trace_gain(5)              # 방향 변화량 1 ~ 10 (클수록 급하게 꺾음)

    # 선 따라가기 시작
    #   floor: 'left' / 'right' / 'center',  line: 'black'(기본) / 'white'
    hamster_s.trace_line('center', 'black')
    time.sleep(5)
    hamster_s.stop_trace()                   # 선 따라가기 종료

    # 교차로까지 이동: 'left' / 'right' / 'forward' / 'uturn'
    hamster_s.trace_intersection('forward', 'black')
    hamster_s.trace_intersection('left', 'black')


# -------------------------------------------------------------
# 3. LED
# -------------------------------------------------------------
def demo_led():
    # 색 이름: 'black' 'red' 'yellow' 'green' 'cyan' 'blue' 'magenta' 'white'
    hamster_s.set_led_color('both', 'red')
    time.sleep(1)
    hamster_s.set_led_color('left', 'blue')
    hamster_s.set_led_color('right', 'green')
    time.sleep(1)

    # RGB 직접 지정 (각 0 ~ 255)
    hamster_s.set_led_color('both', 255, 128, 0)
    time.sleep(1)

    # 현재 색에 RGB 값 더하기 (각 -255 ~ 255)
    hamster_s.set_led_color('both', 0, 0, 0)
    for _ in range(10):
        hamster_s.change_led_color('both', 25, 0, 25)
        time.sleep(0.1)

    # LED 끄기: 'left' / 'right' / 'both'(기본)
    hamster_s.turn_off('both')


# -------------------------------------------------------------
# 4. 소리
# -------------------------------------------------------------
def demo_sound():
    # 주파수(Hz)로 버저음: 122.1 ~ 4186.0, 0 = 끔
    hamster_s.sound_buzz(440)
    time.sleep(0.5)
    hamster_s.sound_buzz(0)

    # 음계 재생: 'C' 'C#' 'D' 'D#' 'E' 'F' 'F#' 'G' 'G#' 'A' 'A#' 'B', 옥타브 3 ~ 7
    for note in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
        hamster_s.sound_note(note, 4)
        time.sleep(0.3)
    hamster_s.sound_off()

    # 내장 효과음
    #   mute, beep, beep2, beep3, beep_repeat, beep_random, beep_random_repeat,
    #   noise, noise_repeat, siren, siren_repeat, engine, engine_repeat,
    #   fart_a, fart_b, noise_random, noise_random_repeat, whistle,
    #   chop, chop_repeat, robot, dibidibidip, random_melody,
    #   good_job, happy, angry, sad, sleep, march, birthday
    hamster_s.sound_clip('happy')            # 끝날 때까지 기다림
    hamster_s.sound_clip('siren', wait=False)# 바로 다음 줄로
    print('재생 중?', hamster_s.sound_playing())
    time.sleep(1)
    hamster_s.sound_off()                    # 소리 끄기


# -------------------------------------------------------------
# 5. 센서 값 읽기 (Ctrl + C로 종료)
# -------------------------------------------------------------
def demo_sensors():
    while True:
        print(
            '근접 L/R:', hamster_s.proximity('left'), hamster_s.proximity('right'),
            '| 바닥 L/R:', hamster_s.floor('left'), hamster_s.floor('right'),
            '| 가속도 x/y/z:', hamster_s.acceleration('x'),
                               hamster_s.acceleration('y'),
                               hamster_s.acceleration('z'),
            '| 두드림:', hamster_s.tap(),
            '| 밝기:', hamster_s.light(),
            '| 온도:', hamster_s.temperature(),
            '| 신호:', hamster_s.signal_strength(),
            '| 배터리:', hamster_s.battery(),
        )
        time.sleep(0.2)


# -------------------------------------------------------------
# 6. 입출력 포트 · 집게 · 슈터 (해당 부품이 있을 때)
# -------------------------------------------------------------
def demo_io():
    # 포트 모드: 'a' / 'b' / 'both'
    #   'analog_input' 'analog_input_voltage' 'digital_input'
    #   'digital_input_pullup' 'digital_input_pulldown'
    #   'servo_output' 'pwm_output' 'digital_output'
    hamster_s.io_mode('a', 'servo_output')
    hamster_s.set_output('a', 90)            # 출력값 0 ~ 180
    hamster_s.change_output('a', 10)         # 출력값 더하기 → 100

    hamster_s.io_mode('b', 'analog_input')
    print('포트 b 입력값:', hamster_s.get_input('b'))


def demo_gripper():
    hamster_s.open_gripper()                 # 집게 열기
    time.sleep(1)
    hamster_s.close_gripper()                # 집게 닫기


def demo_shooter():
    hamster_s.shooter(0)                     # 슈터 각도 0 ~ 180
    time.sleep(1)
    hamster_s.shooter(90)


# =============================================================
#  실행할 데모 고르기: 필요 없는 줄은 앞에 # 붙이기
# =============================================================
RUN = [
    demo_move,
    # demo_grid,
    # demo_pen,
    # demo_line,
    demo_led,
    demo_sound,
    # demo_sensors,     # 무한 반복 → Ctrl + C로 종료
    # demo_io,
    # demo_gripper,
    # demo_shooter,
]

if __name__ == '__main__':
    try:
        for demo in RUN:
            print(f'=== {demo.__name__} ===')
            demo()
    except KeyboardInterrupt:
        print('중지')
    finally:
        # 어떤 경우에도 로봇을 안전하게 멈춤
        hamster_s.stop()
        hamster_s.turn_off('both')
        hamster_s.sound_off()
