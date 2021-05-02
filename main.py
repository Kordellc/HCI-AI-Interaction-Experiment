import sys
import Agent as A
import Enviroment as E
import os
import keyboard

def testRun(AgentID):
    # Use a breakpoint in the code line below to debug your script.
    # recorder
    local_dir = os.path.dirname(__file__)
    Bot_path = os.path.join(local_dir, AgentID)
    Bot = A.Agent()
    Bot.load(Bot_path)
    # # startuser training bit
    # stage = True
    # while stage:
    #

    game = E.Game()
    playing = True
    score = 0
    while playing:
        playing, score, _ = game.update(Bot.getOutput(game.getEnviroment()))
    print(score)


def trainRun(AgentID):
    # Use a breakpoint in the code line below to debug your script.
    # recorder
    local_dir = os.path.dirname(__file__)
    Bot_path = os.path.join(local_dir, AgentID)
    Bot = A.Agent()  # call agent
    Bot.train(Bot_path)


def letMeGameMom():
    g = E.Game()
    x = True
    while E.running:
        g.reset()
        x = True
        y = 0
        while x:
            x, y, _ = g.update()
        print(y)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # try:
    parse = sys.argv
    if parse[1] == "-t":
        trainRun(parse[2])
    elif parse[1] == "-r":
        testRun(parse[2])
    else:
        letMeGameMom()
# except:
#     print("improper commands:")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
