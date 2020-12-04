'''
Created on 9 mei 2017

@author: GerbenRienk
'''
import os

class Reporter(object):
    '''
    Reporter object that creates a file
    to which lines can be added reporting the activities of oodkoc4,
    so it can be sent at the end of the day
    '''

    def __init__(self, report_name='logs/report.txt'):
        '''
        Constructor
        '''
        self.report_name=report_name
        if os.path.exists(report_name):
            mode = 'a'
        else:
            mode = 'w'
        self._file = open(report_name, mode) 
        self._file.close()
        
    def append_to_report(self, report_line):
        self._file.write(report_line + '\n')
        return None
    
    def close_file(self):
        self._file.close()
        return None