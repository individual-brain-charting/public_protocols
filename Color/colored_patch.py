"""
Create colored  and iso-luminant patches.
Naive implementation, that does not take into account gamma corrections etc.
the image size and number of required samples can be set in the main function.

Author: Bertrand Thirion, 2015
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import math


def cluster(xy, n_circles):
    from sklearn.cluster import k_means
    pos, label, _ = k_means(xy, n_clusters=n_circles, max_iter=3)
    # find the max distance
    max_sq_dist = np.max(np.sum((xy - pos[label]) ** 2, 1))
    return pos, max_sq_dist


def iso_luminant_colormap():
    # generate a random iso-luminant color map
    import colorsys
    rand1 = np.arange(n_circles) * 1. / n_circles
    rand2 = np.arange(n_circles) * 1. / n_circles
    np.random.shuffle(rand1)
    np.random.shuffle(rand2)
    color_map = np.array([colorsys.hls_to_rgb(h, .5, s)
                          for h, s in zip(rand1, rand2)])
    return color_map


def random_label(xy, shape, pos, max_sq_dist):
    x, y = xy.T
    n_circles = pos.shape[0]
    label = - np.ones_like(x, np.int16)
    rand_label = np.arange(n_circles)
    np.random.shuffle(rand_label)
    for i in range(n_circles):
        j, k = rand_label[i], rand_label[rand_label[i]]
        label[(x - pos[j, 0]) ** 2 + (y - pos[j, 1]) ** 2 <= max_sq_dist] = k
    label = label.reshape((shape[1], shape[0]))
    return label


def make_figure(label, stim_size, chromatic=False, path=None):
    px = 1/plt.rcParams['figure.dpi']  # pixel in inches
    plt.figure(figsize=(stim_size[0]*px, stim_size[1]*px), facecolor='gray')
    if chromatic:
        color_label = color_map[label]
        plt.imshow(color_label)
    else:
        rand_label = np.linspace(0, 1, n_circles)
        plt.imshow(rand_label[label], cmap='gray', vmin=-.3, vmax=1.3)

    plt.axis('tight')
    plt.axis('off')
    if path is not None:
        plt.savefig(path)


def visual_angles_to_pixels(ang_ecc=2.58, ang_ele=2, ang_stim=1.72,
							screen_xy=(0.6,0.45), res_xy=(1920,1080),
							distance=0.89):

	pix_ecc = (math.tan((ang_ecc/2)*(math.pi/180))*distance*res_xy[0])/(screen_xy[0]/2)
	pix_ele = (math.tan((ang_ele/2)*(math.pi/180))*distance*res_xy[1])/(screen_xy[1]/2)
	pix_stim_x = (math.tan((ang_stim/2)*(math.pi/180))*distance*res_xy[0])/(screen_xy[0]/2)
	pix_stim_y = (math.tan((ang_stim/2)*(math.pi/180))*distance*res_xy[1])/(screen_xy[1]/2)

	return pix_ecc, pix_ele, pix_stim_x, pix_stim_y

if __name__ == '__main__':
    write_dir = 'tmp'
    if not os.path.exists(write_dir):
        os.mkdir(write_dir)

    n_samples = 10
    width, height, center_x, center_y = visual_angles_to_pixels(16, 16)
    stim_size = (int(width), int(height))
    n_circles = 20
    xy = np.array(np.meshgrid(np.arange(stim_size[0]), np.arange(stim_size[1]))).\
        reshape(2, stim_size[0] * stim_size[1]).T
    color_map = iso_luminant_colormap()
    pos, max_sq_dist = cluster(xy, n_circles)
    max_sq_dist *= 1.5
    np.random.seed([0])
    n_iter = 217
    for i in range(n_iter):
        label = random_label(xy, stim_size, pos, max_sq_dist)
        make_figure(label, stim_size, chromatic=False,
                    path=os.path.join(write_dir, 'achromatic_%03d.png' % i))
        make_figure(label, stim_size, chromatic=True,
                    path=os.path.join(write_dir, 'chromatic_%03d.png' % i))

    print("wrote output in directory % s" % write_dir)
