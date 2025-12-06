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



#Find All Prime Numbers in a Range (Sieve of Eratosthenes)

n = int(input("Find primes up to: "))

sieve = [True] * (n + 1)
p = 2

while p * p <= n:
    if sieve[p]:
        for i in range(p * p, n + 1, p):
            sieve[i] = False
    p += 1

primes = [i for i in range(2, n + 1) if sieve[i]]
print("Prime numbers:", primes)



#Find Pairs in a List That Sum to a Target

numbers = list(map(int, input("Enter numbers: ").split()))
target = int(input("Target sum: "))

seen = {}
pairs = []

for num in numbers:
    diff = target - num
    if diff in seen:
        pairs.append((diff, num))
    seen[num] = True

print("Pairs with target sum:", pairs)



#Find Longest Palindrome Substring

def longest_palindrome(s):
    if len(s) < 2:
        return s

    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l+1:r]

    longest = ""

    for i in range(len(s)):
        # odd-length palindromes
        p1 = expand(i, i)
        # even-length palindromes
        p2 = expand(i, i + 1)

        longest = max(longest, p1, p2, key=len)

    return longest

text = input("Enter string: ")
print("Longest palindrome substring:", longest_palindrome(text))


#Check Balanced Parentheses Using Stack

def is_balanced(expr):
    stack = []
    pairs = {')': '(', '}': '{', ']': '['}

    for ch in expr:
        if ch in "({[":
            stack.append(ch)
        elif ch in ")}]":
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()

    return len(stack) == 0

expr = input("Enter expression: ")
print("Balanced" if is_balanced(expr) else "Not balanced")


#Binary Search (Iterative)


def binary_search(arr, target):
    low, high = 0, len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1

arr = list(map(int, input("Enter sorted numbers: ").split()))
x = int(input("Number to search: "))

index = binary_search(arr, x)
print("Found at index:", index if index != -1 else "Not found")

#Word Ladder (Shortest Transformation Sequence)

from collections import deque

def word_ladder(begin, end, word_list):
    if end not in word_list:
        return 0
    
    word_set = set(word_list)
    queue = deque([(begin, 1)])  # (current_word, steps)

    while queue:
        word, steps = queue.popleft()

        if word == end:
            return steps

        for i in range(len(word)):
            for ch in "abcdefghijklmnopqrstuvwxyz":
                new_word = word[:i] + ch + word[i+1:]

                if new_word in word_set:
                    word_set.remove(new_word)  # avoid revisits
                    queue.append((new_word, steps + 1))

    return 0  # no transformation possible


# ----------- Run Program -------------
begin = input("Enter begin word: ")
end = input("Enter end word: ")
word_list = input("Enter dictionary words (space separated): ").split()

result = word_ladder(begin, end, word_list)

if result == 0:
    print("No transformation possible.")
else:
    print("Shortest transformation steps:", result)



#N-Queens Problem (Return All Solutions)

    def solve_n_queens(n):
    solutions = []
    board = ["." * n for _ in range(n)]

    cols = set()        # attacked columns
    diag1 = set()       # r - c
    diag2 = set()       # r + c

    def backtrack(r):
        if r == n:
            solutions.append(board.copy())
            return

        for c in range(n):
            if c in cols or (r - c) in diag1 or (r + c) in diag2:
                continue

            cols.add(c)
            diag1.add(r - c)
            diag2.add(r + c)

            row_list = list(board[r])
            row_list[c] = "Q"
            board[r] = "".join(row_list)

            backtrack(r + 1)

            cols.remove(c)
            diag1.remove(r - c)
            diag2.remove(r + c)

            row_list[c] = "."
            board[r] = "".join(row_list)

    backtrack(0)
    return solutions


# ----------- Run Program -------------
n = int(input("Enter value of N (e.g., 4, 8): "))
result = solve_n_queens(n)

print(f"Total solutions: {len(result)}\n")
for sol in result:
    for row in sol:
        print(row)
    print()



    #Sudoku Solver (Backtracking + Constraint Checking)

def is_valid(board, r, c, num):
    # Check row
    if num in board[r]:
        return False

    # Check column
    for i in range(9):
        if board[i][c] == num:
            return False

    # Check 3×3 box
    box_r = (r // 3) * 3
    box_c = (c // 3) * 3

    for i in range(box_r, box_r + 3):
        for j in range(box_c, box_c + 3):
            if board[i][j] == num:
                return False

    return True


def solve_sudoku(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                for num in range(1, 10):
                    if is_valid(board, r, c, num):
                        board[r][c] = num

                        if solve_sudoku(board):
                            return True

                        board[r][c] = 0  # backtrack
                return False
    return True


# ---------- Run Program -------------
print("Enter Sudoku row by row (use 0 for empty cells):")

board = []
for _ in range(9):
    row = list(map(int, input().split()))
    board.append(row)

if solve_sudoku(board):
    print("\nSolved Sudoku:")
    for row in board:
        print(row)
else:
    print("No solution exists.")




#Edit Distance (Levenshtein Distance)



def edit_distance(s1, s2):
    memo = {}

    def dp(i, j):
        # If already solved
        if (i, j) in memo:
            return memo[(i, j)]

        # If s1 is finished, we need to insert remaining chars of s2
        if i == len(s1):
            return len(s2) - j

        # If s2 is finished, we need to delete remaining chars of s1
        if j == len(s2):
            return len(s1) - i

        # If characters match: move to next
        if s1[i] == s2[j]:
            ans = dp(i + 1, j + 1)
        else:
            insert = 1 + dp(i, j + 1)
            delete = 1 + dp(i + 1, j)
            replace = 1 + dp(i + 1, j + 1)

            ans = min(insert, delete, replace)

        memo[(i, j)] = ans
        return ans

    return dp(0, 0)


# ----------- Run Program -------------
s1 = input("Enter first string: ")
s2 = input("Enter second string: ")

print("Minimum Edit Distance:", edit_distance(s1, s2))



#Course Schedule (Detect Cycle in Directed Graph)



def can_finish(numCourses, prerequisites):
    graph = {i: [] for i in range(numCourses)}

    for a, b in prerequisites:
        graph[b].append(a)

    visited = set()
    cycle = set()

    def dfs(course):
        if course in cycle:
            return False  # cycle detected

        if course in visited:
            return True

        cycle.add(course)

        for neighbor in graph[course]:
            if not dfs(neighbor):
                return False

        cycle.remove(course)
        visited.add(course)
        return True

    for c in range(numCourses):
        if not dfs(c):
            return False

    return True


# ----------- Run Program -------------
num = int(input("Enter number of courses: "))
print("Enter prerequisites like: a b (a depends on b), one pair per line.")
print("Enter 'done' when finished.")

prereq = []
while True:
    line = input()
    if line.lower() == "done":
        break
    a, b = map(int, line.split())
    prereq.append([a, b])

print("Can complete all courses:", can_finish(num, prereq))



#Problem: Detect Overlapping Time Intervals & Merge Them

def to_minutes(t):
    """Convert HH:MM to total minutes."""
    h, m = map(int, t.split(":"))
    return h * 60 + m

def to_timestr(minutes):
    """Convert total minutes back to HH:MM."""
    return f"{minutes//60:02d}:{minutes%60:02d}"

def merge_intervals(intervals):
    # Convert intervals to minute-based integers
    converted = [(to_minutes(s), to_minutes(e)) for s, e in intervals]
    
    # Sort by start time
    converted.sort(key=lambda x: x[0])
    
    merged = []
    for start, end in converted:
        if not merged or start > merged[-1][1]:
            merged.append([start, end])
        else:
            merged[-1][1] = max(merged[-1][1], end)
    
    # Convert back to time strings
    return [(to_timestr(s), to_timestr(e)) for s, e in merged]


# Example
intervals = [
    ("09:00", "11:30"),
    ("10:45", "12:00"),
    ("13:00", "14:00"),
    ("13:30", "15:00"),
    ("16:00", "17:00")
]

print(merge_intervals(intervals))



#Complex Python Problem: Dependency Resolver (Topological Sorting with Cycle Detection)



from collections import defaultdict

def resolve_dependencies(dependencies):
    graph = defaultdict(list)
    visited = {}
    order = []

    # Build adjacency list
    for pkg, dep in dependencies:
        graph[dep].append(pkg)

    def dfs(node, stack):
        visited[node] = "visiting"
        stack.append(node)

        for nei in graph[node]:
            if visited.get(nei) == "visiting":
                cycle_start = stack.index(nei)
                cycle = stack[cycle_start:] + [nei]
                raise Exception("Cycle detected: " + " -> ".join(cycle))

            if visited.get(nei) != "visited":
                dfs(nei, stack)

        visited[node] = "visited"
        order.append(node)
        stack.pop()

    # Run DFS for all unique nodes
    nodes = set([d for _, d in dependencies] + [p for p, _ in dependencies])

    for node in nodes:
        if visited.get(node) != "visited":
            dfs(node, [])

    return order[::-1]   # reverse for correct topological order


# Example usage:
dependencies = [
    ("A", "B"),
    ("B", "C"),
    ("C", "E"),
    ("D", "E"),
    ("F", "A")
]

try:
    result = resolve_dependencies(dependencies)
    print("Valid installation order:", result)
except Exception as e:
    print(str(e))

