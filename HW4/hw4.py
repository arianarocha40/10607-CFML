"""
Name: Ariana Rocha
AndrewID: afrocha

10607 Fall 2023 Homework 4

Instructions: Fill in the functions according to the instructions in the writeup.

Make sure you have Python and numpy installed on your system.

By Jocelyn Tseng
2023
"""

# Question 1: For the sequence functions, n is an integer >= 0
def sequence1(n): #Recursively
    if n <= 3:
        return n
    else:
        return sequence1(n-1) + sequence1(n-2) - ((sequence1(n-4))/(sequence1(n-3)))
    #pass

def sequence2(n): #Iteratively
    if n <= 3:
        return n
    seq = [0] * (n+1)
    for i in range(4):
        seq[i] = i    
    for i in range(4, n+1):
        seq[i] = seq[i-1] + seq[i-2] - (seq[i-4] / seq[i-3])
    return seq[n]
    #pass

table = {}
def sequence3(n): #Recursively with Memoization
    if n <= 3:
        return n
    if n in table:
        return table[n]
    table[n] = sequence3(n-1) + sequence3(n-2) - (sequence3(n-4) / sequence3(n-3))
    return table[n]
    #pass

# Question 2.1: n is an integer >= 1
def recursive_solution(n):
    if n == 1:
        return 1 / (1 * (1 + 1))
    return 1 / (n * (n + 1)) + recursive_solution(n - 1)
    #pass

def static_solution(n): #Just what was given?
    return n / (n + 1)
    #pass

# Question 2.2
def string_length(string):
    if string == "":
        return 0
    return 1 + string_length(string[1:])
    #pass

# Question 2.3
def geometric_sum(a,r,n):
    if n == 0:
        return 0
    return a * (r ** (n - 1)) + geometric_sum(a, r, n-1)
    #pass

def geometric_sum_definition(a,r,n):
    if r == 1:
        return a * n
    return a * (1-r ** n) / (1-r)
    #pass