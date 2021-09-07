
from bs4 import BeautifulSoup

class Platform:
    MCPs = []

    def __init__(self, data):
        mcps = data.find_all("MCP")

        for i in mcps:
            self.MCPs.append(MCP(i))

class MCP:
    MCP_ID = -1
    CORES = []

    def __init__(self, data):
        self.MCP_ID = data.get("Id")
        cores = data.find_all("Core")
        for i in cores:
            self.CORES.append({
                "WCETFactor": i.get("WCETFactor"),
                "Id": i.get("Id"),
            })

    def __str__(self):
        return self.MCP_ID

 

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

        for core in mcp.get("Cores"):
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




    print(mcp_list)

           


if __name__ == "__main__":
    parser()