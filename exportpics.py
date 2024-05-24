'''
用于从.emid和.mid文件生成纸带八音盒设计稿


开发者：Github@axyn45，Bilibili@Alex的八音盒
原作者：bilibili@Bio-Hazard


FairyMusicBox系列软件作者：bilibili@调皮的码农

祝使用愉快！

*错误处理尚不完善，由于使用本程序导致的问题，作者概不负责
*使用前请务必了解可能造成的后果
*请备份重要文件！
'''
from asyncio.windows_events import CONNECT_PIPE_INIT_DELAY
import fractions
import os
import math
# from tkinter import Image
# from tkinter.tix import NoteBook
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from matplotlib.pyplot import fill
from matplotlib.style import available
import mido
import emid
from process_midifile import process_midifile
from process_emidfile import process_emidfile
from util import*
from util import KeyParams as kp
from util import NoteInfo as ni
from bar_ref import bar_ref
from note_ref import note_ref
from notemark import notemark
# from notecounter import getLength
# from collections import OrderedDict

from watermark import watermark_a



def export_pics(file,
                filename: str = None,
                musicname: str = None,
                transposition: int = 0,
                interpret_bpm: float = None,
                scale: float = 1.0,
                heading: tuple = ('B站：Alex的八音盒', CENTER_ALIGN),
                font: str = None,
                papersize=AUTO_SIZE,
                ppi: float = DEFAULT_PPI,
                background=(255, 255, 0, 255),
                save_pic: bool = True,
                overwrite: bool = False,
                track_selection: int = -1,
                is_30_note=False,
                isSuccessful: bool = True,
                watermarkEN=True,
                note_counterEN=True,
                frac_note_hilight=True) -> list:
    '''
    将.emid或.mid文件转换成纸带八音盒设计稿

    参数 file: emid.EmidFile实例 或 mido.MidiFile实例 或 用字符串表示的文件路径
    参数 filename: 输出图片文件名的格式化字符串，
                    例如：'MusicName_%d.png'
                    留空则取参数file的文件名+'_%d.png'
    参数 musicname: 每栏右上角的信息，留空则取参数file的文件名
    参数 transposition: 转调，表示升高的半音数，默认为0（不转调）
    参数 interpret_bpm: 设定此参数会使得note圆点的纵向间隔随着midi的bpm的变化而变化，
                        note圆点间隔的缩放倍数 = interpret_bpm / midi的bpm，
                        例如，midi的bpm被设定为75，interpret_bpm设定为100，
                        则note圆点的间隔拉伸为4/3倍，
                        设置为None则忽略midi的bpm信息，固定1拍=8毫米间隔，
                        默认为None
    参数 scale: 音符位置的缩放量，大于1则拉伸纸带长度，默认为1（不缩放）
    参数 heading: 一个元组，
                heading[0]: 页眉文字字符串，
                heading[1]: exportpics.LEFT_ALIGN 或
                            exportpics.CENTER_ALIGN 或
                            exportpics.RIGHT_ALIGN，指定对齐方式
    参数 font: 用字符串表示的字体文件路径，
                留空则从FONT_PATH中按序取用
    参数 papersize: 字符串或字典
                可以使用PAPER_INFO中的预设值(例如exportpics.A4_VERTICAL)，
                也可以使用字典来自定义，格式为
                {'size': 一个元组(宽, 高)，单位毫米,
                 'col': 一页的分栏数,
                 'row': 一栏的行数}
                也可以使用exportpics.AUTO_SIZE自适应大小
                默认为exportpics.A4_VERTICAL，
    参数 ppi: 输出图片的分辨率，单位像素/英寸，默认为DEFALT_PPI
    参数 background: 背景图片或颜色，
                    可以是用字符串表示的文件路径，
                    也可以是PIL.Image.Image实例，
                    也可以是一个表示颜色的(R, G, B, Alpha)元组，
                    默认为(255, 255, 255, 255)，表示白色
    参数 save_pic: True 或 False，是否将图片写入磁盘，默认为True
    参数 overwrite: True 或 False，是否允许覆盖同名文件，默认为False，
                    警告：设置为True可能导致原有文件丢失，请注意备份！

    函数返回包含若干PIL.Image.Image实例的list
    '''

    print('Processing Data...')
    '打开文件以及处理默认值'
    typ = type(file)
    if typ == str:
        # 文件名替代heading
        strbin, aligntype = heading
        # track_No=None
        if filename is None:
            if track_selection > 0:
                filename = os.path.splitext(
                    file)[0] + '_Track' + str(track_selection)+('@30' if is_30_note else '@15')+'_%d.png'
            else:
                filename = os.path.splitext(file)[0] +('@30' if is_30_note else '@15')+ '_%d.png'
            # 页眉显示曲目名称
            heading = (os.path.splitext(file)[
                       0] + '_Track'+str(track_selection), aligntype)
        if musicname is None:
            if track_selection > 0:
                musicname = os.path.splitext(os.path.split(file)[1])[
                    0] + '_Track'+str(track_selection)
                # 页眉显示曲目名称
                heading = (os.path.splitext(os.path.split(file)[1])[
                           0] + '_Track'+str(track_selection), aligntype)
            else:
                musicname = os.path.splitext(os.path.split(file)[1])[0]
                heading = (os.path.splitext(
                    os.path.split(file)[1])[0], aligntype)

        extention = os.path.splitext(file)[1]
        if extention == '.emid':
            TEmid = emid.EmidFile(file)
            notes, length = process_emidfile(emid.mido.MidiFile(file))
            # TAPE_LENGTH = getLength(filename)
        elif extention == '.mid':
            notes, length = process_midifile(mido.MidiFile(file),transposition=transposition,scale=scale,track_selection=track_selection,is30=is_30_note,interpret_bpm=interpret_bpm)
            # TAPE_LENGTH = getLength(mido.MidiFile(file))
        else:
            raise(ValueError('Unknown file extention (\'.mid\' or \'.emid\' required)'))

    elif typ == emid.EmidFile or mido.MidiFile:
        if filename is None:
            filename = os.path.splitext(file.filename)[0] + '_%d.png'
        if musicname is None:
            musicname = os.path.splitext(os.path.split(file)[1])[0]

        if typ == emid.EmidFile:
            notes, length = process_emidfile(file)
        else:
            notes, length = process_midifile(file,transposition=transposition,scale=scale,track_selection=track_selection,is30=is_30_note,interpret_bpm=interpret_bpm)

    else:
        raise(ValueError(
            'Unknown file type (filename, emid.EmidFile or mido.MidiFile required)'))

    TAPE_LENGTH=round((length+16)/1000,2)
    SUM_NOTES=len(notes)

    # 所有音轨都输出完毕
    if notes == None:
        isSuccessful = False
        return isSuccessful


    if papersize == AUTO_SIZE:  # 计算纸张大小
        col = 1
        row = math.floor(length / 8) + 1
        size = (70, row * 8 + 20)
        pages = 1
        cols = 1
    else:
        if type(papersize) == int:
            papersize = PAPER_INFO[papersize]
        col = papersize['col']
        row = papersize['row']
        size = papersize['size']
        pages = math.floor(length / (col * row * 8)) + 1  # 计算页数
        # 计算最后一页的栏数
        cols = math.floor(length / (row * 8)) - (pages - 1) * col + 1

    kp.total_notes = 30 if is_30_note else 15
    kp.col_offset = 70 if is_30_note else 40
    kp.internote_spacing=2*29 if is_30_note else 2*14

    kp.contentsize = (kp.col_offset * col, 8 * row)
    kp.startpos = (size[0] / 2 - kp.contentsize[0] / 2,
                size[1] / 2 - kp.contentsize[1] / 2)
    kp.endpos = (size[0] / 2 + kp.contentsize[0] / 2,
              size[1] / 2 + kp.contentsize[1] / 2)  # 计算坐标



    if font is None:  # 在FONT_PATH中寻找第一个能使用的字体
        for i in FONT_PATH:
            try:
                font0 = PIL.ImageFont.truetype(i, round(mm2pixel(3.3, ppi)))
                font1 = PIL.ImageFont.truetype(i, round(mm2pixel(3.4, ppi)))
                font2 = PIL.ImageFont.truetype(i, round(mm2pixel(6, ppi)))
                font3 = PIL.ImageFont.truetype(i, round(mm2pixel(8, ppi)))
            except:
                pass
            else:
                break
    else:
        font0 = PIL.ImageFont.truetype(font, round(mm2pixel(3.3, ppi)))
        font1 = PIL.ImageFont.truetype(font, round(mm2pixel(3.4, ppi)))
        font2 = PIL.ImageFont.truetype(font, round(mm2pixel(6, ppi)))
        font3 = PIL.ImageFont.truetype(font, round(mm2pixel(8, ppi)))

    print('Drawing...')
    images0 = []
    images1 = []


    draws0 = []
    draws1 = []


    # 统计小节数，从0开始
    COL_NO = 0

    # 统计已打印的note数量
    DRAWED_NOTES = 0
    
    # 统计总共小节数
    total_bars = 0

    # 每小节的节拍数
    beats_per_bar = 8

    for i in range(pages):
        test_pos = posconvert(size, ppi)
        image0 = PIL.Image.new('RGBA', posconvert(size, ppi), (0, 0, 0, 0))
        image1 = PIL.Image.new('RGBA', posconvert(
            size, ppi * ANTI_ALIAS), (0, 0, 0, 0))

        image2 = PIL.Image.new('RGBA', posconvert(size, ppi), (0, 0, 0, 0))

        draw0 = PIL.ImageDraw.Draw(image0)
        draw1 = PIL.ImageDraw.Draw(image1)

        # draw2 = PIL.ImageDraw.Draw(image2)

        '写字'
        for j in range(col if i < pages - 1 else cols):
            '水印'
            if watermarkEN: image0.paste(watermark_a(),posconvert((-200,-300)))

            '标题文字'
            headingtext, align = heading
            textsize = font0.getbbox(headingtext)   #(left, top, right, bottom)

            if align == LEFT_ALIGN:
                posX = 7
            elif align == CENTER_ALIGN:
                posX = (size[0] - pixel2mm(textsize[2]-textsize[0], ppi)) / 2
            elif align == RIGHT_ALIGN:
                posX = (size[0] - pixel2mm(textsize[2]-textsize[0], ppi)) - 7
            posY = ((size[1] - kp.contentsize[1]) / 2 -
                    pixel2mm(textsize[3]-textsize[1], ppi)) - 1

            draw0.text(xy=posconvert((posX, posY-1), ppi),
                       text=headingtext,
                       font=font0,
                       fill=(0, 0, 0, 255))

            '栏尾页码'
            colnum = i * col + j + 1
            draw1.text(xy=posconvert((kp.startpos[0] + kp.col_offset*j + 6, kp.endpos[1]), ppi),
                       text=str(colnum),
                       font=font1,
                       fill=(0, 0, 0, 255))

            '栏右上角文字'
            if(j == 0):
                for k, char in enumerate(musicname):
                    textsize = font2.getbbox(char)
                    text_horizontal_offset=kp.col_offset*j + 59 if is_30_note else kp.col_offset*j + 29
                    draw1.text(
                        xy=posconvert(
                            (kp.startpos[0] + text_horizontal_offset - pixel2mm(textsize[2]-textsize[0], ppi) / 2,
                             kp.startpos[1] + 8*k + 6 - pixel2mm(textsize[3]-textsize[1], ppi)), ppi),
                        text=char, font=font3, fill=(0, 0, 0, 60))
            '栏右上角页码'
            textsize = font2.getbbox(str(colnum))

            
        '画格子'
        for j in range(col if i < pages - 1 else cols):

            '整拍横线'
            for k in range(row + 1):
                total_bars += 1

                '绘制小节标识和粘贴音名标识图'
                if (total_bars % beats_per_bar == 1 and k != row):

                    # '粘贴音名标识图'
                    # ref_horizontal_offset=kp.col_offset*j + 3.35 if is_30_note else kp.col_offset*j +1.35
                    # if(COL_NO%9==0):
                    #     nr=note_ref(is_30_note)
                    #     image0.paste(nr,posconvert((kp.startpos[0] + ref_horizontal_offset,kp.startpos[1]+8*k+80)),mask=nr)
                    
                    '绘制小节标识'
                    # bar_ref(COL_NO+1).show()
                    br=bar_ref(COL_NO+1)
                    image0.paste(br, posconvert((kp.startpos[0] + kp.col_offset*j + 6.5+kp.internote_spacing, kp.startpos[1] + 8*k+1)), mask=br)
                    COL_NO += 1

                '绘制整拍横线'
                draw0.line(posconvert((kp.startpos[0] + kp.col_offset*j + 6,
                                       kp.startpos[1] + 8*k), ppi) +
                           posconvert((kp.startpos[0] + kp.col_offset*j + 6 + kp.internote_spacing,
                                       kp.startpos[1] + 8*k), ppi),
                           fill=(0, 0, 0, 255), width=1)

            '半拍横线'
            for k in range(row):
                draw0.line(posconvert((kp.startpos[0] + kp.col_offset*j + 6,
                                       kp.startpos[1] + 8*k + 4), ppi) +
                           posconvert((kp.startpos[0] + kp.col_offset*j + 6 + kp.internote_spacing,
                                       kp.startpos[1] + 8*k + 4), ppi),
                           fill=(0, 0, 0, 128), width=1)
            '竖线'
            for k in range(kp.total_notes):
                if is_30_note:
                    if k in [5,11,17,23]:
                        w=6
                    else:
                        w=1
                else:
                    if k in [2,4,6,8,10]:
                        w=6
                    else:
                        w=1
                draw0.line(posconvert((kp.startpos[0] + kp.col_offset*j + 6 + 2*k,
                                       kp.startpos[1]), ppi) +
                           posconvert((kp.startpos[0] + kp.col_offset*j + 6 + 2*k,
                                       kp.endpos[1]), ppi),
                           fill=(0, 0, 0, 255), width=w)
                # image0.show()
            total_bars -= 1
        '分隔线'
        for j in range(col + 1 if i < pages - 1 else cols + 1):
            draw0.line(posconvert((kp.startpos[0] + kp.col_offset*j,
                                   kp.startpos[1]), ppi) +
                       posconvert((kp.startpos[0] + kp.col_offset*j,
                                   kp.endpos[1]), ppi),
                       fill=(0, 0, 0, 255), width=1)

        images0.append(image0)
        # image0.show()
        images1.append(image1)
        # image1.show()

        draws0.append(draw0)
        draws1.append(draw1)

        
    '画note'
    Index = 0
    for pitch, time in notes:
        ni.page = math.floor(time / (col * row * 8))
        ni.coln = math.floor(time / (row * 8)) - ni.page * col
        ni.rowmm = math.modf(time / (row * 8))[0] * (row * 8)
        draw1 = draws1[ni.page]
        Index += 1

        # 高亮没有落在网格线交点的孔位
        # 浮点数有精度误差，需要设置一个误差范围来修正
        if(frac_note_hilight and time % 4 > 0.0001 and time % 1 < 0.9999):
            draw1.ellipse(posconvert((kp.startpos[0] + kp.col_offset*ni.coln + 6 + 2*pitch - DOT_R,
                                      kp.startpos[1] + ni.rowmm - DOT_R), ppi * ANTI_ALIAS) +
                          posconvert((kp.startpos[0] + kp.col_offset*ni.coln + 6 + 2*pitch + DOT_R,
                                      kp.startpos[1] + ni.rowmm + DOT_R), ppi * ANTI_ALIAS),
                          fill=(255, 0, 200, 255))
        else:
            draw1.ellipse(posconvert((kp.startpos[0] + kp.col_offset*ni.coln + 6 + 2*pitch - DOT_R,
                                      kp.startpos[1] + ni.rowmm - DOT_R), ppi * ANTI_ALIAS) +
                          posconvert((kp.startpos[0] + kp.col_offset*ni.coln + 6 + 2*pitch + DOT_R,
                                      kp.startpos[1] + ni.rowmm + DOT_R), ppi * ANTI_ALIAS),
                          fill=(0, 0, 0, 255))
        # 标记孔位编号
        if(note_counterEN):
            notemark(draw1,pitch,DRAWED_NOTES+1,kp,ni,font0,SUM_NOTES,round((length)/10,1),section=200)
        DRAWED_NOTES = DRAWED_NOTES+1


    print('Resizing...')
    for i in range(pages):
        images1[i] = images1[i].resize(posconvert(size), PIL.Image.BILINEAR)
        images0[i] = PIL.Image.alpha_composite(images0[i], images1[i])
        draws0[i] = PIL.ImageDraw.Draw(images0[i])

    '添加border'
    for draw in draws0:
        draw.rectangle(posconvert((0, 0), ppi) +
                       posconvert((BORDER, size[1]), ppi),
                       fill=(255, 255, 255, 0))
        draw.rectangle(posconvert((0, 0), ppi) +
                       posconvert((size[0], BORDER), ppi),
                       fill=(255, 255, 255, 0))
        draw.rectangle(posconvert((size[0] - BORDER, 0), ppi) +
                       posconvert((size[0], size[1]), ppi),
                       fill=(255, 255, 255, 0))
        draw.rectangle(posconvert((0, size[1] - BORDER), ppi) +
                       posconvert((size[0], size[1]), ppi),
                       fill=(255, 255, 255, 0))
    '处理background'
    if type(background) == str:
        bgimage = PIL.Image.open(background).resize(
            (posconvert(size, ppi)), PIL.Image.BICUBIC).convert('RGBA')  # 打开，缩放，转换
    elif type(background) == PIL.Image.Image:
        bgimage = background.resize(
            (posconvert(size, ppi)), PIL.Image.BICUBIC).convert('RGBA')  # 打开，缩放，转换
    elif type(background) == tuple:
        bgimage = PIL.Image.new('RGBA', posconvert(size, ppi), background)
    '导出图片'
    result = []
    for pagenum, image in enumerate(images0):
        cpimage = PIL.Image.alpha_composite(bgimage, image)  # 拼合图像
        if save_pic:
            save_path = filename % (pagenum + 1)
            if not overwrite:
                save_path = emid.find_available_filename(save_path)
            print(f'Exporting pics ({pagenum + 1} of {pages})...')
            # cpimage.show()
            cpimage.save(save_path, dpi=(300, 300))
        result.append(cpimage)
# Parameter
    print('Done!')
    return isSuccessful


def batch_export_pics(path=None,
                      ppi=DEFAULT_PPI,
                      background=(255, 255, 255, 255),
                      overwrite=False,
                      font=None,
                      track_selection=-1,
                      is_30_note=True,
                      scale=1,
                      transposition=0,
                      watermark=True,
                      note_counter=True,
                      fractional_note_highlight=True):
    '''
    批量将path目录下的所有.mid和.emid文件转换为纸带设计稿图片
    如果path参数留空，则取当前工作目录
    '''
    papersize=A4_VERTICAL_30 if is_30_note else A4_VERTICAL_15
    if path is None:
        path = os.getcwd()
    for filename in os.listdir(path):
        extention = os.path.splitext(filename)[1]
        if extention == '.mid' or extention == '.emid':
            print('Converting %s ...' % filename)
            if(track_selection == -1):
                export_pics(file=filename,
                            papersize=papersize,
                            ppi=ppi,
                            background=background,
                            overwrite=overwrite,
                            font=font,
                            is_30_note=is_30_note,
                            scale=scale,
                            transposition=transposition,
                            watermarkEN=watermark,
                            note_counterEN=note_counter,
                            frac_note_hilight=fractional_note_highlight)
            elif (track_selection == 0):
                i = 1
                while export_pics(file=filename,
                                  papersize=papersize,
                                  ppi=ppi,
                                  background=background,
                                  overwrite=overwrite,
                                  font=font,
                                  track_selection=i,
                                  is_30_note=is_30_note,
                                  scale=scale,
                                  transposition=transposition,
                                  watermarkEN=watermark,
                                  note_counterEN=note_counter,
                                  frac_note_hilight=fractional_note_highlight):
                    i += 1
            else:
                export_pics(file=filename,
                            papersize=papersize,
                            ppi=ppi,
                            background=background,
                            overwrite=overwrite,
                            font=font,
                            track_selection=track_selection,
                            is_30_note=is_30_note,
                            scale=scale,
                            transposition=transposition,
                            watermarkEN=watermark)


if __name__ == '__main__':
    # export_pics(r'example.mid',
    #             filename='example_%d.png',
    #             musicname='example',
    #             scale=1,
    #             overwrite=True,
    #             interpret_bpm=None,
    #             save_pic=True,
    #             transposition=0,
    #             papersize=A4_VERTICAL_30,
    #             ppi=300)
    batch_export_pics(is_30_note=True,scale=1,watermark=False,note_counter=True,fractional_note_highlight=False)  # 批量导出
