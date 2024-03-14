# argo-probe-eosccore-helpdesk

Metrics about the EOSC-Core helpdesk.
The first one refers to Helpdesk checkhealth . You can see the current health state of Helpdesk. 

## Overview
The metric does the following interaction with EOSC Helpdesk REST API:

 - api/v1/monitoring/health_check

## Pre-requisites:
- None

## How it works?

```
$ python check_healthcheck.py 
usage: check_healthcheck.py -K https://eosc-helpdesk.eosc-portal.eu/ -t TOKEN [-t TIMEOUT] [-v] 
                       

Helpdesk metric script
required arguments 
 -H URL, --hostname URL     Base URL of HELPDESK instance to test.
 -k, --token                The token to use for the check 

optional arguments:
  -h, --help            show this help message and exit
   -t TIMEOUT, --timeout TIMEOUT
                        Timeout of the test. Positive integer.
  -v, --verbose         Increase output verbosity
```

Example

`$ python check_healthcheck.py  -H https://eosc-helpdesk.eosc-portal.eu/ -k TOKENVALUE -vv`

### Success example response

```
OK, records, metadata schemas and files are accessible.
```

### Critical example response

```
CRITICAL, 92 failing background jobs;Failed to run background job #1
```

## Based on 
Detailed information may be found from here  [Monitoring](https://admin-docs.zammad.org/en/latest/system/monitoring.html)

