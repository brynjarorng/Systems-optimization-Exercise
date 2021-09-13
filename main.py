
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, ElementTree
import random

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

    # print(mcps[0])
    # print(mcps[1])

    return mcps


"""
    param:
        The MCP lsit

    finds a single random task and pops it from the list

    return:
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
    param:
        The MCP list
        The task to insert

    Inserts a task randomly into the MCP list

    returns:
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
    param:
        The MCP list
        Number of items to move

    Moves N tasks to a different core randomly

    return:
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
    param:
        Number of tasks to swap
        The MCP list (main list containing everything)
    
    Swaps tasks randomly

    return:
        New list with swapped values
"""
def swap():
    pass


"""
    param:
        MCP list (main list)
        
    Creates final XML file (SOLUTION)
    
    return:
        xml file with solution
"""
def parse_solution(mcps):
    solutionJson = {}
    taskSize = 0
    # Extract solution data into a Json object
    for mcp in mcps:
        for core in mcp["Cores"]:
            for task in core["TaskList"]:
                taskRes = { "MCP": mcp["Id"], "Core": core["Id"], "WCRT": task["WCRT"] } 
                solutionJson[task["Id"]] = taskRes
                taskSize += 1
    
    # Build Element tree
    top = Element('Solution')
    for n in range(taskSize):
        curTaskRes = solutionJson[str(n)]
        SubElement(top, 'Task', Id=str(n), MCP=curTaskRes["MCP"], Core=curTaskRes["Core"], WCRT=curTaskRes["WCRT"])
    tree = ElementTree(top)
    
    # Write ordered element tree into xml file
    with open ("solution.xml", "wb") as files:
        tree.write(files)

"""
    param:
        MCP list(main list)
        
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
    mcps, tasks = parser()
    initial_state = set_initial_state(mcps, tasks)

