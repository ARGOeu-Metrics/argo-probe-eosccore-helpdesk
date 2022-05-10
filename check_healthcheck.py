#!/usr/bin/env python

import os
import sys
import io
import time
import argparse
import json
import requests


def print_help():
        """ Print help values."""

        print("usage: check_healthcheck.py -H -k")
        print("--- ---- ---- ---- ---- ---- ----\n")
        print("main arguments:")
        print("-H hostname")
        print("-k token")
        print("\n")
        print("optional arguments:")
        print(" -h, --help  show this help message and exit")
        print("-t timeout")
        print("-v verbose")
        print("-k token")

def ValidateValues(arguments):
        """ Validate values - input values """

        if arguments.timeout <= 0:
            print("\nInvalid timeout value: %s\n" % arguments.timeout)
            print_help()
            exit()

        if arguments.hostname is None:
            print("\nNo hostname provided\n")
            print_help()
            exit()

        if arguments.token is None:
            print("\nNo token is provided. Token is needed to fetch the healthcheck\n")
            print_help()
            exit()

        if not arguments.hostname.startswith("http"):
            print("\nNo schema supplied with hostname, did you mean https://%s?\n" % arguments.hostname)
            print_help()
            exit()
 
def debugValues(arguments):
    """ Print debug values.
        Args:
            arguments: the input arguments
    """
    if arguments.debug:
        print("[debugValues] - hostname: %s" % arguments.hostname)
    if arguments.token != '':
        print("[debugValues] - token: %s" % arguments.token)
    if arguments.timeout != '':
        print("[debugValues] - timeout: %s" % arguments.timeout)
    if arguments.debug != '':
        print("[debugValues] - verbose: %s" % arguments.debug)
        
def checkHealth(URL, timeout):
    """ Check service status.
        Args:
           URL : service hostname
           timeout : how long should we wait for a response from the server
    """
    out = None
    u = URL
    try:
        out = requests.get(url=u, timeout=timeout)

    except requests.exceptions.SSLError:
        description = "WARNING - Invalid SSL certificate"
        exit_code = 1
        return description, exit_code
    except requests.exceptions.ConnectionError:
        description = "CRITICAL - Service unreachable"
        exit_code = 2
        return description, exit_code
      
    if out is None:
        description = "UNKNOWN - Status unknown"
        exit_code = 3
        return description, exit_code

    if out.status_code != 200:
        description = "WARNING - Unexpected status code %s" % out.status_code
        exit_code = 1
        return description, exit_code

    content = out.json()
    health = out.json()['healthy']
    message = out.json()['message']
    issues = out.json()['issues']

    if health is True:
        description = "OK - Service reachable:  %s" % message
        exit_code = 0
        return description, exit_code
    else:
        description = "CRITICAL - Unexpected response: %s"  % message
        exit_code = 1
        return description, exit_code

    description = "OK - Service reachable"
    exit_code = 0
    return description, exit_code
  
def printResult(description, exit_code):
    """ Print the predefined values
        Args:
            description: the nagios description
            exit_code: the code that should be returned to nagios
    """

    print(description)
    sys.exit(exit_code)

def main():

    start = time.time()
    parser = argparse.ArgumentParser(description='EOSC Helpdesk metric '
                                                 'Supports healthcheck.')
    parser.add_argument("--hostname", "-H", help='The Hostname of EOSC Helpdesk service')
    parser.add_argument("--timeout", "-t", metavar="seconds", help="Timeout in seconds. Must be greater than zero", type=int, default=30)
    parser.add_argument("--token", "-k", metavar="token", help="the token required to display the status")
    parser.add_argument("--verbose", "-v", dest='debug', help='Set verbosity level', action='count', default=0)
    arguments = parser.parse_args()
    ValidateValues(arguments)

    if arguments.debug > 0 :
        debugValues(arguments)

    URL = arguments.hostname
    URL = URL + 'api/v1/monitoring/health_check?token=' + arguments.token
    description, exit_code = checkHealth(URL, arguments.timeout)

    #time to run 
    rta = time.time()-start
    # Health check failed, unable to continue
    if exit_code > 0:
        printResult(description, exit_code)

    printResult(description, exit_code)

if __name__ == "__main__":
    main()
