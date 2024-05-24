import run


while True:
    text = input("FxPy>>> ")

    result, error = run.run("<stdin>", text)

    if error:
        print(error.as_string())
        continue
    if result:
        print(repr(result))

    if text.strip() == "exit()":
        break
