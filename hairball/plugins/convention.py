"""This module provides plugins for basic programming convention checks"""

from hairball.plugins import HairballPlugin


class SpriteNaming(HairballPlugin):

    """Plugin that keeps track of how often sprites default 
       
    names (like Sprite1, Sprite2...) are used within a project.
    
    """

    def __init__(self):
        super(SpriteNaming, self).__init__()
        self.total_default = 0
        self.list_default = []
        self.default_names = ["Sprite","Objeto"]

    def finalize(self):
        """Output the default sprite names found in the project."""
        print("%d default sprite names found:" % self.total_default)
        for name in self.list_default:
            print name

    def analyze(self, scratch):
        """Run and return the results from the SpriteNaming plugin."""
        for sprite in self.iter_sprites(scratch):
            for default in self.default_names:
                if default in sprite.name:
                    self.total_default += 1
                    self.list_default.append(sprite.name)

class BackdropNaming(HairballPlugin):

    """Plugin that keeps track of how often backdrop default 
       
    names (like backdrop1, backdrop2...) are used within a project.
    
    """

    def __init__(self):
        super(BackdropNaming, self).__init__()
        self.total_default = 0
        self.list_default = []
        self.default_names = ["backdrop"]

    def finalize(self):
        """Output the default backdrop names found in the project."""
        print("%d default backgdrop names found" % self.total_default)
        for name in self.list_default:
            print name

    def analyze(self, scratch):
        """Run and return the results from the BackdropNaming plugin."""
        for background in scratch.stage.backgrounds:
            for default in self.default_names:
                if default in background.name:
                    self.total_default += 1
                    self.list_default.append(background.name)