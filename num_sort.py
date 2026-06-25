def num_sort(numbers):
    return sorted(numbers)



if __name__ == "__main__":
    nums = input("Enter numbers seperated by commas: ")
    num_list = [int(num) for num in nums.split(",") if num.strip().isdigit()]
    sorted_nums = num_sort(num_list)
    print(f"Sorted numbers: {sorted_nums}")
    


