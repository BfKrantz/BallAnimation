from BallAnimation.tower_maker_reverse import tower_maker_reverse
import time
import math

def animate(text, repeats, width=120, delay=0.03):
    tower = tower_maker_reverse(text)

    # normalize line width (prevents jitter)
    max_len = max(len(line) for line in tower)
    tower = [line.ljust(max_len) for line in tower]

    # dynamic movement range
    travel = width - max_len
    if travel < 0:
        travel = 0

    cycles = 0
    t = 0  # time step

    while cycles < repeats:
        # easing using sine wave (-1 to 1 smoothly)
        pos = math.sin(t)  

        # convert to actual shift range
        shift = int(pos * travel)

        for line in tower:
            if shift >= 0:
                shifted = ' ' * shift + line
            else:
                shifted = line[abs(shift):]

            # smush right
            if len(shifted) > width:
                shifted = shifted[:width]

            print(shifted)

        print()
        time.sleep(delay)

        t += 0.08  # controls speed of oscillationTr

        # detect full cycle (when sine completes)
        if t >= (2 * math.pi):
            t = 0
            cycles += 1


if __name__ == "__main__":
    text = input("Enter text: ")
    repeats = int(input("Repeats: "))
    animate(text, repeats)