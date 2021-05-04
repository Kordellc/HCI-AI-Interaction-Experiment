import sys
import Agent as A
import Enviroment as E
import os
import csv


def writeFile(local_dir, AgentID, runnum, data):
    name = f"{AgentID}{runnum}-report.csv"
    path = os.path.join(local_dir, name)
    with open(path, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        line = ['Id', 'Score', 'Human Ctrl', 'Bot Ctrl']
        writer.writerow(line)
        # table

        a = b = c = d = e = f = 0
        for row in data:
            writer.writerow(row)
            if f < 3:
                a += row[1]
            elif f < 6:
                b += row[1]
            else:
                c += row[1]
                d += row[2]
                e += row[3]
            f += 1
        # important bits - Human avrg, AI avg, co Avg ,ov %
        line = ['User Avg', 'AI Avg', 'Co-op Avg', 'H-Frames', '% H-Active']
        writer.writerow(line)
        line = [foo(a, 3), foo(b, 3), foo(c, 3), d, foo(d, (d + e))]
        writer.writerow(line)
        # line = ['pracRuns', 'score']
        # writer.writerow(line)
        # a = 0
        # for shots in data[0]:
        #     if a >= 1:
        #         writer.writerow([a, shots])
        #     a += 1


def foo(a, b):
    return a / b if a else 0

    # of practice runs

def testRun(AgentID, runnum):
    # Use a breakpoint in the code line below to debug your script.
    # recorder
    local_dir = os.path.dirname(__file__)
    Bot_path = os.path.join(local_dir, AgentID)
    Bot = A.Agent()
    Bot.load(Bot_path)
    data = []
    # startuser training bit
    stage = True
    print("\n\n**************************************************************************************\n"
          "Your task will be to run through a game environment, then supervise an AI completing the "
                   "same course, and preventing them from making mistakes by overriding control. In this game you must go "
                   "as far as you can without hitting the yellow squares or the red line. You will submit Three runs. Use WASD to move")
    # part2- human runs
    for w in range(3):
        choice = input(f"Hit enter to begin run {w + 1}.")
        g = E.Game()
        x = True
        y = 0
        a = 0
        b = 0
        while x:
            x, y, z = g.update()
            if z:  # Override rate
                a += 1
            else:
                b += 1
        # record score
        line = [w + 1, y, a, b]
        data.append(line)
        print(f"Run{w + 1} Score:{y}")
    # part3 - AI Runs
    choice = input("now the AI will attempt their runs. You do not to to anything but watch while it completes it's run"
                   " press Enter to start.")
    g = E.Game()
    for w in range(3):
        g.reset(human=False)
        x = True
        y = 0
        a = 0
        b = 0
        while x:
            x, y, z = g.update(Bot.getOutput(g.getEnviroment()))
            if z:
                a += 1
            else:
                b += 1
        # record score
        line = [w + 1, y, a, b]
        data.append(line)
        print(f"Run Score:{y}")
    # part4 - human/AI Runs
    print("Finally, you will run co-op runs. your goal is to let the AI run as much as possible, but you have"
                   " complete override to stop it from dying\n Press Enter to start.")
    for w in range(3):
        choice = input(f"Hit enter to begin run {w + 1}.")
        g.reset()
        a = 0
        b = 0
        x = True
        y = 0
        while x:
            x, y, z = g.update(Bot.getOutput(g.getEnviroment()))
            if z:  # Override rate
                a += 1
            else:
                b += 1
        # record score
        line = [w + 1, y, a, b]
        data.append(line)
        print(f"Run Score:{y}")
    # write file
    writeFile(local_dir, AgentID, runnum, data)
    print(f"Thank you for your time. Please send the finished report, Labeled as {AgentID}{runnum}-report.csv")


def trainRun(AgentID):
    # Use a breakpoint in the code line below to debug your script.
    # recorder
    local_dir = os.path.dirname(__file__)
    Bot_path = os.path.join(local_dir, AgentID)
    Bot = A.Agent()  # call agent
    Bot.train(Bot_path)


def letMeGameMom():
    g = E.Game()
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
        testRun(parse[2], parse[3])
    else:
        letMeGameMom()
# except:
#     print("improper argument:")
