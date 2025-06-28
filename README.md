# Google Calendar AI Agent

A Streamlit-based chat interface for interacting with a Google Calendar AI agent with full calendar management capabilities.

## Features

- **Chat Interface**: Interactive Streamlit chat interface for natural language calendar queries
- **Calendar Management**: 
  - List all calendars
  - List events from calendars
  - Create new events
  - Delete events
  - Update existing events
- **Google Calendar Integration**: Full integration with Google Calendar API
- **Session State Management**: Conversation history persistence
- **Error Handling**: Robust error handling and user feedback

## Setup

1. **Install Dependencies**:
   ```bash
   pip install streamlit google-api-python-client google-auth-httplib2 google-auth-oauthlib
   ```

2. **Google Calendar API Setup**:
   - Ensure you have a `client_secret.json` file in the project directory
   - The first time you run the app, it will prompt for Google Calendar authorization
   - Authorization tokens are automatically saved for future use

## Running the App

```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

## Usage Examples

Once the app is running, you can interact with it using natural language:

- **"List calendars"** - Shows all available calendars
- **"List events"** - Shows upcoming events from your primary calendar
- **"Create event"** - Provides instructions for creating new events
- **"Show my schedule"** - Lists your upcoming events

## Calendar Tools Functions

The app includes the following calendar management functions:

- `list_calendar_lists(max_capacity=200)` - List all calendars
- `list_calendar_events(calendar_id, max_capacity=20)` - List events from a specific calendar
- `insert_calendar_event(calendar_id, summary, start_time, end_time, ...)` - Create new events
- `delete_calendar_event(calendar_id, event_id)` - Delete events
- `update_calendar_event(calendar_id, event_id, **kwargs)` - Update existing events
- `create_calendar_list(calendar_name)` - Create new calendars

## Troubleshooting

1. **Authentication Issues**: 
   - Delete the `token files` directory and restart the app
   - Ensure your `client_secret.json` is valid

2. **Import Errors**:
   - Make sure all dependencies are installed
   - Check that you're in the correct directory

3. **Calendar Access**:
   - Ensure your Google account has access to the calendars you're trying to manage
   - Check that the Google Calendar API is enabled in your Google Cloud Console

## Technical Details

- **Backend**: Python with Google Calendar API
- **Frontend**: Streamlit for the chat interface
- **Authentication**: OAuth 2.0 with automatic token refresh
- **Error Handling**: Comprehensive error handling with user-friendly messages

## Note

This is a fully functional Google Calendar management system that works without external AI libraries. The agent can handle natural language queries and perform calendar operations directly through the Google Calendar API. 