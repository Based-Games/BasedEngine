from pygame import Surface, image, mixer
import os

from engine.common.validated import ValidatedDict
from engine.common.constants import LogConstants
from engine.common.logger import LogManager

class AssetManager:
    '''
    Asset loaders, renderers, transformers and more!
    '''
    asset_prefix = "./engine/assets"

    def __init__(self, config: ValidatedDict, logger: LogManager) -> None:
        self.logger = logger
        self.config = config
    
    def loadImage(self, asset_name: str) -> Surface:
        '''
        Load an image in Texture form.

        Given:
            - asset_name: name of the asset, including extension.
        
        Returns: Asset as a texture.
        '''
        asset_path = f"{self.asset_prefix}/images/{asset_name}"

        if os.path.exists(asset_path):
            self.logger.writeLogEntry(f'Loading asset: {asset_name}', status=LogConstants.STATUS_OK_BLUE, tool="ASSET_MGR")
            return image.load(asset_path)

        else:
            self.logger.writeLogEntry(f'Couldn\'t find {asset_name}!', status=LogConstants.STATUS_FAIL, tool="ASSET_MGR")

    def playSfx(self, asset_name: str) -> Surface:
        '''
        Load a sound in sound form.

        Given:
            - asset_name: name of the asset, including extension.
        
        Returns: Nothing.
        '''
        asset_path = f"{self.asset_prefix}/sfx/{asset_name}"
        sound_settings = self.config.get_dict('sound')
        if sound_settings == None:
            raise Exception("Sound settings in JSON are missing!")

        if os.path.exists(asset_path):
            self.logger.writeLogEntry(f'Loading asset: {asset_name}', status=LogConstants.STATUS_OK_BLUE, tool="ASSET_MGR")
            sound = mixer.Sound(asset_path)
            sound.set_volume(sound_settings.get('sfx_volume', 1.0)-0.4)
            sound.play()

        else:
            self.logger.writeLogEntry(f'Couldn\'t find {asset_name}!', status=LogConstants.STATUS_FAIL, tool="ASSET_MGR")