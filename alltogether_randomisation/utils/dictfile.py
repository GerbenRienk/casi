'''
To read a dictionary from file
Comments are preceded with a #
Empty lines are ignored
Error handling for lines with more than 2 splits should be implemented
All files should be placed in folder "config"
@author: GerbenRienk
'''

if __name__ == '__main__':
    pass

def readDictFile(dictFileName, rel_path=''):
        """
        Rel_path is the relative path to folder config;
        by default it is assumed that folder config is a child of the current folder,
        but this can be specified if otherwise. 
        """
        myDict = {}
        # read the file from disk
        with open(rel_path + 'config/' + dictFileName) as f:
            for line in f:
                # comment lines start with a #
                if line[0] != "#":
                    # only look at lines we can process
                    if len(line.split()) == 2:
                        (key, val) = line.split()
                        myDict[key] = val
                    
        return myDict 
