def get_user_phone():
    while True:
        num = input("what is your phone number: ")
        if num.isdigit():
            return num
