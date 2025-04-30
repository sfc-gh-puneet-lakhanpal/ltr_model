// Create Database, Warehouse, and Image spec stage
USE ROLE kipi_ltr_role;
USE DATABASE partners_db;
USE SCHEMA kipi_sch;
use warehouse XSMALL_WH;

--Image repo

create image repository if not exists image_repo;
show repo image repository image_repo;

create stage if not exists SPECS;

SHOW IMAGE REPOSITORIES IN SCHEMA;

alter compute pool kipi_ltr_spcs_cpu_ngrok_auth stop all;

-- Compute Pools --
CREATE COMPUTE POOL if not exists kipi_ltr_spcs_cpu_ngrok_auth
  MIN_NODES = 4
  MAX_NODES = 4
  INSTANCE_FAMILY = CPU_X64_L
  AUTO_RESUME = true;
-- Services --
drop service if exists kipi_ltr_spcs_ngrok_auth_service force;
CREATE SERVICE kipi_ltr_spcs_ngrok_auth_service
  IN COMPUTE POOL kipi_ltr_spcs_cpu_ngrok_auth 
  FROM @SPECS
  SPEC='ltr_rayservengrokauth.yaml'
  MIN_INSTANCES=4
  MAX_INSTANCES=4
  EXTERNAL_ACCESS_INTEGRATIONS=(ALLOW_ALL_INTEGRATION);

SHOW COMPUTE POOLS LIKE 'KIPI_LTR_SPCS_CPU_NGROK_AUTH';
SELECT VALUE:status::VARCHAR as SERVICESTATUS, VALUE:message::VARCHAR as SERVICEMESSAGE FROM TABLE(FLATTEN(input => parse_json(system$get_service_status('KIPI_LTR_SPCS_NGROK_AUTH_SERVICE')), outer => true)) f;

CALL SYSTEM$GET_SERVICE_LOGS('KIPI_LTR_SPCS_NGROK_AUTH_SERVICE',0 , 'ltr', 1000);



SHOW ENDPOINTS IN SERVICE KIPI_LTR_SPCS_NGROK_AUTH_SERVICE;