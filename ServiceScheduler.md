# Service Scheduler

## Description¶
Design and implement a service scheduler for an in-person customer service center (Very similar to genius bar at the Apple centers or Xfinity store service).

1. Customer walks into the store and checks in. They are given a ticket with a sequential service number.
2. The service number is called by the staff in the order determined by the scheduler.
3. There are 2 different tiers of customers:

   1) Regular customers are serviced in the order they arrive.

   2) VIP customers. VIP customers are given higher priorities compared to Regular customers.

### Part 1¶
Design class for customer and ServiceScheduler with required high-level characteristics.

#### Important notes & answers to common questions:
* Scheduler only need to handle in person scheduling. There is no other type of scheduling, such as online scheduling, phone calls, etc.
* All customers have their information records in the system.
* To schedule, we need customer’s name and phone number.
* For simplicity, all service requests go through the same scheduling/service process.

### Part 2¶
Implement the ServiceScheduler to serve ALL VIP customers before serving regular customers. Implement two methods checkIn(Customer) and getNextCustomer()

#### Important notes & answers to common questions:
* Serving a customer is an atomic operation, i.e., we do not stop serving a regular customer in the middle of the service when a VIP customer walks in.

### Part 3¶
Implement the scheduler to make sure 2:1 VIP vs. Regular customer processing rate. Modify getNextCustomer() method to implement the customer processing rate.

---

## What We’re Looking For
We’re not assessing puzzle-solving ability with this question, we’re assessing overall code quality. We’ll evaluate your assignment by looking for a few things:


**Functionality**
* Does the code do what it should?
* Does it handle edge cases?
  
**Quality**
* Is the code readable & maintainable?
* Is the code well-organized?

**Performance**
* Does the code balance reasonably fast execution with readability?

**Pragmatism**
* Are the above factors balanced well against the limited time to implement the solution?

---
## Submission
Please zip your entire exercise directory and send it back to us via email. You are free, but not required, to create a Git repository for your work, just remember to include your .git directory in your zip if you do!


Best of luck! Thanks for taking the time to interview with Mailchimp.