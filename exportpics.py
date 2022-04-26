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
import os
import math
from tkinter import Image
from tkinter.tix import NoteBook
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
from matplotlib.pyplot import fill
import mido
import emid
import notecounter as nct
from collections import OrderedDict


PITCH_TO_MBNUM = {93: 29, 91: 28, 89: 27, 88: 26, 87: 25, 86: 24, 85: 23, 84: 22,
                  83: 21, 82: 20, 81: 19, 80: 18, 79: 17, 78: 16, 77: 15, 76: 14,
                  75: 13, 74: 12, 73: 11, 72: 10, 71: 9, 70: 8, 69: 7, 67: 6,
                  65: 5, 64: 4, 62: 3, 60: 2, 55: 1, 53: 0}

LEFT_ALIGN = 0
CENTER_ALIGN = 1
RIGHT_ALIGN = 2

A4_VERTICAL = 25
A4_HORIZONAL = 24
A3_VERTICAL = 23
A3_HORIZONAL = 22
B5_VERTICAL = 43
B5_HORIZONAL = 42
B4_VERTICAL = 41
B4_HORIZONAL = 40
AUTO_SIZE = 0
TEST_SIZE = 1

PAPER_INFO = {A4_VERTICAL: {'size': (210, 297), 'col': 3, 'row': 35},
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


def _find_latest_event(l, t):
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

def bar_ref(Number):   # 将音符转换为音符的编号，返回逆时针旋转90°的图像
    Number=str(Number)
    strlen=len(Number)
    img = PIL.Image.new('RGB', posconvert((strlen*1.5, 2.5)), color='#ffffff')
    font = PIL.ImageFont.load_default()
    font = PIL.ImageFont.truetype('C:\Windows\Fonts\msyh.ttc', 30)
    draw=PIL.ImageDraw.Draw(img)
    draw.text(posconvert((0,-0.5)), str(Number), font=font, fill=(0, 0, 0))
    # img.show()
    return img.rotate(90,PIL.Image.NEAREST,expand = 1)

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
                isSuccessful: bool = True) -> list:
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

    def process_emidfile(emidfile, transposition=transposition):
        '处理emid文件'
        notes = []
        for track in emidfile.tracks:
            for note in track:
                pitch, time = note
                if pitch + transposition in PITCH_TO_MBNUM:
                    notes.append(
                        [PITCH_TO_MBNUM[pitch + transposition], float(time * scale)])
        notes.sort(key=lambda a: (a[1], a[0]))
        length = notes[-1][1]
        return notes, length

    def process_midifile(midifile, transposition=transposition):
        '处理midi文件'
        ticks_per_beat = midifile.ticks_per_beat

        notes = []
        prev_time = {93: -8, 91: -8, 89: -8, 88: -8, 87: -8, 86: -8, 85: -8, 84: -8,
                     83: -8, 82: -8, 81: -8, 80: -8, 79: -8, 78: -8, 77: -8, 76: -8,
                     75: -8, 74: -8, 73: -8, 72: -8, 71: -8, 70: -8, 69: -8, 67: -8,
                     65: -8, 64: -8, 62: -8, 60: -8, 55: -8, 53: -8}

        if interpret_bpm is not None:
            tempo_events = []
            time_passed = []
            for track in midifile.tracks:
                miditime = 0
                for msg in track:
                    miditime += msg.time
                    if msg.type == 'set_tempo':
                        tempo_events.append((msg.tempo, miditime))

            realtime = 0.0
            for i in range(len(tempo_events)):
                tempo = 0 if i == 0 else tempo_events[i-1][0]
                delta_miditime = tempo_events[i][1] - tempo_events[i-1][1]
                realtime += mido.tick2second(delta_miditime,
                                             ticks_per_beat, tempo)
                time_passed.append(realtime)
        if track_selection==-1:
            for track in midifile.tracks:
                miditime = 0
                for msg in track:
                    miditime += msg.time
                    if msg.type == 'note_on':
                        if msg.velocity > 0:
                            pitch = msg.note + transposition
                            if pitch in PITCH_TO_MBNUM:
                                if interpret_bpm is None:
                                    beat = miditime / ticks_per_beat
                                else:
                                    i = _find_latest_event(tempo_events, miditime)
                                    tempo, tick = tempo_events[i]
                                    realtime = time_passed[i] + mido.tick2second(
                                        miditime - tick, ticks_per_beat, tempo)
                                    beat = realtime / 60 * interpret_bpm  # 计算beat

                                time = beat * 8 * scale
                                # if time - prev_time[pitch] >= 8:
                                prev_time[pitch] = time
                                notes.append([PITCH_TO_MBNUM[pitch],
                                              time])  # 添加note
                                # else:  # 如果音符过近，则直接忽略该音符
                                #    print(
                                #        f'[WARN] Too Near! Note {pitch} in bar {math.floor(miditime / ticks_per_beat / 4) + 1}')
                            else:  # 如果超出音域
                                print(
                                    f'[WARN] Note {pitch} in bar {math.floor(miditime / ticks_per_beat / 4) + 1} is out of range')
        else:
            noInfoTrackCount=0
            for track in midifile.tracks:
                if track.name=='':
                    noInfoTrackCount+=1
                    continue
            if(len(midifile.tracks)-noInfoTrackCount<track_selection):
                return None,None
            i=1
            for track in midifile.tracks:
                if track.name=='':
                    continue
                elif i!=track_selection:
                    i+=1
                    continue
                miditime = 0
                for msg in track:
                    miditime += msg.time
                    if msg.type == 'note_on':
                        if msg.velocity > 0:
                            pitch = msg.note + transposition
                            if pitch in PITCH_TO_MBNUM:
                                if interpret_bpm is None:
                                    beat = miditime / ticks_per_beat
                                else:
                                    i = _find_latest_event(tempo_events, miditime)
                                    tempo, tick = tempo_events[i]
                                    realtime = time_passed[i] + mido.tick2second(
                                        miditime - tick, ticks_per_beat, tempo)
                                    beat = realtime / 60 * interpret_bpm  # 计算beat

                                time = beat * 8 * scale
                                # if time - prev_time[pitch] >= 8:
                                prev_time[pitch] = time
                                notes.append([PITCH_TO_MBNUM[pitch],
                                              time])  # 添加note
                                # else:  # 如果音符过近，则直接忽略该音符
                                #    print(
                                #        f'[WARN] Too Near! Note {pitch} in bar {math.floor(miditime / ticks_per_beat / 4) + 1}')
                            else:  # 如果超出音域
                                print(
                                    f'[WARN] Note {pitch} in bar {math.floor(miditime / ticks_per_beat / 4) + 1} is out of range')
                break
        notes.sort(key=lambda a: (a[1], a[0]))  # 按time排序
        notes = [i for n, i in enumerate(notes) if i not in notes[:n]]
        length = notes[-1][1]
        return notes, length


    print('Processing Data...')
    '打开文件以及处理默认值'
    typ = type(file)
    if typ == str:
        # 文件名替代heading
        strbin, aligntype = heading
        # track_No=None
        if filename is None:
            if track_selection>0:
                filename = os.path.splitext(file)[0]+ '_Track' + str(track_selection)+'_%d.png'
            else:
                filename = os.path.splitext(file)[0] +'_%d.png'
            # 页眉显示曲目名称
            heading = (os.path.splitext(file)[0]+ '_Track'+str(track_selection), aligntype)
        if musicname is None:
            if track_selection>0:
                musicname = os.path.splitext(os.path.split(file)[1])[0]+ '_Track'+str(track_selection)
                # 页眉显示曲目名称
                heading = (os.path.splitext(os.path.split(file)[1])[0]+ '_Track'+str(track_selection), aligntype)
            else:
                musicname = os.path.splitext(os.path.split(file)[1])[0]
                heading = (os.path.splitext(os.path.split(file)[1])[0], aligntype)
            
        extention = os.path.splitext(file)[1]
        if extention == '.emid':
            TEmid = emid.EmidFile(file)
            notes, length = process_emidfile(emid.mido.MidiFile(file))
            NOTES_SUM, TAPE_LENGTH = nct.notes_and_length(filename)
        elif extention == '.mid':
            notes, length = process_midifile(mido.MidiFile(file))
            NOTES_SUM, TAPE_LENGTH = nct.notes_and_length(mido.MidiFile(file))
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
            notes, length = process_midifile(file)

    
    else:
        raise(ValueError(
            'Unknown file type (filename, emid.EmidFile or mido.MidiFile required)'))

    #所有音轨都输出完毕
    if notes==None:
        isSuccessful=False
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

    contentsize = (70 * col, 8 * row)
    startpos = (size[0] / 2 - contentsize[0] / 2,
                size[1] / 2 - contentsize[1] / 2)
    endpos = (size[0] / 2 + contentsize[0] / 2,
              size[1] / 2 + contentsize[1] / 2)  # 计算坐标

    if font is None:  # 在FONT_PATH中寻找第一个能使用的字体
        for i in FONT_PATH:
            try:
                font_ref = PIL.ImageFont.truetype(i, round(mm2pixel(2, ppi)))
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

    print('Drawing...')
    images0 = []
    images1 = []
    # test
    images2 = []

    draws0 = []
    draws1 = []
    # test
    draws2 = []

    # 统计小节数，从0开始
    COL_NO = 0
    # 统计已打印的note数量
    NOTE_COUNT = 0
    note_ref = PIL.Image.new('RGBA', posconvert(
        (2*12, 2*32), ppi), (255, 255, 255, 255))
    draw_ref = PIL.ImageDraw.Draw(note_ref)

    # 准备音名标识图片
    # vp for vertival position
    vp1 = 2
    vp2 = 8
    vp3 = 14
    vp4 = 20

    # 绘制音名标识图片
    # 1~10
    draw_ref.text(xy=posconvert((vp1, 2), ppi), text="C",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp2, 4), ppi), text="D",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp3, 6), ppi), text="G",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp4, 8), ppi), text="A",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp3, 10), ppi), text="B",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp2, 12), ppi), text="C1",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp1, 14), ppi), text="D1",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp2, 16), ppi), text="E1",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp3, 18), ppi), text="F1",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp4, 20), ppi), text="#F1",
                  font=font_ref, fill=(28, 43, 255, 255))
    # 11~20
    draw_ref.text(xy=posconvert((vp3, 22), ppi), text="G1",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp2, 24), ppi), text="#G1",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp1, 26), ppi), text="A1",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp2, 28), ppi), text="#A1",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp3, 30), ppi), text="B1",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp4, 32), ppi), text="C2",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp3, 34), ppi), text="#C2",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp2, 36), ppi), text="D2",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp1, 38), ppi), text="#D2",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp2, 40), ppi), text="E2",
                  font=font_ref, fill=(28, 43, 255, 255))
    # 21~30
    draw_ref.text(xy=posconvert((vp3, 42), ppi), text="F2",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp4, 44), ppi), text="#F2",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp3, 46), ppi), text="G2",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp2, 48), ppi), text="#G2",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp1, 50), ppi), text="A2",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp2, 52), ppi), text="#A2",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp3, 54), ppi), text="B2",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp4, 56), ppi), text="C3",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp3, 58), ppi), text="D3",
                  font=font_ref, fill=(28, 43, 255, 255))
    draw_ref.text(xy=posconvert((vp2, 60), ppi), text="E3",
                  font=font_ref, fill=(28, 43, 255, 255))
    # note_ref.show()
    # 图片旋转90°
    note_ref = note_ref.rotate(angle=90)
    # 定义裁切点坐标
    # left, upper = posconvert((0, 40), ppi)
    # right, lower = posconvert((2*32, 2*32), ppi)
    # 裁切图片
    # note_ref = note_ref.crop((left, upper, right, lower))
    # note_ref.show()

    #统计总共小节数
    total_bars = 0
    #每小节的节拍数
    beats_per_bar = 8

    for i in range(pages):
        test_pos = posconvert(size, ppi)
        image0 = PIL.Image.new('RGBA', posconvert(size, ppi), (0, 0, 0, 0))
        image1 = PIL.Image.new('RGBA', posconvert(
            size, ppi * ANTI_ALIAS), (0, 0, 0, 0))

        image2 = PIL.Image.new('RGBA', posconvert(size, ppi), (0, 0, 0, 0))

        draw0 = PIL.ImageDraw.Draw(image0)
        draw1 = PIL.ImageDraw.Draw(image1)

        draw2 = PIL.ImageDraw.Draw(image2)
        '写字'
        for j in range(col if i < pages - 1 else cols):
            '标题文字'
            headingtext, align = heading
            textsize = font0.getsize(headingtext)

            if align == LEFT_ALIGN:
                posX = 7
            elif align == CENTER_ALIGN:
                posX = (size[0] - pixel2mm(textsize[0], ppi)) / 2
            elif align == RIGHT_ALIGN:
                posX = (size[0] - pixel2mm(textsize[0], ppi)) - 7
            posY = ((size[1] - contentsize[1]) / 2 -
                    pixel2mm(textsize[1], ppi)) - 1

            draw0.text(xy=posconvert((posX, posY-1), ppi),
                       text=headingtext,
                       font=font0,
                       fill=(0, 0, 0, 255))
            '栏尾页码'
            colnum = i * col + j + 1
            draw0.text(xy=posconvert((startpos[0] + 70*j + 6, endpos[1]), ppi),
                       text=str(colnum),
                       font=font1,
                       fill=(0, 0, 0, 255))
            '栏右上角文字'
            if(j == 0):
                for k, char in enumerate(musicname):
                    textsize = font2.getsize(char)
                    draw0.text(
                        xy=posconvert(
                            (startpos[0] + 70*j + 59 - pixel2mm(textsize[0], ppi) / 2,
                             startpos[1] + 8*k + 7 - pixel2mm(textsize[1], ppi)), ppi),
                        text=char, font=font2, fill=(0, 0, 0, 60))
            '栏右上角页码'
            textsize = font2.getsize(str(colnum))
            # draw0.text(
            #    xy=posconvert(
            #        (startpos[0] + 70*j + 62 - pixel2mm(textsize[0], ppi),
            #         startpos[1] + 8*len(musicname) + 7 - pixel2mm(textsize[1], ppi)), ppi),
            #    text=str(colnum), font=font2, fill=(0, 0, 0, 150))
            sign = ""
            sign1 = "sdbfe"

            # 水印*4/栏
            draw0.text(
                xy=posconvert(
                    (startpos[0] + 70*j + 15 - pixel2mm(textsize[0], ppi),
                     startpos[1] + 8*len(musicname)-120 - pixel2mm(textsize[1], ppi)), ppi),
                text=sign, font=font2, fill=(0, 0, 0, 40))
            draw0.text(
                xy=posconvert(
                    (startpos[0] + 70*j + 15 - pixel2mm(textsize[0], ppi),
                     startpos[1] + 8*len(musicname)-70 - pixel2mm(textsize[1], ppi)), ppi),
                text=sign, font=font2, fill=(0, 0, 0, 40))
            draw0.text(
                xy=posconvert(
                    (startpos[0] + 70*j + 15 - pixel2mm(textsize[0], ppi),
                     startpos[1] + 8*len(musicname)-20 - pixel2mm(textsize[1], ppi)), ppi),
                text=sign, font=font2, fill=(0, 0, 0, 40))
            draw0.text(
                xy=posconvert(
                    (startpos[0] + 70*j + 15 - pixel2mm(textsize[0], ppi),
                     startpos[1] + 8*len(musicname)+30 - pixel2mm(textsize[1], ppi)), ppi),
                text=sign, font=font2, fill=(0, 0, 0, 40))
            #################################################
            draw0.text(
                xy=posconvert(
                    (startpos[0] + 70*j + 15 - pixel2mm(textsize[0], ppi),
                     startpos[1] + 8*len(musicname) + 80 - pixel2mm(textsize[1], ppi)), ppi),
                text=sign, font=font2, fill=(0, 0, 0, 40))
            # draw0.text(
            #     xy=posconvert(
            #         (startpos[0] + 70*j + 15 - pixel2mm(textsize[0], ppi),
            #          startpos[1] + 8*len(musicname)+30 - pixel2mm(textsize[1], ppi)), ppi),
            #     text=sign, font=font2, fill=(0, 0, 0, 40))
            # draw0.text(
            #     xy=posconvert(
            #         (startpos[0] + 70*j + 15 - pixel2mm(textsize[0], ppi),
            #          startpos[1] + 8*len(musicname)+60 - pixel2mm(textsize[1], ppi)), ppi),
            #     text=sign, font=font2, fill=(0, 0, 0, 40))
            # draw0.text(
            #     xy=posconvert(
            #         (startpos[0] + 70*j + 15 - pixel2mm(textsize[0], ppi),
            #          startpos[1] + 8*len(musicname)+90 - pixel2mm(textsize[1], ppi)), ppi),
            #     text=sign, font=font2, fill=(0, 0, 0, 40))

        '画格子'
        for j in range(col if i < pages - 1 else cols):

            '整拍横线'
            for k in range(row + 1):
                # if(j!=0 and k==0):
                #     total_beats+=row
                total_bars += 1
                # 绘制小节标识和粘贴音名标识图
                if (total_bars % beats_per_bar == 1 and k!=row):
                    # 粘贴音名标识图
                    # if(COL_NO%9==0):
                    #    image0.paste(note_ref,posconvert((startpos[0] + 70*j + 2.5,startpos[1]+8*k+80)))
                    # 绘制小节标识
                    # bar_ref(COL_NO+1).show()
                    image0.paste(bar_ref(COL_NO+1), posconvert((startpos[0] + 70*j + 10+2*27+0.5, startpos[1] + 8*k+1)))

                    # if(COL_NO < (10-1)):
                    #     draw0.text(xy=posconvert((startpos[0] + 70*j + 10 + 2*28, startpos[1] + 8*k)), text=str(
                    #         COL_NO+1), font=font0, fill=(0, 0, 0, 255))
                    # elif(COL_NO < 100):
                    #     draw0.text(xy=posconvert((startpos[0] + 70*j + 10 + 2*27, startpos[1] + 8*k)), text=str(
                    #         COL_NO+1), font=font0, fill=(0, 0, 0, 255))
                    # else:
                    #     draw0.text(xy=posconvert((startpos[0] + 70*j + 10 + 2*26, startpos[1] + 8*k)), text=str(
                    #         COL_NO+1), font=font0, fill=(0, 0, 0, 255))
                    COL_NO += 1

                # 绘制整拍横线
                draw0.line(posconvert((startpos[0] + 70*j + 6,
                                       startpos[1] + 8*k), ppi) +
                           posconvert((startpos[0] + 70*j + 6 + 2*29,
                                       startpos[1] + 8*k), ppi),
                           fill=(0, 0, 0, 255), width=1)

            '半拍横线'
            for k in range(row):
                draw0.line(posconvert((startpos[0] + 70*j + 6,
                                       startpos[1] + 8*k + 4), ppi) +
                           posconvert((startpos[0] + 70*j + 6 + 2*29,
                                       startpos[1] + 8*k + 4), ppi),
                           fill=(0, 0, 0, 128), width=1)
            '竖线'
            for k in range(30):
                draw0.line(posconvert((startpos[0] + 70*j + 6 + 2*k,
                                       startpos[1]), ppi) +
                           posconvert((startpos[0] + 70*j + 6 + 2*k,
                                       endpos[1]), ppi),
                           fill=(0, 0, 0, 255), width=1)

            total_bars -= 1
        '分隔线'
        for j in range(col + 1 if i < pages - 1 else cols + 1):
            draw0.line(posconvert((startpos[0] + 70*j,
                                   startpos[1]), ppi) +
                       posconvert((startpos[0] + 70*j,
                                   endpos[1]), ppi),
                       fill=(0, 0, 0, 255), width=1)

        images0.append(image0)
        images1.append(image1)
        images2.append(image2)
        draws0.append(draw0)
        draws1.append(draw1)
        draws2.append(draw2)
    '画note'
    # NOTES_SUM=notes.count()
    Index = 0
    for pitch, time in notes:
        page = math.floor(time / (col * row * 8))
        coln = math.floor(time / (row * 8)) - page * col
        # math.modf(x)[0]取小数部分
        rowmm = math.modf(time / (row * 8))[0] * (row * 8)
        draw1 = draws1[page]
        Index += 1

        # 高亮没有落在网格线交点的孔位
        # 浮点数有精度误差，需要设置一个误差范围来修正
        if(rowmm % 1 > 0.0001 and rowmm % 1 < 0.9999):
            draw1.ellipse(posconvert((startpos[0] + 70*coln + 6 + 2*pitch - DOT_R,
                                      startpos[1] + rowmm - DOT_R), ppi * ANTI_ALIAS) +
                          posconvert((startpos[0] + 70*coln + 6 + 2*pitch + DOT_R,
                                      startpos[1] + rowmm + DOT_R), ppi * ANTI_ALIAS),
                          fill=(255, 0, 200, 255))
        else:
            draw1.ellipse(posconvert((startpos[0] + 70*coln + 6 + 2*pitch - DOT_R,
                                      startpos[1] + rowmm - DOT_R), ppi * ANTI_ALIAS) +
                          posconvert((startpos[0] + 70*coln + 6 + 2*pitch + DOT_R,
                                      startpos[1] + rowmm + DOT_R), ppi * ANTI_ALIAS),
                          fill=(0, 0, 0, 255))

    # 标记孔位编号
    for pitch, time in notes:
        page = math.floor(time / (col * row * 8))
        coln = math.floor(time / (row * 8)) - page * col
        rowmm = math.modf(time / (row * 8))[0] * (row * 8)
        draw1 = draws1[page]
        # 对x求余，即每x个孔显示一次孔位编号，默认50
        if((NOTE_COUNT+1) % 100 == 0 or (NOTE_COUNT+1) == len(notes)):
            if((NOTE_COUNT+1) < 10):
                draw1.text(xy=posconvert((startpos[0] + 70*coln + 6 + 2*pitch - 0.9, startpos[1] + rowmm-2.2),
                           ppi * ANTI_ALIAS), text=str(NOTE_COUNT+1), font=font0, fill=(255, 0, 0, 255))
            elif((NOTE_COUNT+1) < 100):
                draw1.text(xy=posconvert((startpos[0] + 70*coln + 6 + 2*pitch - 1.9, startpos[1] + rowmm-2.2),
                           ppi * ANTI_ALIAS), text=str(NOTE_COUNT+1), font=font0, fill=(255, 0, 0, 255))
            elif((NOTE_COUNT+1) < 1000):
                draw1.text(xy=posconvert((startpos[0] + 70*coln + 6 + 2*pitch - 2.9, startpos[1] + rowmm-2.2),
                           ppi * ANTI_ALIAS), text=str(NOTE_COUNT+1), font=font0, fill=(255, 0, 0, 255))
            elif((NOTE_COUNT+1) < 10000):
                draw1.text(xy=posconvert((startpos[0] + 70*coln + 6 + 2*pitch - 3.9, startpos[1] + rowmm-2.2),
                           ppi * ANTI_ALIAS), text=str(NOTE_COUNT+1), font=font0, fill=(255, 0, 0, 255))
            else:
                draw1.text(xy=posconvert((startpos[0] + 70*coln + 6 + 2*pitch - 4.9, startpos[1] + rowmm-2.2),
                           ppi * ANTI_ALIAS), text=str(NOTE_COUNT+1), font=font0, fill=(255, 0, 0, 255))
            if((NOTE_COUNT+1) == len(notes)):
                draw1.text(xy=posconvert((startpos[0] + 70*coln + 16, endpos[1]), ppi),
                           text="Notes: "+str(NOTE_COUNT+1), font=font0, fill=(0, 255, 255, 255))
                draw1.text(xy=posconvert((startpos[0] + 70*coln + 38, endpos[1]), ppi), text="Length: "+str(
                    round(TAPE_LENGTH*100, 1))+"cm", font=font0, fill=(255, 220, 0, 255))
        NOTE_COUNT = NOTE_COUNT+1

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
            cpimage.save(save_path, dpi=(300, 300))
        result.append(cpimage)

    print('Done!')
    return isSuccessful


def batch_export_pics(path=None,
                      papersize=A4_VERTICAL,
                      ppi=DEFAULT_PPI,
                      background=(255, 255, 255, 255),
                      overwrite=False,
                      font=None,
                      track_selection=-1):
    '''
    批量将path目录下的所有.mid和.emid文件转换为纸带设计稿图片
    如果path参数留空，则取当前工作目录
    '''
    if path is None:
        path = os.getcwd()
    for filename in os.listdir(path):
        extention = os.path.splitext(filename)[1]
        if extention == '.mid' or extention == '.emid':
            print('Converting %s ...' % filename)
            if(track_selection==-1):
                export_pics(file=filename,
                            papersize=papersize,
                            ppi=ppi,
                            background=background,
                            overwrite=overwrite,
                            font=font)
            elif (track_selection==0):
                i=1
                while export_pics(file=filename,
                            papersize=papersize,
                            ppi=ppi,
                            background=background,
                            overwrite=overwrite,
                            font=font,
                            track_selection=i):
                    i+=1
            else:
                export_pics(file=filename,
                            papersize=papersize,
                            ppi=ppi,
                            background=background,
                            overwrite=overwrite,
                            font=font,
                            track_selection=track_selection)


if __name__ == '__main__':
    # export_pics(r'example.mid',
    #             filename='example_%d.png',
    #             musicname='example',
    #             scale=1,
    #             overwrite=True,
    #             interpret_bpm=None,
    #             save_pic=True,
    #             transposition=0,
    #             papersize=A4_VERTICAL,
    #             ppi=300)
    batch_export_pics()  # 批量导出
