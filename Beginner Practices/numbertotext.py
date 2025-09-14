number = input("Phone:")
dict = {
    "1": "One",
    "2": "Two",
    "3": "Three",
    "4": "Four"
    }
text = ""
for numbers in number:
    text += dict.get(numbers, "!") + " "

print(text)