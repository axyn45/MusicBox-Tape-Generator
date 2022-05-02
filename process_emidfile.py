from util import PITCH_TO_MBNUM_15, PITCH_TO_MBNUM_30, prev_time_15, prev_time_30

def process_emidfile(emidfile, transposition,scale):
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