import re

# Get input and ensure it's a string
sentence = str(input("Please enter the sentence: ")).lower()

# Remove punctuation (keep only letters and spaces)
sentence = re.sub(r'[^a-zA-Z ]', '', sentence)  
