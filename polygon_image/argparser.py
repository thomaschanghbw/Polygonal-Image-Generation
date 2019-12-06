import argparse

def get_parsed_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--threads-enabled', type=bool, default=True,
                        help='Determines whether to use multi-threading optimizations')
    # parser.add_argument('--num-threads', type=int, default=100,
    #                     help='Sets the number of threads to use. Only valid if --threads-enabled=True')
    parser.add_argument('--candidates-per-iteration', type=int, default=10,
                        help='Determine how many candidate polygons to generate per iteration')
    parser.add_argument('--show-display', type=bool, default=True,
                        help='Show image during processing')
    parser.add_argument('--use-gpu', type=bool, default=False,
                        help='Use Gpu')
    parser.add_argument('--do-resize', type=bool, default=True,
                        help='Optimization: resize the image')
    parser.add_argument('--resized-width', type=int, default=180,
                        help='The width to resize the image to. Must be less than the input image size')


    args = parser.parse_args()

    return args