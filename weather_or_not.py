# C:\Stuff\projects\weather_or_not\weather_or_not

import os
import webbrowser
import requests
import logging
import csv
from bs4 import BeautifulSoup
from collections import OrderedDict

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


def build_payload(i, airport_route):
    """ Build request payload, add Airport data and time here
    :return: payload
    """
    # Dallas -96.7970, 32.7767
    # Denver -104.9903, 39.7392
    # Salt Lake -111.8910, 40.7608
    # Seattle -122.3321, 47.6062
    # Dallas to Denver:
    # path = str(i) + ';-96.7970,32.7767;-104.9903,39.7392'
    # Salt Lake to Seattle
    path_request = str(i) + airport_route
    payload = {
        'dataSource': 'airsigmets',
        'requestType': 'retrieve',
        'format': 'xml',
        #'flightPath': '57.5;-96.7970,32.7767;-104.9903,39.7392'
        'flightPath': path_request
    }
    return payload

# returns dictionary from csv_file that maps iata code to latitude and longitude
def get_dictionary(csv_file):
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f)
        airport_list = map(tuple, reader)
    # remove title tuple
    airport_list.pop(0)
    # initialize dictionary
    # iterate through tuples in airport_list
    airport_dict = dict()
    for airport in airport_list:
        # airport[0] = iata, airport[5] = lat, airport[6] = long
        airport_dict[airport[0]] = (airport[5], airport[6])
    return airport_dict

def lookup_airport(airport_dict, iata):
    lat_long = airport_dict[iata]
    return lat_long


def build_path(airport_dict, itinerary):
    """
    Build coordinate path string from ordered list of iata codes.
    :param itineray: list of iata codes
    :return: string of semi-color separated lon,lat pairs
    """
    lonlat_string = ''
    for airport in itinerary:
        lat_long = lookup_airport(airport_dict, airport)
        # starts with semi-colon
        lon_lat = ';' + str(lat_long[1]) + ',' + str(lat_long[0])
        lonlat_string += lon_lat
        print 'lonlat_string = ', lonlat_string
    return lonlat_string

def get_severity(severity, segment):
    return 'severity="' + severity + '"' in str(segment)

# TODO: improve runtime performance 
def get_severities_count(bs_search_result):
    severities_count = OrderedDict()

    none = 0
    lt_mod = 0
    mod = 0
    mod_sev = 0
    sev = 0

    for i in bs_search_result.find_all('hazard'):
        if 'severity="' + 'NONE' + '"' in str(i):
            none += 1
        elif 'severity="' + 'LT-MOD' + '"' in str(i):
            lt_mod += 1
        elif 'severity="' + 'MOD' + '"' in str(i):
            mod += 1
        elif 'severity="' + 'MOD-SEV' + '"' in str(i):
            mod_sev += 1
        elif 'severity="' + 'SEV' + '"' in str(i):
            sev += 1

    severities_count['NONE'] = none
    severities_count['LT-MOD'] = lt_mod
    severities_count['MOD'] = mod
    severities_count['MOD-SEV'] = mod_sev
    severities_count['SEV'] = sev

    return severities_count

#########################################################
# noinspection PyPackageRequirements
if __name__ == "__main__":
    # push?
    #turn_on_logging()  # comment out when not

    csv_file = 'airports.csv'
    airport_dict = get_dictionary(csv_file)
    # check "0E0" and "0E8"
    itinerary = ['0E0', '0E8']
    #itinerary = ['SLC', 'SEA']  # Salt Lake Intl to Seattle-Tacoma
    #itinerary = ['TPA', 'TPF']  # Tampa Intl to Peter O. Knight
    path = build_path(airport_dict, itinerary)
    print 'path = ', path

    sig_dict = {}
    with open('Output.txt', 'w') as f:
        f.write('Path Width, Number of AIRSIGMETS\n')
        for i in range(1, 10, 10):
            """request_payload = build_payload(i, path)
            # open a session and get response for default page
            session = requests.Session()
            url = 'https://www.aviationweather.gov/adds/dataserver_current/httpparam'
            response0 = session.get(url, params=request_payload)
            write_response(response0, 'Response')

            open_response_in_browser('Response')"""

            bs_search_result = BeautifulSoup(read_response_content('Response.html'), 'lxml')
            #airsigmet = bs_search_result.find_all('airsigmet')
            output_string = '    ' + str(i) + '            ' +\
                            str(len(bs_search_result.find_all('airsigmet'))) +\
                            '\n'
            f.write(output_string)
            print get_severities_count(bs_search_result)
        # for l in bs_search_result.find_all('hazard'):
        #     # f.write(str(l) + '\n')  # works!
        #     print get_severity('NONE', l)
