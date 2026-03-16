class Agent:
    def __init__ (self, name: str):
        self.name = name
        self.tools = []

    def add_tool(self, tool: str):
        self.tools.append(tool)
    
    def run (self, task: str):
        return f"Agent {self.name} is running: {task}"
    
agent = Agent("my-agent")
agent.add_tool("search")
agent.add_tool("calculator")
print(agent.run("find the weather"))
print(agent.tools)
