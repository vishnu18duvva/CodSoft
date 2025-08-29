def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error! Division by zero."
    return a / b

print(" Simple Calculator ")

try:
    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))

    print("\n Choose the operation:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")

    choice = input("Enter your choice (+, -, *, /): ")

    if choice == '+':
        result = add(num1, num2)
    elif choice == '-':
        result = subtract(num1, num2)
    elif choice == '*':
        result = multiply(num1, num2)
    elif choice == '/':
        result = divide(num1, num2)
    else:
        result = "Invalid operation! Please enter +, -, * or /."

    print(f"\nResult: {result}")

except ValueError:
    print("Error! Please enter valid numbers.")
