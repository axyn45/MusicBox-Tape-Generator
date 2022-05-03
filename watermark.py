from util import *
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from math import sqrt




# draw one tilted watermark at center of each col
def watermark_a(content='Alex'):
    PAPER_SIZE=A4_VERTICAL_30
    ppi=DEFAULT_PPI
    
    for i in FONT_PATH:
        try:
            font = PIL.ImageFont.truetype(i, round(mm2pixel(20, ppi)))
        except:
            pass
        else:
            break

    
    vertical_space=50
    horizontal_space=sqrt(3)*vertical_space

    size1,size2=PAPER_INFO[A4_VERTICAL_30]['size']
    size=(size1*2,size2*2)
    wm=PIL.Image.new('RGBA', posconvert(size, ppi), (255, 255, 255, 255))
    draw=PIL.ImageDraw.Draw(wm)
    x=0
    y=0

    h1=horizontal_space
    h2=vertical_space#horizontal_space%vertical_space
    h1=sqrt(3)*h2

    while(y<size[1]):
        while(x<size[0]):
            draw.text(xy=posconvert((x, y)),text=content, font=font, fill=(0, 0, 0, 40))
            x+=horizontal_space
        y+=vertical_space
        x=y%horizontal_space-horizontal_space
    wm=wm.rotate(angle=-30,expand=1)
    wm.show()
    return wm


# test
if __name__ == '__main__':
    watermark_a()