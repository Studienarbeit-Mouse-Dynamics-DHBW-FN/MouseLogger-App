import time
from pynput import mouse

import matplotlib.pyplot as plt


recording = True

x = []
y = []


def main():
    controller = mouse.Controller()
    current_position = controller.position
    for _ in range(500):
        if current_position != controller.position:
            print(time.time_ns(), controller.position)
            current_position = controller.position
            x.append(controller.position[0])
            y.append(controller.position[1])
        time.sleep(.0001)
        




if __name__ == "__main__":
    main()

    plt.plot(x, y)
    plt.gca().invert_yaxis()
    plt.show()
