import run
import sys

running = True

if len(sys.argv) > 1:
    running = False
    with open(sys.argv[1], "r") as file:
        text = file.read()
        result, error = run.run(sys.argv[1], text)

        if error:
            print(error.as_string())
        if result:
            result = repr(result)
            if result.endswith("0"):
                print(result[:-1])
            else:
                print(result)
        sys.exit()

while running:
    try:
        text = input("FxPy>>> ")
    except KeyboardInterrupt:
        continue

    result, error = run.run("<stdin>", text)

    if error:
        print(error.as_string())
        continue
    if result:
        result = repr(result)
        if result == "0":
            print()
        else:
            print(result)

    if text.strip() == "exit()":
        break
    
    
print("Goodbye!")
    
