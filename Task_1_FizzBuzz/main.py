def fizzbuzz(a, b):
    for num in range(a, b + 1):
        if num % 3 == 0 and num % 5 == 0:
            print("FizzBuzz")
        elif num % 3 == 0:
            print("Fizz")
        elif num % 5 == 0:
            print("Buzz")
        else:
            print(num)


# Read input numbers
n = int(input())
m = int(input())

# Call the fizzbuzz function
fizzbuzz(n, m)
