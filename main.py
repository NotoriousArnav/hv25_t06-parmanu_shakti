import os
import uuid
import streamlit as st
from langgraph.checkpoint.memory import MemorySaver
from open_deep_research.graph import builder
from langgraph.types import Command
from dotenv import load_dotenv

# Set environment variables
load_dotenv()


# Initialize thread configuration
with st.sidebar:
    # Initialize memory and graph
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    
    # Add Github button to as User for Stars and Contribution
    st.write("This is an Open Source Project. You can contribute to it on [Github](https://github.com/NotoriousArnav/hv25_t06-parmanu_shakti.git)")

    st.title('Thread Configuration')
    thread_id = str(uuid.uuid4())
    st.write(f"Thread ID: {thread_id}")
    planner_provider = st.text_input('Planner Provider', 'google-genai')
    planner_model = st.text_input('Planner Model', 'gemini-2.0-flash')
    writer_provider = st.text_input('Writer Provider', 'google-genai')
    writer_model = st.text_input('Writer Model', 'gemini-2.0-flash')
    max_search_depth = st.slider(
                'Max Search Depth',
                min_value=1,
                max_value=10,
                value=3
            )

thread = {
    "configurable": {
        "thread_id": thread_id,
        "search_api": "tavily",
        "planner_provider": planner_provider,
        "planner_model": planner_model,
        "writer_provider": writer_provider,
        "writer_model": writer_model,
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
            pass
        #st.write(event['__interrupt__'][0].value)
        
        with st.spinner("Generating Research Plan"):
            st.markdown("## Research Plan")
            async for event in graph.astream(Command(resume=True), thread, stream_mode="updates"):
                step = event.get('build_section_with_web_research', None)
                if step:
                    completed_section = step['completed_sections']
                    for x in completed_section:
                        st.markdown(f"""
- {x.name} - (Research: {x.research})
{x.description}
                                    """)
                        await asyncio.sleep(1)

            #st.write(event)

        st.download_button(
                "Download Final Report",
                event['compile_final_report']['final_report'],
                "final_report.md",
                "text/plain"
            )

        st.markdown("## Final Report")
        st.write(event['compile_final_report']['final_report'])

    import asyncio
    asyncio.run(run_research())
