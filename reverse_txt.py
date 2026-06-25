def reverse_text(text=None):
    ##Reverses input text
    if text == None:
        text = input("Enter text to reverse: ")
        return f"Reversed text: {text[::-1]}"
    
    else: 
        return text[::-1]
        

if __name__ == "__main__":
    print(reverse_text())
