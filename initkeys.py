import pygame
import pickle
import os
from constants import RSRC_PATH

key_dic = {
    "p1" : {
        "UP" : pygame.K_w,
        "DOWN" : pygame.K_s,
        "LEFT" : pygame.K_a,
        "RIGHT" : pygame.K_d,
        "BOMB": pygame.K_SPACE
    },
    "p2" : {
        "UP" : pygame.K_UP,
        "DOWN" : pygame.K_DOWN,
        "LEFT" : pygame.K_LEFT,
        "RIGHT" : pygame.K_RIGHT,
        "BOMB": pygame.K_RETURN
    }
}


data_dic={
    "p1": "Aunt May",
    "p2": "Uncle Ben",
    "timer": 45,
    "rounds": 2}

def reset():
    with open(os.path.join(RSRC_PATH, 'keycfg.pkl'), 'wb') as f:
        pickle.dump(key_dic, f)
    return key_dic

def reset2():
    with open(os.path.join(RSRC_PATH, 'datacfg.pkl'), 'wb') as f:
        pickle.dump(data_dic, f)
    return data_dic


if __name__ == '__main__':
    reset()
    reset2()