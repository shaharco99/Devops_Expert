print("Hello world")
name = "shahar"
age = 25
is_male = True
old_age = 30
print(f"you are {age}")
hobbies = ["ski", "python"]
print(hobbies[0])
user = {
    "name": "shahar",
    "age": 25
}
print(f"you are {user['age']}")
client = ("shahar", 25)
print(client)
if user['age'] > old_age:
    print(f"you are old {user['age']}")
else:
    print(f"you are young only {user['age']}")
sum_age = age * 2
print(sum_age)
