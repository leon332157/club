import pyscreenshot, os, time

listt = []
for x in range(0, 100):
    t1 = time.time()
    listt.append(pyscreenshot.grab(childprocess=False))
    print(x)
    print(time.time() - t1)
i = 0
for each in listt:
    filename = os.getcwd() + '/cache/{}.png'.format(i)
    print(filename)
    each.save(filename)
    i += 1
