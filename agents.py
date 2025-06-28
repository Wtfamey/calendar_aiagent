# agents.py
from prompts import main_agent_system_prompt, calendar_agent_system_prompt
from calendar_tools import list_calendar_lists, list_calendar_events, insert_calendar_event, create_calendar_list, delete_calendar_event, update_calendar_event
import json
import datetime

MODEL = 'gpt-4o-mini'

# Simple Agent class
class Agent:
    def __init__(self, name, model, instructions, functions=None):
        self.name = name
        self.model = model
        self.instructions = instructions
        self.functions = functions or []
    
    def run(self, prompt):
        # Enhanced implementation that can handle calendar operations
        prompt_lower = prompt.lower()
        
        # Handle calendar-related queries
        if any(word in prompt_lower for word in ['calendar', 'event', 'schedule', 'meeting']):
            return self._handle_calendar_query(prompt)
        
        # Handle function calls
        if any(word in prompt_lower for word in ['list', 'show', 'get', 'find']):
            return self._handle_list_query(prompt)
        
        # Default response
        return f"Agent {self.name} received: {prompt}. Instructions: {self.instructions[:100]}..."
    
    def _handle_calendar_query(self, prompt):
        """Handle calendar-related queries"""
        prompt_lower = prompt.lower()
        
        try:
            if 'list' in prompt_lower and 'calendar' in prompt_lower:
                calendars = list_calendar_lists(10)
                if calendars and 'error' not in calendars[0]:
                    result = "Available calendars:\n"
                    for i, cal in enumerate(calendars, 1):
                        result += f"{i}. {cal.get('name', 'Unknown')} (ID: {cal.get('id', 'Unknown')})\n"
                    return result
                else:
                    return f"Error listing calendars: {calendars[0] if calendars else 'Unknown error'}"
            
            elif 'list' in prompt_lower and 'event' in prompt_lower:
                # Get primary calendar for events
                calendars = list_calendar_lists(5)
                primary_calendar = None
                for cal in calendars:
                    if cal.get('primary', False):
                        primary_calendar = cal.get('id')
                        break
                
                if primary_calendar:
                    events = list_calendar_events(primary_calendar, 10)
                    if events and 'error' not in events[0]:
                        result = "Upcoming events:\n"
                        for i, event in enumerate(events, 1):
                            result += f"{i}. {event.get('summary', 'No Title')} - {event.get('start', 'No start time')}\n"
                        return result
                    else:
                        return f"Error listing events: {events[0] if events else 'Unknown error'}"
                else:
                    return "No primary calendar found"
            
            elif 'create' in prompt_lower and 'event' in prompt_lower:
                # This is a simplified event creation - in a real implementation, you'd parse the prompt for details
                return "To create an event, please provide: title, start time, end time, and optionally description and location. Example: 'Create event: Team Meeting, 2024-01-15T10:00:00Z, 2024-01-15T11:00:00Z, Weekly team sync'"
            
            else:
                return f"Calendar query received: {prompt}. I can help you list calendars, list events, and create events. Please be more specific about what you'd like to do."
        
        except Exception as e:
            return f"Error processing calendar query: {str(e)}"
    
    def _handle_list_query(self, prompt):
        """Handle list-related queries"""
        prompt_lower = prompt.lower()
        
        if 'calendar' in prompt_lower:
            return self._handle_calendar_query(prompt)
        elif 'function' in prompt_lower:
            result = f"Available functions for {self.name}:\n"
            for i, func in enumerate(self.functions, 1):
                result += f"{i}. {func.__name__}\n"
            return result
        else:
            return f"List query received: {prompt}. I can help you list calendars, events, and functions."
    
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
    create_calendar_list,
    delete_calendar_event,
    update_calendar_event
])