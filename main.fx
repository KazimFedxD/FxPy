import modules.math

print("hello\n")

fex add(a, b) -> return a + b

fex sub(a, b):
    return a - b
    end

print(add(1, 2) + "\n")
print(sub(1, 2) + "\n")


print("Enter a number: ")
let x = convert(input(), "number")

print("Enter another number: ")
let y = convert(input(), "number")

print("The sum is: " + add(x, y) + "\n")
print("The difference is: " + sub(x, y) + "\n")



