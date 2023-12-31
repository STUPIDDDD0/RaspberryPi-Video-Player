import time
import RPi.GPIO as GPIO
from tone import TONE

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def beep(channel: int, freq: int, duration: float, *, rising_tone: float = 1):
    """
    播放一个音符
    :param channel: GPIO的数字号，需要和上面的GPIO.setmode(GPIO.BCM)对应
    :param freq: 频率
    :param duration: 播放时长
    :param rising_tone: 升降调 0.3 ~ 1.0 ~ 3.0
    :return:
    """
    if freq <= 0:
        time.sleep(duration)
        return
    pwm = GPIO.PWM(channel, freq * rising_tone) # 输出该频率的电平

    try:
        pwm.start(0)
        pwm.ChangeDutyCycle(50)
        if duration > 0:
            time.sleep(duration) # 播放时长
    finally:
        pwm.stop()

def play(channel: int, sheet: list):
    """
    播放简谱
    简谱可以为如下格式(参照上文的txdx.py):
    - [音符名(string), 持续时间(s)]
    - [频率(int), 持续时间(s)]
    :param channel: GPIO的数字号，需要和上面的GPIO.setmode(GPIO.BCM)对应
    :param sheet: 简谱
    :return:
    """
    GPIO.setup(channel, GPIO.OUT)
    for m in sheet:
        beep(channel, TONE[m[0]] if m[0] in TONE else int(m[0] or 0), m[1])
try:
    from txdx import txdx_sheet
    play(1, txdx_sheet)

finally:
    GPIO.cleanup()
