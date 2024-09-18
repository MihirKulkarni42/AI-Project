import numpy as np
import matplotlib.pyplot as plt

def calculate_travel_distance(layout):
    storage_coords = np.argwhere(layout == 1)
    num_storage = len(storage_coords)

    if num_storage < 2:
        return 0
    
    total_distance = 0
    for i in range(num_storage - 1):
        for j in range(i + 1, num_storage):
            distance = np.linalg.norm(storage_coords[i] - storage_coords[j])
            total_distance += distance
    
    return total_distance

def acceptance_probability(current_distance, new_distance, temperature):
    if new_distance < current_distance:
        return 1.0
    return np.exp((current_distance - new_distance) / temperature)

def explore_layout(layout):
    new_layout = np.copy(layout)
    row1, col1 = np.random.randint(layout.shape[0]), np.random.randint(layout.shape[1])
    row2, col2 = np.random.randint(layout.shape[0]), np.random.randint(layout.shape[1])
    new_layout[row1, col1], new_layout[row2, col2] = new_layout[row2, col2], new_layout[row1, col1]
    return new_layout

def simulated_annealing(initial_layout, temperature, cooling_rate, iterations):
    current_layout = np.copy(initial_layout)
    current_distance = calculate_travel_distance(current_layout)

    for _ in range(iterations):
        new_layout = explore_layout(current_layout)
        new_distance = calculate_travel_distance(new_layout)

        if acceptance_probability(current_distance, new_distance, temperature) > np.random.rand():
            current_layout = np.copy(new_layout)
            current_distance = new_distance

        temperature *= cooling_rate

    return current_layout

initial_layout = np.array([
    [1, 0, 0, 1, 1],
    [0, 1, 0, 0, 0],
    [1, 0, 1, 0, 0],
    [1, 0, 0, 1, 0],
])

initial_temperature = 100.0
cooling_rate = 0.99
iteration_values = [10, 100, 1000, 10000]

for iteration in iteration_values:
    optimized_layout = simulated_annealing(initial_layout, initial_temperature, cooling_rate, iteration)

    initial_distance = calculate_travel_distance(initial_layout)
    optimized_distance = calculate_travel_distance(optimized_layout)

    print(f"\n No. of iterations: {iteration}\n")
    print("------Initial Layout-------")
    print(initial_layout)
    print("\nInitial Travel Distance:", initial_distance)
    print("\n-------Optimized Layout--------")
    print(optimized_layout)
    print("Optimized Travel Distance:", optimized_distance)

results = []
results.append(calculate_travel_distance(initial_layout))
index1 = [1,2,3,4,5]
index = [1,10,100,1000,10000]
for iterations in iteration_values:
    optimized_layout = simulated_annealing(initial_layout, initial_temperature, cooling_rate, iterations)
    optimized_distances = calculate_travel_distance(optimized_layout)
    results.append(optimized_distances)
plt.plot(index, results,label=f"Optimized Distance", color = 'red', linestyle='-')
plt.ylim(30, 90)
plt.xscale('log')
plt.xlabel("Iterations")
plt.ylabel("Optimized Distance")
plt.title("Simulated Annealing Optimization")
plt.legend()
plt.show()