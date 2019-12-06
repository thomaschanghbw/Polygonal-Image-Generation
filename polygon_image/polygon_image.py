from PIL import Image, ImageDraw

import argparser as argparser
import polygon_alg



def main():
    args = argparser.get_parsed_args()
    candidates_per_it = args.candidates_per_iteration

    # TODO: make configurable
    target_image = Image.open("../mona_lisa.png")

    if args.do_resize:
        target_width, target_height = target_image.size
        resized_width = args.resized_width
        resize_proportion = resized_width / target_width
        resized_height = int(resize_proportion * target_height)
        target_image = target_image.resize((resized_width, resized_height))


    # polygon_alg.run_alg(target_image, candidates_per_it, args.threads_enabled)
    polygon_alg.run_alg(target_image, candidates_per_it, args.threads_enabled, args.show_display)


    # cur_image = util.init_image(target_image)
    # cur_image.show()


if __name__ == "__main__":
    main()
