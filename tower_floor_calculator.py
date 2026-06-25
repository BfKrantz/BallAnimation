from BallAnimation.binary_to_numeral import binary_to_numeral

def tower_floor_calculator(text):
    numeral = binary_to_numeral(text)

    n = 0
    while numeral > 0:
        numeral //= 4 
        if n % 2 == 0:
            n += 1
        else:
            n += 2

    floor_list = []

    while n > 0:
        floor_list.append('#' * n)
        n -= 2

    return floor_list


if __name__ == '__main__':
    result = tower_floor_calculator("Hello World")
    print(result)