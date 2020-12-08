'''
The purpose of this module is to try to send a request to the castor-api
to obtain a list of studies.

Created on 6-11-2020
@author: Gerben Rienk
Copyright 2020 TrialDataSolutions
'''

from utils.dictfile import DictFile
from utils.castor_api import CastorApi

def list_study():
    # manually supply the study-id
    study_id = '2A72D9CC-06B5-0078-B089-A5456C7A7024'
    # read configuration file for client id and client secret and other parameters
    config=DictFile('casi.config').read()
    # make an instance of the api
    api = CastorApi(config)
    # try to get an access-token
    api.sessions.get_access_token(verbose=False)
    
    #request the studies
    my_study = api.study.list(study_id, verbose=True)
    print(my_study) 
    # display name if we have that
    if 'name' in my_study:
        print(my_study['name'])
    else:
        print('could not find a name for %s' % study_id)
            
if __name__ == '__main__':
    list_study()