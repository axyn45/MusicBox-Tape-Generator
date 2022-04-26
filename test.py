from ast import Num
from xml.sax import default_parser_list
from PIL import Image, ImageDraw, ImageFont, ImageOps
from numpy import size
import os

from regex import B

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

def mm2pixel(x, ppi=DEFAULT_PPI):
    return x / INCH_TO_MM * ppi


def pixel2mm(x, ppi=DEFAULT_PPI):
    return x * INCH_TO_MM / ppi


def posconvert(pos:tuple, ppi=DEFAULT_PPI):
    x, y = pos
    return (round(mm2pixel(x, ppi) - 0.5), round(mm2pixel(y, ppi) - 0.5))

# font=str()

# if font is None:  # 在FONT_PATH中寻找第一个能使用的字体
#         for i in FONT_PATH:
#             try:
#                 font_ref = ImageFont.truetype(i, round(mm2pixel(2, DEFAULT_PPI)))
#                 font0 = ImageFont.truetype(i, round(mm2pixel(3.3, DEFAULT_PPI)))
#                 font1 = ImageFont.truetype(i, round(mm2pixel(3.4, DEFAULT_PPI)))
#                 font2 = ImageFont.truetype(i, round(mm2pixel(6, DEFAULT_PPI)))
#             except:
#                 pass
#             else:
#                 break
# else:
#     font0 = ImageFont.truetype(font, round(mm2pixel(3.3, DEFAULT_PPI)))
#     font1 = ImageFont.truetype(font, round(mm2pixel(3.4, DEFAULT_PPI)))
#     font2 = ImageFont.truetype(font, round(mm2pixel(6, DEFAULT_PPI)))

def bar_ref(Number):
    Number=str(Number)
    strlen=len(Number)
    img = Image.new('RGB', posconvert((strlen*1.5, 2.5)), color='#ffffff')
    font = ImageFont.load_default()
    font = ImageFont.truetype('C:\Windows\Fonts\msyh.ttc', 30)
    draw=ImageDraw.Draw(img)
    draw.text(posconvert((0,-0.5)), str(Number), font=font, fill=(0, 0, 0))
    # img.show()
    return img.rotate(90,Image.NEAREST,expand = 1)
# beat_ref(20).show()
# beat_ref(200).show()
# beat_ref(2000).show()
# beat_ref(20000).show()
# beat_ref(200000).show()