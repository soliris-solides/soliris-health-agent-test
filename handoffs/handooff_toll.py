from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.graph import  MessagesState
from langgraph.types import Command

def create_handoff_tool(*, agent_name: str, description: str | None = None):
    name = f"transfer_to_{agent_name}"
    description = description or f"Ask {agent_name} for help."

    @tool(name, description=description)
    def handoff_tool(
        state: Annotated[MessagesState, InjectedState],
        tool_call_id: Annotated[str, InjectedToolCallId],
    ) -> Command:
        tool_message = {
            "role": "tool",
            "content": f"Successfully transferred to {agent_name}",
            "name": name,
            "tool_call_id": tool_call_id,
        }
        return Command(
            goto=agent_name,  
            update={**state, "messages": state["messages"] + [tool_message]},  
            graph=Command.PARENT,  
        )

    return handoff_tool

assign_physical_health_agent = create_handoff_tool( 
    agent_name="physical_health_agent", 
    description="Assign task to the Physical Health Agent (💪) for issues related to pain, sleep, or nutrition", 
)

assign_mental_health_agent = create_handoff_tool( 
    agent_name="mental_health_agent", 
    description="Assign task to the Mental Health Agent (🧠) for issues related to anxiety, stress, or emotional well-being", 
)