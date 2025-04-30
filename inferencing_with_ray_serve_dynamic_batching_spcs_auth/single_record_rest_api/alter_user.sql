use role securityadmin;

ALTER USER kipi_ltr_user SET RSA_PUBLIC_KEY='MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAq+zIdgyh92EKM8gQJdCN
bImC4y9MZL4IJum0R04J4GFKTb0UJTHRI9G8nJ6OIpprMCitftWLsliIxLIW6rj+
y55oLpWd8jYFFSc1x/H1LrqX2h+lo0P+cX52wfuAShuYLu6FvwV16myTGST67ppl
qytfQsgjiwti/IFOFTOm9U+dhOgIJYtl506VRHB1q/vs/FhAnH6N4bHOIrnXc/I/
EEbWe9S+/QOikja7QqkFY4zllsp3qfV9mcQk2NUcIcIRJPEGkICeeu7vmC0NjfNT
Z97spEuyIyh7jKoVHRxw6ltaU6fLsKe4l41Dtrl+TCsNiCgxTRxNtbFJzze9huyM
sQIDAQAB';

DESC USER kipi_ltr_user;
SELECT SUBSTR((SELECT "value" FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
  WHERE "property" = 'RSA_PUBLIC_KEY_FP'), LEN('SHA256:') + 1);

-- verify that above matches the result of the following:
--openssl rsa -pubin -in rsa_key.pub -outform DER | openssl dgst -sha256 -binary | openssl enc -base64