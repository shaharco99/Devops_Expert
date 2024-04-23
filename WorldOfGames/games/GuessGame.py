from random import randrange
from games.Live import valid_num
from MainScores import add_score


def generate_number(diff):
    # This function generate a number
    secret_number = randrange(1, int(diff) + 1)
    return int(secret_number)


def get_guess_from_user(diff):
    # This function let the user choose a number between 1 to (diff) + 1
    user_number = input(f"Choose a number between 1 to {int(diff) + 1}: ")
    return int(valid_num(1, diff + 1, user_number))


def compare_results(secret_number, user_number):
    """This function compare secret_number user_number"""
    return bool(secret_number == user_number)


def play(diff,name):
    # This function plays the game GuessGame
    is_equal = compare_results(generate_number(diff), get_guess_from_user(diff))
    if is_equal:
        # print("you won")
        add_score(diff,name)
    else:
        print("you lost")
