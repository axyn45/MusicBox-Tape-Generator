from util import *


def notemark(draw, pitch, number, kp, ni, font, sum_note,tape_length,section=100,tape_summary=True):
    ppi = DEFAULT_PPI
    if((number) % section == 0 or (number) == sum_note):
        if((number) < 10):
            draw.text(xy=posconvert((kp.startpos[0] + kp.col_offset*ni.coln + 6 + 2*pitch - 0.9, kp.startpos[1] + ni.rowmm-2.2),
                       ppi * ANTI_ALIAS), text=str(number), font=font, fill=(255, 0, 0, 255))
        elif((number) < 100):
            draw.text(xy=posconvert((kp.startpos[0] + kp.col_offset*ni.coln + 6 + 2*pitch - 1.9, kp.startpos[1] + ni.rowmm-2.2),
                       ppi * ANTI_ALIAS), text=str(number), font=font, fill=(255, 0, 0, 255))
        elif((number) < 1000):
            draw.text(xy=posconvert((kp.startpos[0] + kp.col_offset*ni.coln + 6 + 2*pitch - 2.9, kp.startpos[1] + ni.rowmm-2.2),
                       ppi * ANTI_ALIAS), text=str(number), font=font, fill=(255, 0, 0, 255))
        elif((number) < 10000):
            draw.text(xy=posconvert((kp.startpos[0] + kp.col_offset*ni.coln + 6 + 2*pitch - 3.9, kp.startpos[1] + ni.rowmm-2.2),
                       ppi * ANTI_ALIAS), text=str(number), font=font, fill=(255, 0, 0, 255))
        else:
            draw.text(xy=posconvert((kp.startpos[0] + kp.col_offset*ni.coln + 6 + 2*pitch - 4.9, kp.startpos[1] + ni.rowmm-2.2),
                       ppi * ANTI_ALIAS), text=str(number), font=font, fill=(255, 0, 0, 255))
        if((number) == sum_note and tape_summary):
            draw.text(xy=posconvert((kp.startpos[0] + kp.col_offset*ni.coln + 16, kp.endpos[1]), ppi),
                       text="Notes: "+str(number), font=font, fill=(0, 255, 255, 255))
            draw.text(xy=posconvert((kp.startpos[0] + kp.col_offset*ni.coln + 38, kp.endpos[1]), ppi), text="Length: "+str(
                tape_length)+"cm", font=font, fill=(255, 220, 0, 255))
