import sys
import Agent
import Enviroment as E


def testRun():
    # Use a breakpoint in the code line below to debug your script.
    # recorder
    Bot = Agent()  # call agent
    for i in enumerate(3):
        E.Game(1)
def trainRun():
    # Use a breakpoint in the code line below to debug your script.
    # recorder
    Bot = Agent()  # call agent
    for i in enumerate(3):
        E.Game(1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        parse = sys.argv
        if parse[0] == "-t":
            trainRun()
        elif parse[0] == "-r":
            testRun()
    except:
        print("improper commands")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
