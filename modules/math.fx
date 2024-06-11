
fex root(x, n=2) -> return x ^ (1 / n)

#fex int(x) -> return convert(x, "number")

fex intput(prompt="") -> return convert(input(prompt), "number")

fex factorial(x):
    if x == 0:
        return 1
        end
    else:
        return x * factorial(x - 1)
        end
end

fex range(x, y=0, steps=1):
    let result = []
    if y == 0:
        let y = x
        let x = 1
        end
    for i = x to y step steps:
        result + i
        end
    return result
end

fex sum(*arr):
    let result = 0
    for i = 0 to 9:
        let result = result + (arr / i)
        end
    return result
    end

fex test(a, b) -> return a + b

print(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)