import json
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
task_file = sys.argv[1]
task_content = graderUtil.load_task_file(task_file)
if task_content:
    print(task_content)

# BEGIN_YOUR_CODE


def random_restart(park, iteration):
    n_times = int(iteration)
    avail_areas = [[i, j] for i in range(park.num_rows) for j in range(park.num_cols)]  # list of areas from given size
    for p in park.playgrounds:
        avail_areas.remove([p.x, p.y])  # exclude areas of the playgrounds

    # hill-climbing for n times
    costs, solutions = [[None]*n_times for i in range(2)]
    if len(park.restrooms) == 0:
        park.add_restrooms(rand.sample(avail_areas, int(park.num_restrooms)))  # generate random restroom locations
    #DEBUG# print(f"1th: cost {park.cost()}, initial state {[[r.x, r.y] for r in park.restrooms]}")
    costs[0], solutions[0] = hill_climbing(park)
    for i in range(n_times-1):
        test_areas = [x for x in avail_areas if x != solutions[i]]  # candidates list (exclude previous test subject)
        park.restrooms.clear()
        park.add_restrooms(rand.sample(test_areas, int(park.num_restrooms)))
        #DEBUG# print(f"{i+2}th: cost {park.cost()}, initial state {[[r.x, r.y] for r in park.restrooms]}")
        costs[i+1], solutions[i+1] = hill_climbing(park)

    return min(costs), solutions[np.argmin(costs)]  # return best_cost and locations of the task_result


def hill_climbing(park):
    r_list = park.restrooms  # initial solution
    p_list = park.playgrounds

    while True:
        for i in range(len(r_list)):
            orig_state = r_list.copy()
            orig_cost = park.cost()
            # find the candidates
            neighbors = get_neighbors(park, r_list[i])  # get neighbors of r
            distance = [calc_dist(n, p_list) for n in neighbors]  # evaluate total distance for each neighbor
            best_neighbor = neighbors[np.argmin(distance)]  # get the minimum distance neighbor
            r_list[i] = best_neighbor
            #DEBUG# print(f"restroom {i}: cost {park.cost()}, move from {[orig_state[i].x, orig_state[i].y]} to {[r_list[i].x, r_list[i].y]}")
            if park.cost() >= orig_cost:
                r_list[i] = orig_state[i]
                #DEBUG# print(f"restroom {i}: move back to {[r_list[i].x, r_list[i].y]}")

        # If the candidates aren’t better, stop. Otherwise, continue with the candidates.
        if park.cost() >= orig_cost:
            r_list = orig_state
            return park.cost(), [[r.x, r.y] for r in r_list]  # return best_cost and locations of the task_result


def calc_dist(r, p_list):
    dist = 0
    for p in p_list:
        dist += graderUtil.manhattan_dist(p, r)
    return dist


def get_neighbors(park, restroom):
    x = restroom.x
    y = restroom.y
    neighbors = []
    modifications = [-1, 1]  # the neighbors are at the up, down, left, or right side

    # get neighbors' locations
    for i in modifications:
        x_new = x + i
        y_new = y + i
        if not x_new < 0 and not x_new > park.num_rows - 1:  # exclude locations outside the borders
            neighbors.append([x_new, y])
        if not y_new < 0 and not y_new > park.num_cols - 1:  # exclude locations outside the borders
            neighbors.append([x, y_new])

    # remove unavailable locations
    for p in park.playgrounds:
        if [p.x, p.y] in neighbors:
            neighbors.remove([p.x, p.y])
    
    return [graderUtil.Restroom(item) for item in neighbors]


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