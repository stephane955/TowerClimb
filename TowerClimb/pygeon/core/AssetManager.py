from os import listdir
from os.path import basename

import pygame


class AssetManager:
    """A class for handling all assets

    Only images at this point

    ...

    Methods
    -------
    load_image(file_path=str, asset_id=str)
        Loads an image from the given path and stores it under the specified id
    get_image(asset_id=str)
        Get the referenced image from the id
    create_internal_image(self, width=int, height=int, color=(int, int, int), asset_id=str)
        Creates an internal image for testing
    """

    def __init__(self, image_missing: pygame.image):
        """
        Parameters
        ----------
        image_missing : pygame.Image
            An image for replacing other images to prevent crashing because of images which could not be found
        """

        self.__image_missing = image_missing
        self.__all_images = {}

    def load_image(self, file_path, asset_id):
        """Tries to load an image

        If the image cannot be loaded it gets replaced by a default error image
        Only loading every image once will reduce the memory needed

        Parameters
        ----------
        file_path : str
            The file path from which the image is loaded
        :asset_id : str
            The id which is used to store the image

        Returns
        -------
        bool
            Whether the image could be loaded or not
        """

        try:
            self.__all_images[asset_id] = pygame.image.load(file_path)  # Store the image under the specified id
            return True
        except FileNotFoundError:
            self.__all_images[asset_id] = self.__image_missing  # If the image could not be found use the missing_image
            return False

    def get_image(self, asset_id: str):
        """Get a reference to a image by its id

        Parameters
        ----------
        asset_id : str
            The id of the required image

        Returns
        -------
        pygame.Image
            Returns a image
        """

        return self.__all_images[asset_id]

    def create_internal_image(self, width: int, height: int, color: (int, int, int), asset_id: str):
        """Creates an internal image for testing

        Parameter
        ---------
        width : int
            The width of the image
        height : int
            The height of the image
        color : (int, int, int)
            The color of the image
        asset_id : str
            The id under which the image is stored
        """
        
        surf = pygame.Surface((width, height))
        surf.fill(color)
        self.__all_images[asset_id] = surf

    def load_all_from_directory(self,base_name, path):
        __files = [(path + file) for file in listdir(path)]
        for i in range(len(__files)):
            self.load_image(__files[i], base_name+"_"+str(i));
