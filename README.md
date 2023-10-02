

# Table of Contents

- [Project Name](#project-name)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)


## Introduction

This is a project in response to Intuit take home assessment for backend engineer role.

## Features

- running the project exposes an API at http://127.0.0.1:5000/api/ on local
- load  http://127.0.0.1:5000/api/hello to test response. 
- project comprises of three endpoints namely checkin, service and servicepro. 
- Flask has been used as the python framework.
- Redis has been used to store and update various data structures used as queue and counters.
- For current scope, JSON is used to store customer data. 

## Installation


```bash
brew install redis
redis-server
python3 -m venv venv
```
clone the repo

```bash
cd backend-service-scheduler-kgaurav
source env/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

venv might need reactivating using after installing requirements.txt.
You should replace the email credentials in config.json but it should work as is. 


## Usage


- Use postman with POST as method, for  "http://127.0.0.1:5000/api/checkin" with a body like 
{
    "client_phone":"123-456-7890"
}


Two methods next_customer and next_customer_pro can b used to achieve the following processing 
 - processing all  VIPs before regular
 - processing VIPS at twice the rate as regular.

This checks in the client depending on the type into one of the two lists. 
- Use postman with POST as method,  "http://127.0.0.1:5000/api/service" to get a service no based on the . 
- Use postman with POST as method,  "http://127.0.0.1:5000/api/servicePRO" to get a service no based on the logic #2. 

 - The application has capability to sms the service no to the customer using Twilio. Twilio creddentials might need updating. 

