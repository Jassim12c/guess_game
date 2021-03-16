#!/usr/bin/env python

from collections import OrderedDict
import random
import sys
import os
import re

def check_file_existence(file):
    if not os.path.isfile(file):
        open(file, "x")

check_file_existence("users.txt")
check_file_existence("easy.txt")
check_file_existence("normal.txt")
check_file_existence("hard.txt")
# Clears Terminal.


def clear():
    if sys.platform == "win32":
        os.system('cls')
    elif sys.platform == "darwin" or sys.platform == "linux":
        os.system('clear')


# Getting username
username = input("Hello! Welcome to guess the number! please enter your username: \n> ").strip()
clear()

# lst is for the usernames in users.txt
lst = []

# taking names from users.txt file then appending them to lst
with open('users.txt', 'r') as a_file:
    for line in a_file:
        data = re.findall(r'^\w+', line)
        listToStr = ' '.join(map(str, data))
        lst.append(listToStr)

# Checking if the username is taken or if they didn't enter one
while username == "" or username in lst:
    username = input("The usernmame is Invalid or Taken.\nPlease enter a valid username: \n> ").strip()
    clear()


# Skipping the '__init__' in the class Play. If it's not skipped 'ask' will print right after the 'username'.
def skip_init(cls):
    """Skips Play()'s init"""
    actual_init = cls.__init__
    cls.__init__ = lambda *args, **kwargs: None
    instance = cls()
    cls.__init__ = actual_init
    return instance


# class for asking the user which difficulty/level he wants to play in
class Play:
    def __init__(self, ask):
        self.ask = ask

    def start(self):
        """Start the game"""
        self.ask = input("""
Choose a difficulty:
            1- (Easy) 1-10
            2- (Normal) 1-15
            3- (Hard) 1-25
> """).lower().strip()

        if self.ask == "easy":
            game.difficulty_easy()

        elif self.ask == "normal":
            game.difficulty_normal()

        elif self.ask == "hard":
            game.difficulty_hard()

        elif self.ask == "quit":
            self.ask = -1
            return menu_loop()


# The game loop (starts after the difficulty is chosen).
class Game:
    def __init__(self, tries=0):
        self.tries = tries

    def guess_loop(self, num, guess_number_text):
        guess = None
        self.tries = 0

        try:
            while guess != num:
                guess = int(input(f"Guess {guess_number_text} \n>"))
                if guess > num:
                    self.tries += 1
                    print("It's lower! try again!")
                elif guess < num:
                    self.tries += 1
                    print("It's higher! try again!")
            else:
                self.tries += 1
                print("CONGRATS! you got the correct number.")
                print(f"It took you {self.tries} attempt(s). \n")
                return menu_loop()
        except ValueError as error:
            print(f"ERROR! Please type a number. \n{error}")

    @staticmethod
    def difficulty_easy():
        easy_number = random.randint(1, 10)
        easy_text = "between 1 and 10"
        game.guess_loop(easy_number, easy_text)

    @staticmethod
    def difficulty_normal():
        normal_number = random.randint(1, 15)
        normal_text = "between 1 and 15"
        game.guess_loop(normal_number, normal_text)

    @staticmethod
    def difficulty_hard():
        hard_number = random.randint(1, 25)
        hard_text = "between 1 and 25"
        game.guess_loop(hard_number, hard_text)


# The user's score in each level.
user_score = {'easy': 0, 'normal': 0, 'hard': 0}

game = Game()

P = skip_init(Play)


# function explained:
def get_scores():
    # taking the amount of tries/attempts that took to find the number
    tried = getattr(game, 'tries')
    # taking the input(difficulty) that was given.
    answer = getattr(P, 'ask')

    try:
        # Checking if the difficulty's score is zero (program won't work properly if I take that if statement out)
        # Example: answer = "easy". checks if "answer's" (which is a key in dict(user_score)) value is 0. if it is:
        if user_score[answer] == 0:
            # the key's ('easy' in our case') value is gonna equal that amount of tries
            user_score[answer] = tried
        # Checks if the key's value is bigger than tried (amount of tries).
        # Example: {key: 6}, tried = 4. if "tried" is lower than 6 (it is):
        if user_score[answer] > tried:
            # The key's value will be 4
            user_score[answer] = tried
        # but if tried isn't lower than the key's value, nothing will happen
        else:
            pass
    except KeyError:
        pass


# This function prints the player's top score in each difficulty.
def scores():
    """Your top scores"""
    d_scores = OrderedDict(user_score)

    for keys, values in d_scores.items():
        print("Your highest score:")
        print(f'{keys.title()}: {values}\n')
    return menu_loop()


# Main menu loop
def menu_loop():
    # updates scores every time the function menu_loop() runs
    try:
        get_scores()
    except AttributeError:
        pass

    print(f"\nHi {username.title()}! please choose one of the options below to continue.\n")

    for key, value in menu.items():
        print(f'<>{key}<> {value.__doc__}')

    choice = input("> ").lower().strip()
    while choice != "quit":
        if choice in menu:
            clear()
            menu[choice]()
        elif choice not in menu:
            print("Please enter one of the options above.")
            choice = input("> ").lower().strip()
    else:
        quit_game()


def help_list():
    """Help menu"""
    print("""
1- You have to find the correct number.
2- There are 3 levels (easy, normal and hard)
3- A- (easy) is from 1-10. 
   B- (normal) is from 1-15. 
   C- (hard) is from 1-25
4- Your scores will be added after you quit
""")
    return menu_loop()


def put_leaderboard():
    with open('easy.txt', 'a') as e_lfile:
        e_lfile.write(username + ":" + str(user_score['easy']) + "\n")
    with open('normal.txt', 'a') as n_lfile:
        n_lfile.write(username + ":" + str(user_score['normal']) + "\n")
    with open("hard.txt", 'a') as h_lfile:
        h_lfile.write(username + ":" + str(user_score['hard']) + "\n")


def get_leaderboard(dif_text):
    e_data = dif_text

    take_score = re.findall(r'\w+', e_data)
    for _ in take_score:
        ','.join(take_score)
        take_score = take_score

    get = [int(num) if num.isdigit() else num for num in take_score]
    player_scores = []
    player_name = []

    for x in get:
        if isinstance(x, int):
            player_scores.append(x)
        else:
            player_name.append(x)

    def sortSecond(val):
        return val[1]

    b_d = zip(player_name, player_scores)
    b_d = list(b_d)
    b_d.sort(key=sortSecond)

    for f in b_d:
        if f[1] == 0:
            pass
        else:
            print(f)

    return menu_loop()


def leaderboard():
    """Leaderboard"""

    choose = input("""
Choose:
    -Easy
    -Normal
    -Hard
> """).lower()

    if choose == "easy":
        easy_file = open("easy.txt", encoding="utf-8")
        easy_file_data = easy_file.read()
        easy_file.close()
        get_leaderboard(easy_file_data)

    elif choose == "normal":
        normal_file = open("normal.txt", encoding='utf-8')
        normal_file_data = normal_file.read()
        normal_file.close()
        get_leaderboard(normal_file_data)

    elif choose == "hard":
        hard_file = open("hard.txt", encoding='utf-8')
        hard_file_data = hard_file.read()
        hard_file.close()
        get_leaderboard(hard_file_data)


def quit_game():
    """Quit Game"""
    put_leaderboard()
    # After quitting the program via typing "quit". the username and user's top scores will be taken and saved in .txt.
    print("Thank you for playing! Come back again!")

    user = f'{username}: {user_score}'
    with open('users.txt', 'a') as tfile:
        tfile.write(f"{user}\n")
    tfile.close()
    sys.exit(0)


menu = OrderedDict([
    ('play', P.start),
    ('help', help_list),
    ('scores', scores),
    ('leaderboard', leaderboard),
    ('quit', quit_game),
])

if __name__ == "__main__":
    clear()
    menu_loop()
