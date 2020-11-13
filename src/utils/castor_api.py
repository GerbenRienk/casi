import requests
import json

class CastorApi(object):

    def __init__(self, config):
        '''
        Takes a config-dictionary as parameter. To create an object of this class 
        the dictionary should at least have Values for Keys api_url, client_id and client_secret
        '''
        # default to zero length strings
        self.url = 'https://api_url.in.config'
        self.client_id = ''
        self.client_secret = ''
        
        try:
            self.url = config['api_url']
            self.client_id = config['client_id']
            self.client_secret = config['client_secret']
        except Exception as _error:
            print(_error)
            
        self.headers = {"content-type": "application/x-www-form-urlencoded"}
        self.access_token = 'x'
        
        self.utils = _Utils(self)
        self.sessions = _Sessions(self)
        self.studies = _Studies(self)
        self.users = _Users(self)

class _Utils(object):

    def __init__(self, castor_api):
        self.api = castor_api
    
    def request(self, data=None, request_type=None, url=None, headers=None, verbose=False):
        """
        Return the result of an API call, or None.

        Exceptions are logged rather than raised.

        Parameters
        :param data: Method name and parameters to send to the API.
        :type data: String
        :param url: Location of the LimeSurvey API endpoint.
        :type url: String
        :param headers: HTTP headers to add to the request.
        :type headers: Dict
        :param request_type: either post or get
        Return
        :return: response of API call, or None.
        """
        if url is None:
            url = self.api.url
        if headers is None:
            headers = self.api.headers
        # by default return nothing
        return_value = None
        if verbose == True:
            print("pre url=     %s   " % url)
            print("pre headers= %s   " % headers)
            print("pre data=    %s   " % data)
            print("pre type=    %s \n" % request_type)

        try:
            if request_type == 'post':
                response = requests.post(url, headers=headers, data=data)
            if request_type == 'get':
                response = requests.get(url, headers=headers, data=data)

            if verbose == True:
                print("req url         = %s   " % response.request.url)
                print("req headers     = %s   " % response.request.headers)
                print("req body        = %s   " % response.request.body)
                print("resp status code= %s   " % response.status_code)
                print("resp text       = %s \n" % response.text)

            return_value = response
            
        except requests.ConnectionError as pe:
            # TODO: some handling here, for now just print pe
            print('when a request to the castor api was made, the following error was raised %s' % (pe))
            return_value = None
            
        return return_value

class _Sessions(object):

    def __init__(self, castor_api):
        self.api = castor_api

    def get_access_token(self, verbose=False):
        """
        Get an access token for all subsequent API calls.
        """
        token_url = self.api.url + "/oauth/token"
        token_data = "grant_type=client_credentials&client_id=%s&client_secret=%s" % (self.api.client_id, self.api.client_secret)
        response = self.api.utils.request(data=token_data, request_type='post', url=token_url, verbose=verbose)
        
        # did we get anything from our request
        if response is not None:
            # set the access_token only if the response status was 200
            if response.status_code == 200:
                resp_json =json.loads(response.text)
                self.api.access_token = resp_json['access_token']
        
        return response

class _Studies(object):
    '''
    endpoint called study, but containing information about all studies in castor
    '''
    def __init__(self, castor_api):
        self.api = castor_api

    def list(self, verbose=False, complete_output=False):
        """
        Get all studies in json for the current user 
        Set verbose=True to get the complete request plus response
        Set complete_output=True to get the complete response; if set to False
        you will skip the nodes ['_embedded']['study']
        """
        my_url = self.api.url + "/api/study"    
        my_authorization = "Bearer %s" % (self.api.access_token)
        my_headers = {'Authorization': my_authorization}
        response = self.api.utils.request(request_type='get', headers=my_headers, url=my_url, data=None, verbose=verbose)
        if response is not None:
            if response.status_code == 200:
                if complete_output:
                    resp_json = json.loads(response.text)
                else:
                    resp_json = json.loads(response.text)['_embedded']['study']
        
        return resp_json

class _Users(object):

    def __init__(self, castor_api):
        self.api = castor_api

    def list(self, user_id=None, verbose=False):
        """
        Retrieve a list of users the currently authenticated user is authorized to see. 
        Default to own User.
        if a user_id is given, then only data about this user are returned
        
        :type user_id: String
        """
        my_url = self.api.url + "/api/user"
        # if a specific user id is given as parameter:
        if user_id is not None:
            my_url = my_url + "/" + user_id
            
        my_authorization = "Bearer %s" % (self.api.access_token)
        my_headers = {'Authorization': my_authorization}
        response = self.api.utils.request(request_type='get', headers=my_headers, url=my_url, data=None, verbose=verbose)
        return response





