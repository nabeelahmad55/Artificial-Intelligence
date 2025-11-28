#Find Largest in List
numbers = list(map(int, input("Enter numbers: ").split()))
print("Largest:", max(numbers))


#Remove Duplicates from List
items = list(map(int, input("Enter numbers: ").split()))
unique = list(set(items))
print("Without duplicates:", unique)


#Check Palindrome
text = input("Enter text: ")

if text == text[::-1]:
    print("Palindrome")
else:
    print("Not Palindrome")



#Find Factorial
num = int(input("Enter number: "))

fact = 1
for i in range(1, num + 1):
    fact *= i

print("Factorial:", fact)


#Sum of Digits
num = input("Enter number: ")
total = sum(int(d) for d in num)
print("Sum of digits:", total)


#Simple Calculator
a = float(input("Enter first number: "))
b = float(input("Enter second number: "))
op = input("Operator (+ - * /): ")

if op == "+":
    print(a + b)
elif op == "-":
    print(a - b)
elif op == "*":
    print(a * b)
elif op == "/":
    print(a / b)
else:
    print("Invalid operator")

#Find Common Elements in Two Lists

list1 = list(map(int, input("List 1: ").split()))
list2 = list(map(int, input("List 2: ").split()))

common = list(set(list1) & set(list2))
print("Common elements:", common)



#Sort a List Without Using sort() Bubble sort (manual sorting)

numbers = list(map(int, input("Enter numbers: ").split()))

for i in range(len(numbers)):
    for j in range(0, len(numbers) - i - 1):
        if numbers[j] > numbers[j + 1]:
            numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]

print("Sorted list:", numbers)


#Check Perfect Number
#Example: 6 → 1 + 2 + 3 = 6

num = int(input("Enter number: "))

divisors = [i for i in range(1, num) if num % i == 0]

if sum(divisors) == num:
    print("Perfect number")
else:
    print("Not perfect")

# Find the Longest Word in a Sentence

sentence = input("Enter a sentence: ")
words = sentence.split()

longest = max(words, key=len)
print("Longest word:", longest)
print("Length:", len(longest))




#Convert Celsius to Fahrenheit

#Formula: F = (C × 9/5) + 32

c = float(input("Enter temperature in Celsius: "))
f = (c * 9/5) + 32
print("Fahrenheit:", f)
