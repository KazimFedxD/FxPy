
def assure_error(name, func):
    confirmation = input(f"Is {name} your name? (yes/no): ")
    if confirmation.lower() == "yes":
        return name
    elif confirmation.lower() == "no":
        return func()
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
        return assure_error(name, func)

def get_name():
    name = input("Enter your name: ")
    return assure_error(name, get_name)

print(get_name())
