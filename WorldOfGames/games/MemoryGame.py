from random import randrange
from time import sleep
from games.Live import valid_num
from Score import add_score
from os import system


def screen_cleaner():
    system('clear')


def generate_sequence(diff):
    """This function generates a sequence of number * diff times"""
    list_of_nums = []
    i = 1
    while i <= diff:
        list_of_nums.append(int(randrange(1, 101)))
        i = i + 1
    print(list_of_nums)
    sleep(0.7)
    screen_cleaner()
    return list_of_nums


def get_list_from_user(diff):
    """This function asks the user of a sequence of number * diff times"""
    i = 1
    list_of_user = []
    while i <= diff:
        new_input = valid_num(1, 101, input("Enter number from 1 - 101: "))
        list_of_user.append(int(new_input))
        i = i + 1
    return list_of_user


def is_list_equal(list_of_nums, list_of_user):
    """This function checks if lists are equal"""
    if list_of_nums == list_of_user:
        list_equal = True
    else:
        list_equal = False
    return list_equal


def play(diff):
    """This function plays the game MemoryGame"""
    list_equal = is_list_equal(generate_sequence(diff), get_list_from_user(diff))
    if list_equal:
        # print("you won")
        add_score(diff)
    else:
        print("you lost")
