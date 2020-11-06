'''
To connect to postgresql database as defined in oli.config
Read subjects and write subjects
Created on 14 apr. 2017

@author: GerbenRienk
'''
import psycopg2
from utils.dictfile import readDictFile

class ConnToOliDB(object):
    '''Class for connecting to the postgresql database as defined in oli.config
    Methods implemented now are read subjects and add subjects '''
    def __init__(self):
        'let us create the connection to use multiple times'
        config=readDictFile('oli.config')
        conn_string = "host='%s' dbname='%s' user='%s' password='%s' port='%s'" % (config['dbHost'], config['dbName'], config['dbUser'], config['dbPass'], config['dbPort'])
        self.init_result = ''
        
        # get a connection, if a connect cannot be made an exception will be raised here
        try:
            self._conn = psycopg2.connect(conn_string)
            connect_result = 'INFO: class connected to %s, %s as %s on port %s' % (config['dbHost'], config['dbName'], config['dbUser'], config['dbPort'])
        except:
            connect_result ='ERROR: unable to class connect to %s, %s as %s on port %s' % (config['dbHost'], config['dbName'], config['dbUser'], config['dbPort'])
        
        self.init_result = connect_result

    def ReadSubjectsFromDB(self):
        'method to read table subjects into a list'
        cursor = self._conn.cursor()  
        try:
            cursor.execute("""SELECT * from subjects""")
        except:
            print ("not able to execute the select")
        results = cursor.fetchall()
        return results

    def AddSubjectToDB(self, sid, response_id):
        """ 
        Method to add a sid-reponse_id to table ls_responses
        """
        cursor = self._conn.cursor()  
        sql_statement = """INSERT INTO ls_responses(sid, response_id) VALUES (%i, %i)""" % (sid, response_id)
        try:
            cursor.execute(sql_statement)
        except:
            print ("not able to execute: ", sql_statement)
        
        self._conn.commit()
        return None
    
    def WriteLSDataToDB(self, ssoid, ls_data, ws_import_response):
        """ Method to write already imported data the table subjects
        For subject with this StudySubjectOID, including the response of the web-service
        """
        cursor = self._conn.cursor()  
        sql_statement = "UPDATE subjects set ls_data='%s', ws_import_response='%s' where study_subject_oid='%s'" % (ls_data, ws_import_response, ssoid)
        try:
            cursor.execute(sql_statement)
        except:
            print ("not able to execute: ", sql_statement)
        self._conn.commit()
        return None

    def DLookup(self, field_name, table_name, where_clause):
        '''Method to read one field of a table with certain criteria
        If no result, then a list containing an empty string is returned
        '''
        cursor = self._conn.cursor()  
        sql_statement = "SELECT " + field_name + " from " + table_name + " where " + where_clause
        try:
            cursor.execute(sql_statement)
        except:
            print ("not able to execute the select: %s" % sql_statement)
        results = cursor.fetchone()
        if not results:
            results = ['']
        return results[0]
        
    def TryToAddSubjectToDB(self, sid, response_id):
        """
        see if this combination is already in the database
        and if not, add it
        """
        #print("in TryToAddSubjectToDB: ", str(sid), str(response_id))
        # check if we must add this response to the table
        if (self.DLookup('response_id', 'ls_responses', 'sid=%i and response_id=%i' % (sid, response_id)) == ''):
            self.AddSubjectToDB(sid, response_id)
        return None
        
    def ResponseIsComplete(self, sid, response_id):
        """
        returns boolean if this combination is already completed
        and if not, add it
        """
        #print("in ResponseIsComplete: ", str(sid), str(response_id))
        # check if we must add this response to the table
        if (self.DLookup('date_completed', 'ls_responses', 'sid=%i and response_id=%i' % (sid, response_id)) == ''):
            return_value = False
        else:
            return_value = True
        return return_value
        
    def SetResponseComplete(self, sid, response_id):
        """ 
        Method to add a sid-reponse_id to table ls_responses
        """
        cursor = self._conn.cursor()  
        sql_statement = """Update ls_responses set date_completed=Now() where sid=%i and response_id=%i""" % (sid, response_id)
        try:
            cursor.execute(sql_statement)
        except:
            print ("not able to execute: ", sql_statement)
        
        self._conn.commit()
        return None
        
    def WriteStudySubjectID(self, sid, response_id, study_subject_id):
        """ 
        Method to write study_subject_id to table ls_responses
        """
        cursor = self._conn.cursor()  
        
        sql_statement = """Update ls_responses set study_subject_id='%s' where sid=%i and response_id=%i""" % (study_subject_id, sid, response_id)
        try:
            cursor.execute(sql_statement)
        except:
            print ("not able to execute: ", sql_statement)
        
        self._conn.commit()
        return None

    def WriteStudySubjectOID(self, sid, response_id, study_subject_oid):
        """ 
        Method to write study_subject_oid to table ls_responses
        """
        cursor = self._conn.cursor()  
        
        # only try to set the study_subject_oid is we have been given one
        if (study_subject_oid is not None):
            sql_statement = """Update ls_responses set study_subject_oid='%s' where sid=%i and response_id=%i""" % (study_subject_oid, sid, response_id)
            try:
                cursor.execute(sql_statement)
            except:
                print ("WriteStudySubjectOID: not able to execute: ", sql_statement)
            
            self._conn.commit()
        return None

    def WriteDataWSRequest(self, sid, response_id, data_ws_request):
        """ 
        Method to write study_subject_oid to table ls_responses
        """
        cursor = self._conn.cursor()  
        # escape the single quotes
        data_ws_request = data_ws_request.replace("'", "''")
        #print("in WriteDataWSRequest: ", str(sid), str(response_id), data_ws_request)
        sql_statement = """Update ls_responses set data_ws_request='%s' where sid=%i and response_id=%i""" % (data_ws_request, sid, response_id)
        try:
            cursor.execute(sql_statement)
            #print('after sql execute: %s' % sql_statement)
        except:
            print ("WriteDataWSRequest: not able to execute: ", sql_statement)
        
        self._conn.commit()
        return None

    def WriteDataWSResponse(self, sid, response_id, data_ws_response):
        """ 
        Method to write study_subject_oid to table ls_responses
        """
        cursor = self._conn.cursor()  
        #print("in WriteDataWSResponse: ", str(sid), str(response_id), data_ws_response)
        data_ws_response = data_ws_response.replace("'", "''")
        sql_statement = """Update ls_responses set data_ws_response='%s' where sid=%i and response_id=%i""" % (data_ws_response, sid, response_id)
        try:
            cursor.execute(sql_statement)
        except:
            print ("WriteDataWSResponse: not able to execute: ", sql_statement)
        
        self._conn.commit()
        return None

class PGSubject(object):
    '''to get the study subject oid from the study subject id
    by calling the rest-webservice
    Only parameter is study subject id
    Connection info is read from oli.config
    '''
    def __init__(self, PGStudySubjectID):
        self._studysubjectid = PGStudySubjectID
        return
    
    def GetSSOID(self):
        'method to get the StudySubjectOID using rest'
        import requests
        import xml.etree.ElementTree as ET
        config=readDictFile('oli.config')
        
        login_url = config['baseUrlRest'] + '/j_spring_security_check'
        login_action = {'action':'submit'}
        login_payload = {
            'j_username': config['userName'],
            'j_password': config['password'],
            'submit':"Login"
                        }
        mySession = requests.Session()
        mySession.post(login_url,params=login_action,data=login_payload)
        cd_url = config['baseUrlRest'] + '/rest/clinicaldata/xml/view/' + config['studyOid'] + '/'
        cd_url = cd_url + self._studysubjectid + '/*/*'
        rest_response = mySession.get(cd_url)
        # only analyze the response, if the status code was 200 
        if(rest_response.status_code == 200):
            document = rest_response.content
            root = ET.fromstring(document)
                        
            for clinical_data in root.findall('{http://www.cdisc.org/ns/odm/v1.3}ClinicalData/'):
                subject_info = clinical_data.attrib
                if subject_info['{http://www.openclinica.org/ns/odm_ext_v130/v3.1}StudySubjectID'] == self._studysubjectid:
                    return subject_info['SubjectKey']



if __name__ == "__main__":
    pass    