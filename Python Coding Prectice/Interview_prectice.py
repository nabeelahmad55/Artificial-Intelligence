#Find Even & Odd Numbers in a List

numbers = list(map(int, input("Enter numbers: ").split()))

even = [n for n in numbers if n % 2 == 0]
odd = [n for n in numbers if n % 2 != 0]

print("Even numbers:", even)
print("Odd numbers:", odd)


#Count Words in a Sentence

sentence = input("Enter a sentence: ")
words = sentence.split()
print("Total words:", len(words))



#Find Second Largest Number

numbers = list(map(int, input("Enter numbers: ").split()))

unique_nums = list(set(numbers))
unique_nums.sort()

if len(unique_nums) < 2:
    print("Not enough unique numbers.")
else:
    print("Second largest:", unique_nums[-2])



# Check Armstrong Number

num = int(input("Enter number: "))
digits = [int(d) for d in str(num)]
power = len(digits)

result = sum(d ** power for d in digits)

if result == num:
    print("Armstrong number")
else:
    print("Not Armstrong")


#Count Frequency of Each Character
text = input("Enter text: ")

freq = {}

for ch in text:
    freq[ch] = freq.get(ch, 0) + 1

print("Character frequency:")
for k, v in freq.items():
    print(f"{k}: {v}")