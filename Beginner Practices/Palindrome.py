word = input("Enter the word: ")
word = word.replace(" ", "").lower()

if word == word[::-1]:
    print("Yes, its a palindrome!")
else:
    print("No, its not a palindrome.")
