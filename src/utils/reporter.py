'''
Created on 9 mei 2017

@author: GerbenRienk
'''

class Reporter(object):
    '''
    Reporter object that creates per day a file
    to which lines can be added reporting the activities of oli,
    so it can be sent at the end of the day
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._file = open('logs/report.txt','w') 
        self._file.write('\n')
        
    def append_to_report(self, report_line):
        self._file.write(report_line + '\n')
        return None
    
    def close_file(self):
        self._file.close()
        return None