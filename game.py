import matplotlib.pyplot as plt
import matplotlib.patches as pat
from threading import Thread
import sys, os

datas = 10000

def getchar():
  #Returns a single character from standard input
  import tty, termios, sys
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
     tty.setraw(sys.stdin.fileno())
     ch = sys.stdin.read(1)
  finally:
     termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch

def save_data(data, start):
  file = open("humandata.txt", "r")
  lines = file.readlines()
  existing = [False] * datas
  out = [[-1,0,0]] * datas
  for i in range(len(lines)):
    l = lines[i]
    if len(l) < 5: continue
    x = list(map(float, l.split()))
    if start <= x[0] and x[0] < start + len(data):
      existing[int(x[0])] = True
      out[int(x[0])] = [x[0], (x[1] * x[2] + data[int(x[0]) - start]) / (x[2] + 1), x[2] + 1]
  for i in range(len(existing)):
    if existing[i] == False and start <= i and i < start + len(data):
      out[i] = [i, data[i - start], 1]
  file.close()

  file2 = open("humandata.txt", "w")
  for x in out:
    if x[0] != -1:
      file2.write(f'{x[0]} {x[1]} {x[2]}\n')
  file2.close()

def plot_graph(args):
    pos2 = args[0]
    j = 1

    plt.ion()
    fig = plt.figure()
    ax = plt.gcf().gca()
    ax.set_xlim((-10, 10))
    ax.set_ylim((-5, 5))

    while j < len(args):
      # print(args[j], args[j+1])
      circle = plt.Circle((args[j], args[j + 1]), 0.05 + 0.01 * (j // 2), color="g", fill=True)
      ax.add_artist(circle)
      j += 2

    rect = pat.Rectangle((9.6, pos2), 0.4, 2, color="b", fill=True)
    ax.add_patch(rect)

    text = plt.text(-8, -3, '#' + str(i))
    ax.add_artist(text)

    plt.pause(0.001)
    plt.show()

def user_input(*args):
  while 1:
    ch = getchar()
    #print("you pressed " + ch)
    if ch == 'p':
      plt.close('all')
      save_data(data, start_line)
      os._exit(0)
      break
    elif ch == 'w':
      print(1)
      data.append(1)
      sys.exit()
      break
    elif ch == 's':
      print(-1)
      data.append(-1)
      sys.exit()
      break
    elif ch == 'd':
      print(0)
      data.append(0)
      sys.exit()

start_line = int(input("starting game #? "))
data = []

file = open("games.txt", "r")
lines = file.readlines()
for i in range(len(lines)):
  if i >= start_line:
    game = list(map(float, lines[i].split()))
    t = Thread(target=user_input, args=game)
    t.start()

    #print(game)
    plot_graph(game)
    #print("hi")
    
    t.join()
    #print("hi2")