'''
用于转换.emid文件与.mid文件

作者：bilibili@Bio-Hazard
    QQ3482991796
    QQ群586134350

FairyMusicBox系列软件作者：bilibili@调皮的码农

祝使用愉快！
'''

import os.path
import math
import mido


DEFAULT_BPM = 120.0
TIME_PER_BEAT = 8
DEFAULT_TICKS_PER_BEAT = 96
'FL导出的midi默认为此值'

PITCH_TO_MBNUM = [93, 91, 89, 88, 87, 86, 85, 84, 83, 82, 81, 80, 79, 78,
                  77, 76, 75, 74, 73, 72, 71, 70, 69, 67, 65, 64, 62, 60, 55, 53]
MBNUM_TO_PITCH = {93: 0, 91: 1, 89: 2, 88: 3, 87: 4, 86: 5, 85: 6, 84: 7, 83: 8,
                  82: 9, 81: 10, 80: 11, 79: 12, 78: 13, 77: 14, 76: 15, 75: 16,
                  74: 17, 73: 18, 72: 19, 71: 20, 70: 21, 69: 22, 67: 23, 65: 24,
                  64: 25, 62: 26, 60: 27, 55: 28, 53: 29}


def pitch2MBnum(pitch):
    return MBNUM_TO_PITCH[pitch]


def MBnum2pitch(MBnum):
    return PITCH_TO_MBNUM[MBnum]


class EmidTrack(list):
    def __init__(self, name: str):
        self.name = name
        self.length = 0

    def add_note(self, pitch: int, time: int) -> None:
        'note的pitch使用midi音高而非八音盒序号存储'
        self.append([pitch, time])
        if time > self.length:
            self.length = time

    def is_empty(self) -> bool:
        return self == []

    def _update_length(self) -> int:
        for note in self:
            if note[1] > self.length:
                self.length = note[1]
        return self.length


class EmidFile:
    '带有bpm信息，但是保存为emid文件时会丢失'

    def __init__(self, file=None, bpm: float = DEFAULT_BPM):
        self.tracks = []
        self.length = 0
        self.bpm = bpm

        if type(file) == str:
            with open(file, 'r', encoding='utf-8') as file:
                self._load(file)
        else:
            self._load(file)

    def _load(self, file) -> None:
        self.filename = file.name
        emidtext = file.read()
        notestext, s2 = emidtext.split('&')
        length, tracksname = s2.split('*')
        self.length = int(length)
        notelist = notestext.split('#')
        tracknamelist = tracksname.split(',')
        tracknamedict = {k: v for v, k in enumerate(tracknamelist)}
        
        '添加空轨道'
        for trackname in tracknamelist:
            self.tracks.append(EmidTrack(trackname))
        '添加音符'
        for note in notelist:
            MBnum, time, trackname = note.split(',')
            pitch = MBnum2pitch(int(MBnum))
            time = float(time)
            
            if trackname not in tracknamedict:
                tracknamedict[trackname]=len(trackname)

            trackidx = tracknamedict[trackname]
            self.tracks[trackidx].add_note(pitch, time)
        '更新长度'
        self._update_length()

    def _update_length(self) -> int:
        for track in self.tracks:
            tracklength = track._update_length()
            if tracklength > self.length:
                self.length = tracklength
        return self.length

    def del_empty_tracks(self) -> None:
        self.tracks = [track for track in self.tracks if not track.is_empty()]

    def save(self,
             filename=None,
             file=None,
             overwrite: bool = False,
             delemptytracks: bool = True) -> None:
        '注意：overwrite设置为True可能会覆盖现有文件！'
        if delemptytracks:
            self.del_empty_tracks()
        if file is not None:
            self._save(file)
        elif filename is not None:
            if not overwrite:
                filename = find_available_filename(filename)
            with open(filename, 'w', encoding='utf-8') as file:
                self._save(file)

    def _save(self, file) -> None:
        firstnote = True
        for track in self.tracks:
            for note in track:
                pitch, time = note
                if not firstnote:
                    file.write('#')  # 第一个音符前不需要加'#'分隔
                file.write('%d,%d,%s' %
                           (pitch2MBnum(pitch), time, track.name))
                firstnote = False
        file.write('&')
        '计算并存储长度'
        file.write(str(math.ceil(self.length / 4) + 1))
        file.write('*')
        tracknamelist = []
        for track in self.tracks:
            tracknamelist.append(track.name)
        file.write(','.join(tracknamelist))

    def export_Midi(self,
                    filename=None,
                    file=None,
                    overwrite: bool = False,
                    transposition: int = 0,
                    ticks_per_beat: int = DEFAULT_TICKS_PER_BEAT) -> mido.MidiFile:
        '''
        导出midi文件
        该方法返回一个mido.MidiFile()实例
        注意：overwrite设置为True可能会覆盖现有文件！
        '''
        midifile = mido.MidiFile(type=1)
        midifile.ticks_per_beat = ticks_per_beat

        '空轨道用于保存tempo信息'
        emptytrack = mido.MidiTrack()
        emptytrack.append(mido.MetaMessage(
            type='set_tempo', tempo=mido.bpm2tempo(self.bpm), time=0))
        midifile.tracks.append(emptytrack)

        for track in self.tracks:
            events = []
            for pitch, time in track:
                events.append(mido.Message(
                    type='note_on',
                    note=pitch + transposition,
                    time=round(ticks_per_beat * time / TIME_PER_BEAT)))
                events.append(mido.Message(
                    type='note_off',
                    note=pitch + transposition,
                    time=round(ticks_per_beat * ((time / TIME_PER_BEAT) + 1))))
            events.sort(key=lambda msg: msg.time)

            miditrack = mido.MidiTrack()
            miditrack.append(mido.MetaMessage(
                type='track_name', name='Track ' + track.name, time=0))
            miditrack.append(mido.Message(
                type='program_change', program=10, time=0))

            passtime = 0
            for msg in events:
                miditrack.append(msg.copy(time=msg.time - passtime))
                passtime = msg.time
            midifile.tracks.append(miditrack)
        '添加轨道结束事件'
        for miditrack in midifile.tracks:
            miditrack.append(mido.MetaMessage(type='end_of_track', time=0))

        if file is not None:
            midifile.save(file=file)
        elif filename is not None:
            if overwrite:
                midifile.save(filename)
            else:
                midifile.save(find_available_filename(filename))
        return midifile


def import_Midi(file, transposition: int = 0) -> EmidFile:
    '''
    导入midi
    transposition参数控制移调
    '''
    if type(file) == str:
        midifile = mido.MidiFile(file)
    elif type(file) == mido.MidiFile:
        midifile = file

    emidfile = EmidFile()
    bpm = None
    for trackidx, miditrack in enumerate(midifile.tracks):
        emidtrack = EmidTrack(str(trackidx))
        miditime = 0
        for msg in miditrack:
            miditime += msg.time
            if msg.type == 'note_on':
                if msg.velocity > 0:
                    emidtime = miditime / midifile.ticks_per_beat * TIME_PER_BEAT
                    if msg.note + transposition in MBNUM_TO_PITCH:
                        emidtrack.add_note(msg.note + transposition, emidtime)
            elif msg.type == 'set_tempo':
                if bpm is None:
                    bpm = mido.tempo2bpm(msg.tempo)
        if bpm is None:
            bpm = DEFAULT_BPM
        emidfile.tracks.append(emidtrack)
    emidfile._update_length()
    return emidfile


def midi2emid(midifilename, emidfilename):
    '快速将.mid文件转换为.emid文件'
    import_Midi(midifilename).save(emidfilename)


def emid2midi(emidfilename, midifilename):
    '快速将.emid文件转换为.mid文件'
    EmidFile(emidfilename).export_Midi(midifilename)


def find_available_filename(path):
    name, extension = os.path.splitext(path)
    if os.path.exists(name + extension):
        i = 1
        while os.path.exists(name + ' (%d)' % i + extension):
            i += 1
        return name + ' (%d)' % i + extension
    else:
        return name + extension


def batch_conv_midi2emid(path=None):
    '''
    批量将path目录下的所有.mid文件转换为.emid文件
    如果path参数留空，则取当前工作目录
    '''
    if path is None:
        path = os.getcwd()
    for filename in os.listdir(path):
        name, extention = os.path.splitext(filename)
        if extention == '.mid':
            midi2emid(filename, name + '.emid')


def batch_conv_emid2midi(path=None):
    '''
    批量将path目录下的所有.emid文件转换为.mid文件
    如果path参数留空，则取当前工作目录
    '''
    if path is None:
        path = os.getcwd()
    for filename in os.listdir(path):
        name, extention = os.path.splitext(filename)
        if extention == '.emid':
            emid2midi(filename, name + '.mid')


if __name__ == '__main__':
    # emidfile1 = import_Midi('example1.mid')
    # emidfile1.save('example1.emid')
    # emidfile2 = EmidFile('example2.emid')
    # emidfile2.export_Midi('example2.mid')
    batch_conv_midi2emid()

batch_conv_emid2midi(path=None)
#batch_conv_midi2emid()