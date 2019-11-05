import numpy as np
from psychopy import core, visual, event
from utils import show_fixation_cross


def get_wedge(angular_position,
              checker_phase=0.,
              checker_cycles_radial=10, 
              checker_cycles_angular=2.5, 
              outer_radius=500,
              inner_radius=80,
              size=None, 
              angular_width=30,
              soft=False,
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

    raw_angular_checker = np.cos(
        (angles - the_phase) * 
        360. / angular_width * 
        checker_cycles_angular)

    raw_radial_checker = np.cos(radii / (outer_radius - inner_radius) * 
                                2 * np.pi * 
                                checker_cycles_radial)

    radial_mask = (inner_radius <= radii) & (radii <= outer_radius)

    angular_mask = np.abs(
        (angles / (2 * np.pi) - (angular_position / 360.) + .5) % 1. 
        - .5) <= angular_width / 360. / 2.

    image = raw_angular_checker * raw_radial_checker * \
        radial_mask * angular_mask

    if not soft:
        return np.sign(image)

    return image


def get_ring(radial_position,
             checker_phase=0.,
             checker_cycles_radial=2, 
             checker_cycles_angular=30, 
             radial_width=50,
             size=500, 
             soft=False,
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

    raw_radial_checker = np.cos(radii / radial_width * 
                                2 * np.pi * 
                                checker_cycles_radial - the_phase)

    radial_mask = (radial_position <= radii) & (radii <=
                                                radial_position +
                                                radial_width)

    image = raw_angular_checker * raw_radial_checker * radial_mask

    if not soft:
        return np.sign(image)

    return image



# def retino_wedge_iterator(period_seconds=32, flicker_hertz=5,
#                     n_rounds=2,
#                     frame_rate_hertz=10,
#                     inner_radius=40, outer_radius=250,
#                     checker_radial=10,
#                     checker_angular=2.5,
#                     angular_width=30,
#                     reverse=False,
#                           preload=True):

#     if reverse:
#         r = -1
#     else:
#         r = 1

#     n_degrees_total = 360. * n_rounds
#     n_frames_total = n_rounds * period_seconds * frame_rate_hertz

#     deg_per_frame = n_degrees_total / n_frames_total

#     frame_degs = np.arange(n_frames_total) * deg_per_frame
#     frame_times = np.arange(n_frames_total) / float(frame_rate_hertz)

#     flicker_sign = (((frame_times * flicker_hertz) % 2) > 1) * 2. - 1
#     if preload:
#         all_frames = [
#             (get_wedge(r * d,
#                       inner_radius=inner_radius,
#                       outer_radius=outer_radius,
#                       checker_cycles_radial=checker_radial,
#                       checker_cycles_angular=checker_angular,
#                       angular_width=angular_width), f, t)
#             for d, t, f in zip(frame_degs, frame_times, flicker_sign)]
#         # import IPython
#         # IPython.embed()
#         for image, f, t in all_frames:
#             yield image * f, t
#         return

#     for d, t, f in zip(frame_degs, frame_times, flicker_sign):
#         image = get_wedge(r * d,
#                           inner_radius=inner_radius,
#                           outer_radius=outer_radius,
#                           checker_cycles_radial=checker_radial,
#                           checker_cycles_angular=checker_angular,
#                           angular_width=angular_width)
#         yield image * f, t


# def retino_ring_iterator(period_seconds=32, flicker_hertz=5,
#                     n_rounds=2,
#                     frame_rate_hertz=10,
#                     radial_width=30,
#                     size=500,
#                     checker_radial=2.5,
#                     checker_angular=30,
#                     reverse=False):

#     r = -1 if reverse else 1

#     r_step = 1. / (period_seconds * frame_rate_hertz)

#     total_frames = n_rounds * period_seconds * frame_rate_hertz

#     rs = (np.arange(total_frames) * r_step) % 1.
#     frame_times = np.arange(total_frames) / float(frame_rate_hertz)
#     flicker_sign = (((frame_times * flicker_hertz) % 2) > 1) * 2. - 1
#     max_radius = size / 2 - radial_width

#     # import IPython
#     # IPython.embed()

#     for r, t, f in zip(rs[::r], frame_times, flicker_sign):
#         image = get_ring(r * max_radius,
#                          radial_width=radial_width,
#                          size=size,
#                          checker_cycles_radial=checker_radial,
#                          checker_cycles_angular=checker_angular)
#         yield image * f, t


# class StimBuffer(object):
#     """Takes a stimulus iterator and precaches a certain amount of images"""

#     def __init__(self, stim_iterator, buffer_size=300):
#         self.stim_iterator = stim_iterator
#         self.buffer_size = buffer_size

#     def init_buffer(self):
#         self.stim_iterator_ = iter(self.stim_iterator)
#         self.buffer_ = []
#         self.times = []
#         self.skipped = []
#         for i in range(self.buffer_size):
#             try:
#                 image, timing = next(self.stim_iterator_)
#                 self.buffer_.append(image)
#                 self.times.append(timing)
#             except StopIteration:
#                 break

#     def fetch(self, ):
#         pass



# def show_retino_iterator(window, iterator):


#     clock = core.Clock()
#     true_timings = []

#     active_index = -1

#     stim_container = visual.ImageStim(window, size=(500, 500), units='pix',
#                                       autoLog=False)

#     for i, (image, timing) in enumerate(iterator):
#         while True:
#             if 'escape' in event.getKeys(['escape']):
#                 return
#             t = clock.getTime()
#             if (t >= timing) and (active_index < i):
#                 true_timings.append((t, timing))
#                 stim_container.setImage(image)
#                 stim_container.draw()
#                 show_fixation_cross(window)
#                 window.flip()
#                 active_index = i
#                 break
#     return true_timings


def _preload_round(type="wedge", reverse=False,
                   duration_seconds=32.,
                   frame_rate_hertz=30.,
                   flicker_hertz=1.,
                   wedge_angular_width=30.,
                   ring_radial_width=30.,
                   size=500):
    """
    Specifies the type of movement: wedge (anti-clock,
    clock) and ring(expanding, contracting):
    duration: time per round
    frame_rate: no. images/s
    flicker_hertz: how many times black and white changes/s
    wedge_angular_width: how much angle it is covered by the width of the wedge (degrees)
    ring_radial_width: width of the ring in no. of pixels
    size: images' size, i.e. no. of pixels in x and y direction
    """
    func_args = dict(
              checker_phase=0.,
              size=size, 
              soft=False
              )

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

    frames = [stimfunc(d, **func_args) * f
              for d, f in zip(steps[::r], flicker_sign)]

    return frames


def preload_images(type="wedge", direction="clockwise",
                   duration_seconds=32.,
                   frame_rate_hertz=20.,
                   n_rounds=10,
                   flicker_hertz=5.,
                   wedge_angular_width=30,
                   ring_radial_width=30,
                   size=500,
                   ):
    """
    It gives a list of all the images that will be presented.
    """

    one_round = list(_preload_round(type, direction,
                                    duration_seconds=duration_seconds,
                                    frame_rate_hertz=frame_rate_hertz,
                                    flicker_hertz=flicker_hertz,
                                    wedge_angular_width=wedge_angular_width,
                                    ring_radial_width=ring_radial_width,
                                    size=size))
    all_rounds = one_round * n_rounds
    return all_rounds


def present(window, stimulus_list, fixation_callback=None, frame_hertz=30.):
    """
    It presents the stimulus.
    window parameter is a psychopy window, and the stimulus list comes from
    the previous function, i.e., preload_images().
    """
    n_frames = len(stimulus_list)

    clock = core.Clock()
    stim_container = visual.ImageStim(window, size=(600, 600),
                                      units="pix", autoLog=False)

    shown_frame = -1
    shown_frames = []
    shown_times = []
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
    return shown_times, shown_frames


def get_retino_fixation(run):
    import pandas
    from utils import colors as color_dict
    from utils import get_fixation_cross_presenter
    df = pandas.load("retino_fixation_%d.csv" % run)

    times = df['times'].values
    colors = df['colors'].values
    count = dict([(c, 0) for c in np.unique(colors)])

    # get majority color. Horrible code. Fast hack. pandas can do it ootb
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


color_button_correspondence = dict(
    red='b', green='y', blue='g', yellow='r',
    b='red', y='green', g='blue', r='yellow')

translation = dict(red='rouge', green='vert', blue='bleu', yellow='jaune')

if __name__ == "__main__":
    # import matplotlib.pyplot as plt
    # plt.figure()

    # plt.subplot(2, 2, 1)
    # plt.imshow(get_wedge(0.), interpolation='nearest')
    # plt.gray()
    # plt.subplot(2, 2, 2)
    # plt.imshow(get_wedge(90.), interpolation='nearest')
    # plt.subplot(2, 2, 3)
    # plt.imshow(get_wedge(180.), interpolation='nearest')
    # plt.subplot(2, 2, 4)
    # plt.imshow(get_wedge(270.), interpolation='nearest')

    # plt.show()

    # import matplotlib.pyplot as plt
    # plt.figure()

    # plt.subplot(2, 2, 1)
    # plt.imshow(get_ring(0.), interpolation='nearest')
    # plt.gray()
    # plt.subplot(2, 2, 2)
    # plt.imshow(get_ring(50.), interpolation='nearest')
    # plt.subplot(2, 2, 3)
    # plt.imshow(get_ring(100.), interpolation='nearest')
    # plt.subplot(2, 2, 4)
    # plt.imshow(get_ring(200.), interpolation='nearest')

    # plt.show()

    # window = visual.Window(fullscr=False)
    # it = retino_ring_iterator(reverse=False)

    # true_timings = show_retino_iterator(window, it)
    # window.close()

    from utils import show_init_screen, quiz
    from argparse import ArgumentParser
    parser = ArgumentParser()

    parser.add_argument('number')
    args = parser.parse_args()

    number = int(args.number)

    if number in [2, 4, 6, 8]:
        reverse = True
    elif number in [1, 3, 5, 7]:
        reverse = False
    else:
        raise Exception("expect 1, 2, 3, 4, 5, 6, 7, 8 as argument")

    if number in [1, 2, 5, 6]:
        retino_type = "wedge"
    elif number in [3, 4, 7, 8]:
        retino_type = "ring"
    fixation_callback, pref_color = get_retino_fixation(number)

    window = visual.Window(fullscr=True)
    show_init_screen(window, u"Chargement \n"
                        u"Lors de cette exp\u00E9rience, fixer le point central.\n"
                        u"Le point changera de couleur. D\u00E9terminer"
                        u" laquelle \n"
                        u"des couleurs est pr\u00E9sent\u00E9e le plus de "
                        u"temps.", wait_key=None)
        # true_timings = show_retino_iterator(window, iterator)
    images = preload_images(retino_type, reverse, size=600)
    show_init_screen(window, u"Chargement TERMINE.\n"
                     u"Lors de cette exp\u00E9rience, fixer le point central.\n"
                     u"Le point changera de couleur. D\u00E9terminer"
                     u" laquelle \n"
                     u"des couleurs est pr\u00E9sent\u00E9e le plus de "
                     u"temps.", wait_key="space")
    if show_init_screen(window, "", wait_key="t"):
        shown_times, shown_frames = present(
            window, images, fixation_callback=fixation_callback)
        show_init_screen(window, "", wait_key=None)
        clock = core.Clock()
        while clock.getTime() < 10.:
            pass
        quiz(window, u"Quelle couleur a \u00E9t\u00E9 pr\u00E9sent\u00E9e "
             u"le plus? Appuyez sur le point correspondant:\n"
             u"rouge - pouce\nvert - index\nbleu - majeur\njaune - annuaire",
             color_button_correspondence[pref_color],
             wrong_feedback=u"Non, c'\u00E9tait %s" % translation[pref_color])


    window.close()
