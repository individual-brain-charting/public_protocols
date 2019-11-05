#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# =============================================================================
# Script on Retinotopy for the IBC project
#
# Author: Michael Eickenberg
# Contributor: Ana Luísa Pinho
#
# email: ana.pinho@inria.fr
# =============================================================================

import numpy as np
from psychopy import core, visual, event
# from utils import show_fixation_cross
import time


# %%
def get_wedge(angular_position, checker_phase=0., checker_cycles_radial=10,
              checker_cycles_angular=2.5, outer_radius=500, inner_radius=80,
              size=None, angular_width=30, soft=False,
              phase_is_relative_to_wedge=True):
    """Will return an array of 2 * radius x 2 * radius containing a
    checkerboard wedge of given width, given checker frequency and phase"""

    if size is None:
        size = 2 * outer_radius

    half_size = size / 2

    wedge_cartesian_coords = np.mgrid[-half_size:half_size,
                                      -half_size:half_size]

    radii = np.sqrt((wedge_cartesian_coords ** 2).sum(axis=0))
    angles = np.arctan2(*wedge_cartesian_coords[::-1]) + np.pi

    the_phase = checker_phase / 180. * np.pi
    if phase_is_relative_to_wedge:
        the_phase += angular_position / 180. * np.pi

    raw_angular_checker = np.cos((angles - the_phase) * 360. / angular_width *
                                 checker_cycles_angular)

    raw_radial_checker = np.cos(radii / (outer_radius - inner_radius) * 2 *
                                np.pi * checker_cycles_radial)

    radial_mask = (inner_radius <= radii) & (radii <= outer_radius)

    angular_mask = np.abs((angles / (2 * np.pi) -
                          (angular_position / 360.) + .5) % 1. -
                          .5) <= angular_width / 360. / 2.

    image = raw_angular_checker * raw_radial_checker * \
        radial_mask * angular_mask

    if not soft:
        return np.sign(image)

    return image


def get_ring(radial_position, checker_phase=0., checker_cycles_radial=2,
             checker_cycles_angular=30, radial_width=50, size=500, soft=False,
             phase_is_relative_to_ring=True):

    half_size = size / 2

    wedge_cartesian_coords = np.mgrid[-half_size:half_size,
                                      -half_size:half_size]

    radii = np.sqrt((wedge_cartesian_coords ** 2).sum(axis=0))
    angles = np.arctan2(*wedge_cartesian_coords[::-1]) + np.pi

    the_phase = checker_phase / 180. * np.pi

    raw_angular_checker = np.cos(
        angles * checker_cycles_angular)

    if phase_is_relative_to_ring:
        the_phase = (radial_position / radial_width *
                     2 * np.pi * checker_cycles_radial)

    raw_radial_checker = np.cos(radii / radial_width * 2 * np.pi *
                                checker_cycles_radial - the_phase)

    radial_mask = (radial_position <= radii) & (radii <=
                                                radial_position +
                                                radial_width)

    image = raw_angular_checker * raw_radial_checker * radial_mask

    if not soft:
        return np.sign(image)

    return image


def _preload_round(type="wedge", reverse=False, duration_seconds=32.,
                   frame_rate_hertz=20., flicker_hertz=10.,
                   wedge_angular_width=30., ring_radial_width=30., size=500):

    func_args = dict(checker_phase=0., size=size, soft=False)

    n_frames = duration_seconds * frame_rate_hertz
    frame_times = np.arange(n_frames) / frame_rate_hertz
    if type == "wedge":
        stimfunc = get_wedge
        step = 360. / n_frames
        func_args["checker_cycles_radial"] = 10
        func_args["checker_cycles_angular"] = 2.5
        func_args["angular_width"] = wedge_angular_width
        func_args["inner_radius"] = 5.
        func_args["outer_radius"] = size / 2.

    elif type == "ring":
        stimfunc = get_ring
        max_radius = float(size) / 2 - ring_radial_width
        step = max_radius / n_frames
        func_args["checker_cycles_radial"] = 2.5
        func_args["checker_cycles_angular"] = 30
        func_args["radial_width"] = ring_radial_width
    else:
        raise ValueError("type must be 'wedge' or 'ring'")

    r = -1 if reverse else 1

    steps = np.arange(n_frames) * step
    flicker_sign = (((frame_times * flicker_hertz) % 2) > 1) * 2. - 1

    frames = [(stimfunc(d, **func_args) * f).astype('int8')
              for d, f in zip(steps[::r], flicker_sign)]

    return frames


def load_images(retino_type, direction):

    if direction == 'anticlockwise':
        reverse = False
    elif direction == 'clockwise':
        reverse = True
    else:
        raise ValueError('direction must be clockwise or anticlockwise')

    folder = os.environ.get('RETINO_DATA', '.')

    filename = "retino_{rtype}.npz".format(rtype=retino_type)

    rev = -1 if reverse else 1

    try:
        data = np.load(os.path.join(folder, filename))['data']
    except ValueError:
        print("Please first run retinoto.py --precalculate")
        return False
    return list(data[::rev]) * 10


def present(window, stimulus_list, fixation_callback=None, frame_hertz=20.):

    n_frames = len(stimulus_list)

    clock = core.Clock()
    stim_container = visual.ImageStim(window, size=(600, 600), units="pix",
                                      autoLog=False)

    shown_frame = -1
    shown_frames = []
    shown_times = []
    empty_loops = []
    empty_loop = 0

    while True:
        if "escape" in event.getKeys(["escape"]):
            break
        t = clock.getTime()
        current_frame = int(t * frame_hertz)
        # print current_frame, t
        if current_frame > n_frames - 1:
            break
        if current_frame > shown_frame:
            stim_container.setImage(stimulus_list[current_frame])
            stim_container.draw()
            if fixation_callback is not None:
                # import IPython
                # IPython.embed()
                fixation_callback(window, t)
            window.flip()
            shown_frame = current_frame
            shown_frames.append(shown_frame)
            shown_times.append(t)
            empty_loops.append(empty_loop)
            empty_loop = 0
        else:
            empty_loop += 1
    return shown_times, shown_frames, empty_loops


def get_retino_fixation(run):
    import pandas
    from utils import colors as color_dict
    from utils import get_fixation_cross_presenter
    df = pandas.read_csv("retino_fixation_%d.csv" % run)

    times = df['times'].values
    colors = df['colors'].values
    count = dict([(c, 0) for c in np.unique(colors)])

    for c in colors:
        count[c] = count[c] + 1
    pref_color = None
    pref_presence = 0
    for k, v in count.items():
        if v > pref_presence:
            pref_presence = v
            pref_color = k

    color_vals = [color_dict[c] for c in colors]

    return get_fixation_cross_presenter(zip(color_vals, times)), pref_color

# %%
color_button_correspondence = dict(
    red='b', green='y', blue='g', yellow='r',
    b='red', y='green', g='blue', r='yellow')

translation = dict(red='rouge', green='vert', blue='bleu', yellow='jaune')

if __name__ == "__main__":

    import os
    import imp
    utils = imp.load_source('utils', os.pardir + '/utils.py')
    from utils import show_init_screen, quiz

    # Create log files folder
    path_log = os.path.join(os.getcwd(), 'log_files/')
    if not os.path.exists(path_log):
        os.makedirs(path_log)

    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('number', nargs='*')
    parser.add_argument('--precalculate', action='store_true')
    args = parser.parse_args()

    number = int(args.number[0]) if args.number else None
    precalculate = args.precalculate

    if precalculate:
        print("Precalculating...")
        folder = os.environ.get('RETINO_DATA', '.')
        for retino_type in ['wedge', 'ring']:
            filename = "retino_{rtype}.npz".format(rtype=retino_type)
            print(filename)
            one_round = _preload_round(retino_type, reverse=False)
            np.savez(os.path.join(folder, filename), data=one_round)
            del one_round

        print("Done.")
    else:
        if number in [2, 4, 6, 8]:
            direction = 'clockwise'
        elif number in [1, 3, 5, 7]:
            direction = 'anticlockwise'
        else:
            raise Exception("expect 1, 2, 3, 4, 5, 6, 7, 8 as argument")

        if number in [1, 2, 5, 6]:
            retino_type = "wedge"
        elif number in [3, 4, 7, 8]:
            retino_type = "ring"
        fixation_callback, pref_color = get_retino_fixation(number)

        window = visual.Window(fullscr=True)
        window.mouseVisible = False
        show_init_screen(
            window, u"Chargement... \n", wait_key=None, with_fixation=False)
        images = load_images(retino_type, direction)
        show_init_screen(
            window, u"Chargement TERMIN\u00C9.\n", wait_key="space",
            with_fixation=False)
        show_init_screen(
            window,
            u" Lors de cette exp\u00E9rience, fixez la croix centrale.\n"
            u"             La croix changera de couleur.\n\n"
            u"D\u00E9terminez quelle couleur a été pr\u00E9sent\u00E9e\n"
            u"                       le plus longtemps.",
            wait_key="space", with_fixation=False)
        if show_init_screen(window, "", wait_key="t"):
            shown_times, shown_frames, empty_loops = present(
                window, images, fixation_callback=fixation_callback)
            show_init_screen(window, "", wait_key=None)
            clock = core.Clock()
            np.savez(path_log + 'log_retino_{stamp}.npz'.format(
                     stamp=time.strftime('%Y%m%d%H%M%S')),
                     times=shown_times, frames=shown_frames,
                     empty_loops=empty_loops)
            while clock.getTime() < 10.:
                keys = event.getKeys(('escape',))
                if keys:
                    break
            # Clear all keyboard events from the buffer
            keys = event.clearEvents(eventType='keyboard')
            # Quiz display
            pt_ans = quiz(window,
                          u"     Quelle couleur a \u00E9t\u00E9 "
                          u"pr\u00E9sent\u00E9e\n"
                          u"               le plus longtemps?\n\n"
                          u"Appuyez sur le bouton correspondant:",
                          u"rouge - pouce", u"vert - index", u"bleu - majeur",
                          u"jaune - annulaire",
                          pref_color, color_button_correspondence[pref_color],
                          error_message=u"Non, c'\u00E9tait           .",
                          wrong_feedback=u"%s" % translation[pref_color])
        window.close()
        # Create log file with participant's answer
        path_output = os.path.join(os.getcwd(), path_log,
                                   'pt_answer_%s_{stamp}.txt'.format(
                                   stamp=time.strftime('%Y%m%d%H%M%S')) %
                                   number)
        answer_log = open(path_output, "w")
        answer_log.write("Correct answer: " +
                         color_button_correspondence[pref_color])
        if str(pt_ans[0]) == 'escape':
            answer_log.write("\nParticipant's answer: None\n")
        else:
            answer_log.write("\nParticipant's answer: " + str(pt_ans[0]) +
                             '\n')
        answer_log.close()
