import sys

def main():
    if len(sys.argv) < 4:
        print("Usage: push.sys.argv.py <num1> <num2> <num3>")
        return

    numbers = [int(arg) for arg in sys.argv[1:]]
    total = sum(numbers)
    print("Sum of the numbers:", total)

if __name__ == "__main__":
    main()
