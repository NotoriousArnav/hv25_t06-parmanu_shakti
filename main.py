import streamlit as st
import os
import uuid
import asyncio
from langgraph.checkpoint.memory import MemorySaver
from open_deep_research.graph import builder
from langgraph.types import Command

# Set your API keys
os.environ['GROQ_API_KEY'] = "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"
os.environ['TAVILY_API_KEY'] = "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"

# Build the research graph
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Streamlit UI
st.title("📚 Open Deep Research Assistant")
topic = st.text_input("Enter your research topic:", 
                      "Is it true that Muslims will be charged a New Tax from September of 2025 in India?")

if st.button("Run Research"):
    with st.spinner("Researching..."):
        thread = {
            "configurable": {
                "thread_id": str(uuid.uuid4()),
                "search_api": "tavily",
                "planner_provider": "groq",
                "planner_model": "llama-3.3-70b-versatile",
                "writer_provider": "groq",
                "writer_model": "llama-3.3-70b-versatile",
                "max_search_depth": 3,
            }
        }

        async def run_research(topic, thread):
            final_event = None
            async for event in graph.astream({"topic": topic}, thread, stream_mode="updates"):
                final_event = event
            yield final_event['__interrupt__'][0].value

            # Resume and compile final report
            async for event in graph.astream(Command(resume=True), thread, stream_mode="updates"):
                pass
            yield event['compile_final_report']['final_report']

        result = asyncio.run(run_research(topic, thread))

        if result:
            for section in result:
                st.markdown(f"### 📝 Final Report")
                st.markdown(section)