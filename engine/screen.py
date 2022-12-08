import pygame, platform
from screeninfo import get_monitors
from engine.common.validated import ValidatedDict
from typing import Tuple

class Screen():
    def __init__(self, system_config: ValidatedDict):
        # Load the screen config and the game config
        self.screen_conf = system_config.get_dict('display')
        self.engine_conf = system_config.get_dict('engine')

        # Sanity checks on file
        if self.screen_conf == None:
            raise Exception('Null screen config!\nCheck your files!')
        if self.engine_conf == None:
            raise Exception('Null engine config!\nCheck your files!')

        # Get the system so that we can load a larger icon for MacOS.
        system = platform.system()
        print(f'Running on {system}!')
        if system == 'Darwin':
            self.icon = './engine/assets/icons/icon_high.png'
        else:
            self.icon = './engine/assets/icons/icon_low.png'

    def initScreen(self):
        # start display
        pygame.display.init()

        # this can be 
        # - full
        # - borderless
        # - window

        mode = self.screen_conf.get_str('video_mode', 'window')
        screen_id = self.screen_conf.get_int('screen')
        resolution = self.screen_conf.get_str('resolution', '1920x1080').split('x')
        
        # Sanity check.
        if len(resolution) != 2:
            resolution = ['1920', '1080']

        window_height = int(resolution[1])
        window_width = int(resolution[0])
        pygame_flags = 0

        if mode == 'full':
            monitors = get_monitors()
            if len(monitors) < screen_id:
                raise Exception('Your screen variable is too large!')
            
            display = monitors[screen_id]

            window_height = display.height
            window_width = display.width
            pygame_flags = pygame.FULLSCREEN|pygame.NOFRAME

        elif mode == 'borderless':
            pygame_flags = pygame.NOFRAME

        # We should init the caption and icon before the screen runs.
        ver = self.engine_conf.get_str('build')
        pygame.display.set_caption(f'BasedEngine V{ver} (init...)')
        pygame.display.set_icon(pygame.image.load(self.icon))

        # Start the screen
        screen = pygame.display.set_mode((window_width, window_height), pygame_flags, display=screen_id, vsync=self.screen_conf.get_bool('vsync'))
        return (screen, (window_width, window_height))