import numpy as np
# from psychopy import core
from psychopy import visual, event
import pandas
from sklearn.utils import check_random_state


colors = dict(red=(1, -1, -1), green=(-1, 1, -1), blue=(-1, -1, 1),
              yellow=(1, 1, -1))


def show_init_screen(window, text="Hello", wait_key="t", with_fixation=True):
    textbox = visual.TextStim(window, text, wrapWidth=600)
    textbox.draw()
    if with_fixation:
        show_fixation_cross(window, style='cross')
    window.flip()

    if wait_key is None:
        return True
    # wait for TTL
    while True:
        keys = event.getKeys([wait_key, 'escape'])
        if 'escape' in keys:
            return False
        if wait_key in keys:
            return True


def show_response_window(window, text='END', expected_keys=('a', 'b', 'c')):
    textbox = visual.TextStim(window, text)
    textbox.draw()
    window.flip()

    while True:
        keys = event.getKeys(['escape'] + list(expected_keys))
        if 'escape' in keys:
            return False
        else:
            return keys


def show_fixation_cross(window, size=20, color=(1., -1., -1.), style='point'):
    if style == 'point':
        rect = visual.ImageStim(window, size=size, units='pix', mask=None,
                                color=color)
        rect.draw()
    elif style == 'cross':
        rect1 = visual.ImageStim(window, size=(size, size / 3.), units="pix",
                                 color=color, mask=None)
        rect2 = visual.ImageStim(window, size=(size / 3., size), units="pix",
                                 color=color, mask=None)
        rect1.draw()
        rect2.draw()
    else:
        raise ValueError('style must be point or cross')


def get_fixation_cross_presenter(color_sequence, size=20):

    colors, times = zip(*color_sequence)
    times = np.array(times)

    def draw_fixation_cross(window, time):
        current_time_index = np.where(times <= time)[0].max()
        current_color = colors[current_time_index]
        rect1 = visual.ImageStim(window, size=(size, size / 3.), units="pix",
                                 color=current_color, mask=None)
        rect2 = visual.ImageStim(window, size=(size / 3., size), units="pix",
                                 color=current_color, mask=None)
        rect1.draw()
        rect2.draw()

    return draw_fixation_cross

mask_files = dict(
    circle='fixation_crosses/ci1.png',
    square='fixation_crosses/sq5.png',
    cross='fixation_crosses/cr3.png',
    star='fixation_crosses/ot2.png')


def get_fixation_cross_presenter_mondrian(mask_sequence):

    from PIL import Image
    masks = {k: ((np.array(Image.open(v))[:, :, 0] > 0) * 2 - 1).astype(int)
             for k, v in mask_files.items()}

    mask_names, times = zip(*mask_sequence)
    times = np.array(times)
    size = 10

    def draw_fixation_cross(window, time):
        current_time_index = np.where(times <= time)[0].max()
        current_mask = mask_names[current_time_index]
        rect = visual.ImageStim(window, size=size, units="pix",
                                color=(1., 1., 1.), mask=masks[current_mask])
        rect.draw()

    return draw_fixation_cross


def prepare_fixation_sequence(preference=0, preferential_percentage=34,
                              corpus=('red', 'green', 'blue', 'yellow'),
                              total_duration_seconds=320,
                              random_state=42):

    rng = check_random_state(random_state)

    remainder = (100 - preferential_percentage)

    remainder_indices = rng.permutation(100)[:remainder]
    color_repartition = rng.permutation(remainder) % 3 + 1

    indicator = np.zeros(100, dtype='int64')

    indicator[remainder_indices] = color_repartition

    corpus = np.roll(np.array(corpus), -preference)

    repartition = corpus[indicator]

    times = np.arange(100) * (total_duration_seconds / 100.)

    return repartition, times


def create_retino_fixation_times(run):
    fname = "retino_fixation_%d.csv" % run

    rng = check_random_state(run)

    preference = rng.randint(4)

    repartition, times = prepare_fixation_sequence(preference)

    df = pandas.DataFrame.from_dict(dict(colors=repartition, times=times))

    df.to_csv(fname)


def create_mondrian_fixation_times():
    fname = "color_fixation.csv"

    rng = check_random_state(0)

    preference = rng.randint(4)

    repartition, times = prepare_fixation_sequence(
        preference,
        corpus=('circle', 'square', 'cross', 'star'),
        total_duration_seconds=360)

    df = pandas.DataFrame.from_dict(dict(colors=repartition, times=times))

    df.to_csv(fname)


def quiz(window, question, opt_red, opt_green, opt_blue, opt_yellow,
         color_select, correct_answer, correct_feedback="CORRECT!",
         error_message="faux", wrong_feedback="faux",
         possible_answers=('b', 'y', 'g', 'r', 'comma')):

    text_box = visual.TextStim(window, text=question, pos=(0, 0.2),
                               height = 0.065)
    text_box_red = visual.TextStim(window, text=opt_red, pos=(0, -0.1),
                                   height = 0.065, color=colors['red'],
                                   colorSpace='rgb')
    text_box_green = visual.TextStim(window, text=opt_green,
                                     pos=(0, -0.2), height = 0.065,
                                     color=colors['green'], colorSpace='rgb')
    text_box_blue = visual.TextStim(window, text=opt_blue, pos=(0, -0.3),
                                    height = 0.065, color=colors['blue'],
                                    colorSpace='rgb')
    text_box_yellow = visual.TextStim(window, text=opt_yellow,
                                      pos=(0, -0.4), height = 0.065,
                                      color=colors['yellow'], colorSpace='rgb')
    text_box.draw()
    text_box_red.draw()
    text_box_green.draw()
    text_box_blue.draw()
    text_box_yellow.draw()
    window.flip()
    while True:
        keys = event.getKeys(('escape',) + possible_answers)
        answer = keys
        if keys:
            break
    if correct_answer in keys:
        text_box.setText(correct_feedback)
        text_box.draw()
        window.flip()
        while True:
            keys = event.getKeys(('space', 'escape'))
            if keys:
                return answer
    elif 'escape' in keys:
        return answer
    else:
        text_box.setText(error_message)
        text_box.setPos((0, 0))
        text_box_answ = visual.TextStim(window, text=wrong_feedback,
                                        pos=(0.11, 0), height = 0.065,
                                        color=colors[color_select],
                                        colorSpace='rgb')
        text_box.draw()
        text_box_answ.draw()
        window.flip()
        while True:
            keys = event.getKeys(('space', 'escape'))
            if keys:
                return answer

if __name__ == "__main__":
    # make retino fixations
    for i in range(1, 9):
        create_retino_fixation_times(i)

    create_mondrian_fixation_times()
