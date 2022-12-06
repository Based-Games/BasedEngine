# Main game engine.
# We setup the engine, start a game thread, and stay running with a local API for getting states

import pygame

# Start importing game libs
from engine.jsondata import JSONData
from engine.screen import Screen
from engine.validated import ValidatedDict
from engine.asset import AssetManager

class GameEngine():
    def __init__(self, engine_config: ValidatedDict, game_config: ValidatedDict):
        self.run = True
        self.framerate = 60
        self.clock = pygame.time.Clock()

        self.engine_conf = engine_config.get_dict('system')

        # Let's start up the game.
        # Init pygame
        pygame.init()

        # Init pygame screen, return
        self.screen, self.resolution = Screen(engine_config.get_dict('system')).initScreen()
        pygame.display.update()

        # Current scene/screen state. Here's a list of them.
        # - INIT
        # - WAITING
        # - LOGO_IN
        # - LOADING
        # - ERROR
        # - LOGO_OUT
        # - UPDATING
        # - TEST_MODE
        # We will init this with None so that the engine can decide what to do.

        self.current_state = 'INIT'
        self.current_events = None

        # Now, we begin the loop
        self.engineLoop()

    def eventHandler(self):
        '''
        Handles engine events and a few other things.
        '''
        engine_mode = {
            'INIT': "(init...)",
            'WAITING': "(game loading...)",
            'LOGO_IN': "(loading...)",
            'LOGO_OUT': "(goodbye!)",
            'LOADING': "(loading...)",
            'ERROR': "(error!)",
            'UPDATING': "(updating...)",
            'TEST_MODE': "(test_menu)"
        }[self.current_state]

        ver = self.engine_conf.get_dict('engine', ValidatedDict({})).get_str('build')
        pygame.display.set_caption(f'BasedEngine V{ver} {engine_mode}')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                self.fadeLogoOut()
                print('thank you for playing!')
                pygame.display.quit()
                exit()

    def fadeLogoIn(self):
        '''
        Render the Logo and the background. Also play a jingle. 
        '''
        # Set the state
        self.current_state = "LOGO_IN"

        # Start by playing the jingle.
        AssetManager.playSfx('jingle.wav')

        # Blank the screen
        self.screen.fill((0, 0, 0))

        logo = AssetManager.loadImage('logo.png')

        for i in range(50):
            self.eventHandler()
            self.clock.tick(self.framerate)

            # Fade screen to white with the fade in.
            self.screen.fill((160+i, 160+i, 160+i))

            logo.set_alpha(115+(i*2))
            self.screen.blit(logo, ((self.resolution[0]-500)/2, 60-i))
            pygame.display.update()
            i += 1

    def fadeLogoOut(self):
        '''
        Render the Logo and the background fading out.
        '''
        # Set the state
        self.current_state = "LOGO_OUT"

        # Blank the screen
        self.screen.fill((210, 210, 210))

        logo = AssetManager.loadImage('logo.png')

        for i in range(55):
            self.eventHandler()
            self.clock.tick(self.framerate)

            # Fade screen to white with the fade in.
            self.screen.fill((160-i, 160-i, 160-i))

            logo.set_alpha(115-(i*2))
            self.screen.blit(logo, ((self.resolution[0]-500)/2, 60+i))
            pygame.display.update()
            i += 1

    def engineLoop(self):
        '''
        The main loop of the engine. Everything is started by this loop.
        '''
        has_looped = False
        while self.run:
            # First, we should start our loop with the event manager
            self.eventHandler()

            # Now, let's make sure that the game is locked to a framerate.
            self.clock.tick(self.framerate)

            # Load the fade in animation, but only if it's the first loop.
            if not has_looped:
                self.fadeLogoIn()

            # Update screen.
            pygame.display.update()
            # Set has_looped.
            has_looped = True

if __name__ == "__main__":
    path_prefix = './engine/json'
    config = JSONData.loadJsonFile(f'{path_prefix}/config.json')
    game = JSONData.loadJsonFile(f'{path_prefix}/game.json')

    GameEngine(config, game)

    # Game is over
    print('thank you for playing!')
    pygame.display.quit()
    exit()