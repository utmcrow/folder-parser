__author__ = 'crow'

from os import listdir
from os.path import isfile, join
import os.path, time

def main():

    mypath = '/Users/utmcrow/Dropbox/test/'
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    for file in onlyfiles:
        print "last modified: %s" % time.ctime(os.path.getmtime(mypath+file))
        print "created: %s" % time.ctime(os.path.getctime(mypath+file))
    pass

if __name__ == "__main__":
    main()

