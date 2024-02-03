# # answer for question num 1
# try:
#     a = 1/0
# except ZeroDivisionError:
#     print("error you cant divide a number with zero")

# # answer for question num 2
# no because there is no except so the try is use less


# # answer for question num 3
# run time error

# # answer for question num 4
# you dont know what is the error


# # answer for question num 5
# a.
# b. when you divide a number with zero


# # answer for question num 6
# write_file = open("words.txt", "w")
# write_file.write("shahar")
# write_file.close()

# # answer for question num 7
# read_file = open("words.txt")
# for line in read_file:
#     print(line, end="")
# read_file.close()

# # answer for question num 8
# write_file = open("words.txt", "w", encoding='utf-8')
# write_file.write("שחר כהן")
# write_file.close()
# read_file = open("words.txt")
# for line in read_file:
#     print(line, end="")
# read_file.close()


# # answer for question num 10
# from PIL import Image
# color = "green"
# img = Image.new('RGB', (60, 30), color=color)
# img.save(f'pil_{color}.png')


# # answer for extra question num 1 file is empty
# read_file = open("words.txt")
# line_count = 0
# for line in read_file:
#     line_count = line_count + 1
# if line_count == 0:
#     print("The file is empty")
# else:
#     print(line, end="")
# read_file.close()

# # answer for extra question num 2 read line num 4 from file
# read_file = open("words.txt")
# line_count = 0
# while line_count < 4:
#     for line in read_file:
#         line_count = line_count + 1
#         if line_count == 4:
#             print(line)
# read_file.close()

# answer for extra question num 3 longest words in a file


# answer for extra question num 4 frequency of words in a file


