import os
import uuid
import streamlit as st
from langgraph.checkpoint.memory import MemorySaver
from open_deep_research.graph import builder
from langgraph.types import Command

# Set environment variables
os.environ['GROQ_API_KEY'] = "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"
os.environ['TAVILY_API_KEY'] = "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"

# Initialize memory and graph
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Initialize thread configuration
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

# Streamlit UI
st.title('Research Topic Analysis')
topic = st.text_area('Enter your Research Topic', 'Is it true that Muslims will be charged a New Tax from September of 2025 in India?')

if st.button('Start Research'):
    # Run the research process
    async def run_research():
        async for event in graph.astream({"topic": topic}, thread, stream_mode="updates"):
            st.write(event)
        st.write(event['__interrupt__'][0].value)

        value = st.text_input("Feedback: ") or True

        async for event in graph.astream(Command(resume=True), thread, stream_mode="updates"):
            st.write(event)
        st.write(event['compile_final_report']['final_report'])

    import asyncio
    asyncio.run(run_research())
