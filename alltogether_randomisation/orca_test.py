'''
Copied on 17 Oct 2019
from /utils/oli_test.py
@author: GerbenRienk
'''
import time
import datetime
from utils.logmailer import MailThisLogFile
from utils.dictfile import readDictFile
from utils.castor_api import CastorApi
from utils.pg_api import ConnToOliDB, PGSubject
from utils.reporter import Reporter
#from _operator import itemgetter

access_token = "x"

def cycle_through_syncs():
    # indicate that we are going to use access_token globally
    global access_token
    # read configuration file for client id and client secret and other parameters
    config=readDictFile('alltogether.config')
    # start a report
    my_report = Reporter()
    
    # start with requesting an access token, which we can use for about an hour
    api = CastorApi(config['ApiUrl'])
    access_token_request = api.sessions.get_access_token(config['client_id'], config['client_secret'])
    access_token = access_token_request.get('access_token')
    # print('access token before loops %s' % access_token)            
    if(access_token is None):
        # something is wrong with either the url, the client id or the client secret 
        my_report.append_to_report('could not get a access token with given client id and secret')
    else:
        # apparenty we have a token, so let's start looping    
        start_time = datetime.datetime.now()
        my_report.append_to_report('cycle started at ' + str(start_time))
    
        # create a connection to the postgresql database
        # conn = ConnToOliDB()
        # my_report.append_to_report(conn.init_result)
        
        while True:
            update_token(api, config)
            my_report.append_to_report('I\'m in the loop with access token %s' % access_token)
             
            # some book keeping to check if we must continue looping, or break the loop
            # first sleep a bit, so we do not eat up all CPU
            time.sleep(int(config['sleep_this_long']))
            current_time = datetime.datetime.now()
            difference = current_time - start_time
            loop_this_long = config['loop_this_long']
            max_diff_list = loop_this_long.split(sep=':') 
            max_difference = datetime.timedelta(hours=int(max_diff_list[0]), minutes=int(max_diff_list[1]), seconds=int(max_diff_list[2]))
            if difference > max_difference:
                break
        
        # we're finished looping, so write this in the report
        my_report.append_to_report('finished looping from %s till %s.' % (start_time, current_time))
        # close the file so we can send it

    my_report.close_file()
    # MailThisLogFile('logs/report.txt')

def update_token(api, config):
    global access_token
    # use endpoint user to check if the access token is still valid and if not
    # then request a new one
    # let's first request the user info
    if  api.users.user(access_token) is None:
        access_token_request = api.sessions.get_access_token(config['client_id'], config['client_secret'])
        access_token = access_token_request.get('access_token')

    
if __name__ == '__main__':
    cycle_through_syncs()
