import os
import neat
import visualize
import Enviroment as E
import pickle


class Agent():
    def __init__(self):
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config-FeedForward.txt")
        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_path)
        self.jumpyBoy = neat.nn.FeedForwardNetwork

    def train(self, filename):
        winner, stats = run(self.config)
        playing = True
        boy = neat.nn.FeedForwardNetwork.create(winner, self.config)
        game = E.Game()
        while playing:
            output = boy.activate(game.getEnviroment())
            finalOP = [False, False, False]
            for out in enumerate(output):
                if round(out[1]):
                    finalOP[out[0]] = True
            playing, score, _ = game.update(finalOP)
        with open(f"{filename}.pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close()
        visualize.draw_net(self.config, winner, filename=f'{filename}')
        visualize.plot_stats(stats, ylog=False, filename=f'{filename}-stats.svg')
    def load(self, filename):
        # genome = None
        with open(f"{filename}.pkl", "rb") as f:
            genome = pickle.load(f)
            f.close()
        # genomes = [(1, genome)]
        self.jumpyBoy = neat.nn.FeedForwardNetwork.create(genome, self.config)
    def getOutput(self, input):
        finalOP = [False, False, False]
        output = self.jumpyBoy.activate(input)
        finalOP = [False, False, False]
        for out in enumerate(output):
            if round(out[1]):
                finalOP[out[0]] = True
        return finalOP

def eval_genomes(genomes, config):
    nets = []
    ge = []
    games = []
    run = True
    p = False
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)  # build network
        nets.append(net)
        g.fitness = 0
        ge.append(g)
        games.append(E.Game(show=p, human=False))
        if p:
            p = False
        # games.append(E.Game(p))

    while run:
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         run = False
        #         pygame.quit()

        for x, game in enumerate(games):

            # ge[x].fitness -= .5
            # ball.move(platforms[x])
            input =  game.getEnviroment()
            output = nets[x].activate(input)
            finalOP = [False, False, False]
            for out in enumerate(output):
                if round(out[1]):
                    finalOP[out[0]] = True
            # finalOP = output.index(max(output)) + 1
            playing, score, _ = game.update(finalOP)
            # output = nets[x].activate(
            #     (ball.dx, ball.dy, abs(platforms[x].y - ball.y), abs(platforms[x].x - ball.x)))  # game imput
            # finalOP = output.index(max(output)) - 1
            #
            # platforms[x].move(finalOP)
            # platforms[x].draw(win)
            # ball.draw(win)

            if ge[x].fitness >= 100000000:
                # print("SCORE -> {}".format(balls[x].score))
                run = False
                break
            # ge[x] += .1
            # print((counts[x] - score))
            if 10000 < score < -100:
                playing = False
            if not playing: #(score+ 100):
                ge[x].fitness += game.getScore()
                # ge[x].fitness -= 5
                nets.pop(x)
                ge.pop(x)
                games.pop(x)
                # print(f"chungus - {len(games)}/20 : {score}")
        if len(games) == 0:
            run = False
            break


def run(config):

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(eval_genomes)

    # neat.save_checkpoint(config, population, species_set, generation)

    print("Best fitness -> {}".format(winner))
    return winner, stats

# if __name__ == "__main__":
#     local_dir = os.path.dirname(__file__)
#     config_path = os.path.join(local_dir, "config-FeedForward.txt")
#     run(config_path)
