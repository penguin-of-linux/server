from model import *

#  prepare + put = 150 + 100 = 250 на оба ребра
# (2) -------- (3) -------- (4)
#               |
# send info x 2 | prepare x 2 = 200 ms
#      = 200 ms |
#               (1)
#               |
# send info x 2 | prepare x 2 = 200 ms
#      = 200 ms |
#              (0) -------- (5)

if __name__ == "__main__":
    model = Model()
    d = model \
        .edge(0, 1, 50, 100) \
        .edge(1, 3, 50, 100) \
        .edge(2, 3, 50, 100) \
        .edge(3, 4, 50, 100) \
        .edge(0, 5, 50, 100) \
        .send(0, 3, 4, 1) \
        .send(0, 3, 2, 1) \
        .calculate()

    for i in d.keys():
        print("(%s)-(%s): %s" % (i[0], i[1], d[i]))
