from application import *
from genNumbers_PersonEntrance import genPersonData


def main():
    user_input = input("Time in Format: YYYY-MM-DD HH:mm:ss\n")
    # genPersonData()  # remove comment to generate new

    context = QApplication([])
    context.setStyle('Fusion')
    our_app = AssetApplication(user_input)
    our_app.show()
    context.exec()


if __name__ == "__main__":
    main()
