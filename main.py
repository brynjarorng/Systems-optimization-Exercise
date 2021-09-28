
from bs4 import BeautifulSoup
import random
import xml.etree.cElementTree as ET
import math
import copy

SOLUTION_FILE = 'large.xml'
FILE_TO_READ = 'test_cases/large.xml'
GLOBAL_OPTIMUM_SOLUTION = (None, -50000000000000000000000)
MIN_TASKS_PER_CORE = 1
SOLUTION_FOUND = False


"""
    Sets a random initial state

    Args:
        mcps: The MCP list (main list)
        tasks: Tasks list

    Returns:
        Updated list of values
"""
def set_initial_state(mcps, tasks):
    number_of_mcps = len(mcps)
    avg_per_core = len(tasks) / sum( [ len(listElem["Cores"]) for listElem in mcps])

    # Evenly distribute
    for mcp in mcps:
        for c in mcp["Cores"]:
            for i in range(0, int(avg_per_core)):
                c["TaskList"].append(tasks[0])
                del tasks[0]

    number_of_cores = []
    for mcp in mcps:
        number_of_cores.append(len(mcp['Cores']))

    for t in tasks:
        random_mcp = random.randint(0, number_of_mcps - 1)
        random_core = random.randint(0, number_of_cores[random_mcp] - 1)

        mcps[random_mcp]['Cores'][random_core]['TaskList'].append(t)

    return mcps


"""
    Gets a random task

    Args:
        mcps: The MCP list

    Returns:
        mcp_index: the index of the mcp
        core_index: the index of the core in an mcp
        task_index: the index of the task in a core
        task: the selected random task

"""
def get_random_task(mcps):
    while True:
        # We run until we find a task - since there might be no cores and no tasks in some MCPs.
        # MCPs should always have cores, and there should always be tasks, but better safe than sorry
        mcp_index = random.randrange(0, len(mcps))
        if len(mcps[mcp_index]['Cores']) == 0:
            continue

        core_index = random.randrange(0, len(mcps[mcp_index]['Cores']))
        if len(mcps[mcp_index]['Cores'][core_index]['TaskList']) == 0:
            continue

        task_index = random.randrange(
            0, len(mcps[mcp_index]['Cores'][core_index]['TaskList']))

        return mcp_index, core_index, task_index, mcps[mcp_index]['Cores'][core_index]['TaskList'][task_index]


"""
    Inserts a task randomly into the MCP list

    Args:
        mcps: The MCP list
        task: The task to insert

    Returns:
        A new mcps list
"""
def insert_random(mcps, task):
    number_of_mcps = len(mcps)
    random_mcp = random.randint(0, number_of_mcps - 1)
    num_cores = len(mcps[random_mcp]["Cores"])
    random_core = random.randint(0, num_cores - 1)
    mcps[random_mcp]["Cores"][random_core]["TaskList"].append(task)

    return mcps


"""
    Moves N tasks to a different core randomly

    Args:
        mcps: The MCP list
        num_to_move: Number of items to move

    Returns:
        The updated list of values
"""
def move(num_to_move, mcps):
    moves = 0;
    while (moves < num_to_move):
        # Select random task and remove it
        mcp_index, core_index, task_index, task = get_random_task(mcps);

        bool, _ = is_schedulable(mcps[mcp_index]['Cores'][core_index]['TaskList'], mcps[mcp_index]['Cores'][core_index]['WCETFactor'])
        if bool and not SOLUTION_FOUND:
            moves += 1
            continue

        del mcps[mcp_index]['Cores'][core_index]['TaskList'][task_index]

        # Insert task somewhere else
        mcps = insert_random(mcps, task)

        moves += 1
        
    return mcps


"""
    Swaps tasks randomly

    Args:
        Number of tasks to swap
        The MCP list (main list containing everything)

    Returns:
        New list with swapped values
"""
def swap(swap_count, mcps):
    swaps = 0;
    while (swaps < swap_count):
        mcp1_index, core1_index, task1_index, task1 = get_random_task(mcps);
        mcp2_index, core2_index, task2_index, task2 = get_random_task(mcps);

        # bool, _ = is_schedulable(mcps[mcp1_index]['Cores'][core1_index]['TaskList'], mcps[mcp1_index]['Cores'][core1_index]['WCETFactor'])
        # if bool:
        #     swaps += 1
        #     continue

        # Only do swaps if the two task are different
        if (task1 != task2):
            mcps[mcp1_index]['Cores'][core1_index]['TaskList'][task1_index] = task2;
            mcps[mcp2_index]['Cores'][core2_index]['TaskList'][task2_index] = task1;
            swaps += 1;
    return mcps;


"""
    Creates final XML file (SOLUTION)

    Args:
        mcps: MPC list (main list)    
    
    Returns:
        xml file with solution
"""
def parse_solution(mcps):
    root = ET.Element("Solution")

    for mcp in mcps:
        for core in mcp['Cores']:
            for task in core['TaskList']:
                WCRT = str(round(float(task['WCET']) *
                                 float(core['WCETFactor']), 2))

                ET.SubElement(
                    root, "Task", Id=task['Id'], MCP=mcp['Id'], Core=core['Id'], WCRT=WCRT)

    tree = ET.ElementTree(root)
    tree.write(SOLUTION_FILE)


"""
    Determines whether a list of tasks is schedulable on a single processor

    Args:
        Tasks list (on a single core) ordered by unique priority 
        and adjusted for WCETFactor of core's performance beforehand
        
    Returns:
        boolean respresenting whether assignment is schedulable
        list of corresponding WCRTs found
"""
def is_schedulable(tasks, core_factor):
    wcrts = []
    for i in range(0,len(tasks)):
        l = 0
        while True:
            r = l + tasks[i]["WCET"] * core_factor
            if r > tasks[i]["Deadline"]:
                return False, []
            l = 0
            for j in range(0,i):
                l += math.ceil(r/tasks[j]["Period"]) * tasks[j]["WCET"] * core_factor
            if l + tasks[i]["WCET"] * core_factor <= r:
                wcrts.append(r)
                break
    
    return True, wcrts


"""
    Calculate the laxity

    Args:
        mcps: main list

    Returns:
        Laxity value
"""
def laxity_calculator(mcps):
    laxity = 0
    r = 0
    deadlines = 0
    #sum(task['Deadline'] for task in tasks)
    for mcp in mcps:
        for core in mcp['Cores']:
            tasks = core['TaskList']
            for task in tasks:
                deadlines += task['Deadline']
            bool, wcrts = is_schedulable(tasks, core["WCETFactor"])
            for w in wcrts:
                r += w
            if not bool:
                r += deadlines * 209000

    laxity = deadlines - r

    return laxity, deadlines


"""
    Parses the input file from xml into python dicts

    Args:
        file_to_read: The input file to be read

    Returns:
        python dict representation of an input XML file. This is the list
        of MCPs which contain cores which then contain the tasks
"""
def parser(file_to_read):
    with open(file_to_read, 'r') as f:
        data = f.read()

    Bs_data = BeautifulSoup(data, "xml")

    # Parse the platform data
    mcps = []
    mcp_list = Bs_data.find_all("MCP")
    for mcp in mcp_list:
        cores = []

        for core in mcp.find_all("Core"):
            cores.append({
                "Id": core.get("Id"),
                "WCETFactor": float(core.get("WCETFactor")),
                "TaskList": []
            })

        mcps.append({
            "Id": mcp.get("Id"),
            "Cores": cores
        })

    # Parse the task list
    tasks = []
    task_list = Bs_data.find_all("Task")
    for task in task_list:
        tasks.append({
            "Deadline": int(task.get("Deadline")),
            "Id": task.get("Id"),
            "Period": int(task.get("Period")),
            "WCET": int(task.get("WCET"))
        })

    return mcps, tasks


"""
    The simple annealing function 
"""
def sa(mcps):
    global SOLUTION_FOUND
    global GLOBAL_OPTIMUM_SOLUTION
    switcher = [True, False]
    T_max = 20000000000
    T = T_max
    r = 0.0002
    laxity, _ = laxity_calculator(mcps)
    state_list = []

    while T > 1:
        # Generate neighbour using either swap or move
        if SOLUTION_FOUND:
            change_ammount = random.randrange(1, 6)
            if random.choice(switcher):
                mcps_new = swap(change_ammount, copy.deepcopy(mcps))
            else:
                mcps_new = move(change_ammount, copy.deepcopy(mcps))
        else:
            change_ammount = random.randrange(5, 20)
            mcps_new = move(change_ammount, copy.deepcopy(mcps))

        new_laxity, deadline = laxity_calculator(mcps_new)

        if laxity < new_laxity or random.randrange(0, T_max) < T:
            # Set new state
            mcps = mcps_new
            laxity = new_laxity

            # Set global best solution found so far
            if GLOBAL_OPTIMUM_SOLUTION[1] < laxity:
                GLOBAL_OPTIMUM_SOLUTION = (copy.deepcopy(mcps), laxity, deadline)
                print(laxity)
                l = []
                for i in GLOBAL_OPTIMUM_SOLUTION[0]:
                    for c in i["Cores"]:
                        l.append(is_schedulable(c['TaskList'], c["WCETFactor"])[0])
                if all(l) is True:
                    parse_solution(GLOBAL_OPTIMUM_SOLUTION[0])
                    print(l)
                    SOLUTION_FOUND = True
        
        T = T * (1 - r)

    return state_list, mcps



if __name__ == "__main__":
    mcps, tasks = parser(FILE_TO_READ)

    initial_state = set_initial_state(mcps, tasks)

    results, mcps = sa(mcps)

    print(GLOBAL_OPTIMUM_SOLUTION[1])
    print(GLOBAL_OPTIMUM_SOLUTION[2])

    for i in GLOBAL_OPTIMUM_SOLUTION[0]:
        for c in i["Cores"]:
            print(is_schedulable(c['TaskList'], c["WCETFactor"]))

    parse_solution(GLOBAL_OPTIMUM_SOLUTION[0])
