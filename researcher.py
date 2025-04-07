from langgraph.checkpoint.memory import MemorySaver
from open_deep_research.graph import builder
from dotenv import load_dotenv

load_dotenv()

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

import uuid
thread = {"configurable": {
                            "thread_id": str(uuid.uuid4()),
                            "search_api": "tavily",
                            "planner_provider": "groq",
                            "planner_model": "llama-3.3-70b-versatile",
                            "writer_provider": "groq",
                            "writer_model": "llama-3.3-70b-versatile",
                            "max_search_depth": 3,
                           }
          }

# @title Enter your Research Topic
# @markdown Open research will use Tavily to deep Research about the Topic
topic = "Is it true that Muslims will be charged a New Tax from September of 2025 in India?" # @param {"type":"string"}
async for event in graph.astream({"topic":topic,}, thread, stream_mode="updates"):
    print(event)

print(event['__interrupt__'][0].value)

from langgraph.types import Command
async for event in graph.astream(
        Command(
resume = True # @param {"type":"raw"}
        ),
        thread,
        stream_mode="updates"
    ):
    ...
print(event['compile_final_report']['final_report'])

async for event in graph.astream(Command(resume=True), thread, stream_mode="updates"):
    print(event)

from IPython.display import display, Markdown
display(Markdown(event['compile_final_report']['final_report']))
