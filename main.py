
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

    platorm = Platform(Bs_data)
    print(platorm.MCPs[1])

           


if __name__ == "__main__":
    parser()