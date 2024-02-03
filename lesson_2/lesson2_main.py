# is_true = False
# a = 2
# b = 2.5
# str_one = "One"
# str_three = "Three"
#
# if type(a) == int:
#     if a > 2.5:
#         print("Hi from if scope")
#
# names = ['Doron', 'Shahar', 'Momo']
# if len(names) > 0:
#     print(names[1])

# slots = range(5)


# print(type(slots))
# print(len(slots))
# print(slots)
# print(slots[3])

# for slots in range(5):
#     print(slots)

# counter = 1
# while counter <= 10:
#     print(counter)
#     counter = counter+1

# password = "shahar"
# all_type = type(password)
# while True:
#     pass_from_user = input("enter password: ")
#     if all_type(pass_from_user) == password:
#         print("hi shahar")
#     else:
#         print("wrong password")

# # 7 boom
# boom7 = range(0, 101)
# for num in boom7:
#     if num % 7 == 0 or '7' in str(num):
#         print("BOOM!")
#     else:
#         print(num)

# def squre(x):
#     print(x * x)
#
#
# for i in range(10):
#     squre(i)
#
#
# def get_name():
#     return input('What is your name: ')
#
#
# print(f"Your name is {get_name()}")

#
# def int_to_str(num):
#     num_to_str = ["one", "two", "three", "four", "five", "six"]
#     if num > len(num_to_str):
#         return "num is not supported"
#     else:
#         return num_to_str[num - 1]
#
#
# print(int_to_str(int(input("enter number between 1-6: "))))

from lasson2_function import get_user_phone

print(get_user_phone())
