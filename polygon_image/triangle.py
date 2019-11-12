import random

class Triangle:
    def __init__(self, v0, v1, v2):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.area = 0.5 * (-self.v1[1]*self.v2[0] + self.v0[1]*(-self.v1[0]+self.v2[0])
                           + self.v0[0]*(self.v1[1]-self.v2[1]) + self.v1[0]*self.v2[1])

    def sign(self, p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    def contains_pt(self, pt):
        """
        a = ((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
        b = ((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 - y3))
        c = 1 - a - b

        Area = 0.5 *(-p1y*p2x + p0y*(-p1x + p2x) + p0x*(p1y - p2y) + p1x*p2y);
        s = 1/(2*Area)*(p0y*p2x - p0x*p2y + (p2y - p0y)*px + (p0x - p2x)*py);
        t = 1/(2*Area)*(p0x*p1y - p0y*p1x + (p0y - p1y)*px + (p1x - p0x)*py);
        """
        # s = 1 / (2*self.area) * (self.v0[1] * self.v2[0] - self.v0[0]*self.v2[1]
        #                      + (self.v2[1] - self.v0[1]) * pt[0] + (self.v0[0] - self.v2[0]) * pt[1])
        # t = 1 / (2 * self.area) * (self.v0[0] * self.v1[1] - self.v0[1] * self.v1[0]
        #                            + (self.v0[1] - self.v1[1]) * pt[0] + (self.v1[0] - self.v0[0]) * pt[1])
        # return s >= 0

        d1 = self.sign(pt, self.v0, self.v1)
        d2 = self.sign(pt, self.v1, self.v2)
        d3 = self.sign(pt, self.v2, self.v0)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    @staticmethod
    def get_random_triangle(img_width, img_height):
        v0 = (random.randint(0, img_width), random.randint(0, img_height))
        v1 = (random.randint(0, img_width), random.randint(0, img_height))
        v2 = (random.randint(0, img_width), random.randint(0, img_height))
        return Triangle(v0, v1, v2)