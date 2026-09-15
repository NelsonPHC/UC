# Error introduced: removed the colon after def calculate_sum(arr).
def calculate_sum(arr)
    total = 0
    for num in arr:
        total += num
    return total

numbers = [1, 2, 3, 4, 5]
result = calculate_sum(numbers)
print("Sum in Python :", result)


# Error message
#   File "script.py", line 2
#     def calculate_sum(arr)
#                           ^
# SyntaxError: invalid syntax