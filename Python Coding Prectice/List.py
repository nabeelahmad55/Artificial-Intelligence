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
