
from bs4 import BeautifulSoup


"""
    param:
        The MCP list (main list)

    Sets a random initial state

    return:
        Updated list of values
"""
def set_initial_state():
    pass


"""
    param:
        The MCP list
        Number of items to move
        Tasks list

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


    print(mcps[0])
    print(mcps[1])

           


if __name__ == "__main__":
    parser()