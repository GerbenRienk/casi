'''
The purpose of this module is to try to send a request to the castor-api
to obtain a list of records.

Created on 6-11-2020
@author: Gerben Rienk
Copyright 2020 TrialDataSolutions
'''

from utils.dictfile import DictFile
from utils.castor_api import CastorApi

def list_records():
    # read configuration file for client id and client secret and other parameters
    config=DictFile('casi.config').read()
    # make an instance of the api
    api = CastorApi(config)
    # try to get an access-token
    api.sessions.get_access_token(verbose=False)
    
    #request the studies
    response = api.records.list(study_id='2A72D9CC-06B5-0078-B089-A5456C7A7024', verbose=False)
    
    # display the records in the response    
    for one_record in response['records']:
        print(one_record) 
          
if __name__ == '__main__':
    list_records()