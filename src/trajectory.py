from dataclasses import dataclass

from src.llm import Response


@dataclass
class Step:
    """A single step in a an agent's trajectory"""

    thought: str = ""
    action: dict | None = None
    observation: str | None = None  # output of tool usage
    answer: str | None = None  # final answer of the model
    metadata: dict | None = None


class Trajectory:
    """Records agent's execution as a sequence of runs"""

    def __init__(self) -> None:
        self.runs: list[dict] = []

    def initialize(self, query: str) -> None:
        """Registers a NEW run with the given query"""
        run = {"query": query, "steps": []}
        self.runs.append(run)

    def add(self, response: Response, observation: str | None = None) -> None:
        """Records a step from a Response; optionally with an observation"""
        # Add thought
        step = Step()
        step.thought = response.reasoning or ""
        step.metadata = response.metadata

        # Add Action / Observation or ANSWER
        if observation is not None:
            step.action = response.tool_call
            step.observation = observation
        else:
            step.answer = response.content

        # append the step to the run
        self.runs[-1]["steps"].append(step)
