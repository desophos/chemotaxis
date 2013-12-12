SCREEN_SIZE = 400

def toPygame(xy):
    """ convert pymunk coordinates to pygame coordinates """
    return xy[0], SCREEN_SIZE-xy[1]