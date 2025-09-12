string = input("Enter a string: ").replace(" ", "")

char_count = {}

for char in string:
    if char in char_count:
        char_count[char] += 1
    else:
        char_count[char] = 1

max_frequency = max(char_count, key=char_count.get)
print(f"Most frequent character: {max_frequency}")
