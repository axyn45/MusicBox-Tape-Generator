import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from util import FONT_PATH,DEFAULT_PPI,mm2pixel,posconvert


def note_ref(is30=True,font=None,ppi=DEFAULT_PPI):
    if font is None:  # 在FONT_PATH中寻找第一个能使用的字体
        for i in FONT_PATH:
            try:
                font_ref = PIL.ImageFont.truetype(i, round(mm2pixel(4, ppi)))
            except:
                pass
            else:
                break
    else:
        font_ref = PIL.ImageFont.truetype(font, round(i, round(mm2pixel(4, ppi))))

    lx=2*10+1 if is30 else 2*8+1
    ly=2*32 if is30 else 2*19-1
    ref = PIL.Image.new('RGBA', posconvert(
        (lx, ly), ppi), (0, 0, 0, 0))
    draw_ref = PIL.ImageDraw.Draw(ref)

    # 准备音名标识图片
    # vp for vertival position
    vp1 = 3
    vp2 = 14 if is30 else 11
    vp3 = vp1
    vp4 = vp2

    # 绘制音名标识图片
    if is30:
        # 1~10
        draw_ref.text(xy=posconvert((vp1, 0), ppi), text="C",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2, 2), ppi), text="D",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp3, 4), ppi), text="G",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp4, 6), ppi), text="A",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp3, 8), ppi), text="B",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2, 10), ppi), text="C1",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp1, 12), ppi), text="D1",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2, 14), ppi), text="E1",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp3, 16), ppi), text="F1",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp4-2.6, 18), ppi), text="#F1",
                  font=font_ref, fill=(28, 43, 255, 255))
        # 11~20
        draw_ref.text(xy=posconvert((vp3, 20), ppi), text="G1",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2-2.6, 22), ppi), text="#G1",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp1, 24), ppi), text="A1",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2-2.6, 26), ppi), text="#A1",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp3, 28), ppi), text="B1",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp4, 30), ppi), text="C2",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp3-2.6, 32), ppi), text="#C2",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2, 34), ppi), text="D2",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp1-2.6, 36), ppi), text="#D2",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2, 38), ppi), text="E2",
                  font=font_ref, fill=(28, 43, 255, 255))
        # 21~30
        draw_ref.text(xy=posconvert((vp3, 40), ppi), text="F2",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp4-2.6, 42), ppi), text="#F2",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp3, 44), ppi), text="G2",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2-2.6, 46), ppi), text="#G2",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp1, 48), ppi), text="A2",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2-2.6, 50), ppi), text="#A2",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp3, 52), ppi), text="B2",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp4, 54), ppi), text="C3",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp3, 56), ppi), text="D3",
                  font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2, 58), ppi), text="E3",
                  font=font_ref, fill=(28, 43, 255, 255))
    else:
        # 1~10
        draw_ref.text(xy=posconvert((vp1, 2), ppi), text="C",
                    font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2, 4), ppi), text="D",
                    font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp3, 6), ppi), text="E",
                    font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp4, 8), ppi), text="F",
                    font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp3, 10), ppi), text="G",
                    font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2, 12), ppi), text="A",
                    font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp1, 14), ppi), text="B",
                    font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2, 16), ppi), text="C1",
                    font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp3, 18), ppi), text="D1",
                    font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp4, 20), ppi), text="E1",
                    font=font_ref, fill=(28, 43, 255, 255))
        # 11~15
        draw_ref.text(xy=posconvert((vp3, 22), ppi), text="F1",
                    font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2, 24), ppi), text="G1",
                    font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp1, 26), ppi), text="A1",
                    font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp2, 28), ppi), text="B1",
                    font=font_ref, fill=(28, 43, 255, 255))
        draw_ref.text(xy=posconvert((vp3, 30), ppi), text="C2",
                    font=font_ref, fill=(28, 43, 255, 255))

    # ref.show()
    # 图片旋转90°
    ref = ref.rotate(angle=90,expand=1)
    # 定义裁切点坐标
    # left, upper = posconvert((0, 40), ppi)
    # right, lower = posconvert((2*32, 2*32), ppi)
    # 裁切图片
    # note_ref = note_ref.crop((left, upper, right, lower))
    # note_ref.show()
    return ref