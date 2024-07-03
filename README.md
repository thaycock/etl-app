
# FYI

Added via file upload because of the configuration with my personal account and key management. The Pycache files should not be in there but they are even though they are specified to not be inlcluded in the gitignore. This can be fixed by deleting them and doing another git init if they are still tracked by the diff system.


# Project

This project acts as an ETL service to obtain and load data for an exercise.

Please ask any questions with thoughts or concerns, Failing a  pre-employment screening after being asked to write an exercise is not a nice feeling when these exercises represent a day of my life to create, a simple question or asking for clarification on something is something I would happily answer

https://www.linkedin.com/in/travis-haycock-b9a53b2a0/




# How To Run And Testing

 1. ./scripts/build_container.sh
 2. docker-compose up
 3. execute sanity check and other requests

 ## Sanity check   /status endpoint

 curl -X GET http://localhost:5000/status

 - Expected response is: {
  "message": "Public status check endpoint is operational",
  "success": true
}


## Start ETL Service
 curl -X GET http://localhost:5000/start-etl-job

# Get all collections from the DB
 curl -X GET http://localhost:5000/latest-event-data



# About This App

I decided to use a Flask application for this ETL. The reason why I did this is because ETL services and projects exist in different states, some exist as a stand-alone application with an entry script that runs ETL services on a service like AWS Batch, Ec2, or more. For this specific exercise instead of just creating an entry script I thought it would be beneficial to set up a web server with it to demonstrate competency working with other stacks as well as there were no restrictions against designing it like this.

The application leverages Docker so it should be easily run on a host machine with the expectation and precondition that Docker is set up on the host machine see more here: https://www.docker.com/


As previously mentioned Flask is used on this application as a controller, there are (3) endpoints total a status endpoint to verify the server is up and running, this can be pasted in the terminal and ran.

The second endpoint is `start_etl_job` this job does the data collection, transformation, and loading/mapping into the table called ` us_event_data`. after which point the data would be present.

My third endpoint obtains all the loaded data into the database, if the above is called N amount of times there will be an equal amount of data or rows present in the `us_event_data` which is achieved using the select all statement.



# Design choices

Because I did not put this on another service like AWS I used the Flask approach, although not common to use an ETL like this to interface with, working in and around a Flask application or another service is common while working on these types of projects. Normally the ETL exists as a standalone piece of the pipeline, a component of the pipeline that is called from somewhere else with some cron job, timer or periodic run that is controlled by various pieces of technology.

In the past, I have contributed to a ETL using AWS Batch. The ETL had an entry script into the application that allowed env vars to be set. The ETL was part of 4 pieces a Vuejs front end, Flask backend, AWS, and a Python application and the ETL was called ultimately by the front via user events which then relayed the requested action to the backend where more context was added about the specific user or client and ultimately that information was served to the AWS Batch configuration which received all it's runtime variables and other required pieces of information by this call.


# Handlers

Handlers refer to a specific piece of functionality that is handled in this application i.e to break it up further in the future a 
An Extraction Handler could be used, a Transform Handler, and finally a Loader handler. Because this application is quite small and does not have a lot of routes and only loads data from one endpoint I did not create these separate handlers rather just created a generic ETL handler for now, I would be motivated to break it up more if more complexity was added.


# Blueprints

Blueprints are a design pattern used for routes in this context, it would allow me to quickly add another file pertaining to specific routes and create a new endpoint and have it up and running within five minutes, the scalability this gives is great and it really supersets itself when leveraging the idea about the handlers where we again, can add another handler if there is justification to do so and keep all business logic or actions separate from one another - this really aids us in clean scalable code and testing when we want to really compartmentalize the functionality.


# Queries 

For this application, I used raw queries my motivation behind this is that there was no specific project requirement here and I know both queries and ORM, sometimes ORM can be a bit of an investment upfront configuring it in a Flask or Django application. 80%
of the time ORMs are employed because of database versioning and not everyone always knows SQl which can make it hard to maintain in bugs can arise. I created a folder called query services which houses all my queries for the application.

# Extraction

Extraction is done inside the `__extract_zip_file` but this is not the best area for it as it's done in the API loader base class, the base class should just be fetching the response for us, but because there is only one endpoint that is being called and there, this would be refactored in the instance more than one endpoint if called or data gathered from different sources.


# Transformation

Transformation is done inside the `__extract_zip_file` which in this context are the mappings


# Loaders

adopted idea of loaders, each request or different future areas of the apps that load data from different sources would have their own loaders for testability and seperation of concerns


# Theme

As you can see throughout this app there is a clear separation of concerns in key areas, I try to keep things separated and think within the scope of the application both present and future while remaining flexible to welcome scalable code and structures to the application. 



# Database

The database I used was PG as requested, I used liquibase to make this possible so there is a database living within the container(s) that can be accessed during runtime, the table structure is defined in `initial_tables.yaml` where all changesets are applied at container init.


# What I would do differently or what I would do if I had more time

I would first try to understand the target env as this dictates the application shape and form if this is to be launched on a batch, host computer, Jenkins server etc. The Flask application allows for a certain degree of flexibility and remains largely agnostic to runtime specifications; I can justify it like this - with the Flask application any cron job like AWS event bridge or another service can call the endpoint which will trigger a job along with the other endpoints, this separates any celery tasks or internal cron configuration. If this application is running on a Linux server there are a few options, we can create a cron job in Linux to call the endpoint every 1x hours which will trigger the ETL, or integrate Celery into this application to internalize a cron job.

- CircleCI config (1 hour)
- Testing pipeline ( 3 hours )
- Gather Future Project Requirements
- Implement JWT ( hypothetically if we were calling this from a authenticated service) i'd employ decorators and potential ACLs
- Advanced monitoring 


## Summary

There is a lot to do or can be done, but proper requirements and communication takes priority before advancing with development.



# What shows maturity in this application

Understanding that running this on different envs dictates architecture and other patterns applied to this application and things can change drastically depending on the project requirements.

Dividing the main functionality up into folders that pertain to a grouping or common functionality adds to scalability.

Not optimizing prematurely. Projects change, requirements, and features change - the software itself changes and is in constant refactoring during its lifecycle with a successful product. Investing too much time into a solution that is subject to change without
more context about the application where it would live, other services that it would interact with etc is a recipe for optimizing a codebase that will only need a bigger refactor in the near future.


- scalability ***
- proper pep8 formatting with black and isort
- use of doctrings
- classes
- keeping things more simple and clean rather that complicated and abstract where there is only one endpoint to load from


# Data Warehousing and tools

There are different tool sets I would use for this, we have access to application runtime logs in Cloudwatch but for extra business intelligence, we need to leverage different tooling and software classes that would be responsible for collecting this data.
The tooling is subjective and project specific and even the data we want to analyze. The classes to be built to manage this need to be well understood both from the software engineering side and business analytics side, the job of an engineering team in this context is to translate problems into digital solutions.

- New Relic for application specifics
- AWS Data Lake
- Metabase for customized queries to share with other non-technical teammates to pull stats 


There are many more options for this, there will be more options every Q as tools roll out and incentivize companies to try them.
What's important to remember is the tool is reliable and the right information can be obtained from it, if something works well
and is trusted without price gouging there is little value in changing the tooling set until it becomes a pain point or arrests us
from accomplishing a required task. My first Engineering Manager always used to say, we want to be cutting edge - not bleeding edge. The longer I go in my career the more I understand the truth and reality in that statement.


# AWS services I have worked with and know well

- Batch
- EC2
- S3
- Event bridge
- Mqtt
- Amplify
- App-Runner
- Routes
- Lambda
- Step Functions


I have personally built applications with all these technologies both professionally and personally and actively apply these daily and can back that up with my own applications in AWS.


# Testing Implementation

Pytest can be employed here, we can create another container that spins up our test env which can then run our tests, we can use tox or some other env management service to call this, i'd also have to add another entry script called run_tests.sh with the correct persmissions to call the tox command or entry point to our tests.

# Selenium 

I have used Selenium for Scraping and testing.
The Telus EMR app Canada: https://www.telus.com/en/health/health-professionals/clinics/med-access

The app was built by Macadamian Technologies 2017-2019 I worked both on the mobile app and the Robot testing framework that used Selenium we built whole testing suites based off Selenium.


