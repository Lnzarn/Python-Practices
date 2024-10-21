
#STRINGS
print("Hello, world!")
print('\n')
print("Testing    HAHAHAH")
print("Testing "+"HAHAHAH")

print('\n')


#MATH
print(50 + 50)
print(50-50)
print(50*50)
print(50/50)
print(10**2)

print('\n')

#VARIABLES AND METHODS

Love = "Alliana is the one I love"

print(Love)

print(Love.upper()) #making the string uppercase
print(Love.lower())
print(Love.title()) #Every first letter of a word is uppercase
print(len(Love))

name = "Lanz"
age = 18
grades = 96.4 

print(int(age))
print("Hello! I am " + name + " and I am " + str(age) + " years old")


print('\n')


#FUNCTIONS

def who_am_i():
        name = "Alliana"
        age = 18
        print("Hello! I am " + name + " and I am " + str(age) + " years old")

who_am_i()

def add_one_hundred(num):
        print(num + 100)

add_one_hundred(100)

def add_vars(x,y):
        print(x + y)

add_vars(7,7)

def multiply(x,y):
        return x * y

multiply(7,7)

print(multiply(7,7))

def nl():
        print('\n')

nl()


#BOOLEAN EXPRESSIONS

bool1 = True
bool2 = 3*3 == 9
bool3 = False
bool4 = 3*3 != 9

print(bool1, bool2, bool3, bool4)


nl()


#RELATIONAL AND BOOLEAN OPERATORS

greater_than = 7 > 5
less = 5 < 7
greater_equal = 7 >= 7

test_and = (7 > 5) and (5 < 7) #true
test_and2 = (7 > 5) and (5 > 7) #false
test_and3 = (7 > 5) or (5 < 7) #true
test_and4 = (7 > 5) or (5 > 7) #true

test_not = not True #false


nl()


#CONDITIONAL STATEMENTS - if/else

def drink(money):
        if money >= 2:
                return "You've got yourself a drink!"
        else:
                return "No drink for you!"
        
print(drink(3))
print(drink(1))

nl()

def alcohol(age,money):
        if (age >= 21) and (money >= 5):
                return "We're getting a drink!"
        elif (age >= 21) and (money < 5):
                return "Come back with more money."
        elif (age < 21) and (money >= 5):
                return "Nice try, kid!"
        else:
                return "You're too young and too poor"
        
print(alcohol(21,5))
print(alcohol(20,5))
print(alcohol(21, 3))
print(alcohol(10,1))

nl()


#LISTS - have brackets []

movies = ["La Casa De Papel", "Your Name", "No Game No Life"]

print(movies[0])
print(movies[0:2]) #return the first until the last, but not printing the last number
print(movies[0:])
print(movies[:2])

print("List of Movies: " + str(len(movies)))

movies.append("Outside") #adding to the end of the list
print(movies)

movies.insert(2 , "Firefly") #insert to specific
print(movies)

movies.pop() #removes the last
print(movies)

movies.pop(0) #removes specific
print(movies)

Alliana_movies = ["Ten days to lose a guy", "That kind of love", "Inside"]

our_movies = movies + Alliana_movies

print(our_movies)


grades = [["Bob", 82], ["Alice", 90], ["Alliana", 99]]

bobs_grade = grades[0][1]

print(bobs_grade)

nl()

#TUPLES - do not change, ()

grades = ("a", "b", "c", "d", "f")



#LOOPING

#For loops - starts to finish of an iterate

vegetables = ["cucumber", "spinach", "cabbage"]

for x in vegetables:
        print(x)


#While loops - execute as long as True

i = 1

while i < 10:
        print(i)
        i += 1



nl()

#ADVANCED STRINGS

my_name = "Lanz"
print(my_name[0]) #first letter
print(my_name[-1]) #last letter

sentence = "This is a sentence."
print(sentence[:4])
print(sentence.split()) #delimeter - default is space

sentence_split = sentence.split() #splitting
sentence_join = ' '.join(sentence_split) #joining them back together with space

print(sentence_join)

quote = "Give me your 'money'!"
print(quote)
quote = 'Give me your "money"!'
print(quote)
quote = "Give me your \"money\"!"
print(quote)

too_much_space = "               hello          "
print(too_much_space.split())

print("A" in "Apple") #true
print("a" in "Apple") #false

Letter = "A"
word = "Apple"

print(Letter.lower() in word.lower()) #making them lowercase to match

movie = "Outside"

print("My Favorite movie is {}.".format(movie))
print("My Favorite movie is %s" % movie)
print(f"My Favorite movie is {movie}.")

#DICTIONARIES - key/value pairs {}

drinks = {"White Russian": 7, "Old Fashioned": 10, "Lemon Drop": 8} #drink is the key, price is the value

print(drinks)

employees = {"Finance": ["Bob", "Linda", "Tina"], "IT": ["Gene", "Louise", "Teddy"], "HR": ["Jimmy Jr.", "Mort"]}

print(employees)

employees['Legal'] = ["Mr.Frond"] #addes new key:value pair

print(employees)

employees.update({"Sales": ["Andie", "Ollie"]}) #also adds key:value

print(employees)

drinks['White Russian'] = 8
print(drinks)
