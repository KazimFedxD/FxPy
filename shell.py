import run

string = "fdfdf"
string.endswith

while True:
    text = input("FxPy>>> ")


    result, error = run.run("<stdin>", text)

    if error:
        print(error.as_string())
        continue
    if result:
        result = repr(result)
        if result.endswith("0"):
            print(result[:-1])
        else:
            print(result)

    if text.strip() == "exit()":
        break
