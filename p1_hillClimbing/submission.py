import json
import os
import sys
import graderUtil
import numpy as np

# a dict stores the final result
task_result = {
    "ini_cost": -1,
    "best_cost": -1,
    "locations": []
} 

#######################################################################
# read task file content
#task_file = sys.argv[1]
tasks = ["task_0_0.txt", "task_0_1.txt", "task_1_0.txt", "task_1_1.txt", "task_2_1.txt", "task_3_1.txt"]
task_file = tasks[2]
task_content = graderUtil.load_task_file(task_file)
if task_content:
    print(task_content)
# BEGIN_YOUR_CODE

# TODO
# multiple initial states?
# get_neighbors(park, "restroom"), r_list?
# random_start

# hill climbing algorithm
def hill_climbing(park):
    r_list = park.restrooms  # initial solution
    p_list = park.playgrounds
    while True:
        # identify the type of algorithm to use
        if park.algo_code == '0':  # simple search
            neighbors = get_neighbors(park, r_list)  # get neighbors of r
        elif park.algo_code == '1':  # random search
            neighbors = random_start()  # random generate start point
        else:
            print("ERROR: Unknown algorithm type.")
            return

        # implement the algorithm
        for i in range(len(r_list)):
            orig_state = r_list[i]
            orig_cost = park.cost()

            distance = [calc_dist(n, p_list) for n in neighbors]  # evaluate total distance for each neighbor
            best_neighbor = neighbors[np.argmin(distance)]  # get the minimum distance neighbor
            r_list[i] = best_neighbor
            if park.cost() >= orig_cost:  # if the best neighbor isn't better than the original state, stop
                r_list[i] = orig_state
                return park.cost(), [[r.x, r.y] for r in r_list]  # return best_cost and locations of the task_result
            # otherwise, continue with the best neighbor

def calc_dist(r, p_list):
    dist = 0
    for p in p_list:
        dist += graderUtil.manhattan_dist(p, r)
    return dist

def get_neighbors(park, r_list):
    neighbours = []
    for r in r_list:
        x = r.x  # current state coordinates
        y = r.y
        modifications = [-1, 0, 1]  # the neighbor is within the nine-square grid of the current state.

        # get neighbors' locations
        for i in modifications:
            x_new = x + i
            if not x_new < 0 and not x_new > park.num_rows - 1:  # exclude locations outside the borders
                for j in modifications:
                    y_new = y + j
                    if not y_new < 0 and not y_new > park.num_cols - 1:
                        neighbours.append([x_new, y_new])

        # remove unavailable locations
        neighbours.remove([x, y])
        for p in park.playgrounds:
            if [p.x, p.y] in neighbours:
                neighbours.remove([p.x, p.y])

    return [graderUtil.Restroom(item) for item in neighbours]

def random_start(park, restroom):
    return 0

# task_0_0
park1 = graderUtil.Park(task_content)
task_result["ini_cost"] = park1.cost()
task_result["best_cost"], task_result["locations"] = hill_climbing(park1)

#task_result["best_cost"] = 7
#task_result["locations"] = [[2,1]]


#task_result["ini_cost"] = 9
#task_result["best_cost"] = 7
#task_result["locations"] = [[0,1],[1,2]]

#task_result["best_cost"] = 5
#task_result["locations"] = [[1,0],[2,1]]


# END_YOUR_CODE
#######################################################################

# output your final result
print(json.dumps(task_result))