import numpy as np 

fname_template = 'im%07d.png'

zero_buffer_length = 150



framelist = [fname_template % 0] * zero_buffer_length

start_frame = 1801
end_frame = 2701

framelist = framelist + [fname_template % i for i in range(start_frame, end_frame)] + framelist
print framelist
print '\n'.join(framelist)
out_file_name = 'val_1min.index'

f = open(out_file_name, 'w')
f.write('\n'.join(framelist))

