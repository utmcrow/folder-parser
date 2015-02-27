__author__ = 'crow'


import os.path
import time
import collections
import logging.config
import yaml

from datetime import timedelta
from os import listdir
from os.path import isfile, join
from shutil import move


def main():

    try:
        config = yaml.load(open('local.yml', 'r'))
    except:
        config = yaml.load(open('config.yml', 'r'))

    logging.config.dictConfig(yaml.load(open('logging.yml', 'r')))

    log_process = logging.getLogger('process')
    logging.getLogger('error')
    log_move = logging.getLogger('move')

    past = int(time.time())

    total_size = 0
    time_array = {}
    size_array = {}

    log_process.info('Start processing')

    onlyfiles = [f for f in listdir(
        config['source-path']) if isfile(join(config['source-path'], f))]
    log_process.info('processing {} files'.format(len(onlyfiles)))
    for file in onlyfiles:
        (mode,
         ino,
         dev,
         nlink,
         uid,
         gid,
         size,
         atime,
         mtime,
         ctime) = os.stat(config['source-path'] + file)

        diff = past - os.path.getmtime(config['source-path'] + file)

        if diff > config['rotating-timer']:
            log_process.info(
                '{} : rotate by timer: {}'.format(
                    file, timedelta(
                        seconds=diff)))
            if config['enable-moving']:
                move(
                    config['source-path'] +
                    file,
                    config['destination-path'] +
                    file)
                log_process.info(
                    '{} : last modified {} : size {}'.format(
                        file,
                        time.ctime(mtime),
                        size))
                log_move.info(
                    '{} : move to: {}'.format(
                        file,
                        config['destination-path']))
            continue

        total_size += size
        size_array[file] = size
        if not mtime in time_array:
            time_array[mtime] = []
        time_array[mtime].append(file)

    od = collections.OrderedDict(sorted(time_array.items()))
    log_process.info('total size after time processing : {} GB'.format(
        round(float(total_size) / (1024 * 1024 * 1024), 3)))

    for timetick, data in od.iteritems():
        if total_size > config['source-max-size']:
            for file in data:
                if config['enable-moving']:
                    move(
                        config['source-path'] +
                        file,
                        config['destination-path'] +
                        file)
                    log_move.info(
                        '{} : move to: {}'.format(
                            file, timedelta(
                                seconds=diff)))
                total_size -= size_array[file]
                log_process.info(
                    '{} : rotate by size: {} bytes left'.format(
                        file,
                        total_size -
                        config['source-max-size']))
        else:
            break

if __name__ == "__main__":
    main()
