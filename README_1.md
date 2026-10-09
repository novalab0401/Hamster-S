# 햄스터 S 파이썬 정리

로보메이션 `robomation` 파이썬 패키지로 햄스터 S를 제어하기 위한 정리 문서입니다.
기준 환경: Windows 노트북 + 햄스터 S USB 동글 (+ 아두이노)

설치:

```
python -m pip install -U robomation
```

---

## 햄스터 S · 아두이노

햄스터 S 동글과 아두이노는 둘 다 COM 포트로 잡히므로, 함께 쓸 때는 포트 번호를 직접 지정합니다.

### 포트 확인

| 방법 | 하는 일 |
| --- | --- |
| 장치 관리자 → 포트(COM & LPT) | 연결된 장치의 COM 번호 확인 (하나씩 꽂았다 빼며 구분) |
| `python -m serial.tools.list_ports` | 터미널에서 COM 포트 목록 출력 (pyserial 필요) |
| `mode` | cmd에서 사용 중인 COM 포트 확인 |

### 햄스터 S 주요 코드

| 코드 | 하는 일 |
| --- | --- |
| `from robomation import *` | 라이브러리 불러오기 |
| `hamster_s = HamsterS()` | 자동 탐색으로 연결 |
| `hamster_s = HamsterS('COM3')` | 포트를 지정해 연결 |
| `hamster_s.set_wheel_speed('both', 30)` | 양쪽 바퀴 속도 30 (범위 -100~100, 음수는 후진) |
| `hamster_s.set_wheel_speed('left', 30)` | 왼쪽 바퀴만 설정 (`'right'`는 오른쪽) |
| `hamster_s.set_wheel_speed('both', 0)` | 정지 |
| `time.sleep(2)` | 2초 대기 (`import time` 필요) |

### 첫 구동 테스트 (operate_test.py)

```python
from robomation import *
import time

hamster_s = HamsterS()          # 자동 탐색
hamster_s.set_wheel_speed('both', 30)
time.sleep(2)
hamster_s.set_wheel_speed('both', 0)
```

아두이노 시리얼 모니터가 열려 있으면 파이썬이 같은 포트를 쓰지 못하므로, 파이썬 실행 전에 꼭 닫습니다.

---

## 햄스터 S 파이썬 함수 전체

블록 코딩의 블록 하나하나가 아래 함수 하나에 대응합니다. 모든 함수는 `hamster_s.함수명(...)` 형태로 쓰고, `wait=True`인 함수는 동작이 끝날 때까지 다음 줄로 넘어가지 않습니다.

### 연결하기

| 코드 | 설명 |
| --- | --- |
| `HamsterS()` | 자동 탐색으로 연결 |
| `HamsterS(0)` | 인스턴스 번호 지정 (0부터) |
| `HamsterS("COM3")` | 포트 지정 |
| `HamsterS("D9:4B:8B:A4:E1:67")` | 제품 고유 주소 지정 (`:` 생략·대소문자 무관) |
| `HamsterS(0, port_name="COM3", address="D94B8BA4E167")` | 번호 + 포트 + 주소 |

로봇 2대 이상: `HamsterS(0, address=...)`, `HamsterS(1, address=...)`처럼 번호를 다르게 하고 주소를 지정해야 매번 같은 로봇에 연결됩니다. 고유 주소는 연결 시 출력되는 `HamsterS[0] Connected: COM3 D9:4B:...` 메시지나 제품 라벨에서 확인합니다.

### 이동·회전

| 사용 예 | 설명 |
| --- | --- |
| `set_wheel_speed('both', 50)` | 바퀴 속도 설정. 바퀴: left, right, both / 속도: -100~100 (0 = 정지) |
| `change_wheel_speed('both', 10)` | 현재 속도에 값을 더해 변경. -200~200 |
| `move_distance(50, 'cm')` | 정해진 거리만큼 이동. 단위: cm(기본), mm, inch |
| `move_time(5)` | 정해진 시간(초)만큼 이동 |
| `turn_degree('left', 90)` | 제자리 회전. 방향: left, right / 각도(도) |
| `stop()` | 이동 멈춤 |
| `wheel_moving()` | 바퀴가 움직이는 중이면 True |
| `grid_move()` | 말판 위에서 한 칸 이동 |
| `grid_turn('left')` | 말판 위에서 90도 회전. left, right |
| `pivot('left_pen', 'forward', 90)` | 펜 홀더 사용 시 기준점 중심 회전. 기준: left_pen, right_pen, left_wheel, right_wheel / 방향: forward, backward |
| `pivot_circle('left_pen', 'left_forward', 90, 1, 'cm')` | 펜 홀더 사용 시 원 그리기. 기준: left_pen, right_pen / 방향: left_forward, left_backward, right_forward, right_backward / 각도, 반지름, 단위 |

이동·회전 함수는 `wait=False`를 붙이면 끝나기를 기다리지 않고 다음 줄로 넘어갑니다.

### 선 따라가기

| 사용 예 | 설명 |
| --- | --- |
| `trace_line('left', 'black')` | 바닥 센서로 선 따라가기 시작. 센서: left, right, center / 선: black(기본), white |
| `trace_intersection('left', 'black')` | 지정 방향으로 돈 뒤 다음 교차로까지 이동. 방향: left, right, forward, uturn |
| `set_trace_speed(5)` | 선 따라가기 속도. 1~10 |
| `set_trace_gain(5)` | 방향 변화량(클수록 급하게 꺾음). 1~10 |
| `stop_trace()` | 선 따라가기 종료 |

### LED

| 사용 예 | 설명 |
| --- | --- |
| `set_led_color('both', 'red')` | LED 색 설정. 위치: left, right, both / 색: black, red, yellow, green, cyan, blue, magenta, white |
| `set_led_color('both', 255, 0, 0)` | RGB 값(각 0~255)으로 색 설정 |
| `change_led_color('both', 10, 0, 0)` | 현재 색에 RGB 값을 더해 변경. 각 -255~255 |
| `turn_off('both')` | LED 끄기 |

### 소리

| 사용 예 | 설명 |
| --- | --- |
| `sound_buzz(440)` | 지정 주파수(Hz)로 버저음. 122.1~4186.0 |
| `sound_note('D', 5)` | 음계 재생. 음: C, C#, D, D#, E, F, F#, G, G#, A, A#, B / 옥타브: 3~7 (기본 4) |
| `sound_clip('siren')` | 내장 효과음 재생 (아래 클립 이름) |
| `sound_off()` | 소리 끄기 |
| `sound_playing()` | 소리 재생 중이면 True |

효과음 클립 이름: mute, beep, beep2, beep3, beep_repeat, beep_random, beep_random_repeat, noise, noise_repeat, siren, siren_repeat, engine, engine_repeat, fart_a, fart_b, noise_random, noise_random_repeat, whistle, chop, chop_repeat, robot, dibidibidip, random_melody, good_job, happy, angry, sad, sleep, march, birthday

### 센서 값 읽기

모두 값을 돌려주는 함수라 `print(hamster_s.light())`처럼 출력하거나 `if`문 조건에 넣어 씁니다.

| 사용 예 | 돌려주는 값 |
| --- | --- |
| `wheel_speed('left')` | 해당 바퀴의 현재 속도. left, right |
| `proximity('left')` | 앞쪽 근접 센서 값. left, right |
| `floor('left')` | 바닥 센서 값. left, right |
| `acceleration('x')` | 축별 중력 가속도 값. x, y, z |
| `tap()` | 두드림이 감지되면 True |
| `light()` | 밝기 센서 값 |
| `temperature()` | 내부 온도 센서 값 |
| `signal_strength()` | 무선 신호 세기 |
| `battery()` | 배터리 전압 |

### 입출력 포트 · 집게 · 슈터

| 사용 예 | 설명 |
| --- | --- |
| `io_mode('both', 'analog_input')` | 입출력 포트 모드 설정. 포트: a, b, both / 모드: analog_input, analog_input_voltage, digital_input, digital_input_pullup, digital_input_pulldown, servo_output, pwm_output, digital_output |
| `set_output('a', 90)` | 포트 출력값 설정. 0~180 |
| `change_output('a', 10)` | 포트 출력값을 더해 변경 |
| `get_input('a')` | 포트 입력값 읽기. a, b |
| `open_gripper()` | 집게 열기 |
| `close_gripper()` | 집게 닫기 |
| `shooter(45)` | 슈터 각도 설정. 0~180 |

---

참고: [Robomation_Python Wiki – HamsterS](https://github.com/RobomationLAB/Robomation_Python/wiki/HamsterS)
