numbers = list(map(int, input("Enter numbers seperated by spaces: ").split()))


unique = sorted(set(numbers))

print(unique)