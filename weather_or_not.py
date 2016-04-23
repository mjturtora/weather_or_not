# C:\Stuff\projects\weather_or_not\weather_or_not

import os
import webbrowser
import requests
import logging
from bs4 import BeautifulSoup

# http://stackoverflow.com/questions/10588644/how-can-i-see-the-entire-http-request-thats-being-sent-by-my-python-application
# These two lines enable debugging at httplib level (requests->urllib3->http.client)
# You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# The only thing missing will be the response.body which is not logged.


def turn_on_logging():
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1

    # You must initialize logging, otherwise you'll not see debug output.
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def pretty_print_post(req):
    """
    Prints prepared requests to console
    Pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


def write_response(response, fname):
    ''' Save html to fname
    :param response: requests object
    :param fname: root name to save to
    '''
    with open(fname + '.html', 'w') as f:
        f.write(response.content)


def read_response_content(fname):
    with open(fname, 'r') as f:
        return f.read()


def open_response_in_browser(fname):
    """ Open in default browser
    :param fname: root name to save to
    """
    webbrowser.open(fname + '.html')


def build_payload():
    """ Build request payload, add Airport data and time here
    :return: payload
    """
    payload = {
        'dataSource': 'airsigmets',
        'requestType': 'retrieve',
        'format': 'xml',
        'flightPath': '57.5;-96.7970,32.7767;-104.9903,39.7392'
    }
    return payload

#########################################################
# noinspection PyPackageRequirements
if __name__ == "__main__":
    #turn_on_logging()  # comment out when not needed
    request_payload = build_payload()
    # open a session and get response for default page
    session = requests.Session()
    url = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam'
    response0 = session.get(url, params=request_payload)
    write_response(response0, 'Response')
    open_response_in_browser('Response')
    bs_search_result = BeautifulSoup(read_response_content('Response.html'), 'lxml')
    print(bs_search_result.get_text())
