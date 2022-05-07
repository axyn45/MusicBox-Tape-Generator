from util import *
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from math import sqrt




# draw one tilted watermark at center of each col
def watermark_a(heading='B站@',content='Alex的八音盒'):
    PAPER_SIZE=A4_VERTICAL_30
    ppi=DEFAULT_PPI

    for i in FONT_PATH:
        try:
            font1 = PIL.ImageFont.truetype(i, round(mm2pixel(16, ppi)))
            font2=PIL.ImageFont.truetype(i, round(mm2pixel(8, ppi)))
        except:
            pass
        else:
            break

    vertical_space_1=8
    vertical_space_2=35
    horizontal_space=180

    size1,size2=PAPER_INFO[A4_VERTICAL_30]['size']
    size=(size1*2,size2*2)
    wm=PIL.Image.new('RGBA', posconvert(size, ppi), (255, 255, 255, 255))
    draw=PIL.ImageDraw.Draw(wm)
    x=0
    y=0

    # h1=horizontal_space
    # h2=vertical_space#horizontal_space%vertical_space
    # h1=sqrt(3)*h2
    x0=0
    while(y<size[1]):
        while(x<size[0]):
            draw.text(xy=posconvert((x+2, y)),text=heading, font=font2, fill=(0, 0, 0, 15))
            draw.text(xy=posconvert((x, y+vertical_space_1)),text=content, font=font1, fill=(0, 0, 0, 15))
            x+=horizontal_space
        y+=vertical_space_1+vertical_space_2
        if x0==0:x0=-horizontal_space/2
        else: x0=0
        x=x0    #x=y%horizontal_space-horizontal_space
    wm=wm.rotate(angle=-30,expand=1)
    size=wm.size
    # wm.show()
    return wm


# test
if __name__ == '__main__':
    watermark_a()