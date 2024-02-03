from pathlib import Path

scores_file_name = Path(__file__).parent / "./Scores.txt"



def add_score(diff):
    """add the points_of_winning to score"""
    try:
        cur_score = read_score()
        new_score = cur_score + ((diff * 3) + 5)
        file = open(scores_file_name, 'w')
        file.write(str(new_score))
        print(f"your new score is {new_score}")
        file.close()
    except FileNotFoundError:
        print(f"Something went wrong when adding the score to {scores_file_name} please check the file path")


def read_score():
    """read the score"""
    file = open(scores_file_name)
    read = file.readlines()
    for line in read:
        return int(line)
    file.close()
