#!/usr/bin/env python2.5

import sys
import os
import showmovie

cwd = os.path.abspath(os.path.split(__file__)[0])
types = dict(val=("val%03d_3min", "valseq3minby10_%02d.index"), trn=("trn%03d", "trnseq.index"))
seq = [("trn", 1), ("val", 1), ("trn", 2), ("val", 2), ("trn", 3), ("val", 3), ("trn", 4), ("val",5)]
### added ("val",5) for a 10 x 1-min repeatability test run
### 9/3/2012 SN

_, folder, indexfile = sys.argv

# t, r = seq[int(run)-1]
# impath, idxfile = types[t]
# if t == "val":
# 	impath  = impath%int(session)
# 	idxfile = idxfile % r
# else:
# 	impath  = impath%((int(session)-1)*4+r)

# impath = os.path.join(cwd, impath)+'/'
# idxfile = os.path.join(cwd, idxfile)

impath = folder
idxfile = indexfile

print impath
print idxfile

showmovie.fixationcolor = ((255, 80, 80), (80,255,80), (80, 80, 255), (255, 80, 80), (80, 255, 80), (80, 80, 255), (255, 255, 80))
showmovie.fcchange = 2
showmovie.show_hz = 15
showmovie.tfactor = 1.0000 #1.03365
showmovie.show(impath, idxfile)
