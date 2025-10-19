import datetime
from zoneinfo import ZoneInfo
from flask import Flask, jsonify, send_from_directory
import all_events_fetcher


#RUN THIS!


# 1. Initialize the Flask App
app = Flask(__name__)

# 3. Create the API endpoint to serve the data
@app.route('/api/events')
def get_events():
    events_data_raw = all_events_fetcher.fetch_all_events()
    # JSON cannot handle Python datetime objects, so we must convert them to strings.
    # ISO 8601 format is the standard and works great with JavaScript.
    json_ready_events = []
    for event in events_data_raw:
        # Create a copy to avoid modifying the original list
        event_copy = event.copy()
        
        # Standardize the datetime key and format it
        if 'Datetime' in event_copy:
            dt_obj = event_copy['Datetime']
            # Convert datetime object to a string (e.g., "2025-08-30T18:00:00-05:00")
            event_copy['datetime_str'] = dt_obj.isoformat()
            del event_copy['Datetime'] # Remove the original datetime object
        
        json_ready_events.append(event_copy)
        
    return jsonify(json_ready_events)

# 4. Create a route to serve your HTML file
@app.route('/')
def index():
    # This serves the aggie_traditions.html file from the same directory
    return send_from_directory('.', 'aggie_traditions.html')

# 5. Run the app
app.run(debug=True)