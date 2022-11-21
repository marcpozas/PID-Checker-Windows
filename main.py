from os import mkdir
import subprocess
import datetime

class main:
    def __init__(self):
        self.output = self.getConnections()
        self.date = self.getDate()
        self.connections = self.cleanOutput(self.output)
        self.PIDS = self.getPIDS(self.connections)
        self.APP_PID_DICT = self.identifyAPPS(self.PIDS)
        self.checkPIDS(self.APP_PID_DICT)
        self.createLOG(self.connections, self.APP_PID_DICT, self.date)

    def getConnections(self):
        '''
        This function gets all active processes in your PC.
        :return: String of all information about TCP and UDP protocols.
        '''
        print("Getting all the connections in your PC...")
        output = subprocess.check_output("netstat -ano", shell=True)
        output = str(output)
        output = output.split("PID\\r\\n")[1]
        output = output.split("\\r\\n")

        return output

    def getDate(self):
        """
        This function gets the actual time (Y:M:D H:MIN:S).
        :return: The date.
        """
        return str(datetime.datetime.now()).split('.')[0]

    def cleanOutput(self, output: list()):
        '''
        This function cleans the TCP and UDP string.
        :arg output: The output string.
        :return: String cleaned.
        '''
        connections = list()
        for i in output:
            i = i.split()
            i = [j + ' ' for j in i]
            i.append('\n')
            connections.append(i)

        return connections

    def getPIDS(self, connections: list()):
        '''
        This function gets all the PIDS from the output and returns them.
        :arg connections: String of cleaned output.
        :return: Set with all PIDS.
        '''
        PIDS = list()
        for connection in connections:
            for element in connection:
                if element[0:-1].isnumeric():
                    PIDS.append(element[0:-1])
        return set(PIDS)
    
    def identifyAPPS(self, PIDS: set()):
        '''
        This functions finds which application is using each PID and writes the results in a dictionary.
        :arg PIDS: Set with all PIDs.
        :return: Dictionary with format ({NameApp} : {PID}).
        '''
        print("Identifying APPS...")
        APP_PID_DICT = dict()
        for PID in PIDS:
            output = str(subprocess.check_output('tasklist /fi "pid eq {}"'.format(PID), shell=True))
            output = output.split('\\r\\n')[-2].split()
            APP_PID_DICT[PID] = output[0]
        return APP_PID_DICT

    def checkPIDS(self, APP_PID_DICT: dict()):
        '''
        This function checks which one of the PIDS is not in the whitelist.txt list and shows it to the user. If user says that it's a confident APP the funciton save it in the whitelist.txt for next times. If not, it writes it on checklist.txt.
        :arg APP_PID_DICT: Dictionary with all the APPs names and its respectives PIDs.
        '''
        try:
            open(file='checklist.txt', mode='r+', encoding='UTF8').close()
        except:
            open(file='checklist.txt', mode='w', encoding='UTF8').close()

        try:
            open(file='whitelist.txt', mode='r+', encoding='UTF8').close()
        except:
            open(file='whitelist.txt', mode='w', encoding='UTF8').close()


        approve, reject = list(), list()
        g = open(file='checklist.txt', mode='r+', encoding='UTF8')
        with open(file='whitelist.txt', mode='r+', encoding='UTF8') as f:
            friendlyAPPS = f.read()
            for pair in APP_PID_DICT:
                if not APP_PID_DICT[pair] in friendlyAPPS:
                    if input(f"\nWe found a new app with next features:\nPID: {pair} | NAME: {APP_PID_DICT[pair]}\nDo you want to add this APP to the whitelist? (y/n)\n") in ["y","Y",""]:
                        approve.append(APP_PID_DICT[pair])
                    else:
                        reject.append(APP_PID_DICT[pair])

            for i in set(approve):
                f.write(i + " ")
            for i in set(reject):
                g.write(i + " ")
        f.close()
        g.close()
    
    def createLOG(self, connections: list(), SELF_APP_DICT: dict(), date: str()):
        '''
        This function creates a LOG.txt file for this results run and saves it in a folder with name {Y:M:D} and in a file {H:MIN:S}.
        :arg connections: String of cleaned output.
        :arg APP_PID_DICT: Dictionary with all the APPs names and its respectives PIDs.
        :date: The program execution date.
        '''
        try:
            mkdir('log')
        except:
            pass
        try:
            mkdir(f'log\\{date.split()[0]}')
        except:
            pass
        with open(file=f'log\\{date.split()[0]}\\{date.split()[1].replace(":", "-")}.txt', mode='w', encoding='UTF8') as f:
            print(f'Creating log file in path: "log\\{date.split()[0]}\\{date.split()[1].replace(":", "-")}.txt"')
            for connection in connections:
                connection.pop(-1)
                for element in connection:
                    if element[0:-1].isnumeric():
                        connection.append(SELF_APP_DICT[element[0:-1]])
                        connection.append('\n')
                        f.writelines(connection)
        f.close()

CONN = main()