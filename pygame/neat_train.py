# neat_train.py
import neat
import os
from env import SimpleGridEnv

# --- util: escribe un config básico si no existe ---
DEFAULT_CONFIG = """\
[NEAT]
fitness_criterion     = max
fitness_threshold     = 4.5
pop_size              = 50
reset_on_extinction   = False

[DefaultGenome]
# Tamaños
num_inputs            = 7
num_outputs           = 4
num_hidden            = 0

# Topología inicial
feed_forward          = True
initial_connection    = full_direct

# Activaciones y agregación
activation_default    = sigmoid
activation_mutate_rate= 0.0
activation_options    = sigmoid

aggregation_default   = sum
aggregation_options   = sum

# Bias
bias_init_mean        = 0.0
bias_init_stdev       = 1.0
bias_max_value        = 30.0
bias_min_value        = -30.0
bias_mutate_power     = 0.5
bias_mutate_rate      = 0.7
bias_replace_rate     = 0.1

# Compatibilidad
compatibility_disjoint_coefficient = 1.0
compatibility_weight_coefficient   = 0.5

# Mutaciones estructurales
conn_add_prob         = 0.3
conn_delete_prob      = 0.2
node_add_prob         = 0.2
node_delete_prob      = 0.1

# Conexiones
enabled_default       = True
enabled_mutate_rate   = 0.01

# Respuesta (no suele usarse, pero inofensivo)
response_init_mean    = 1.0
response_init_stdev   = 0.0
response_max_value    = 30.0
response_min_value    = -30.0
response_mutate_power = 0.0
response_mutate_rate  = 0.0
response_replace_rate = 0.0

# Pesos
weight_init_mean      = 0.0
weight_init_stdev     = 1.0
weight_max_value      = 30
weight_min_value      = -30
weight_mutate_power   = 0.5
weight_mutate_rate    = 0.8
weight_replace_rate   = 0.1

[DefaultSpeciesSet]
compatibility_threshold = 3.0

[DefaultStagnation]
species_fitness_func = max
max_stagnation       = 15
species_elitism      = 1

[DefaultReproduction]
elitism              = 2
survival_threshold   = 0.2
"""


def ensure_config(path="neat-config.ini"):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(DEFAULT_CONFIG)
    return path


# --- evaluación de un genoma ---
def eval_genome(genome, config, episodes=3):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    total_fitness = 0.0
    for _ in range(episodes):
        env = SimpleGridEnv()
        obs = env.reset()
        done = False
        while not done:
            # red -> 4 salidas, elegimos argmax como acción
            out = net.activate(obs)
            action = max(range(len(out)), key=lambda i: out[i])
            obs, reward, done, info = env.step(action)
            total_fitness += reward
    # fitness medio por episodio
    return total_fitness / episodes


def eval_genomes(genomes, config):
    for gid, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run():
    cfg_path = ensure_config()
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, cfg_path)

    pop = neat.Population(config)
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)

    winner = pop.run(eval_genomes, n=50)  # 50 generaciones como demo

    # guarda al mejor
    import pickle
    with open("best-genome.pkl", "wb") as f:
        pickle.dump(winner, f)
    print("Winner saved to best-genome.pkl")


if __name__ == "__main__":
    run()
