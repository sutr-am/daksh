class DakshAgent:
    def __init__(self) -> None:
        self.llm = None
        self.memory = None
        self.tools = None
        self.planner = None

    def run(self, task: str) -> str:
        """Runs teh agent on a task"""
        return self._step(task)

    def _step(self, task: str) -> str:
        """Performs a single step"""
        return f"Received: {task=}"

    def _execute_action(self, action: str) -> str:
        """Executes a tool action"""
        return f"Executed: {action=}"
