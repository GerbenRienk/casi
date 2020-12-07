'''
The purpose of this module is to send multiple requests to the castor-api
to obtain a list of records for each study

This script uses a configuration file in json format with the same name.

Created on 7-12-2020
@author: Gerben Rienk
Copyright 2020 TrialDataSolutions
'''

from utils.dictfile import DictFile
from utils.castor_api import CastorApi
import json

def list_records():
    # start with reading the configuration file for this scriptlet
    with open('./list_records_multiple_studies.json') as script_conf_file:
        script_conf = json.load(script_conf_file)
    
    for api_conf in script_conf['configs']:
        print(api_conf['config_name'])
        
        # read configuration file for client id and client secret and other parameters
        config=DictFile(api_conf['config_name']).read()
        # make an instance of the api
        api = CastorApi(config)
        # try to get an access-token
        api.sessions.get_access_token(verbose=False)
        for study in api_conf['studies']:
            print(study['study_id'])
        
            #request the studies
            response = api.records.list(study_id=study['study_id'], verbose=False)
    
            # display the records in the response    
            for one_record in response['records']:
                print(one_record) 
          
if __name__ == '__main__':
    list_records()