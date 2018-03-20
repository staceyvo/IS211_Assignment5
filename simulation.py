import argparse
import csv
import datetime
import urllib2


class Server:
    def __init__(self, ppm):
        self.page_rate = ppm
        self.current_task = None
        self.time_remaining = 0

    def tick(self):
        if self.current_task != None:
            self.time_remaining = self.time_remaining - 1
            if self.time_remaining <= 0:
                self.current_task = None


    def busy(self):
        if self.current_task != None:
            return True
        else:
        return False


    def start_next(self, new_task):
            self.current_task = new_task
            self.time_remaining = new_task.get_pages() * 60 /
            self.page_rate


class Request:
    def __init__(self, arrival, filepath, duration):
        self.filepath = filepath
        self.duration = duration
        self.arrival = arrival

    #TODO work it on out, ya dig
    def measure_wait_time(self, current_time):
        self.wait_time = current_time - self.timestamp


def simulateOneServer(filename):
    requests = []
    with open(filename, 'r') as handle:
        reader = csv.DictReader(handle, fieldnames=['arrival', 'filepath', 'duration'])
        for row in reader:
            requests.append(Request(row['arrival'], row['filepath'], row['duration']))

    requests.sort(key=lambda x: x['arrival'])
    requests[0]['completion'] = requests[0]['duration'] - requests[0]['arrival']



    process_time = requests[0]['duration']
    for index in range(1, len(requests)):
        index_item = requests[index]
        prior_item = requests[index - 1]

        index_item['completion'] = prior_item['completion'] + index_item['duration']
        process_time += index_item['duration'] - index_item['arrival']

    return process_time / float(len(requests))
        



def simulateManyServers():
    raise Exception('Not yet implemented')


if __name__ == '__main__':
    #'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'
    #setting up argparse
    parser = argparse.ArgumentParser(description='request simulator')
    parser.add_argument('--filename', help='File Name', required=True)
    args = vars(parser.parse_args('filename'))

    filename = args['filename']

    simulateOneServer(filename)

    #we will add an additional function to test against
    simulateManyServers()
