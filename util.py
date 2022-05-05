import os

PITCH_TO_MBNUM_30 = {93: 29, 91: 28, 89: 27, 88: 26, 87: 25, 86: 24, 85: 23, 84: 22,
                     83: 21, 82: 20, 81: 19, 80: 18, 79: 17, 78: 16, 77: 15, 76: 14,
                     75: 13, 74: 12, 73: 11, 72: 10, 71: 9, 70: 8, 69: 7, 67: 6,
                     65: 5, 64: 4, 62: 3, 60: 2, 55: 1, 53: 0}

PITCH_TO_MBNUM_15 = {56: 0, 58: 1, 60: 2, 61: 3, 63: 4, 65: 5,
                     67: 6, 68: 7, 70: 8, 72: 9, 73: 10, 75: 11, 77: 12, 79: 13, 80: 14}

prev_time_30 = {93: -8, 91: -8, 89: -8, 88: -8, 87: -8, 86: -8, 85: -8, 84: -8,
                83: -8, 82: -8, 81: -8, 80: -8, 79: -8, 78: -8, 77: -8, 76: -8,
                75: -8, 74: -8, 73: -8, 72: -8, 71: -8, 70: -8, 69: -8, 67: -8,
                65: -8, 64: -8, 62: -8, 60: -8, 55: -8, 53: -8}

prev_time_15 = {56: -8, 58: -8, 60: -8, 61: -8, 63: -8, 65: -8,
                67: -8, 68: -8, 70: -8, 72: -8, 73: -8, 75: -8, 77: -8, 79: -8, 80: -8}

LEFT_ALIGN = 0
CENTER_ALIGN = 1
RIGHT_ALIGN = 2
A4_VERTICAL_30 = 25
A4_HORIZONAL = 24
A3_VERTICAL = 23
A3_HORIZONAL = 22
A4_VERTICAL_15 = 21

B5_VERTICAL = 43
B5_HORIZONAL = 42
B4_VERTICAL = 41
B4_HORIZONAL = 40
AUTO_SIZE = 0
TEST_SIZE = 1

PAPER_INFO = {A4_VERTICAL_30: {'size': (210, 297), 'col': 3, 'row': 35},
              A4_VERTICAL_15: {'size': (210, 297), 'col': 5, 'row': 35},
              A4_HORIZONAL: {'size': (297, 210), 'col': 4, 'row': 24},
              A3_VERTICAL: {'size': (297, 420), 'col': 4, 'row': 50},
              A3_HORIZONAL: {'size': (420, 297), 'col': 6, 'row': 35},
              B5_VERTICAL: {'size': (176, 250), 'col': 2, 'row': 29},
              B5_HORIZONAL: {'size': (250, 176), 'col': 3, 'row': 20},
              B4_VERTICAL: {'size': (250, 353), 'col': 3, 'row': 42},
              B4_HORIZONAL: {'size': (353, 250), 'col': 5, 'row': 29},
              TEST_SIZE: {'size': (70, 4000), 'col': 1, 'row': 420}}

FONT_PATH = [
    'C:\\Users\\' + os.getlogin() +
    r'\AppData\Local\Microsoft\Windows\Fonts\SourceHanSansSC-Regular.otf',  # 思源黑体
    r'C:\Windows\Fonts\msyh.ttc',  # 微软雅黑
    r'C:\Windows\Fonts\simsun.ttc'  # 宋体
]

DEFAULT_PPI = 300.0  # 默认ppi
INCH_TO_MM = 25.4  # 1英寸=25.4毫米

DOT_R = 1.14  # 圆点半径（单位毫米）
BORDER = 3.0  # 边框宽度（单位毫米）
ANTI_ALIAS = 1  # 抗锯齿缩放倍数

class KeyParams:
    total_notes = None
    col_offset = None
    internote_spacing = None
    contentsize = None
    startpos = None
    endpos = None

# NOTE_SUM=0
# LENGTH=0

class NoteInfo:
    page = None
    coln = None
    rowmm = None


def find_latest_event(l, t):
    i = len(l) - 1
    while l[i][1] > t:
        i -= 1
    return i


def mm2pixel(x, ppi=DEFAULT_PPI):
    return x / INCH_TO_MM * ppi


def pixel2mm(x, ppi=DEFAULT_PPI):
    return x * INCH_TO_MM / ppi


def posconvert(pos, ppi=DEFAULT_PPI):
    x, y = pos
    return (round(mm2pixel(x, ppi) - 0.5), round(mm2pixel(y, ppi) - 0.5))
