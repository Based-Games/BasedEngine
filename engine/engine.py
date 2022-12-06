# Main game engine.
# We setup the engine, start a game thread, and stay running with a local API for getting states

import pygame

# Start importing game libs
from engine.jsondata import JSONData
from engine.screen import Screen
from engine.validated import ValidatedDict

class GameEngine():
    def __init__(self, engine_config: ValidatedDict, game_config: ValidatedDict):
        self.run = True
        self.framerate = 60
        self.clock = pygame.time.Clock()

        # Let's start up the game.
        # Init pygame
        pygame.init()

        # Init pygame screen, return
        self.screen, self.resolution = Screen(engine_config.get_dict('system')).initScreen()

        # Current scene/screen state. Here's a list of them.
        # - INIT
        # - STARTUP
        # - TEST_MODE
        # - ATTRACT
        # We will init this with None so that the engine can decide what to do.

        self.current_state = 'INIT'
        self.current_events = None

        # Now, we begin the loop
        self.engineLoop()

    def eventHandler(self):
        '''
        Handles game events.
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                print('thank you for playing!')
                pygame.display.quit()
                exit()

    def engineLoop(self):
        '''
        The main loop of the engine. Everything is started by this loop.
        '''
        while self.run:
            # First, we should start our loop with the event manager
            self.eventHandler()

            # Now, let's make sure that the game is locked to a framerate.
            self.clock.tick(self.framerate)

if __name__ == "__main__":
    path_prefix = './engine/json'
    config = JSONData.loadJsonFile(f'{path_prefix}/config.json')
    game = JSONData.loadJsonFile(f'{path_prefix}/game.json')

    GameEngine(config, game)

    # Game is over
    print('thank you for playing!')
    pygame.display.quit()
    exit()