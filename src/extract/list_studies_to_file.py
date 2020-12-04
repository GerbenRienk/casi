'''
scriptlet to list all studies we have access to and export them into a csv-file

@author: TrialDataSolutions
Created on 16 Nov 2020
'''
from utils.dictfile import DictFile
from utils.castor_api import CastorApi
import csv 

def write_all_studies_to_file():
    # read configuration file for client id and client secret and other parameters
    config=DictFile('casi.config').read()
    # make an instance of the api
    api = CastorApi(config)
    # try to get an access-token
    api.sessions.get_access_token(verbose=False)
    
    #request data about the studies
    all_studies = api.studies.list(verbose=False, complete_output=False)
    
    # define the columns for our output: these must match the names in the dict
    columns = ['name', 'study_id', 'version','crf_id', 'surveys_enabled', '_links', 'randomization_enabled', 'domain', 'created_on', 'expected_centers', 'created_by', 'expected_records', 'main_contact', 'gcp_enabled', 'premium_support_enabled', 'slug', 'live', 'duration'] 
    filename_with_path = "../output/studies.csv"
    with open(filename_with_path, 'w', newline='') as f: 
        wr = csv.DictWriter(f, fieldnames = columns) 
        wr.writeheader() 
        wr.writerows(all_studies) 
    
if __name__ == '__main__':
    write_all_studies_to_file()
