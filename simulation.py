import argparse
import csv

class Request:
    """A class that represents a generic Request."""

    def __init__(self, arrival, filepath, duration):
        """Constructor for the Request class.

              Args:
                  arrival (int): second the request arrives
                  filepath (str): the file path of the request
                  duration (int): time it takes to process

              Attributes:
                  arrival (int): second the request arrives
                  filepath (str): the file path of the request
                  duration (int): time it takes to process
              """
        self.filepath = filepath
        self.duration = duration
        self.arrival = arrival


def read_file(filename):
    """This function, read_file will read our file and process it into a dictionary.

                            Args:
                                filename is the file we are reading

                            Returns:
                                Returns our data in a dictionary

                    """
    requests = []
    with open(filename, 'r') as handle:
        reader = csv.DictReader(handle, fieldnames=['arrival', 'filepath', 'duration'])
        for row in reader:
            requests.append(Request(int(row['arrival']), row['filepath'], int(row['duration'])))

    requests.sort(key=lambda x: x.arrival)
    return requests

def simulateOneServer(requests):
    """This function, simulateOneServer will calculate the average latency for requests.

                            Args:
                                requests holds all requests to the server

                            Returns:
                                Returns the process_time

                    """
    requests[0].completion = requests[0].duration + requests[0].arrival

    process_time = requests[0].duration
    for index in range(1, len(requests)):
        index_item = requests[index]
        prior_item = requests[index - 1]

        if prior_item.completion >= index_item.arrival:
            index_item.completion = prior_item.completion + index_item.duration
        else:
            index_item.completion = index_item.arrival + index_item.duration
        process_time += index_item.completion - index_item.arrival

    return process_time / float(len(requests))



#distribute requests to each server, then calculate avg latency for each
def simulateManyServers(requests, servers):
    """This function, simulateManyServers will process many requests at once,
            distributing requests in a round robin fashion

                            Args:
                                requests holds all requests to the server
                                servers is the number of servers given

                            Returns:
                                average latency for each server


                    """
    #divide requests into the same number as servers
    result = []
    for index in range(servers):
        result.append(requests[index::servers])

    #call simulateOneserver on each list
    return [simulateOneServer(element) for element in result]


if __name__ == '__main__':
    #'http://s3.amazonaws.com/cuny-is211-spring2015/requests.csv'
    #setting up argparse
    parser = argparse.ArgumentParser(description='request simulator')
    parser.add_argument('--filename', help='File Name', required=True)
    parser.add_argument('--servers',type=int, help='Number of Servers', required=False)
    args = vars(parser.parse_args())

    requests = read_file(args['filename'])

    if 'servers' in args:
        print(simulateManyServers(requests, args['servers']))
    else:
        print(simulateOneServer(requests))
