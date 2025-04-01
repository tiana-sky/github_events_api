0. Name: GitHub Events Tracker

1. Description:
An application for tracking activity in specified GitHub repositories.
It collects events, saves them to a database, and provides statistics via REST API.


3. Functionality:
Monitoring of up to five repositories.
Statistics collection: 7 days or 500 events (whichever is less).
Providing statistics via REST API.
Calculating the average time between consecutive events for each combination of event type and repository name.
Updates statistics every hour.

4. Run:
python main.py

5. Run the scheduler to automatically update the data:
python scheduler.py


6. Structure the project:
main.py - here we add the repositories we want to track 
github_client.py 
api.py
scheduler.py 
events.db - database which contans events
.env - this is where we write the GITHUB token. 

7. Launch the application:
uvicorn api:app --reload



