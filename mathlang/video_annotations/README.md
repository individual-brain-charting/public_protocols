## Notes about video annotations of the *MathLang* task  

Authors: Juan Jesús Torre, Ana Luisa Pinho  
e-mail: ana.pinho@inria.fr

Each video presents the sequence of stimuli displayed during one single run. There were 4 different sequences and each of them refers to two possible types (see README.md file in protocol folder for more information). Because each sequence pertains to both visual and audio stimuli, the visual and audio stimuli in type **a** corresponds to the audio and visual stimuli in type **b**, respectively.

Note that, in IBC, we didn't run the 4<sup>th</sup> run tybe **b** and, therefore, the corresponding video annotation is not provided herein.

The randomization performed to divide the stimuli between 5 blocks (although we only used blocks 1-4) was performed by estipulating the contents of a single block:

    * 8 false for control
    * 4 true and 4 false for arithfact, arithprin, general and geomfact
    * 2 true-true, 2 true-false, 2 false-true, 2 false-false for context and tom
    * Half of each type are auditory and half are visual (written)

After grouping all sentences in a single file, random picks were performed for the five blocks in order to conform the conditions described above. Every sentence exists in visual and auditory formats. Only one of those was picked for the all-sentences file, with a 50% auditory and 50% visual. Then, after making the picks for each block, 8 new stimuli were added for the empty stimuli, and then the order of the stimuli within a block is randomized. Lastly, the "b" blocks are generated changing the file type of each sentence in its corresponding "a" block. 
