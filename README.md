## Enterprise IaC Challenge

### Overview
This challenge consists of multiple exercises intended to evaluate the extent
of your ability to do the following within an Enterprise level structure:
  - Design and implement Terraform based IaC automation solutions
  - Design for and utilize an AWS based ecosystem
  - Use software development best practices

Each exercise can be viewed as a phase where the previous exercise is a
prerequisite of the next. Therefore read through all exercises before designing
as each will impact the overall approach.

### Expectations / Requirements
1. The solutions / code must be your own but can be based on research, and/or
   incorporation of other tools, libraries, and frameworks.
2. Follow software development best practices. Remember what IaC stands for.
3. Open-source Terraform must be utilized as the basis of the solutions.
4. You are encouraged to utilize any other open-source tools, libraries, and/or
   frameworks that will wrap around or integrate with open-source Terraform in
   order to successfully complete this challenge as effectively and efficiently
   as possible.
5. Non open-source products / services, such as Terraform Cloud and Terraform
   Enterprise, are not in scope and should not be utilized.
6. Your version control repositories should be git based and publically
   available.
7. AWS CloudFormation is out of scope with the exception of situations where it
   required in order to properly configure / utilize another AWS service.
8. AWS account(s) and initial user based credentials for running foundational
   automation will be provided.
9. For any infrastructure created, assume it is for production. Therefore the
   IaC / configuration should reflect production best practices. Part of best
   practices is cost optimization. Keep the resource sizing as small as
   possible while ensuring resiliency.
10. The resulting IaC, images, etc must be functional. We will execute your IaC
    based on your instructions to validate that the in scope ecosystem:
    - can be properly created.
    - can be successfully destroyed.
    - functions correctly. Ensure the application is working properly by
      querying the api. Examples:
```bash
curl localhost:8080/vehicles | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  292k  100  292k    0     0  7100k      0 --:--:-- --:--:-- --:--:-- 10.9M
[
  {
    "city": "Heshui",
    "country": "China",
    "id": 1,
    "make": "Nissan",
    "model": "Murano",
    "postal_code": null,
    "price": "192647.33",
    "state": null,
    "street_address": "501 Crownhardt Court",
    "vin": "3GYT4MEF2BG786575",
    "year": 2011
  },
  {
    "city": "Prinza",
    "country": "Philippines",
    "id": 2,
    "make": "Mitsubishi",
    "model": "Galant",
    "postal_code": "2008",
    "price": "71771.61",
    "state": null,
    "street_address": "8797 Bowman Lane",
    "vin": "WAUGL58E15A942818",
    "year": 1986
  },
  {
    "city": "Gala",
    "country": "Portugal",
    "id": 3,
    "make": "Volvo",
    "model": "XC70",
    "postal_code": "3090-710",
    "price": "180010.20",
    "state": "Coimbra",
    "street_address": "64 Warner Junction",
    "vin": "JH4KB16637C976351",
    "year": 2007
  },
  .
  .
  .
```
```bash
curl localhost:8080/vehicles/56 | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   291  100   291    0     0  38717      0 --:--:-- --:--:-- --:--:--  142k
{
  "city": "Philadelphia",
  "country": "United States",
  "id": 56,
  "make": "Nissan",
  "model": "Sentra",
  "postal_code": "19151",
  "price": "185853.53",
  "state": "Pennsylvania",
  "street_address": "50 Messerschmidt Pass",
  "vin": "JTHKD5BH1D2870961",
  "year": 2010
}
```

### Instruction
1. Read through all remaining information below before starting to build.
2. In your primary repository, ensure there is:
   - a README.md file
     - Provide step by step instructions for how to utilize your solution for
       both creation and destruction.
   - a SOLUTION.md file
     - Utilize to provide insight into your thought process. At a minimum,
       explain the rationale behind your design and tools decisions.
   - the Dockerfile that is the basis for a container with all necessary tools
     to execute your solution.
3. When you have finished, notify the person who provided you this challenge.
   Be sure to include:
   - the link to your primary repository
   - any feedback you have regarding this challenge

### Background Scenario
A company has a Cloud and Automation Center of Excellence (CoE) group and two
application (app) teams. Part of the responsibilities of the CoE are:
 - enabling app teams to be as effective and efficient as possible with the
   proper guardrails in place.
 - standardization and operational management of the foundational elements of
   AWS (Ex: AWS accounts creation, non app specific IAM, core networking, 
   encryption, monitoring, etc) and the IaC for these elements.
 - standardizing and packaging reusable IaC for the various app teams to utilize.
 - providing oversight, guidance, recommendations, etc for the app teams.
 - potentially acting as a resource on one or both app teams.
 - performing the above with a strong focus on security and cost efficiency.

Each app team is responsible for the development, testing, cloud based
infrastructure, and automation specifically for their apps. These teams are
required to follow the CoE standards and utilize the CoE designated tools,
libraries, modules, etc. Due to the security requirement of least privilege,
each app team should not have the ability to modify the infrastructure of the
other. 

For this challenge, you are a member of the CoE group and also acting as a
resource on both app teams delivering IaC. The first app team will be called
"B2C". They primarily write custom applications to be used by consumers. The
second app teams is called "B2B". They primarily write custom applications and
manage large amounts of data for use by business customers.


### Exercise 1 - The Big Picture
Before the app teams can create their app specific infrastructure and deploy,
they each need a production environment that their automation can be written
and executed against. They will expect that any information they need to
know about their AWS environment is provided via Terraform state file(s) where
the patterns in naming and location of state file(s) is/are well defined.

As a CoE resource, you are tasked with:
 - creating/configuring the foundational elements for the AWS environments where:
   - only the us-east-1 region will be utilized.
   - HA will be required.
   - OS level access is out of scope.
   - there will be interaction between some systems of each app team.
 - providing identity and permissions for execution of the application related
   IaC that cannot modify the foundational elements the CoE is responsible for
   nor the resources of the other app team.
 - providing the app teams need to know information regarding the AWS
   environments for their IaC via Terraform state file(s).

### Exercise 2 - Common Occurrences
Relational databases and containers for web based applications are often
utilized by both app teams. As a CoE resource, you are tasked with:
- writing a Terraform remote module for standardizing the creation of
  relational databases and loading initial data
   - utilize AWS RDS
   - only Aurora serverless is allowed
   - can be MySQL 8.0 or PostgreSQL 13
   - for MySQL:
     - ensure table names are converted to lowercase on storage and lookup
       (lower_case_table_names = 1)
     - change the time a InnoDB transaction waits for a row lock to 2 minutes
       (innodb_lock_wait_timeout = 120)
   - for PostgreSQL:
     - set time to wait on a lock before checking for a deadlock to 2 minutes
       (deadlock_timeout = 120s)
- writing a Terraform remote module for standardizing the creation of a
  kubernetes cluster and workload deployment
   - utilize AWS EKS with Fargate
   - remember to keep it small as possible by default

### Exercise 3 - Help out the App Teams
1. The B2B app team needs a rdbms for storing inventory of vehicles. The ddl
   and data for this database is [here](/b2b/data/vehicle_inventory/). Provide
   a solution that:
    - utilizes the RDS module you wrote in exercise 2
    - is based on PostgreSQL compatibility
    - is highly available

2. The B2C app team has developed a python based REST API for retrieving
   information about vehicles for sale based on the data source being the B2B
   app team's vehicle inventory database. The application code to deploy is
   [here](/b2c/src/vehicles_api/). Provide a solution that:
    - utilizes the module you wrote in exercise 2 for kubernetes cluster
      and workload deployment
    - allows the application to utilize the vehicle inventory database
      - limit to read only access


    Note: The functional testing of the application is out of scope. Assume the
    application logic will always be successfully tested prior to your
    packaging / deployment code being executed.

 
