Notes to run the protocol of Gallant's lab
Author: Ana Luisa Pinho
Date: 11th March 2016
##############################################################################################

To run, typewrite in the terminal under the directory containing all scripts:
> python play.py <arg1> <arg2>

arg1 --> session number = [1,3]
arg2 --> sequence type = [1,8]

The sequence type depends on the images that are loaded and the sequence pre-defined.

Example 1.1: > python play.py 1 1
It will load the images from trn001 folder and the sequence trnseq.index

Example 1.2: > python play.py 1 2
It will load the images from val001_3min folder and the sequence valseq3minby10_01.index

Example 1.3: > python play.py 1 3
It will load the images from trn002 folder and the sequence trnseq.index

Example 1.4: > python play.py 1 4
It will load the images from val001_3min folder and the sequence valseq3minby10_02.index

Example 1.5: > python play.py 1 5
It will load the images from trn003 folder and the sequence trnseq.index

Example 1.6: > python play.py 1 6
It will load the images from val001_3min folder and the sequence valseq3minby10_03.index

Example 1.7: > python play.py 1 7
It will load the images from trn004 folder and the sequence trnseq.index

Example 1.8: > python play.py 1 8
It will load the images from val001_3min folder and the sequence valseq3minby10_04.index

Example 2.1: > python play.py 2 1
It will load the images from trn005 folder and the sequence trnseq.index

Example 2.2: > python play.py 2 2
It will load the images from val002_3min folder and the sequence valseq3minby10_01.index

Example 2.3: > python play.py 2 3
It will load the images from trn006 folder and the sequence trnseq.index

Example 2.4: > python play.py 2 4
It will load the images from val002_3min folder and the sequence valseq3minby10_02.index

_________________________________________________________________________________________________

For full screen: set the parameter 'fullscreen' in showmovie.py to 1

_________________________________________________________________________________________________

Create directory 'log' to store log files of each session.

_________________________________________________________________________________________________

The folders containing the images, i.e. trn*/ and val*/, are not stored on github. The folder words/ is not stored on github, either.
Please, download them from: /neurospin/unicog/protocols/IBC/protocols/gallant_movies

_________________________________________________________________________________________________

To set the key for the TTL, change parameter on line 125 in showmovie.py

_________________________________________________________________________________________________

Preset resolution for video display:
800x600