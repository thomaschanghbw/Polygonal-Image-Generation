from constants import BASE_LOG_FILE

import os

class Logger:
    def __init__(self, save_img_per_num_iterations=25):
        self.iter_steps = save_img_per_num_iterations
        i = 0
        while os.path.exists(BASE_LOG_FILE % i):
            i += 1

        self.output_dir = BASE_LOG_FILE % i
        os.mkdir(self.output_dir)
        self.fh = open(self.output_dir + "log.log", "w")

    def log(self, img, loss, timestamp, iteration):
        log_string = "Loss: {:.4f}, iteration: {}, timestamp: {}\n"
        self.fh.write(log_string.format(loss, iteration, timestamp))

        if iteration % self.iter_steps == 0:
            print("Need to save")