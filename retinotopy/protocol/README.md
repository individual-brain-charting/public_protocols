## Protocol of the *Retinotopy* task  

Author: Michael Eickenberg  

Adaptations made by: Ana Luisa Pinho   
email: ana.pinho@inria.fr  

Retinotopy protocols:
To run them, typewrite:
> `python retinoto.py` 1 #first wedge clock video  
> `python retinoto.py` 2 #first wedge anti-clock video  
> `python retinoto.py` 3 #first ring expanding video   
> `python retinoto.py` 4 #first ring contracting video   
> `python retinoto.py` 5 #second wedge clock video  
> `python retinoto.py` 6 #second wedge anti-clock video   
> `python retinoto.py` 7 #second ring expanding video  
> `python retinoto.py` 8 #second ring contracting video

________________________________________________________________________________________________________
In order to generate the videos:
> `python retinoto.py 1  --precalculate`  

This generates "retino_wedge.npz" and "retino_wing.npz". Do not push the videos to github.

________________________________________________________________________________________________________
In order to generate the ".csv" files, run in the parent directory the following:
> `python utils.py`  

And then, it will generate 8 "retino_fixation_*.csv" files:
"retino_fixation_1.csv" – for the wedge  
"retino_fixation_2.csv" - for the wedge  
"retino_fixation_3.csv" – for the ring  
"retino_fixation_4.csv" - for the ring  
"retino_fixation_5.csv" – for the wedge  
"retino_fixation_6.csv" - for the wedge  
"retino_fixation_7.csv" – for the ring  
"retino_fixation_8.csv" - for the ring

These files contain 3 columns with the following info:  
first column – index number  
second column – colour fixation cross presentation  
third column – onsets of the colour presentation  

To generate more of these ".csv" files, change both `utils.py` and `retinoto.py` scripts. 
By default, copy the ".csv" files to the current directory.
