import re

# Get input and ensure it's a string
sentence = str(input("Please enter the sentence: ")).lower()

# Remove punctuation (keep only letters and spaces)
sentence = re.sub(r'[^a-zA-Z ]', '', sentence)  

words = sentence.split()  # Split words by spaces
sentence_count = {}  # Dictionary to store word frequencies

# Count word occurrences
for word in words:
    if word in sentence_count:
        sentence_count[word] += 1  # Increase count if word already exists
    else:
        sentence_count[word] = 1  # Initialize count

# Print the word frequencies
for word, count in sentence_count.items():
    print(f"{word}: {count}")
