import numpy as np
import tensorflow as tf
from tensorflow.keras.models import clone_model
from snake import gameloop

# Número de redes na população
POPULATION_SIZE = 20
# Taxa de mutação
MUTATION_RATE = 0.1
# Número de gerações
GENERATIONS = 50

# Função para criar uma população inicial
def create_population():
    population = []
    for _ in range(POPULATION_SIZE):
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(2,)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(4, activation='softmax')
        ])
        population.append(model)
    return population

# Avaliar o desempenho da rede
def evaluate(model):
    return gameloop(model)

# Selecionar os melhores modelos
def select_parents(population, fitness_scores, tournament_size=3):
    selected_parents = []
    population_size = len(population)

    for _ in range(population_size):
        indices = np.random.choice(range(population_size), tournament_size, replace=False)
        best_individual_idx = indices[np.argmax([fitness_scores[i] for i in indices])]
        selected_parents.append(population[best_individual_idx])

    return selected_parents

# Crossover entre dois modelos
def crossover(parent1, parent2):
    child = clone_model(parent1)
    weights1 = parent1.get_weights()
    weights2 = parent2.get_weights()
    new_weights = []
    for w1, w2 in zip(weights1, weights2):
        mask = np.random.randint(0, 2, w1.shape)
        new_weight = mask * w1 + (1 - mask) * w2
        new_weights.append(new_weight)
    child.set_weights(new_weights)
    return child

# Mutação no modelo
def mutate(model):
    weights = model.get_weights()
    new_weights = []
    for weight in weights:
        if np.random.rand() < MUTATION_RATE:
            mutation = np.random.normal(0, 1, weight.shape)
            new_weight = weight + mutation
        else:
            new_weight = weight
        new_weights.append(new_weight)
    model.set_weights(new_weights)

# Algoritmo Genético
def genetic_algorithm():
    population = create_population()
    for generation in range(GENERATIONS):
        fitness_scores = [evaluate(model) for model in population]
        parents = select_parents(population, fitness_scores)
        new_population = []
        for p in range(POPULATION_SIZE // 2):
            print(generation+1, p+1)
            parent1, parent2 = np.random.choice(parents, 2, replace=False)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent1, parent2)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])
        population = new_population

# Executar o algoritmo genético
genetic_algorithm()
