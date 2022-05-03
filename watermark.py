from util import *
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont



content='Alex的八音盒'

# draw one tilted watermark at center of each col
def watermark_a(PAPER_SIZE=A4_VERTICAL_30,font=None,ppi=DEFAULT_PPI,is30=True):
    if font is None:  # 在FONT_PATH中寻找第一个能使用的字体
        for i in FONT_PATH:
            try:
                font = PIL.ImageFont.truetype(i, round(mm2pixel(24, ppi)))
            except:
                pass
            else:
                break
    else:
        font = PIL.ImageFont.truetype(font, round(mm2pixel(12, ppi)))

    vertical_space=200
    horizontal_space=60

    if is30:
        size1,size2=PAPER_INFO[A4_VERTICAL_30]['size']
        size=(size1*2,size2*2)
        wm=PIL.Image.new('RGBA', posconvert(size, ppi), (255, 255, 255, 255))
        draw=PIL.ImageDraw.Draw(wm)
        x=0
        y=0
        while(y<size[1]):
            while(x<size[0]):
                draw.text(xy=posconvert((x, y)),text=content, font=font, fill=(0, 0, 0, 40))
                x+=vertical_space
            y+=horizontal_space
            x=y%vertical_space-vertical_space
        wm.show()


# test
if __name__ == '__main__':
    watermark_a()