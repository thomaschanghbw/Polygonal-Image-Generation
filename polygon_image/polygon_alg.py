from PIL import Image, ImageDraw
from constants import *
from triangle import Triangle
from display import Display

import numpy as np
import polylogger
import time

def init_image(target_image):
    single_pix_image_avg = target_image.resize(SINGLE_PIXEL_DIM, Image.ANTIALIAS)
    avg_image_color = single_pix_image_avg.getpixel((0,0))

    return Image.new('RGBA', target_image.size, avg_image_color)

def apply_triangle(to, triangle, target_im):
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

def generate_best_candidate(target_image, cur_image, candidates_per_it, prev_loss):
    im_width, im_height = target_image.size
    target_im_np = np.asarray(target_image)
    has_found_improvement = False
    best_loss, best_im = np.inf, None

    # TODO: refactor to allow arbitrary shapes
    while not has_found_improvement:
        for _ in range(candidates_per_it):
            cand_image = cur_image.copy()
            cand_triangle = Triangle.get_random_triangle(im_width, im_height)
            apply_triangle(to=cand_image, triangle=cand_triangle, target_im=target_image)

            cur_loss = np.linalg.norm(target_im_np - np.asarray(cand_image))
            if cur_loss < best_loss:
                best_loss = cur_loss
                best_im = cand_image

                if cur_loss < prev_loss:
                    has_found_improvement = True

    return best_im, best_loss


def run_alg(target_image, candidates_per_it):
    display = Display(target_image)
    logger = polylogger.Logger()
    starttime = time.time()

    cur_image = init_image(target_image)
    loss = np.inf

    for i in range(100):
        cur_image, loss = generate_best_candidate(target_image, cur_image, candidates_per_it, loss)
        logger.log(cur_image, loss, time.time() - starttime, i)
        display.show(cur_image, "Number of shapes: {}. Loss: {:.4f}".format(i, loss))
    # while True:
    #     new_image = generate_best_candidate(target_image, cur_image, candidates_per_it)
