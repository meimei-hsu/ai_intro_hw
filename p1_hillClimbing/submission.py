import json
import os
import sys
import graderUtil
import numpy as np
import random as rand

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
task_file = tasks[4]
task_content = graderUtil.load_task_file(task_file)
if task_content:
    print(task_content)

# BEGIN_YOUR_CODE
def random_restart(park, iteration):
    n_times = int(iteration)
    avail_areas = [[i, j] for i in range(park.num_rows) for j in range(park.num_cols)]  # list of areas from given size
    for p in park.playgrounds:
        avail_areas.remove([p.x, p.y])  # exclude areas of the playgrounds

    costs, solutions = [[None]*n_times for i in range(2)]
    # hill-climbing for n times
    if len(park.restrooms) == 0:
        park.add_restrooms(rand.sample(avail_areas, int(park.num_restrooms)))  # generate random restroom locations
    costs[0], solutions[0] = hill_climbing(park)
    for i in range(n_times-1):
        test_areas = [x for x in avail_areas if x != solutions[i]]  # candidates list (exclude previous test subject)
        park.restrooms.clear()
        park.add_restrooms(rand.sample(test_areas, int(park.num_restrooms)))
        costs[i+1], solutions[i+1] = hill_climbing(park)

    return min(costs), solutions[np.argmin(costs)]  # return best_cost and locations of the task_result


def hill_climbing(park):
    r_list = park.restrooms  # initial solution
    p_list = park.playgrounds

    while True:
        orig_state = r_list.copy()
        orig_cost = park.cost()
        # find the candidates
        for i in range(len(r_list)):
            neighbors = get_neighbors(park, r_list[i])  # get neighbors of r
            distance = [calc_dist(n, p_list) for n in neighbors]  # evaluate total distance for each neighbor
            best_neighbor = neighbors[np.argmin(distance)]  # get the minimum distance neighbor
            r_list[i] = best_neighbor

        # if the candidates aren’t better, stop
        # otherwise, continue with the candidates
        if park.cost() >= orig_cost:
            r_list = orig_state
            return park.cost(), [[r.x, r.y] for r in r_list]  # return best_cost and locations of the task_result


def calc_dist(r, p_list):
    dist = 0
    for p in p_list:
        dist += graderUtil.manhattan_dist(p, r)
    return dist


def get_neighbors(park, restroom):
    neighbours = []
    x = restroom.x  # current state coordinates
    y = restroom.y
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


# task result
if task_content[0] == "0":  # simple search
    task_park = graderUtil.Park(task_content)
    task_result["ini_cost"] = task_park.cost()
    task_result["best_cost"], task_result["locations"] = hill_climbing(task_park)
elif task_content[0] == "1":  # random restart
    task_park = graderUtil.Park(task_content)
    if len(task_content) == 4:
        task_content.append(10)  # set the number of repetitions to 10 times if it's not given
    task_result["best_cost"], task_result["locations"] = random_restart(task_park, task_content[4])
else:
    print("ERROR: Algorithm type undefined.")

# END_YOUR_CODE
#######################################################################

# output your final result
print(json.dumps(task_result))