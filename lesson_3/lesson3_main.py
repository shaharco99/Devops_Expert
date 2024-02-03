# import requests
# res = requests.get('https://github.com')
# print(res.status_code)

# # default is read  a = append, w = write
# read_file = open("my_names.txt", "a")
# read_file.write("Hi shahar" + "\n")
# # always close when finished
# read_file.close()

def save_name(name):
    write_file = open("my_names.txt", "a")
    write_file.write(name + "\n")
    write_file.close()


def print_name():
    read_file = open("my_names.txt")
    for line in read_file:
        print(line, end="")
    read_file.close()


save_name("shahar")
save_name("doron")
print_name()
