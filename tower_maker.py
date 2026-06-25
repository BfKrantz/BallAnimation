from BallAnimation.tower_floor_calculator import tower_floor_calculator

def tower_maker(text):
    # get raw tower levels from your chain
    lines = tower_floor_calculator(text)
    
    #Takes lines of #'s, sorts by length, and stacks from middle, e.g.
    #      #
    #     ###
    #    #####
    #    #####
    #    #####

    # sort smallest to largest
    sorted_list = sorted(lines, key=len)
    longest_line = len(sorted_list[-1])

    for line in sorted_list:
        if len(line) == longest_line:
            print(line)
        else:
            padding = (longest_line - len(line)) // 2
            print(' ' * padding + line)


if __name__ == "__main__":
    tower_maker("Hello World")