from user_interface import * 

# Run the program.
if __name__ == "__main__":
    while True:
        reset = main.run("white")
        if reset:
            continue
        main.run("black")
