class Tabu_Search:

    def __init__(self):
        self.given_route = [1,2,3,4,5]
        self.distance_matrix = [[0,4.24,1.41,5.65,7.28] , [4.24,0,5.65,1.41,6.40] , [1.41,5.65,0,7.07,8.06] , [5.65,1.41,7.07,0,6.70] , [7.28,6.40,8.06,6.70,0]]

    def path_distance(self , route : list):
        distance = 0
        route_length = len(route)
        for i in range (0 , route_length - 1):
            distance += self.distance_matrix[route[i]-1][route[i+1]-1]
        distance += self.distance_matrix[route[-1]-1][route[0]-1]
        return distance
    
    def swap_cities(self , route : list , i , j) -> list:
        temp_route = route
        temp = temp_route[i]
        temp_route[i] = temp_route[j]
        temp_route[j] = temp

        return temp_route
    
    def all_routes(self , route:list):
        temp_solution = []
        swap_list = route.copy()
        for i in range (len(route)):
            for j in range (len(route)):
                if i == j:
                    continue
                # print(temp_solution)
                swap_list = self.swap_cities(swap_list.copy() , i , j)
                temp_solution.append(swap_list)
                # print(temp_solution)
        return temp_solution
    
    def implement_tabu(self , iterations, tabu_tenure):
        self.iterations = iterations
        best_route = self.given_route
        possible_route = self.given_route
        tabu_list = [self.given_route]

        for i in range (iterations):
            temp_sol = self.all_routes(possible_route)
            # if(temp_sol):
            possible_route = temp_sol[0]

            for path in temp_sol:
                # paths.append(paths.copy()[0])
                # print(path)
                # print(self.path_distance(path))
                if(self.path_distance(path) < self.path_distance(possible_route) and path not in tabu_list):
                    possible_route = path

                if(self.path_distance(possible_route) < self.path_distance(best_route)):
                    best_route = possible_route

                tabu_list.append(possible_route)
                if(len(tabu_list) > tabu_tenure):
                    tabu_list.pop(0)

        best_route.append(best_route.copy()[0])
        return best_route , self.path_distance(best_route)
    

if __name__ == '__main__':
    tabu = Tabu_Search()
    best , distance = tabu.implement_tabu(iterations=10000, tabu_tenure=50)
    print(f"The best path is: {best} with a distance of : {distance}")