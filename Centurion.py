import os
from core.Bot import Bot
from sys import platform


def main():

    try:
        token = os.environ["TOKEN"]
        centurion = Bot()
        centurion.init(token)
    except:
        error = "Failed to retrieve bot token from Environment variable\nYou can set the bot token with:\n\n".upper()

        if platform == "linux" or platform == "linux2":
            # linux
            error += "export TOKEN=your_token"
            exit(error)
        elif platform == "darwin":
            # OS X
            error += "export TOKEN=your_token"
            exit(error)
        elif platform == "win32":
            # Windows
            error += "set TOKEN=your_token"
            exit(error)


if __name__ == "__main__":
    main()
