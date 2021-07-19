import numpy as np
import random as rnd
import math
import pygame
from pygame.draw import *

N = 200
A = []
beta = 2
h = +0.03
block_size = 5
Full_time = 0


#Инициализация массива

for i in range(N):
    arr = []
    for i in range(N):
        curr = -1
        if rnd.random() > 0.5:
            curr = 1
        arr.append(curr)
    A.append(arr)
A = np.array(A)
print(A)


def delta_E(i_curr, j_curr, A_curr):
    """

    Расчёт изменения энергии

    """
    summ = 0
    X = [(i_curr+1)%N, (i_curr-1)%N, i_curr]
    Y = [(j_curr+1)%N, (j_curr-1)%N, j_curr]
    for x in X:
        for y in Y:
            if ((x-i_curr)*(y-j_curr)==0) and ((y-j_curr)**2+(x-i_curr)**2!=0):
                summ += A_curr[x, y]
    delta = 2*A_curr[i_curr, j_curr]*(h+summ)
    return delta

def change(A_curr):
    """

    изменение направления всех спинов(по очереди)

    """

    for n in range(int((N*N))):
        i = rnd.randint(0, N - 1)
        j = rnd.randint(0, N - 1)
        delta_curr = delta_E(i, j, A_curr)
        if (delta_curr < 0):
            A_curr[i, j] = -A_curr[i, j]
        else:
            if rnd.random() < math.exp((-delta_curr) / (beta)):
                A_curr[i, j] = -A_curr[i, j]
    return A_curr

def draw(A_curr):
    """

    Отрисовка решётки Изинга

    """
    pygame.init()

    FPS = 100
    WHT = (255, 255, 255)
    BLC = (0, 0, 0)
    RED = (255, 0, 0)
    LBL = (125, 196, 250)
    screen = pygame.display.set_mode((int(N *block_size), int(N*block_size)))
    screen.fill(WHT)
    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    for i in range(N):
        for j in range(N):
            if A_curr[i, j] > 0:
                rect(screen, BLC, (i*block_size, j*block_size, block_size, block_size))

    while not finished:
        clock.tick(FPS)
        for i in range(N):
            for j in range(N):
                if A_curr[i, j] > 0:
                    rect(screen, BLC, (i * block_size, j * block_size, block_size, block_size))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    finished = True
    pygame.quit()

def draw_timer(A_curr):
    """

    Отрисовка решётки Изинга

    """
    pygame.init()

    FPS = 100
    WHT = (255, 255, 255)
    BLC = (0, 0, 0)
    RED = (255, 0, 0)
    LBL = (125, 196, 250)
    screen = pygame.display.set_mode((int(N *block_size), int(N*block_size)))
    screen.fill(WHT)
    pygame.display.update()
    clock = pygame.time.Clock()
    timer = 0
    A111 = A_curr
    finished = False
    for i in range(N):
        for j in range(N):
            if A111[i, j] > 0:
                rect(screen, BLC, (i*block_size, j*block_size, block_size, block_size))

    while not finished:
        clock.tick(FPS)
        screen.fill(WHT)
        for i in range(N):
            for j in range(N):
                if A111[i, j] > 0:
                    rect(screen, BLC, (i * block_size, j * block_size, block_size, block_size))
        pygame.display.update()
        timer+=1
        if(timer>Full_time):
            A111 = change(A111)
            timer = 0
    pygame.quit()

draw_timer(A)

while(True):
    A1 = change(A)
    draw(A1)