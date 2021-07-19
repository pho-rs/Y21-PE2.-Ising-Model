import numpy as np
import random as rnd
import math
import matplotlib.pyplot as plt
import time
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from pygame.draw import *

time_per_size2 = 0.012*0.01

wrong_ansers = ["Неправильно", "Попробуй ещё раз", "Неправильно", "Попробуй ещё раз", "Неправильно", "Попробуй ещё раз",
                "Неправильно", "Попробуй ещё раз", "Неправильно", "Попробуй ещё раз", "Некорректный ввод",
                "Некорректный ввод", "Некорректный ввод", "Некорректный ввод", "Некорректный ввод", "Некорректный ввод",
                "Некорректный ввод", "Нет", "Нет", "Нет", "Нет", "Нет", "Бронза и забвение", "Глупости",
                "Я сейчас перестану работать", "Вон из сборной!", "Нет", "Press \"Ctrl+C\" to continue",
                "Пользовательская ошибка. Замените пользователя"]

def init_grid(n):
    A_in = []
    for i in range(n):
        arr = []
        for i in range(n):
            curr = -1
            if rnd.random() > 0.5:
                curr = 1
            arr.append(curr)
        A_in.append(arr)
    return np.array(A_in)


def delta_E(i_curr, j_curr, A_curr, h_curr):
    """

    Расчёт изменения энергии

    """
    summ = 0
    n_curr = A_curr.shape[0]
    X = [(i_curr+1)%n_curr, (i_curr-1)%n_curr, i_curr]
    Y = [(j_curr+1)%n_curr, (j_curr-1)%n_curr, j_curr]
    for x in X:
        for y in Y:
            if ((x-i_curr)*(y-j_curr)==0) and ((y-j_curr)**2+(x-i_curr)**2!=0):
                summ += A_curr[x, y]
    delta = 2*A_curr[i_curr, j_curr]*(h_curr+summ)
    return delta


def change(A_curr, h_curr, beta_curr):
    """

    изменение направления всех спинов(по очереди)

    """
    n_curr = A_curr.shape[0]
    for n in range(int((n_curr*n_curr))):
        i = rnd.randint(0, n_curr - 1)
        j = rnd.randint(0, n_curr - 1)
        delta_curr = delta_E(i, j, A_curr, h_curr)
        if (delta_curr < 0):
            A_curr[i, j] = -A_curr[i, j]
        else:
            if rnd.random() < math.exp((-delta_curr) / (beta_curr)):
                A_curr[i, j] = -A_curr[i, j]
    return A_curr


def draw(A_curr, block_size):
    """

    Отрисовка решётки Изинга

    """
    pygame.init()
    n_curr = A_curr.shape[0]
    FPS = 100
    WHT = (255, 255, 255)
    BLC = (0, 0, 0)
    screen = pygame.display.set_mode((int(n_curr*block_size), int(n_curr*block_size)))
    screen.fill(WHT)
    pygame.display.update()
    clock = pygame.time.Clock()
    finished = False
    for i in range(n_curr):
        for j in range(n_curr):
            if A_curr[i, j] > 0:
                rect(screen, BLC, (i*block_size, j*block_size, block_size, block_size))

    while not finished:
        clock.tick(FPS)
        for i in range(n_curr):
            for j in range(n_curr):
                if A_curr[i, j] > 0:
                    rect(screen, BLC, (i * block_size, j * block_size, block_size, block_size))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    finished = True
            elif event.type == pygame.QUIT:
                finished = True
    pygame.quit()


def modeling(beta_curr, h_curr, Iter_num, Gr_start):
    aver_magnetization = []
    Grid = Gr_start
    aver_magnetization.append(Grid.mean())
    for i in range(Iter_num):
        Grid = change(Grid, h_curr, beta_curr)
        aver_magnetization.append(Grid.mean())
    return Grid, np.array(aver_magnetization)


def plot_aver_magn(aver_magn):
    plt.grid()
    plt.plot(np.arange(1, aver_magn.shape[0]+1), aver_magn)
    plt.show()


def smechenie(x,y,Gr):
    n = Gr.shape[0]
    ans = 0
    for i in range(n):
        for j in range(n):
            ans += Gr[i, j]*Gr[(i+x) % n, (j+y) % n]
    ans = (ans*1.0) / (1.0 * n * n)
    return ans


def is_num(st):
    if st.isdigit():
        return True
    else:
        try:
            float(st)
            return True
        except ValueError:
            return False


def incorrect_ans():
    str = wrong_ansers[rnd.randint(0, len(wrong_ansers)-1)]
    return str

h_curr = 0.0
beta_curr = 10.0
size = 100
A = init_grid(size)
simulated = False

while True:
    print("\n"+"Введите необходимое действие: "+"\n")
    order = input()
    if order == "1":
        print("\n"+"Введите размер решётки: "+"\n")
        curr = input()
        if curr.isdigit():
            if int(curr) > 0:
                size = int(curr)
                A = init_grid(size)
            else:
                print("\n" + incorrect_ans())
        else:
            print("\n" + incorrect_ans())
    elif order == "2":
        simulated = True
        print("\n"+"Введите число итераций: "+"\n")
        num_iter1 = input()
        if num_iter1.isdigit():
            if int(num_iter1) > 0:
                num_iter = int(num_iter1)
                start_time = time.time()
                A, aver_magn = modeling(beta_curr, h_curr, num_iter, A)
                end_time = time.time()
                if end_time - start_time > time_per_size2 * size * size * num_iter:
                    print("\n" + "Среднее m: " + str(round(aver_magn.mean(), 4)) + "\n")
                    print("Среднее m^2: " + str(round((aver_magn * aver_magn).mean(), 6)) + "\n")
                    print("Среднее m^4: " + str(round((aver_magn * aver_magn * aver_magn * aver_magn).mean(), 8)))
                    print("\n" + "Время симуляции: " + str(round(end_time - start_time, 2)) + " сек")
                else:
                    time.sleep(time_per_size2 * size * size * num_iter - (end_time - start_time))
                    end_time_1 = time.time()
                    print("\n" + "Среднее m: " + str(round(aver_magn.mean(), 4)) + "\n")
                    print("Среднее m^2: " + str(round((aver_magn * aver_magn).mean(), 6)) + "\n")
                    print("Среднее m^4: " + str(round((aver_magn * aver_magn * aver_magn * aver_magn).mean(), 8)))
                    print("\n" + "Время симуляции: " + str(round(end_time_1 - start_time, 2)) + " сек")
            else:
                print("\n" + incorrect_ans())
        else:
            print("\n" + incorrect_ans())
    elif order == "3":
        if simulated:
            draw(A, int(1000 / size))
            plot_aver_magn(aver_magn)
        else:
            print("\n"+"Последнее измерение отсутствует")
    elif order == "4":
        if simulated:
            print("\n"+"Введите смещение по x: "+"\n")
            x_sm = input()
            print("\n"+"Введите смещение по y: " + "\n")
            y_sm = input()
            if x_sm.isdigit() and y_sm.isdigit():
                sm = smechenie(int(x_sm), int(y_sm), A)
                print("\n" + "Корреляционная функция принимает значение: " + str(round(sm, 4)))
            else:
                print("\n" + incorrect_ans())
        else:
            print("\n" + "Последнее измерение отсутствует")
    elif order == "5":
        print("\n"+"Введите величину магнитного поля: "+"\n")
        h_curr1 = input()
        if is_num(h_curr1):
            h_curr = float(h_curr1)
    elif order == "6":
        print("\n"+"Введите температуру: "+"\n")
        curr = input()
        if is_num(curr):
            if float(curr) > 0:
                beta_curr = float(curr)
            else:
                print("\n" + incorrect_ans())
        else:
            print("\n" + incorrect_ans())
    elif order == "7":
        print("\n"+"Температура: "+str(round(beta_curr, 2))+"\n")
        print("Величина магнитного поля: " + str(round(h_curr, 2)) + "\n")
        print("Размер решётки: " + str(size))
    else:
        print("\n"+incorrect_ans())