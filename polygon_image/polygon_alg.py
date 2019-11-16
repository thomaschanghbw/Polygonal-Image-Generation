from PIL import Image, ImageDraw
from constants import *
from triangle import Triangle
from display import Display
from multiprocessing import Process, Manager

import numpy as np
import polylogger
import time

def init_image(target_image):
    """
    Creates a blank image based on the target_image. The image background is the average color of the target.
    :param target_image:
    :return:
    """
    single_pix_image_avg = target_image.resize(SINGLE_PIXEL_DIM, Image.ANTIALIAS)
    avg_image_color = single_pix_image_avg.getpixel((0,0))

    return Image.new('RGBA', target_image.size, avg_image_color)

def apply_triangle(to, triangle, target_im):
    """
    Draws a triangle onto the image, filling in the triangle with the average color for that region of the image
    :param to:
    :param triangle:
    :param target_im:
    :return:
    """
    img = to
    temp_img = Image.new('RGBA', img.size)
    temp_img_draw = ImageDraw.Draw(temp_img)

    v0, v1, v2 = triangle.v0, triangle.v1, triangle.v2

    min_x = min(v0[0], v1[0], v2[0])
    min_y = min(v0[1], v1[1], v2[1])
    max_x = max(v0[0], v1[0], v2[0])
    max_y = max(v0[1], v1[1], v2[1])
    # Calculate color
    num_pts_in_triangle = 0
    rgb_sums = np.zeros(3).astype(int)
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            pt = (x, y)
            if triangle.contains_pt(pt):
                num_pts_in_triangle += 1
                rgb_sums[0] += target_im.getpixel(pt)[0]
                rgb_sums[1] += target_im.getpixel(pt)[1]
                rgb_sums[2] += target_im.getpixel(pt)[2]

    if num_pts_in_triangle:
        avg_color_in_triangle = rgb_sums // num_pts_in_triangle
        # TODO: tune this alpha value, maybe make it change dynamically
        temp_img_draw.polygon((v0,v1,v2), fill=(avg_color_in_triangle[0], avg_color_in_triangle[1], avg_color_in_triangle[2], 175))
        img.alpha_composite(temp_img)

def generate_best_candidate_worker(target_image, cur_image, candidates_per_it, prev_loss, result_pool):
    # start = time.time()

    im_width, im_height = target_image.size
    target_im_np = np.asarray(target_image)
    has_found_improvement = False
    best_loss, best_im = np.inf, None
    # print("Time to reach loop: {}", time.time() - start)
    for _ in range(candidates_per_it):
        # startstart = time.time()
        cand_image = cur_image.copy()
        cand_triangle = Triangle.get_random_triangle(im_width, im_height)
        apply_triangle(to=cand_image, triangle=cand_triangle, target_im=target_image)

        cur_loss = np.linalg.norm(target_im_np - np.asarray(cand_image))
        if cur_loss < best_loss:
            best_loss = cur_loss
            best_im = cand_image
            if cur_loss < prev_loss:
                has_found_improvement = True
        # print("Time for run " + str(_) +": {}", time.time() - startstart)

    if has_found_improvement:
        result_pool.append((best_loss, best_im))

    # print("Total thread time: {}", time.time() - start)

def generate_best_candidate(target_image, cur_image, candidates_per_it, prev_loss, threads_enabled):
    has_found_improvement = False
    best_loss, best_im = np.inf, None

    start = time.time()
    # Generate AT LEAST candidates_per_it
    # If none of them improve the previous image, then generate another candidates_per_it candidates
    while not has_found_improvement:
        if threads_enabled:
            # TODO: don't hard code number of threads?
            num_threads = 10
            threads = []
            manager = Manager()
            result_pool = manager.list()
            for i in range(num_threads):
                t = Process(target=generate_best_candidate_worker,
                                     args=(target_image, cur_image, candidates_per_it // num_threads, prev_loss, result_pool,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            # result_pool holds all candidates that improve over the previous image
            if result_pool:
                has_found_improvement = True

                best_loss, best_im = result_pool[0]
                for loss, im in result_pool:
                    if loss < best_loss:
                        best_loss = loss
                        best_im = im
        else:
            result_pool = []
            generate_best_candidate_worker(target_image, cur_image, candidates_per_it, prev_loss, result_pool)
            if result_pool:
                has_found_improvement = True
                best_loss, best_im = result_pool[0]

    print("Time to find candidate: {}".format(time.time() - start))
    return best_im, best_loss

# def generate_best_candidate(target_image, cur_image, candidates_per_it, prev_loss, thread_enabled):
#     im_width, im_height = target_image.size
#     target_im_np = np.asarray(target_image)
#     has_found_improvement = False
#     best_loss, best_im = np.inf, None
#
#     # TODO: refactor to allow arbitrary shapes
#     while not has_found_improvement:
#         for _ in range(candidates_per_it):
#             cand_image = cur_image.copy()
#             cand_triangle = Triangle.get_random_triangle(im_width, im_height)
#             apply_triangle(to=cand_image, triangle=cand_triangle, target_im=target_image)
#
#             cur_loss = np.linalg.norm(target_im_np - np.asarray(cand_image))
#             if cur_loss < best_loss:
#                 best_loss = cur_loss
#                 best_im = cand_image
#
#                 if cur_loss < prev_loss:
#                     has_found_improvement = True
#
#     return best_im, best_loss


def run_alg(target_image, candidates_per_it, threads_enabled):
    display = Display(target_image)
    logger = polylogger.Logger()
    starttime = time.time()

    cur_image = init_image(target_image)
    loss = np.inf

    # Currently hard coded to run for 100 iterations
    for i in range(100):
        cur_image, loss = generate_best_candidate(target_image, cur_image, candidates_per_it, loss, threads_enabled)
        logger.log(cur_image, loss, time.time() - starttime, i)
        display.show(cur_image, "Number of shapes: {}. Loss: {:.4f}".format(i, loss))
    # while True:
    #     new_image = generate_best_candidate(target_image, cur_image, candidates_per_it)
