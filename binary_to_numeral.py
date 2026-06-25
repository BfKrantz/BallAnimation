from BallAnimation.txt_to_binary import txt_to_binary
from BallAnimation.reverse_txt import reverse_text

def binary_to_numeral(text=None, binary=None):
    if text is None:
        if binary is None:
            raise ValueError("Provide either text or binary")

        binary = reverse_text(binary)
    else:
        binary = txt_to_binary(text)
        binary = reverse_text(binary)

    number = 0
    n = 0
    for num in binary:
        number += int(num) * (2 ** n)
        n += 1

    return number


if __name__ == "__main__":
    result = binary_to_numeral(binary=txt_to_binary('Hello World'))  # FIX
    print(result)
