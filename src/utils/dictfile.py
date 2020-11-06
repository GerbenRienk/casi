'''
To read a dictionary from file
Comments are preceded with a #
Empty lines are ignored
Error handling for lines with more than 2 splits should be implemented
All files should be placed in folder "config"
@author: Gerben Rienk
'''

if __name__ == '__main__':
    pass

class DictFile(object):
    '''
    Reads the contents of a file and returns a dictionary.
    Parameters are the file-name, required, and the relative path,
    which is not required and defaults to ../config/
    '''
    def __init__(self, file_name, rel_path='../config/'):
        self.file_name = file_name
        self.rel_path = rel_path
    
    def read(self):
        '''
        Reads all lines from the file and stores the info in a dictionary.
        Key and Value should be separated by a space.
        Lines starting with a # are considered comments.
        '''
        # start with an empty dictionary
        _my_dict = {}
        # read the file from disk
        try:
            with open(self.rel_path + self.file_name) as f:
                for line in f:
                    # comment lines start with a #
                    if line[0] != "#":
                        # only look at lines we can process
                        if len(line.split()) == 2:
                            (key, val) = line.split()
                            _my_dict[key] = val
        
        except Exception as _error:
            print('something went wrong when trying to open %s' % self.rel_path + self.file_name)
            print(_error)
                    
        return _my_dict 

