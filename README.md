
# Project Name

This is a project in response to Intuit take home assessment for backend engineer role.

## Table of Contents

- [Project Name](#project-name)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)


## Introduction

A brief introduction to your project and what it does.

## Features

- running the project exposes an API at http://127.0.0.1:5000/api/ on local
- load  http://127.0.0.1:5000/api/hello to test response. 
- project comprises of three endpoints namely provider schedule post, client appointment request post and appoinment validation with expiry.
- Flask has been used as the python framework.
- logic for slots comprises of breaking providers schedule into 15 mins slot with index, checking for the same during client appointment request and then removing if available and validated.
- saving data between schedule request and validation been implemented using a key value pair in redis. 
- generated JSON token(also sent as part of request validation email) have been used as the key for above. 
- JSON files have been used to store providers and clients data as temp soln.
- next step would be to create config files, break up resources into different files before adding tests for  positive/negative scenarios.

## Installation


```bash
brew install redis
redis-server
python3 -m venv venv
```
clone the repo

```bash
cd scheduler
source venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```


venv might need reactivating using after installing requirements.txt.
You should replace the email credentials in config.json but it should work as is. 


## Usage

- add your own email and details to helpers.py

- Use postman with POST as method,  "http://127.0.0.1:5000/api/schedule" with a body like 
{   
    "date": "2023-07-28",
    "start_time": "14:30",
    "end_time":"18:30",
    "provider_id":124
}
- Use postman with POST as method,  "http://127.0.0.1:5000/api/client_schedule" with a body like 
{   
    "date": "2023-07-28",
    "provider_id":124,
    "client_id":124,
    "requested_slot":60
}



# add your own email and details to helpers.py
# 

# Additional features

## Add a queue update mechanism
## Add an expected wait time.
## Send a text when turn arrives
