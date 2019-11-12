import argparse

def get_parsed_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--threads-enabled', type=bool, default=False,
                        help='Determines whether to use multi-threading optimizations')
    parser.add_argument('--num-threads', type=int, default=100,
                        help='Sets the number of threads to use. Only valid if --threads-enabled=True')
    parser.add_argument('--candidates-per-iteration', type=int, default=5,
                        help='Determine how many candidate polygons to generate per iteration')

    args = parser.parse_args()

    return args