# LTR Model

This repo contains a Snowflake notebook called `LTR model.ipynb` that builds a Learning to Rank (LTR) model designed for personalized credit card offer recommendations and deploys to SPCS for inferencing via model registry. 



## Best practices for setting up REST API

### Provide minimal access to the application that will be used to access resources.
USAGE on DATABASE, SCHEMA AND SERVICE ENDPOINT

For example:

```
use database partners_db;
use schema kipi_sch;
use role securityadmin;

create role if not exists kipi_ltr_role;
CREATE USER if not exists kipi_ltr_user PASSWORD='Snowflake123!' DEFAULT_ROLE = kipi_ltr_role MUST_CHANGE_PASSWORD = false;
grant role kipi_ltr_role to user kipi_ltr_user;
grant role kipi_ltr_role to role sysadmin;

use role sysadmin;
grant usage on database PARTNERS_DB to role kipi_ltr_role;
grant usage on schema KIPI_SCH to role kipi_ltr_role;
GRANT SERVICE ROLE PARTNERS_DB.KIPI_SCH.KIPI_LTR_SERVICE!ALL_ENDPOINTS_USAGE TO ROLE kipi_ltr_role; 
```


### Setup Key pair auth
- openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
- openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
- ALTER USER kipi_ltr_user SET RSA_PUBLIC_KEY='MIIBIjANBgkqh...';

For example: see alter_user.sql in single_record_rest_api folder

### Testing REST API

Two methods are included here. 

#### Single call to REST API via notebook
See `single_record_rest_api` folder.

#### Using locust
See `locust` folder. 
1. Make changes to locustfile.py
2. Make changes to execute.sh
3. Run `sh execute.sh`
