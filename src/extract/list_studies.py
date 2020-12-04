'''
The purpose of this module is to try to send a request to the castor-api
to obtain a list of studies.

Created on 6-11-2020
@author: Gerben Rienk
'''

from utils.dictfile import DictFile
from utils.castor_api import CastorApi

def list_studies():
    # read configuration file for client id and client secret and other parameters
    config=DictFile('casi.config').read()
    # make an instance of the api
    api = CastorApi(config)
    # try to get an access-token
    api.sessions.get_access_token(verbose=False)
    
    #request the studies
    all_studies = api.studies.list(verbose=False, complete_output=False)
     
    # display name and id
    for one_study in all_studies:
        print(one_study['name'], '\t', one_study['study_id'])
            
if __name__ == '__main__':
    list_studies()