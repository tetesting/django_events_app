# Django Events App


An events app that aims to follow the best practices of developing Django web apps (while some dude, a.k.a. me, is learning how to use Django). Hopefully I can one day create a useful tutorial out of this.


## What it Currently does:

Features for Users:

    - Registration
    - Log on / Log off
    - Change Profile Settings

Features for Events:
    
    - Create Event
    - Inspect Event
    - Attend Event
    - Withdraw from Event
    - Change Event details
    - Delete Event

Home Page:

    - shows events that the current user is organizing
    - shows events that the current user is attending
    - shows upcoming events that the user is not attending

My Events:
    
    - shows events that the current user is organizing
    - shows events that the current user is attending
    
Upcoming events:

    - shows all upcoming events ( you can still attend/withdraw from them )

Past Events:

    - shows past events ( you cannot attend/withdraw from them )


## To-Do:

    - TESTS
    - user notifications
    - notifications for when events are modified or deleted
    - Calendar interface for inputting dates
    - event pagination
    - search events
    - tag events
    - tag users
    - AJAXify things up
    - flash messages for event attend/withdraw, event creation, event deletion
    - advanced search