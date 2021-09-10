
from bs4 import BeautifulSoup
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
        print('MCP number ' + str(random_mcp))
        print('Core number ' + str(random_core))

        mcps[random_mcp]['Cores'][random_core]['TaskList'].append(t)

    print(mcps[0])
    print(mcps[1])

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
        MPC list (main list)
        
    Creates final XML file (SOLUTION)
    
    return:
        xml file with solution
"""
def parse_solution():
    pass

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
    mcps, tasks = parser()
    initial_state = set_initial_state(mcps, tasks)
