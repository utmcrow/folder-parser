__author__ = 'crow'

from os import listdir
from os.path import isfile, join
import os.path, time
import collections
from datetime import datetime ,timedelta
from shutil import move

def main():

    past = int(time.time())

    mypath = '/Users/utmcrow/Pictures/test/'
    movepath = '/Users/utmcrow/Pictures/moved/'
    move_max_time = 60*60*24*30
    folder_max_size = 1024*1024*1

    total_size = 0
    time_array = {}
    size_array = {}

    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    for file in onlyfiles:
        print "file: %s" % file
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(mypath+file)

        total_size += size
        size_array[file] = size
        if not mtime in time_array:
            time_array[mtime] = []
        time_array[mtime].append(file)

        print "last modified: %s" % time.ctime(os.path.getmtime(mypath+file))
        print "created: %s" % time.ctime(os.path.getctime(mypath+file))
        diff = past-os.path.getmtime(mypath+file)
        print "diff: %s" % timedelta(seconds=diff)

        #if diff > move_max_time:
        #    print 'nedd to move'
        #    move(mypath+file,movepath+file)

    od = collections.OrderedDict(sorted(time_array.items()))


    for timetick,data in od.iteritems():
        if total_size > folder_max_size:
            for file in data:
                move(mypath+file,movepath+file)
                total_size -= size_array[file]



if __name__ == "__main__":
    main()

