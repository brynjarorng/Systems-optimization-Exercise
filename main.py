
from bs4 import BeautifulSoup

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
                "WCETFactor": core.get("WCETFactor")
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