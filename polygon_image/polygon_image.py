from PIL import Image, ImageDraw

import argparser as argparser
import polygon_alg



def main():
    args = argparser.get_parsed_args()
    candidates_per_it = args.candidates_per_iteration

    # TODO: make configurable
    target_image = Image.open("../mona_lisa.png")

    polygon_alg.run_alg(target_image, candidates_per_it, args.threads_enabled)
    # cur_image = util.init_image(target_image)
    # cur_image.show()


if __name__ == "__main__":
    main()
