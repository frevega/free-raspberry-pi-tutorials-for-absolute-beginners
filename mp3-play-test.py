from pygame import mixer
# import os

# user = os.getlogin()
# user_home = os.path.expanduser(f"~{user}")


if __name__ == "__main__":
    mixer.init()

    try:
        # mixer.music.load(f"{user_home}/Downloads/burglar_alarm.mp3")
        mixer.music.load("resources/burglar_alarm.mp3")
        mixer.music.set_volume(0.5)
        mixer.music.play(-1)

        while True:
            pass
    except KeyboardInterrupt:
        mixer.music.stop()
        print("\nSee you later RPi!")