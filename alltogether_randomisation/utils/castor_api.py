import requests
import json
from collections import OrderedDict

class CastorApi(object):

    def __init__(self, url):
        self.url = url
        # self.headers = {"content-type": "application/json"}
        # next line sets the default headers which for limesurvey were as above, but 
        # in the MsAccess tool we used:
        self.headers = {"content-type": "application/x-www-form-urlencoded"}
        
        self.utils = _Utils(self)
        self.sessions = _Sessions(self)
        self.users = _Users(self)
        self.surveys = _Surveys(self)
        self.tokens = _Tokens(self)
        self.questions = _Questions(self)
        self.responses = _Responses(self)


class _Utils(object):

    def __init__(self, castor_api):
        self.api = castor_api
    
    def request(self, data=None, request_type=None, url=None, headers=None):
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
        :return: Dictionary containing result of API call, or None.
        """
        if url is None:
            url = self.api.url
        if headers is None:
            headers = self.api.headers
        return_value = None
        try:
            # print("req url='%s'" % url)
            # print("req headers='%s'" % headers)
            # print("req data='%s'" % data)
            if request_type == 'post':
                # print("req type=post")
                response = requests.post(url, headers=headers, data=data)
            if request_type == 'get':
                # print("req type=get")
                response = requests.get(url, headers=headers, data=data)
            
            # print(response)
            if response.status_code == 200:
                return_value = response.json()
            else:
                print('request to %s returned status code %i' % (url, response.status_code))
        except requests.ConnectionError as pe:
            # TODO: some handling here, for now just print pe
            print('when a request to the castor api was made, the following error was raised %s' % (pe))
            return_value = None
        return return_value

    @staticmethod
    def prepare_params(method, params):
        """
        Prepare remote procedure call parameter dictionary.

        Important! Despite being provided as key-value, the API treats all
        parameters as positional. OrderedDict should be used to ensure this,
        otherwise some calls may randomly fail.

        Parameters
        :param method: Name of API method to call.
        :type method: String
        :param params: Parameters to the specified API call.
        :type params: OrderedDict

        Return
        :return: JSON encoded string with method and parameters.
        """
        data = OrderedDict([
            ('method', method),
            ('params', params),
            ('id', 1)
        ])
        data_json = json.dumps(data)
        return data_json

class _Sessions(object):

    def __init__(self, castor_api):
        self.api = castor_api

    def get_access_token(self, client_id, client_secret):
        """
        Get an access token for all subsequent API calls.

        Parameters
        :param client_id: castor specs: see https://helpdesk.castoredc.com/article/124-application-programming-interface-api
        :type client_id: String
        :param client_secret: castor specs, see above
        :type client_secret: String
        
        """
        token_url = self.api.url + "/oauth/token"
        token_data = "grant_type=client_credentials&client_id=%s&client_secret=%s" % (client_id, client_secret)
        response = self.api.utils.request(data=token_data, request_type='post', url=token_url)
        return response

class _Users(object):

    def __init__(self, castor_api):
        self.api = castor_api

    def user(self, access_token, user_id=None):
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
            
        my_authorization = "Bearer %s" % (access_token)
        my_headers = {'Authorization': my_authorization}
        response = self.api.utils.request(request_type='get', headers=my_headers, url=my_url, data=None)
        return response


class _Surveys(object):

    def __init__(self, castor_api):
        self.api = castor_api

    def list_surveys(self, session_key, username):
        """
        List surveys accessible to the specified username.

        Parameters
        :param session_key: Active LSRC2 session key
        :type session_key: String
        :param username: LimeSurvey username to list accessible surveys for.
        :type username: String
        """
        params = OrderedDict([
            ('sSessionKey', session_key),
            ('iSurveyID', username)
        ])
        data = self.api.utils.prepare_params('list_surveys', params)
        response = self.api.utils.request(data)
        return response


class _Tokens(object):

    def __init__(self, castor_api):
        self.api = castor_api

    def add_participants(self, session_key, survey_id, participant_data,
                         create_token_key=True):
        """
        Add participants to the specified survey.

        Parameters
        :param session_key: Active LSRC2 session key
        :type session_key: String
        :param survey_id: ID of survey to delete participants from.
        :type survey_id: Integer
        :param participant_data: List of participant detail dictionaries.
        :type participant_data: List[Dict]
        """
        params = OrderedDict([
            ('sSessionKey', session_key),
            ('iSurveyID', survey_id),
            ('participantData', participant_data),
            ('bCreateToken', create_token_key)
        ])
        data = self.api.utils.prepare_params('add_participants', params)
        partbit = json.dumps(participant_data)
        data = data.replace(partbit, '['+partbit+']')
        response = self.api.utils.request(data)
        return response

    def list_participants(self, session_key, survey_id, start=0, limit=10000):
        """
        List participants of the specified survey.
        * @access public
        * @param string $sSessionKey Auth credentials
        * @param int $iSurveyID Id of the survey to list participants
        * @param int $iStart Start id of the token list
        * @param int $iLimit Number of participants to return
        * @param bool $bUnused If you want unused tokens, set true
        * @param bool|array $aAttributes The extented attributes that we want
        * @param array $aConditions Optional conditions to limit the list, e.g. with array('email' => 'info@example.com')
        * @return array The list of tokens
        Parameters
        :param session_key: Active LSRC2 session key
        :type session_key: String
        :param survey_id: ID of survey to list participants from.
        :type survey_id: Integer
        """
        params = OrderedDict([
            ('sSessionKey', session_key),
            ('iSurveyID', survey_id),
            ('iStart', start),
            ('iLimit', limit),
            ('bUnused', False),
            ('aAttributes', ('attributes_bit'))
        ])
        # transform into json-format
        data = self.api.utils.prepare_params('list_participants', params)
        # but the attributes bit is not well formed, so we manually correct that
        data = data.replace('"attributes_bit"', '["completed"]')
        response = self.api.utils.request(data)
        return response

    def get_participant_properties(self, session_key, survey_id, token_id):    
        """
        get_participant_properties
        /**
        * RPC Routine to return settings of a token/participant of a survey .
        *
        * @access public
        * @param string $sSessionKey Auth credentials
        * @param int $iSurveyID Id of the Survey to get token properties
        * @param int $iTokenID Id of the participant to check
        * @param array $aTokenProperties The properties to get
        * @return array The requested values
        */
        """
        params = OrderedDict([
            ('sSessionKey', session_key),
            ('iSurveyID', survey_id),
            ('iTokenID', token_id),
            ('aaTokenProperties', ('token'))
           ])
        
        return

    def delete_participants(self, session_key, survey_id, tokens):
        """
        Delete participants (by token) from the specified survey.

        Parameters
        :param session_key: Active LSRC2 session key
        :type session_key: String
        :param survey_id: ID of survey to delete participants from.
        :type survey_id: Integer
        :param tokens: List of token IDs for participants to delete.
        :type tokens: List[Integer]
        """
        params = OrderedDict([
            ('sSessionKey', session_key),
            ('iSurveyID', survey_id),
            ('aTokenIDs', tokens)
        ])
        data = self.api.utils.prepare_params('delete_participants', params)
        response = self.api.utils.request(data)
        return response


class _Questions(object):

    def __init__(self, castor_api):
        self.api = castor_api

    def list_questions(self, session_key, survey_id,
                       group_id=None, language=None):
        """
        Return a list of questions from the specified survey.

        Parameters
        :param session_key: Active LSRC2 session key
        :type session_key: String
        :param survey_id: ID of survey to list questions from.
        :type survey_id: Integer
        :param group_id: ID of the question group to filter on.
        :type group_id: Integer
        :param language: Language of survey to return for.
        :type language: String
        """

        params = OrderedDict([
            ('sSessionKey', session_key),
            ('iSurveyID', survey_id),
            ('iGroupID', group_id),
            ('sLanguage', language)
        ])
        data = self.api.utils.prepare_params('list_questions', params)
        response = self.api.utils.request(data)
        return response
 
class _Responses(object):

    def __init__(self, castor_api):
        self.api = castor_api

    def export_responses(self, session_key, survey_id,
                       document_type='json', language='en'):
        """
        Return a list of questions from the specified survey.

        Parameters
        :param session_key: Active LSRC2 session key
        :type session_key: String
        :param survey_id: ID of survey to list questions from.
        :type survey_id: Integer
        :param document_type: pdf,csv,xls,doc,json.
        :type document_type: String
        :param language: Language of survey to return for.
        :type language: String
        """

        params = OrderedDict([
            ('sSessionKey', session_key),
            ('iSurveyID', survey_id),
            ('sDocumentType', document_type),
            ('sLanguage', language)
        ])
        data = self.api.utils.prepare_params('export_responses', params)
        response = self.api.utils.request(data)
        return response   
"""
from the online documentation:
export_responses
/**
* RPC Routine to export responses.
* Returns the requested file as base64 encoded string
*
* @access public
* @param string $sSessionKey Auth credentials
* @param int $iSurveyID Id of the Survey
* @param string $sDocumentType pdf,csv,xls,doc,json
* @param string $sLanguageCode The language to be used
* @param string $sCompletionStatus Optional 'complete','incomplete' or 'all' - defaults to 'all'
* @param string $sHeadingType 'code','full' or 'abbreviated' Optional defaults to 'code'
* @param string $sResponseType 'short' or 'long' Optional defaults to 'short'
* @param integer $iFromResponseID Optional
* @param integer $iToResponseID Optional
* @param array $aFields Optional Selected fields
* @return array|string On success: Requested file as base 64-encoded string. On failure array with error information
* */
"""