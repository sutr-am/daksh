from src.llm import LLM
from src.trajectory import Trajectory


class DakshAgent:
    def __init__(self, llm: LLM) -> None:
        self.llm = llm
        self.memory = None
        self.tools = None
        self.planner = None
        self.trajectory = Trajectory()

    def run(self, task: str) -> str:
        """Run the agent on a task"""
        self.trajectory.initialize(query=task)
        return self._step(task)

    def _step(self, task: str) -> str:
        """Performa single step"""
        messages = [{"role": "user", "content": task}]
        response = self.llm.generate(messages=messages)
        self.trajectory.add(response=response)
        return response.content

    def _execute_action(self, action: str) -> str | None:
        """Execute a tool action"""
        return f"Executed Action: {action=}"
