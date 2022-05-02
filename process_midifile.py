import mido
import math
from util import PITCH_TO_MBNUM_15, PITCH_TO_MBNUM_30, prev_time_15,prev_time_30
from util import find_latest_event

def process_midifile(midifile, transposition,scale,track_selection,is30,interpret_bpm):
        '处理midi文件'
        ticks_per_beat = midifile.ticks_per_beat

        notes = []
        prev_time = prev_time_30 if is30 else prev_time_15
        PITCH_TO_MBNUM=PITCH_TO_MBNUM_30 if is30 else PITCH_TO_MBNUM_15

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
        if track_selection == -1:
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
                                    i = find_latest_event(
                                        tempo_events, miditime)
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
            noInfoTrackCount = 0
            for track in midifile.tracks:
                if track.name == '':
                    noInfoTrackCount += 1
                    continue
            if(len(midifile.tracks)-noInfoTrackCount < track_selection):
                return None, None
            i = 1
            for track in midifile.tracks:
                if track.name == '':
                    continue
                elif i != track_selection:
                    i += 1
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
                                    i = find_latest_event(
                                        tempo_events, miditime)
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