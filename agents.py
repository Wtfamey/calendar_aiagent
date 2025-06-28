# agents.py
from prompts import main_agent_system_prompt, calendar_agent_system_prompt
from calendar_tools import list_calendar_lists, list_calendar_events, insert_calendar_event, create_calendar_list

MODEL = 'gpt-4o-mini'

# Simple Agent class
class Agent:
    def __init__(self, name, model, instructions, functions=None):
        self.name = name
        self.model = model
        self.instructions = instructions
        self.functions = functions or []
    
    def run(self, prompt):
        # Simple implementation - you can enhance this later
        return f"Agent {self.name} received: {prompt}. Instructions: {self.instructions[:100]}..."
    
    def chat(self, prompt):
        return self.run(prompt)

def transfer_to_main_agent():
    return main_agent

def transfer_to_calendar_agent():
    return calendar_agent

main_agent = Agent(
    name="Main Agent",
    model=MODEL,
    instructions=main_agent_system_prompt,
    functions=[transfer_to_calendar_agent]
)

calendar_agent = Agent(
    name="Google Calendar Agent",
    model=MODEL,
    instructions=calendar_agent_system_prompt,
    functions=[transfer_to_main_agent]
)

calendar_agent.functions.extend([
    list_calendar_lists,
    list_calendar_events,
    insert_calendar_event,
    create_calendar_list
])