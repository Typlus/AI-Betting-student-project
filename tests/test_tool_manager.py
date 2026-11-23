from agent.tool_manager import ToolManager

def sample_tool(name):
    return f"Hello, {name}!"

def main():
    manager = ToolManager()


    manager.register_tool(
        name="greeting",
        function=sample_tool,
        description="Returns a greeting."
    )

    print("\n--- AVAILABLE TOOLS ---")
    print(manager.get_available_tools())

    print("\n--- TOOL EXECUTION ---")
    result = manager.execute_tool(
        "greeting",
        name="Tyler"
    )

    print(result)


if __name__ == "__main__":
    main()
