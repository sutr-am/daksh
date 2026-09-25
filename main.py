# from daksh.agent import DakshAgent
from rich import print

from src.agent import DakshAgent
from src.llm import LLM

my_llm = LLM(model="gemma4:e2b")
# messages = [{"role": "user", "content": "Hi! How is life?!"}]

# response = my_llm.generate(messages=messages)
# print("------" * 20)
# print(response)
# print("------" * 20)

ax = DakshAgent(llm=my_llm)

print("🤖", "------" * 20)
print(ax.run("What is your identity?"))
print("🤖", "------" * 20)
