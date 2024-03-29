#!/usr/bin/env python3
import argparse
import sys

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
    print("-h, --help  show this help message and exit")
    print("-t timeout")
    print("-v verbose")
    print("-k token")


def ValidateValues(arguments):
    """ Validate values - input values """

    if arguments.timeout <= 0:
        print(f"CRITICAL - Invalid timeout value: {arguments.timeout}\n")
        print_help()
        sys.exit(2)

    if arguments.url is None:
        print("CRITICAL - No URL provided\n")
        print_help()
        sys.exit(2)

    if arguments.token is None:
        print(
            "CRITICAL - No token is provided. "
            "Token is needed to fetch the healthcheck\n"
        )
        print_help()
        sys.exit(2)

    if not arguments.url.startswith("http"):
        print(
                f"CRITICAL - No schema supplied with URL, "
                f"did you mean https://{arguments.url}?\n"
        )
        print_help()
        sys.exit(2)


def debugValues(arguments):
    """ Print debug values.
        Args:
            arguments: the input arguments
    """
    if arguments.debug:
        print(f"[debugValues] - URl: {arguments.url}")
    if arguments.timeout != '':
        print(f"[debugValues] - timeout: {arguments.timeout}")
    if arguments.debug != '':
        print(f"[debugValues] - verbose: {arguments.debug}")


def checkHealth(url, timeout):
    """ Check service status.
        Args:
           url : service URL
           timeout : how long should we wait for a response from the server
    """
    u = url
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

    else:
        perf_data = \
            f"|time={out.elapsed.total_seconds()}s;size={len(out.content)}B"
        if out.status_code != 200:
            description = \
                f"WARNING - Unexpected status code {out.status_code}{perf_data}"
            exit_code = 1
            return description, exit_code

        else:
            health = out.json()['healthy']
            message = out.json()['message']

            if health is True:
                description = f"OK - Service reachable: {message}{perf_data}"
                exit_code = 0
                return description, exit_code
            else:
                description = \
                    f"CRITICAL - Unexpected response: {message}{perf_data}"
                exit_code = 1
                return description, exit_code


def printResult(description, exit_code, arguments):
    """ Print the predefined values
        Args:
            description: the nagios description
            exit_code: the code that should be returned to nagios
            arguments: probe arguments
    """

    print(description)

    if arguments.debug > 0:
        debugValues(arguments)

    sys.exit(exit_code)


def main():
    parser = argparse.ArgumentParser(
        description='EOSC Helpdesk metric Supports healthcheck.'
    )
    parser.add_argument(
        "--url", "-u", help='The URL of EOSC Helpdesk service'
    )
    parser.add_argument(
        "--timeout", "-t", metavar="seconds", type=int, default=30,
        help="Timeout in seconds. Must be greater than zero"
    )
    parser.add_argument(
        "--token", "-k", metavar="token",
        help="the token required to display the status"
    )
    parser.add_argument(
        "--verbose", "-v", dest='debug', help='Set verbosity level',
        action='count', default=0
    )
    arguments = parser.parse_args()
    ValidateValues(arguments)

    url = arguments.url
    url = f"{url}/api/v1/monitoring/health_check?token={arguments.token}"

    description, exit_code = checkHealth(url, arguments.timeout)

    printResult(description, exit_code, arguments)


if __name__ == "__main__":
    main()
