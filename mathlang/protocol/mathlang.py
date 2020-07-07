#! /usr/bin/env python
# Time-stamp: <2018-03-28 16:31:03 cp983411>


#import sys
import io
import os.path as op
import argparse
import csv

import expyriment.control
from expyriment import stimuli
from expyriment.misc import Clock

from queue import PriorityQueue

# constants (which can be modified by optional command line arguments)
WORD_DURATION = 350
PICTURE_DURATION = 1000
TEXT_DURATION = 350
TOTAL_EXPE_DURATION = 568000  # time in ms / last onset (white cross) = 567000
BACKGROUND_COLOR=(0, 0, 0)
TEXT_FONT = 'ARIALN.TTF'  # Must be in local Fonts directory
TEXT_SIZE = 48
TEXT_COLOR = (255, 255, 255)
RED_TEXT_SIZE = 75  # For red cross
RED_TEXT_COLOR = (255, 0, 0) # RGB - For red cross

# process command line options

parser = argparse.ArgumentParser()
parser.add_argument("--splash", help="displays a picture (e.g. containing instructions) before starting the experiment")

parser.add_argument('csv_files',
                    nargs='+',
                    action="append",
                    default=[])
parser.add_argument('--total-duration',
                    type=int,
                    default=-1,
                    help="time to wait for after the end of the stimuli stream")
parser.add_argument("--rsvp-display-time",
                    type=int,
                    default=WORD_DURATION,
                    help="set the duration of display of single words \
                          in rsvp stimuli")
parser.add_argument("--picture-display-time",
                    type=int,
                    default=PICTURE_DURATION,
                    help="set the duration of display of pictures")
parser.add_argument("--text-display-time",
                    type=int,
                    default=TEXT_DURATION,
                    help="set the duration of display of pictures")
parser.add_argument("--text-font",
                    type=str,
                    default=TEXT_FONT,
                    help="set the font for text stimuli")
parser.add_argument("--text-size",
                    type=int,
                    default=TEXT_SIZE,
                    help="set the vertical size of text stimuli")
parser.add_argument("--text-color",
                    nargs='+',
                    type=int,
                    default=TEXT_COLOR,
                    help="set the font for text stimuli")
parser.add_argument("--background-color",
                    nargs='+',
                    type=int,
                    default=BACKGROUND_COLOR,
                    help="set the background color")
parser.add_argument('-r', '--run', metavar='SessionNum', type=int,
                    default=1, choices=[1, 2, 3, 4, 5],
                    help="Session number. Choices: "
                         "%(choices)s. Default: %(default)s")
parser.add_argument('-t', '--type', metavar='SessionType', type=str,
                    default='a', choices=['a', 'b'],
                    help="Session type. Choices: "
                         "%(choices)s. Default: %(default)s")


args = parser.parse_args()
splash_screen = args.splash
WORD_DURATION = args.rsvp_display_time
PICTURE_DURATION = args.picture_display_time
TEXT_DURATION = args.text_display_time
TEXT_SIZE = args.text_size
TEXT_COLOR = tuple(args.text_color)
TEXT_FONT = args.text_font
BACKGROUND_COLOR = tuple(args.background_color)
TOTAL_EXPE_DURATION = args.total_duration
run = "%02d" % args.run
ses_type = args.type

csv_files = args.csv_files[0]
suffix = run + ses_type

expyriment.design.defaults.experiment_background_colour = BACKGROUND_COLOR
expyriment.control.set_develop_mode(False)


exp = expyriment.design.Experiment(name="HiRes Experiment",
                                   background_colour=BACKGROUND_COLOR,
                                   foreground_colour=TEXT_COLOR,
                                   text_size=TEXT_SIZE,
                                   text_font=TEXT_FONT,
                                   filename_suffix=suffix)

expyriment.misc.add_fonts('fonts')
expyriment.control.initialize(exp)

exp._screen_colour = BACKGROUND_COLOR
kb = expyriment.io.Keyboard()
bs = stimuli.BlankScreen(colour=BACKGROUND_COLOR)
wm = stimuli.FixCross(size=(25, 25), line_width=3, colour=(204, 0, 0))
fs = stimuli.FixCross(size=(25, 25), line_width=3, colour=TEXT_COLOR)

events = PriorityQueue()  # all stimuli will be queued here

# load stimuli

mapsounds = dict()
mapspeech = dict()
maptext = dict()
mappictures = dict()
mapvideos = dict()

for listfile in csv_files:
    stimlist = csv.reader(io.open(listfile, 'r', encoding='utf-8'))
    bp = op.dirname(listfile)
    for row in stimlist:
        # onset = timing for the stimulus
        # stype = type of the stimulus (sound, picture, video, text, rsvp)
        # cond = condition
        # pm = (True/False)
        # f = file name or sentence in rsvp
        onset, stype, cond, pm, f = int(row[0]), row[1], row[2], row[3], row[4]
        if stype == 'sound':
            if not f in mapsounds:
                mapsounds[f] = stimuli.Audio(op.join(bp, f))
                mapsounds[f].preload()
            events.put((onset, 'sound', f, mapsounds[f], cond, pm))
        elif stype == 'picture':
            if not f in mappictures:
                mappictures[f] = stimuli.Picture(op.join(bp, f))
                mappictures[f].preload()
            events.put((onset, 'picture', f, mappictures[f], cond, pm))
            events.put((onset + PICTURE_DURATION, 'blank', 'blank', bs, '', ''))
        elif stype == 'video':
            if not f in mapvideos:
                mapvideos[f] = stimuli.Video(op.join(bp, f))
                mapvideos[f].preload()
            events.put((onset, 'video', f, mapvideos[f], cond, pm))
        elif stype == 'text':
            maptext[f] = stimuli.TextLine(f,
                                          text_font=TEXT_FONT,
                                          text_size=TEXT_SIZE,
                                          text_colour=TEXT_COLOR,
                                          background_colour=BACKGROUND_COLOR)
            maptext[f].preload()
            events.put((onset, 'text', f, maptext[f], cond, pm))
            events.put((onset + TEXT_DURATION, 'blank', 'blank', fs, '', ''))
        elif stype == 'redtext':
            maptext[f] = stimuli.TextLine(f,
                                          text_font=TEXT_FONT,
                                          text_size=RED_TEXT_SIZE,
                                          text_colour=RED_TEXT_COLOR,
                                          background_colour=BACKGROUND_COLOR)
            maptext[f].preload()
            events.put((onset, 'redtext', f, maptext[f], cond, pm))
            events.put((onset + TEXT_DURATION, 'blank', 'blank', fs, '', ''))
        elif stype == 'rsvp':
            for i, w in enumerate(f.split()):
                if not w in maptext:
                    maptext[w] = stimuli.TextLine(w,
                                                  text_font=TEXT_FONT,
                                                  text_size=TEXT_SIZE,
                                                  text_colour=TEXT_COLOR,
                                                  background_colour=BACKGROUND_COLOR)
                    maptext[w].preload()
                events.put((onset + i * WORD_DURATION, 'text', w, maptext[w], cond+str(i), pm))
            events.put((onset + (i + 1) * WORD_DURATION, 'blank', 'blank', fs, '', ''))

exp.add_data_variable_names(['time', 'cond', 'pm', 'stype', 'id', 'target_time'])

expyriment.control.start()

if not (splash_screen is None):
    splashs = stimuli.Picture(splash_screen)
    splashs.present()
    kb.wait_char(' ')

wm.present()
kb.wait_char('t')  # wait for scanner TTL
fs.present()  # clear screen, presenting fixation cross

a = Clock()

while not(events.empty()):
    onset, stype, id, stim, cond, pm = events.get()
    while a.time < (onset - 10):
        a.wait(1)
        k = kb.check()
        if k is not None:
            exp.data.add([a.time, 'keypressed,{}'.format(k)])

    stim.present()
    exp.data.add([a.time, '{},{},{},{},{}'.format(cond, pm, stype, id, onset)])

    k = kb.check()
    if k is not None:
        exp.data.add([a.time, 'keypressed,{}'.format(k)])


fs.present()

if TOTAL_EXPE_DURATION != -1:
    while a.time < TOTAL_EXPE_DURATION:
        a.wait(10)

expyriment.control.end('Merci !', 2000)
