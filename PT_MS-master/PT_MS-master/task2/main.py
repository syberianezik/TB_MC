import math
import numpy as np


def task3(k, v, n, bw, b):
    a = 1
    while 1:
        a = task1(k, v, n, bw, b)
        if a > 0.0001:
            b += 1
        else:
            break
    print("Preferable buffer size: ", b)


def task2(bw, k, mu, m):
    np.random.seed(100)

    n_rep = 1
    p_refuse = 0

    n_lost = 0
    n_packets = 10000000
    for i in range(n_rep):
        t = 0
        queue = 0
        t_free = np.zeros(k)

        for f in range(n_packets):
            t += np.random.exponential(scale=1 / bw)
            n = 0
            if queue > 0:
                for j in range(k):
                    while t_free[j] < t and queue > 0:
                        t_free[j] += np.random.exponential(scale=1/mu)
                        queue -= 1
            for h in range(k):
                if t_free[h] < t:
                    t_free[h] = t + np.random.exponential(scale=1/mu)
                    break
                else:
                    n += 1
            if n == k:
                if queue < m:
                    queue += 1
                else:
                    n_lost += 1
    p_refuse += n_lost/n_packets

    p_refuse /= n_rep

    return p_refuse


def task1(k, v, n, bw, b):
    u = v / n
    p1 = bw / u
    m = k * b + b - 1

    top = (p1 ** k / math.factorial(k)) * (p1 ** m / k ** m)

    bot1 = 0
    for j in range(0, k + 1):
        bot1 += p1 ** j / math.factorial(j)

    bot2 = 0
    for j in range(1, m + 1):
        bot2 += p1 ** j / k ** j
    bot2 *= p1 ** k / math.factorial(k)

    return top / (bot1 + bot2)


con = 8         # Количество концентраторов
sp = 2400       # Скорость передачи, бит/с
val = 1200      # Средняя длина пакета, бит
bw1 = 8         # Интенсивность входного потока днем (с 8 до 24 часов)
bw2 = 0.5       # Интенсивность входного потока ночью (с 0 до 8 часов)
buff = 1        # Размер буфера, пакетов

print("Probability of blocking a daytime package", task1(con, sp, val, bw1, buff))
print("Probability of blocking a nighttime package", task1(con, sp, val, bw2, buff))
print("Probability of blocking a daytime package by Monte-Carlo", task2(bw1, con, sp / val, con * buff + buff - 1))
print("Probability of blocking a daytime package by Monte-Carlo", task2(bw2, con, sp / val, con * buff + buff - 1))
task3(con, sp, val, bw1, buff)
