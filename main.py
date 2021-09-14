
from bs4 import BeautifulSoup
import random
import xml.etree.cElementTree as ET

"""
    param:
        The MCP list (main list)
        Tasks list

    Sets a random initial state

    return:
        Updated list of values
"""


def set_initial_state(mcps, tasks):
    number_of_mcps = len(mcps)
    number_of_cores = []
    for mcp in mcps:
        number_of_cores.append(len(mcp['Cores']))

    for t in tasks:
        random_mcp = random.randint(0, number_of_mcps - 1)
        random_core = random.randint(0, number_of_cores[random_mcp] - 1)
        # print('MCP number ' + str(random_mcp))
        # print('Core number ' + str(random_core))

        mcps[random_mcp]['Cores'][random_core]['TaskList'].append(t)

    # print("From initial state function: ", mcps[0])
    # print(mcps[1])

    return mcps


"""
    param:
        The MCP list
        Number of items to move

    Moves N tasks to a different core randomly

    return:
        The updated list of values
"""


def move():
    pass


"""
    param:
        The MCP list

    Gets a random task

    return:
        A random task
"""


def getTask(mcps):
    while (True):
        # We run until we find a task - since there might be no cores and no tasks in some MCPs.
        # MCPs should always have cores, and there should always be tasks, but better safe than sorry
        mcp_index = random.randrange(0, len(mcps))
        if (len(mcps[mcp_index]['Cores']) == 0):
            continue
        core_index = random.randrange(0, len(mcps[mcp_index]['Cores']))
        if (len(mcps[mcp_index]['Cores'][core_index]['TaskList']) == 0):
            continue
        task_index = random.randrange(
            0, len(mcps[mcp_index]['Cores'][core_index]['TaskList']))
        return mcp_index, core_index, task_index, mcps[mcp_index]['Cores'][core_index]['TaskList'][task_index]


"""
    param:
        Number of tasks to swap
        The MCP list (main list containing everything)

    Swaps tasks randomly

    return:
        New list with swapped values
"""


def swap(swap_count, mcps):
    swaps = 0;
    while (swaps < swap_count):
        mcp1_index, core1_index, task1_index, task1 = getTask(mcps);
        mcp2_index, core2_index, task2_index, task2 = getTask(mcps);
        # Only do swaps if the two task are different
        if (task1 != task2):
            mcps[mcp1_index]['Cores'][core1_index]['TaskList'][task1_index] = task2;
            mcps[mcp2_index]['Cores'][core2_index]['TaskList'][task2_index] = task1;
            swaps += 1;
    return mcps;


"""
    param:
        MPC list (main list)

    Creates final XML file (SOLUTION)

    return:
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
    tree.write('filename.xml')


"""
    param:
        MPC list(main list)

        Runs the main algorithm (Simulated Annealing) to find the best solution

        return:
            best version of the MCP list
"""


def algorithm_sa():
    pass


def parser():
    with open('test_cases/small.xml', 'r') as f:
        data = f.read()

    Bs_data = BeautifulSoup(data, "xml")

    # Parse the platform data
    # platorm = Platform(Bs_data)
    mcps = []
    mcp_list = Bs_data.find_all("MCP")
    for mcp in mcp_list:
        cores = []

        for core in mcp.find_all("Core"):
            cores.append({
                "Id": core.get("Id"),
                "WCETFactor": core.get("WCETFactor"),
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
            "Deadline": task.get("Deadline"),
            "Id": task.get("Id"),
            "Period": task.get("Period"),
            "WCET": task.get("WCET")
        })

    return mcps, tasks


if __name__ == "__main__":
    swap_count = 4
    mcps, tasks = parser()
    initial_state = set_initial_state(mcps, tasks)
    swap_state = swap(swap_count, mcps)
    parse_solution = parse_solution(mcps)
