import numpy as np
import matplotlib.pyplot as plt

def distance_two_cities(city1 , city2):
    return np.sqrt(np.sum((city1 - city2)**2))

def plot_cities(city_coords):
    plt.figure(figsize=(8, 6))
    plt.scatter(city_coords[:, 0], city_coords[:, 1], c='r', marker='o')

    for i in range(len(city_coords)-1):
      plt.plot([city_coords[i, 0], city_coords[i+1, 0]],[city_coords[i, 1], city_coords[i+1, 1]],
                  c='b', linestyle='-', linewidth=1)
    plt.plot([city_coords[i+1, 0], city_coords[0, 0]],[city_coords[i+1, 1], city_coords[0, 1]],
                  c='b', linestyle='-', linewidth=1)

    for i in range(len(city_coords)): 
      plt.annotate(i+1, (city_coords[i,0], city_coords[i,1] + 0.02))
    plt.xlabel('X Label')
    plt.ylabel('Y Label')
    plt.title('Cities and Connections')
    plt.show()

def aco(city_cords , ants , iterations ,beta , alpha , evaporation_rate):
    no_of_cities = len(city_cords)
    pheromone_matrix = np.ones((no_of_cities , no_of_cities))
    best_route = None
    best_route_distance = 1000000

    for i in range (iterations):
        paths = {}

        for ant in range(ants):
            cities_visited = np.zeros(no_of_cities)
            start_city = np.random.randint(no_of_cities)
            cities_visited[start_city] = 1
            ant_path = [start_city]
            ant_path_dist = 0
            current_city = start_city

            while(0 in cities_visited):
                unvisited_cities = np.where(np.logical_not(cities_visited))[0]
                next_city_probability = np.zeros(len(unvisited_cities))

                for i , unvisited_city in enumerate(unvisited_cities):
                    next_city_probability[i] = (pheromone_matrix[current_city][unvisited_city])**alpha / (distance_two_cities(city_cords[current_city] , city_cords[unvisited_city]))**beta
                    
                next_city_probability = next_city_probability / np.sum(next_city_probability)

                next_city = np.random.choice(a=unvisited_cities , p=next_city_probability)
                ant_path.append(next_city)
                ant_path_dist += distance_two_cities(city_cords[current_city] , city_cords[next_city])
                current_city = next_city
                cities_visited[current_city] = 1

            ant_path.append(ant_path[0])
            ant_path_dist += distance_two_cities(city_cords[current_city] , city_cords[start_city])
            paths[frozenset(ant_path)] = ant_path_dist

            if(ant_path_dist < best_route_distance):
                best_route_distance = ant_path_dist
                best_route = ant_path

        pheromone_matrix *= evaporation_rate

        for path in paths:
            path_list = list(path)
            for i in range(no_of_cities-1):
                pheromone_matrix[path_list[i]][path_list[i + 1]] += 1 / paths[path]
            pheromone_matrix[path_list[-1]][path_list[0]] += 1 / paths[path]

    print(f"{best_route} and distance: {best_route_distance}")

    plot_cities(points)

    
    plt.figure(figsize=(8, 6))
    plt.scatter(points[:, 0], points[:, 1], c='r', marker='o')
    
    for i in range(no_of_cities):
        plt.plot([points[best_route[i], 0], points[best_route[i+1], 0]],
                 [points[best_route[i], 1], points[best_route[i+1], 1]],
                 c='g', linestyle='-', linewidth=1)
    
    plt.xlabel('X Label')
    plt.ylabel('Y Label')
    plt.title('Optimized Connections b/w Cities')
    plt.show()

points = np.random.rand(10, 2)
aco(points, ants=10, iterations=10, alpha=1, beta=1, evaporation_rate=0.5)