from BallAnimation.tower_floor_calculator import tower_floor_calculator

def tower_maker_reverse(text=None):
    lines = tower_floor_calculator(text)

    sorted_list = sorted(lines, key=len)
    longest_line = len(sorted_list[-1])

    tower = []

    # top
    for line in sorted_list:
        padding = (longest_line - len(line)) // 2
        tower.append(' ' * padding + line)

    # bottom (skip middle)
    for line in reversed(sorted_list[:-1]):
        padding = (longest_line - len(line)) // 2
        tower.append(' ' * padding + line)

    return tower


if __name__ == "__main__":
    for line in tower_maker_reverse("Hello World"):
        print(line)
