
from bs4 import BeautifulSoup
import random
import xml.etree.cElementTree as ET

SOLUTION_FILE = 'filename.xml'

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
    number_of_cores = []
    for mcp in mcps:
        number_of_cores.append(len(mcp['Cores']))

    for t in tasks:
        random_mcp = random.randint(0, number_of_mcps - 1)
        random_core = random.randint(0, number_of_cores[random_mcp] - 1)

        mcps[random_mcp]['Cores'][random_core]['TaskList'].append(t)

    return mcps


"""
    Finds a single random task and pops it from the list

    Args:
        The MCP lsit

    Returns:
        A tuple where the first item is the new mcps list and second is the poped item
"""
def get_random_task(mcps):
    number_of_mcps = len(mcps)

    while True:
        random_mcp = random.randint(0, number_of_mcps - 1)
        num_cores = len(mcps[random_mcp]["Cores"])
        random_core = random.randint(0, num_cores - 1)
        num_tasks = len(mcps[random_mcp]["Cores"][random_core]["TaskList"])

        if num_tasks == 0:
            # Try again since task list is empty
            continue

        random_task = random.randint(0, num_tasks - 1)
        selected_task_to_move = mcps[random_mcp]["Cores"][random_core]["TaskList"][random_task]

        del mcps[random_mcp]["Cores"][random_core]["TaskList"][random_task]

        return mcps, selected_task_to_move


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
        The MCP list
        Number of items to move

    Returns:
        The updated list of values
"""
def move(mcps, num_to_move):
    for i in range(num_to_move):
        # Select random task
        mcps, selected_task_to_move = get_random_task(mcps)

        # Insert task somewhere else
        mcps = insert_random(mcps, selected_task_to_move)
        
    return mcps


"""
    Swaps tasks randomly

    Args:
        Number of tasks to swap
        The MCP list (main list containing everything)

    Returns:
        New list with swapped values
"""
def swap():
    pass


"""
    Creates final XML file (SOLUTION)

    Args:
        MPC list (main list)    
    
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
    Runs the main algorithm (Simulated Annealing) to find the best solution
    
    Args:
        MPC list(main list)
        
    Returns:
        best version of the MCP list
"""
def algorithm_sa():
    pass


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
    file_to_read = 'test_cases/small.xml'
    mcps, tasks = parser(file_to_read)
    initial_state = set_initial_state(mcps, tasks)
    parse_solution = parse_solution(initial_state)


