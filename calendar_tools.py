# calendar_tools.py
from google_apis import create_service
import datetime
from typing import List, Dict, Any, Optional

client_secret = 'client_secret.json'

# Use the service created by google_apis.py
try:
    calendar_service = create_service(client_secret, 'calendar', 'v3', ['https://www.googleapis.com/auth/calendar'])
    if calendar_service is None:
        raise Exception("Failed to create calendar service")
except Exception as e:
    print(f"Error creating calendar service: {e}")
    calendar_service = None

def create_calendar_list(calendar_name: str) -> Dict[str, Any]:
    """
    Creates a new calendar list.

    Parameters:
    - calendar_name (str): The name of the new calendar list.

    Returns:
    - dict: A dictionary containing the ID of the new calendar list.
    """
    if not calendar_service:
        return {"error": "Calendar service not available"}
    
    if not calendar_name or not isinstance(calendar_name, str):
        return {"error": "Invalid calendar name provided"}
    
    try:
        calendar_list = {
            'summary': calendar_name,
            'timeZone': 'UTC'
        }
        created_calendar_list = calendar_service.calendarList().insert(body=calendar_list).execute()
        return {
            "success": True,
            "calendar_id": created_calendar_list.get('id'),
            "summary": created_calendar_list.get('summary'),
            "message": f"Calendar '{calendar_name}' created successfully"
        }
    except Exception as e:
        return {"error": f"Failed to create calendar: {str(e)}"}

def list_calendar_lists(max_capacity: int = 200) -> List[Dict[str, str]]:
    """
    Lists calendar lists until the total number of items reaches max_capacity.

    Parameters:
    - max_capacity (int or str, optional): The maximum number of calendar lists to retrieve. Defaults to 200.
    | If a string is provided, it will be converted to an integer.

    Returns:
    - list: A list of dictionaries containing cleaned calendar list information with 'id', 'name', and 'description'.
    """
    if not calendar_service:
        return [{"error": "Calendar service not available"}]
    
    try:
        if isinstance(max_capacity, str):
            max_capacity = int(max_capacity)
        
        if max_capacity <= 0:
            max_capacity = 200
            
        all_calendars = []
        all_calendars_cleaned = []
        next_page_token = None
        capacity_tracker = 0

        while True:
            calendar_list = calendar_service.calendarList().list(
                maxResults=min(200, max_capacity - capacity_tracker),
                pageToken=next_page_token
            ).execute()
            calendars = calendar_list.get('items', [])
            all_calendars.extend(calendars)
            capacity_tracker += len(calendars)
            if capacity_tracker >= max_capacity:
                break
            next_page_token = calendar_list.get('nextPageToken')
            if not next_page_token:
                break

        for calendar in all_calendars:
            all_calendars_cleaned.append({
                'id': calendar.get('id', ''),
                'name': calendar.get('summary', ''),
                'description': calendar.get('description', ''),
                'primary': calendar.get('primary', False),
                'accessRole': calendar.get('accessRole', '')
            })

        return all_calendars_cleaned
    except Exception as e:
        return [{"error": f"Failed to list calendars: {str(e)}"}]

def list_calendar_events(calendar_id: str, max_capacity: int = 20, time_min: Optional[str] = None, time_max: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Lists events from a specified calendar until the total number of events reaches max_capacity.

    Parameters:
    - calendar_id (str): The ID of the calendar from which to list events.
    - max_capacity (int or str, optional): The maximum number of events to retrieve. Defaults to 20.
    | If a string is provided, it will be converted to an integer.
    - time_min (str, optional): Start time for events (ISO format). Defaults to now.
    - time_max (str, optional): End time for events (ISO format). Defaults to 30 days from now.

    Returns:
    - list: A list of events from the specified calendar.
    """
    if not calendar_service:
        return [{"error": "Calendar service not available"}]
    
    if not calendar_id or not isinstance(calendar_id, str):
        return [{"error": "Invalid calendar ID provided"}]
    
    try:
        if isinstance(max_capacity, str):
            max_capacity = int(max_capacity)
        
        if max_capacity <= 0:
            max_capacity = 20
        
        # Set default time range if not provided
        if not time_min:
            time_min = datetime.datetime.utcnow().isoformat() + 'Z'
        if not time_max:
            time_max = (datetime.datetime.utcnow() + datetime.timedelta(days=30)).isoformat() + 'Z'
        
        all_events = []
        next_page_token = None
        capacity_tracker = 0

        while True:
            events_list = calendar_service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=min(250, max_capacity - capacity_tracker),
                pageToken=next_page_token,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            events = events_list.get('items', [])
            all_events.extend(events)
            capacity_tracker += len(events)
            if capacity_tracker >= max_capacity:
                break
            next_page_token = events_list.get('nextPageToken')
            if not next_page_token:
                break

        # Clean up event data
        cleaned_events = []
        for event in all_events:
            start = event.get('start', {})
            end = event.get('end', {})
            cleaned_events.append({
                'id': event.get('id', ''),
                'summary': event.get('summary', 'No Title'),
                'description': event.get('description', ''),
                'start': start.get('dateTime', start.get('date', '')),
                'end': end.get('dateTime', end.get('date', '')),
                'location': event.get('location', ''),
                'attendees': [attendee.get('email', '') for attendee in event.get('attendees', [])],
                'status': event.get('status', '')
            })

        return cleaned_events
    except Exception as e:
        return [{"error": f"Failed to list events: {str(e)}"}]

def insert_calendar_event(calendar_id: str, summary: str, start_time: str, end_time: str, 
                         description: str = "", location: str = "", attendees: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Inserts an event into the specified calendar.

    Parameters:
    - calendar_id (str): The ID of the calendar where the event will be inserted.
    - summary (str): The title/summary of the event.
    - start_time (str): Start time in ISO format (e.g., "2024-01-01T10:00:00Z").
    - end_time (str): End time in ISO format (e.g., "2024-01-01T11:00:00Z").
    - description (str, optional): Description of the event.
    - location (str, optional): Location of the event.
    - attendees (list, optional): List of attendee email addresses.

    Returns:
    - dict: The created event or error information.
    """
    if not calendar_service:
        return {"error": "Calendar service not available"}
    
    if not all([calendar_id, summary, start_time, end_time]):
        return {"error": "Missing required parameters: calendar_id, summary, start_time, end_time"}
    
    try:
        event_body = {
            'summary': summary,
            'description': description,
            'location': location,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            }
        }
        
        if attendees:
            event_body['attendees'] = [{'email': email} for email in attendees]
        
        event = calendar_service.events().insert(
            calendarId=calendar_id,
            body=event_body,
            sendUpdates='all'
        ).execute()
        
        return {
            "success": True,
            "event_id": event.get('id'),
            "summary": event.get('summary'),
            "start": event.get('start', {}).get('dateTime'),
            "end": event.get('end', {}).get('dateTime'),
            "message": f"Event '{summary}' created successfully"
        }
    except Exception as e:
        return {"error": f"Failed to create event: {str(e)}"}

def delete_calendar_event(calendar_id: str, event_id: str) -> Dict[str, Any]:
    """
    Deletes an event from the specified calendar.

    Parameters:
    - calendar_id (str): The ID of the calendar containing the event.
    - event_id (str): The ID of the event to delete.

    Returns:
    - dict: Success or error information.
    """
    if not calendar_service:
        return {"error": "Calendar service not available"}
    
    if not all([calendar_id, event_id]):
        return {"error": "Missing required parameters: calendar_id, event_id"}
    
    try:
        calendar_service.events().delete(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
        
        return {
            "success": True,
            "message": f"Event {event_id} deleted successfully"
        }
    except Exception as e:
        return {"error": f"Failed to delete event: {str(e)}"}

def update_calendar_event(calendar_id: str, event_id: str, **kwargs) -> Dict[str, Any]:
    """
    Updates an existing event in the specified calendar.

    Parameters:
    - calendar_id (str): The ID of the calendar containing the event.
    - event_id (str): The ID of the event to update.
    - **kwargs: Event properties to update (summary, description, start, end, location, etc.)

    Returns:
    - dict: The updated event or error information.
    """
    if not calendar_service:
        return {"error": "Calendar service not available"}
    
    if not all([calendar_id, event_id]):
        return {"error": "Missing required parameters: calendar_id, event_id"}
    
    try:
        event = calendar_service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=kwargs
        ).execute()
        
        return {
            "success": True,
            "event_id": event.get('id'),
            "summary": event.get('summary'),
            "message": f"Event '{event.get('summary', '')}' updated successfully"
        }
    except Exception as e:
        return {"error": f"Failed to update event: {str(e)}"}