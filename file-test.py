from time import sleep

file_path = "resources/file-test.txt"

def read_file(content):
    global file_path
    try:
        with open(file_path) as file:
            string = file.read()
            
            print(string if string == content else "nope")
    except FileNotFoundError:
        # print("File not found!")
        raise

def write_file(content):
    with open(file_path, "w") as file:
        file.write(content)

def run_example():
    try:
        read_file("This is a line")
    except:
        print("File not found! in line 24")
    sleep(.5)
    write_file("This is a line")
    sleep(.5)
    read_file("This is a line")
    sleep(.5)
    write_file("This is another line")
    sleep(.5)
    read_file("This is a line")
    sleep(.5)
    read_file("This is another line")

run_example()