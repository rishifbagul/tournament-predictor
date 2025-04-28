def get_combination(n, num_vars):
    n -= 1  # Convert to 0-based index
    digits = []
    for _ in range(num_vars):
        digits.append(n % 3)
        n = n // 3
    # Reverse the digits to get the correct order
    return tuple(reversed(digits))



for i in range (1,10):
    print(f"Combination {i}: ", end="")
    print(get_combination(i,2))