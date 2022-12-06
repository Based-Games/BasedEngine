from pygame import Surface, image, mixer
import os
from sys import exit

from engine.jsondata import JSONData

class AssetManager:
    '''
    Asset loaders, renderers, transformers and more!
    '''
    asset_prefix = "./engine/assets"
    config = JSONData.loadJsonFile(f'./engine/json/config.json').get_dict('system')

    @classmethod
    def loadImage(self, asset_name: str) -> Surface:
        '''
        Load an image in Texture form.

        Given:
            - asset_name: name of the asset, including extension.
        
        Returns: Asset as a texture.
        '''
        asset_path = f"{self.asset_prefix}/images/{asset_name}"

        if os.path.exists(asset_path):
            print(f'loading asset: {asset_name}')
            return image.load(asset_path)

        else:
            print(f'{asset_name} was not found. Check your file paths.')
            exit()

    @classmethod
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
            print(f'loading asset: {asset_name}')
            sound = mixer.Sound(asset_path)
            sound.set_volume(sound_settings.get('sfx_volume', 1.0)-0.4)
            sound.play()

        else:
            print(f'{asset_name} was not found. Check your file paths.')
            exit()