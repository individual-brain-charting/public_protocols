import numpy as np

show_hz = 15

num_seconds = 120
num_repeats = 4

num_junk_seconds = 10
num_blank_seconds = 10

img_template = "im%07d.png"

blank_img = img_template % 0

stimlist = []

blank = [blank_img] * (num_blank_seconds * show_hz)

stimlist = stimlist + blank

junk_offset = num_seconds * show_hz + 1

junk = [img_template % i 
                 for i in range(junk_offset, 
                                junk_offset + num_junk_seconds * show_hz)]

stimlist = stimlist + junk

stimlist = stimlist + [img_template % j 
                       for j in range(num_seconds * show_hz)] * num_repeats

stimlist = stimlist + junk

stimlist = stimlist + blank

filename = "test_seq_4x2.index"

f = open(filename, "w")
f.write("\n".join(stimlist))

