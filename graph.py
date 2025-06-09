""" import os
from dotenv import load_dotenv
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY') """

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END
from agents.mental import mental_health_agent
from agents.physical import physical_health_agent
from agents.supervisor import supervisor_agent
from langgraph.graph import StateGraph, START, MessagesState



memory = MemorySaver()


supervisor = (
    StateGraph(MessagesState)
    .add_node(supervisor_agent, destinations=("mental_health_agent", "physical_health_agent", END))
    .add_node(mental_health_agent)
    .add_node(physical_health_agent)
    .add_edge(START, "supervisor")
    # always return back to the supervisor
    .add_edge("mental_health_agent", "supervisor")
    .add_edge("physical_health_agent", "supervisor")
    .compile(checkpointer=memory)
)

#config = {"configurable": {"thread_id": "1"}}

""" for chunk in supervisor.stream(
    {
        "messages": [
            {
                "role": "user",
                "content": "Estou me sentindo ansioso ultimamente"
            }
        ]
    }, config
):
    pretty_print_messages(chunk, last_message=True) """

