
class ToolManager:
    def __init__(self):
        self.tools = {}

    def register_tool(self,name,function,description):
        """regester a python function as a tool"""
        if name in self.tools:
            raise ValueError(f"tool '{name} is already registered.")

        self.tools[name] = {
            "function": function,
            "description":description 
        }

    def  get_available_tools(self):
        return {
            name: tool["description"]
            for name, tool in self.tools.items()
        }
    def execute_tool(self, tool_name, **kwargs):
            """Execute a registered tool."""
            if tool_name not in self.tools:
                raise ValueError(f"Tool '{tool_name}' is not registered.")

            try:
                return self.tools[tool_name]["function"](**kwargs)
            except Exception as error:
                return {
                    "success": False,
                    "error": str(error)
                }
