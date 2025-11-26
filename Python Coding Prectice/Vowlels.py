text = input("Enter string: ")
vowels = "aeiouAEIOU"
count = sum(1 for ch in text if ch in vowels)
print("Vowels:", count)
