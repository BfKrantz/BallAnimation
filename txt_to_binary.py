def txt_to_binary(string):
    #Converts a String to binary
    binary = ''.join(format(ord(char), '08b') for char in string)
    return binary


if __name__ == "__main__": 
   string = "Hello World"
   print(txt_to_binary(string)) 
   
   