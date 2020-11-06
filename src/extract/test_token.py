'''
Created on 3 nov. 2020
@author: Gerben Rienk
The purpose of this module is to try to send a request to the castor-api
to obtain an access-token. 
This access_token is a requirement for all further interaction.
'''
from utils.dictfile import readDictFile
from utils.castor_api import CastorApi

def get_an_access_token():
    # read configuration file for client id and client secret and other parameters
    config=readDictFile('casi.config')
    
    # start with requesting an access token, which we can use for about an hour
    api = CastorApi(config)
    #access_token_request = api.sessions.get_access_token(verbose=True)
    api.sessions.get_access_token(verbose=True)
    #print(access_token_request)
    print('the access-token is %s' % api.access_token)
    
if __name__ == '__main__':
    get_an_access_token()