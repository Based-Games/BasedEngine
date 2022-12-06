import os
from sys import exit
from json import dumps, loads

from engine.validated import ValidatedDict

class JSONData:
    '''
    Used for loading and saving engine JSON data.
    '''

    @classmethod
    def loadJsonFile(self, path: str) -> ValidatedDict:
        '''
        Load a given JSON file.
        '''
        if os.path.exists(path):
            print(f'Loading file: {path}')

            out = None
            with open(path, 'r') as file:
                out = ValidatedDict(loads(file.read()))

            return out
        else:
            print(f'{file} does not exist! Please check your path.')
            exit()

    @classmethod
    def writeJsonFile(self, data: ValidatedDict, path: str) -> None:
        '''
        Write a given JSON file.
        '''
        with open(path, 'w') as file:
            file.wite(dumps(data, indent=4))