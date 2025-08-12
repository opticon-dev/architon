# genetic_algorithm.py
import random
import math

# 목표 함수 정의
def objective_function(x, points):
    distances = [math.hypot(x[0] - pt[0], x[1] - pt[1]) for pt in points]
    radius = max(distances)  # 가장 먼 거리(반지름)
    if radius == 0:
        return float("inf")
    area = math.pi * radius**2
    return 1 / area

class GeneticAlgorithm:
    def __init__(self, population_size, generations, crossover_rate, mutation_rate, bounds, points):
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.bounds = bounds
        self.points = points

    def initialize_population(self):
        min_x, max_x, min_y, max_y = self.bounds
        return [(random.uniform(min_x, max_x), random.uniform(min_y, max_y)) for _ in range(self.population_size)]

    def evaluate_fitness(self, population):
        return [objective_function(individual, self.points) for individual in population]

    def selection(self, population, fitness):
        total_fitness = sum(fitness)
        if total_fitness == 0:
            return random.choices(population, k=self.population_size)
        selection_probs = [f / total_fitness for f in fitness]
        selected_indices = random.choices(range(self.population_size), weights=selection_probs, k=self.population_size)
        return [population[i] for i in selected_indices]

    def crossover(self, parents):
        offspring = []
        for i in range(0, self.population_size, 2):
            parent1 = parents[i % self.population_size]
            parent2 = parents[(i + 1) % self.population_size]
            if random.random() < self.crossover_rate:
                alpha = random.random()
                child1 = (alpha * parent1[0] + (1 - alpha) * parent2[0], alpha * parent1[1] + (1 - alpha) * parent2[1])
                child2 = ((1 - alpha) * parent1[0] + alpha * parent2[0], (1 - alpha) * parent1[1] + alpha * parent2[1])
                offspring.extend([child1, child2])
            else:
                offspring.extend([parent1, parent2])
        return offspring[:self.population_size]

    def mutation(self, offspring):
        min_x, max_x, min_y, max_y = self.bounds
        for i in range(len(offspring)):
            if random.random() < self.mutation_rate:
                mutation_value_x = random.uniform(-1, 1)
                mutation_value_y = random.uniform(-1, 1)
                x = offspring[i][0] + mutation_value_x
                y = offspring[i][1] + mutation_value_y
                x = max(min_x, min(max_x, x))
                y = max(min_y, min(max_y, y))
                offspring[i] = (x, y)
        return offspring

    def run(self):
        population = self.initialize_population()
        best_solutions = []
        best_individual = None
        best_fitness = -float("inf")

        for gen in range(self.generations):
            fitness = self.evaluate_fitness(population)
            max_fitness = max(fitness)
            best_index = fitness.index(max_fitness)
            if max_fitness > best_fitness:
                best_fitness = max_fitness
                best_individual = population[best_index]
            best_solutions.append(1 / best_fitness)

            parents = self.selection(population, fitness)
            offspring = self.crossover(parents)
            population = self.mutation(offspring)

        return best_individual, best_fitness, best_solutions
