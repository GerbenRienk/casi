'''
The purpose of this module is to try to send a request to the castor-api
to obtain an access-token. 
This access_token is a requirement for all further interaction with the api.

Created on 3 nov. 2020
@author: TrialDataSolutions

'''
from utils.dictfile import DictFile
from utils.castor_api import CastorApi

def get_an_access_token():
    # read configuration file for client id and client secret and other parameters
    config=DictFile('casi.config').read()
    
    # make an instance of the api, using the settings of the configuration file
    api = CastorApi(config)
    
    # try to get an access-token
    api.sessions.get_access_token(verbose=False)
    
    #show the result
    print('the access-token is: %s' % api.access_token)
    
if __name__ == '__main__':
    get_an_access_token()