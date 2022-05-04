import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from util import posconvert

def bar_ref(Number):   # 返回小节编号逆时针旋转90°的图像
    Number = str(Number)
    strlen = len(Number)
    img = PIL.Image.new('RGBA', posconvert((strlen*1.5, 2.5)), (0, 0, 0, 0))
    font = PIL.ImageFont.load_default()
    font = PIL.ImageFont.truetype('C:\Windows\Fonts\msyh.ttc', 30)
    draw = PIL.ImageDraw.Draw(img)
    draw.text(posconvert((0, -0.5)), str(Number), font=font, fill=(0, 0, 0))
    # img.show()
    return img.rotate(90, PIL.Image.NEAREST, expand=1)