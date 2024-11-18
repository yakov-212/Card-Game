import random
import PlayerInfo as p


class Card:
    face_cards = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace',
                  'jack': 11, 'queen': 12, 'king': 13, 'ace': 14}

    def __init__(self, num, suit):
        self.num = num
        self.suit = suit

    def __str__(self):
        if self.num in self.face_cards:
            return f'The {self.face_cards[self.num]} of {self.suit}'
        else:
            return f'The {self.num} of {self.suit}'


def new_deck():
    suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
    deck = [Card(num, suit) for num in range(2, 15) for suit in suits]
    return deck


def deal_card(deck):
    if len(deck) == 0:
        return None
    rand = random.randint(0, len(deck) - 1)
    card = deck[rand]
    deck.remove(card)
    return card


def dots():
    print("...." * 15)


def guess(prompt, question):
    allowed = {"rb": [["red", "r", ], ["black", "b"]],
               "ou": [["over", "o", ], ["under", "u"]],
               "io": [["inbetween", "in", "i"], ["outside", "out", "o"]],
               "st": [["spades", "spade", "s"], ["clubs", "club", "c"],
                      ["diamonds", "diamond", "d"], ["hearts", "heart", "h"]]
               }
    while True:
        answer = input(prompt)
        for i in allowed[question]:
            for a in i:
                if a == answer.lower():
                    return i[0]
        print("That Was Not an Acceptable Answer")
        dots()


def red_black(card):
    answer = guess('Guess if The Next Card Will be Red or Black: ', "rb")
    color = {"red": ("Diamonds", "Hearts"), "black": ("Spades", "Clubs")}
    if card.suit in color["red"] and answer == "red":
        t = True
    elif card.suit in color["black"] and answer == "black":
        t = True
    else:
        t = False
    if t:
        print("Correct\n"
              f"The Card Was {card}")
    else:
        print("Incorrect\n"
              f"The Card Was {card}")
    return t


def over_under(card, last_card):
    answer = guess(f"Guess if The Next Card Will be Over or Under {last_card}: ", "ou")
    if answer == "over" and card.num >= last_card.num:
        t = True
    elif answer == "under" and card.num <= last_card.num:
        t = True
    else:
        t = False
    if t:
        print("Correct\n"
              f"The Card Was {card} Which is {answer.capitalize()} {last_card}")
    else:
        print("Incorrect\n"
              f"The Card Was {card} Which is Not {answer.capitalize()} {last_card}")
    return t


def inbetween_outside(card, last_card, two_cards_ago):
    answer = guess(f"Guess if The Next Card Will be Inbetween or Outside {last_card} And {two_cards_ago}: ", "io")
    print(answer)
    if answer == "inbetween" and two_cards_ago.num <= card.num <= last_card.num \
            or answer == "inbetween" and last_card.num <= card.num <= two_cards_ago.num:
        t = True
    elif answer == "outside" and two_cards_ago.num > card.num < last_card.num \
            or answer == "outside" and last_card.num < card.num > two_cards_ago.num:
        t = True
    else:
        t = False
    if t:
        print("Correct\n"
              f"The Card Was {card} Which is {answer.capitalize()} {last_card} and {two_cards_ago}")
    else:
        print("Incorrect\n"
              f"The Card Was {card} Which is Not {answer.capitalize()} {last_card} and {two_cards_ago}")
    return t


def guess_suit(card):
    answer = guess("Guess The Suit: ", "st")
    if card.suit == answer.capitalize():
        t = True
    else:
        t = False
    if t:
        print("Correct\n"
              f"The Card Was {card}")
    else:
        print("Incorrect\n"
              f"The Card Was {card}")
    return t


def main():
    score = 0
    deck = new_deck()
    card = deal_card(deck)
    last_card = card
    correct = red_black(card)
    dots()
    if correct:
        score += 1
        card = deal_card(deck)
        correct = over_under(card, last_card)
        two_cards_ago = last_card
        last_card = card
        dots()
    if correct:
        score += 1
        card = deal_card(deck)
        correct = inbetween_outside(card, last_card, two_cards_ago)
        two_cards_ago = last_card
        last_card = card
        dots()
    if correct:
        score += 1
        card = deal_card(deck)
        correct = guess_suit(card)
        dots()
    while correct:
        score += 1
        rand = random.randint(1, 21)
        two_cards_ago = last_card
        last_card = card
        card = deal_card(deck)
        if rand < 8:
            correct = red_black(card)
        elif rand < 15:
            correct = over_under(card, last_card)
        elif rand < 19:
            correct = inbetween_outside(card, last_card, two_cards_ago)
        else:
            correct = guess_suit(card)
        dots()
    return score


def name():
    name = input("whats your name: ")
    if name in p.players and p.highscore > 0:
        if p.players[name] == p.highscore:
            print(f"{name.capitalize()} Has The Highscore of {p.highscore}")
        else:
            for names in p.players:
                if p.players[names] == p.highscore:
                    print(f"{names.capitalize()} Has The Highscore of {p.players[names]}")
        if p.highscore > p.players[name] > 0:
            print(f"{name} You Have a Personal Highscore of {p.players[name]}")
    dots()
    return name


def reset_file(save):
    with open(save, "w") as file:
        file.write("players = {}")
        file.write("highscore = 0")


def save_player_info(saved_file, name, score):
    if name not in p.players:
        p.players[name] = score
    elif p.players[name] < score:
        p.players[name] = score
    if score > p.highscore:
        p.highscore = score
    with open("PlayerInfo.py", "w") as file:
        file.write(f"players = {p.players}\n")
        file.write(f"highscore = {p.highscore}\n")


def play_again():
    again = input("Would you like to play again? (y/n): ")
    while again.lower() not in ["y", "n"]:
        print("Please enter either 'y' or 'n'")
        again = input("Would you like to play again? (y/n): ")
    if again.lower() == 'y':
        print("<><>"*15)
        return True
    elif again.lower() == 'n':
        return False
