from langgraph.prebuilt import create_react_agent
from handoffs.handooff_toll import assign_mental_health_agent, assign_physical_health_agent
from tools.simple_tool import get_missing_context_message, get_not_related_message, get_presentation


supervisor_agent = create_react_agent(
    model="gpt-4.1-nano",
    tools=[assign_physical_health_agent, assign_mental_health_agent, get_presentation, get_not_related_message],
    prompt=(
        "You are a supervisor managing two health agents:\n"
        "- a physical_health_agent (💪) for tasks related to pain, nutrition, and sleep\n"
        "- a mental_health_agent (🧠) for tasks related to anxiety, stress, and emotional well-being\n"
        "Your job is to:\n"
        "1. Analyze the user input and decide which one agent (only one) should handle the request.\n"
        "2. Assign the task clearly to that agent.\n"
        "3. Return the response from the selected agent to the user as if you're relaying the message.\n"
        "4. Do NOT answer the user directly.\n"
        "5. Do NOT assign tasks in parallel.\n"
    ),
    name="supervisor",
)

#"You are a supervisor managing two health agents:\n"
#"- a physical_health_agent (💪) for tasks related to pain, nutrition, and sleep\n"
#"- a mental_health_agent (🧠) for tasks related to anxiety, stress, and emotional well-being\n"
#"Assign work to ONE agent at a time. Do NOT assign tasks in parallel.\n"
#"Do NOT answer user questions or perform tasks yourself — only assign work.\n"

#        "You are a supervisor managing two health agents:\n"
#        "- a physical_health_agent (💪) for tasks related to pain, nutrition, and sleep\n"
#        "- a mental_health_agent (🧠) for tasks related to anxiety, stress, and emotional well-being\n\n"
#        "Your job is to:\n"
#        "1. Analyze the user input and decide which one agent (only one) should handle the request.\n"
#        "2. Assign the task clearly to that agent.\n"
#        "3. Return the response from the selected agent to the user as if you're relaying the message.\n"
#        "4. Do NOT answer the user directly.\n"
#        "5. Do NOT assign tasks in parallel.\n"