import random

num_of_cities = 5
cities = "12345"
start_city = "1"
population_size = 10

distance_matrix = [
    [0, 2, 4, 1, 7],
    [2, 0, 5, 2, 6],
    [4, 5, 0, 8, 3],
    [1, 2, 8, 0, 4],
    [7, 6, 3, 4, 0]
]

# Structure of an individual in the population
class Individual:
    def __init__(self, gnome=None):
        if gnome is None:
            self.gnome = [start_city] + random.sample(cities.replace(start_city, ""), num_of_cities - 1)
        else:
            self.gnome = gnome
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        total_distance = 0
        for i in range(num_of_cities - 1):
            current_city = self.gnome[i]
            next_city = self.gnome[i + 1]
            total_distance += distance_matrix[cities.index(current_city)][cities.index(next_city)]
        return 1 / total_distance  # Inverse of distance as fitness

def crossover(parent1, parent2):
    # Perform ordered crossover
    start = random.randint(0, num_of_cities - 1)
    end = random.randint(start + 1, num_of_cities)
    child_gnome = [None] * num_of_cities

    # Copy genetic material from parent1
    child_gnome[start:end] = parent1.gnome[start:end]

    # Fill in the rest from parent2
    index = end
    for city in parent2.gnome[end:] + parent2.gnome[:end]:
        if city not in child_gnome:
            child_gnome[index % num_of_cities] = city
            index += 1

    return Individual(child_gnome)

def mutate(individual):
    # Perform swap mutation
    index1, index2 = random.sample(range(num_of_cities), 2)
    individual.gnome[index1], individual.gnome[index2] = individual.gnome[index2], individual.gnome[index1]

# Genetic Algorithm main loop
def genetic_algorithm():
    population = [Individual() for _ in range(population_size)]
    generations = 1000  # Adjust as needed

    for generation in range(generations):
        population.sort(key=lambda x: x.fitness, reverse=True)

        # Perform crossover and mutation to create the next generation
        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = random.sample(population[:population_size // 2], 2)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            mutate(child1)
            mutate(child2)
            new_population.extend([child1, child2])

        population = new_population

        # Print the best route in each generation
        best_route = population[0]
        # print(f"Generation {generation + 1}: Best Route = {best_route.gnome}, Fitness = {best_route.fitness}")

    # Return the best route found
    return population[0]

if __name__ == "__main__":
    best_route = genetic_algorithm()

    print("\nBest Route:", best_route.gnome)