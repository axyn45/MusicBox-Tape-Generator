from util import *
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont



content='水印'

# draw one tilted watermark at center of each col
def watermark_a(draw,PAPER_SIZE=A4_VERTICAL_30,font=None,ppi=DEFAULT_PPI,is30=True):
    if font is None:  # 在FONT_PATH中寻找第一个能使用的字体
        for i in FONT_PATH:
            try:
                # font_ref = PIL.ImageFont.truetype(i, round(mm2pixel(2, ppi)))
                # font_ref2=PIL.ImageFont.truetype(i, round(mm2pixel(4, ppi)))
                font0 = PIL.ImageFont.truetype(i, round(mm2pixel(3.3, ppi)))
                font1 = PIL.ImageFont.truetype(i, round(mm2pixel(3.4, ppi)))
                font2 = PIL.ImageFont.truetype(i, round(mm2pixel(6, ppi)))
            except:
                pass
            else:
                break
    else:
        font0 = PIL.ImageFont.truetype(font, round(mm2pixel(3.3, ppi)))
        font1 = PIL.ImageFont.truetype(font, round(mm2pixel(3.4, ppi)))
        font2 = PIL.ImageFont.truetype(font, round(mm2pixel(6, ppi)))

    if is30:
        draw.text((posconvert((0, 0)), '水印'), font=font, fill=(0, 0, 0, 0))
        draw.text((posconvert((0, 0)), '水印'), font=font, fill=(0, 0, 0, 0))
        draw.text((posconvert((0, 0)), '水印'), font=font, fill=(0, 0, 0, 0))
