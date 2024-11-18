import Benami_funcs as b

if __name__ == "__main__":
    play = True
    while play:
        name = b.name()
        score = b.main()
        print(f"{name} has a score of {score}")
        b.save_player_info("PlayerInfo.py", name, score)
        play = b.play_again()

