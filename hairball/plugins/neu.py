"""This module provides plugins for NEU metrics."""

import kurt
from hairball.plugins import HairballPlugin
#from PIL import Image
import os



class Variables(HairballPlugin):

    """Plugin that counts the number of variables in a project."""

    def __init__(self):
        super(Variables, self).__init__()
        self.total = 0

    def finalize(self):
        """Output the number of variables in the project."""
        print("Number of variables: %i" % self.total)

    def analyze(self, scratch):
        """Run and return the results of the Variables plugin."""          
        self.total = len(scratch.variables)
        for sprite in scratch.sprites:
            self.total += len(sprite.variables)

class Lists(HairballPlugin):

    """Plugin that counts the number of lists in a project."""

    def __init__(self):
        super(Lists, self).__init__()
        self.total = 0

    def finalize(self):
        """Output the number of lists in the project."""
        print("Number of lists: %i" % self.total)

    def analyze(self, scratch):
        """Run and return the results of the Lists plugin."""
        self.total = len(scratch.lists)
        for sprite in scratch.sprites:
            self.total += len(sprite.lists)

class Backgrounds(HairballPlugin):

    """Plugin that counts the number of backgrounds in a project."""

    def __init__(self):
        super(Backgrounds, self).__init__()
        self.total = 0
        self.use = "No"

    def finalize(self):
        """Output the number of backgrounds in the project."""
        print("Number of backgrounds: %i" % self.total)
        print "Uses blocks to modify backdrops?: " + self.use

    def analyze(self, scratch):
        """Run and return the results of the Backgrounds plugin."""          
        self.total = len(scratch.stage.backgrounds)
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if name == 'switch backdrop to %s' or name == 'next backdrop' or name == 'switch backdrop to %s and wait':
                    self.use = "Yes"
                    break
            if self.use == "Yes":
                break

class Costumes(HairballPlugin):

    """Plugin that counts the number of costumes in a project."""

    def __init__(self):
        super(Costumes, self).__init__()
        self.total = 0
        self.sprites = 0
        self.use = 'No'


    def finalize(self):
        """Output the number of costumes in the project."""
        print "Number of costumes: %i" % self.total
        print "Number of sprites: %i" % self.sprites
        if self.sprites > 0:
            output = str(self.total/float(self.sprites))
        else:
            output = "0"
        print "Average of costumes by sprite:" + output
        print "Uses blocks to modify costumes?: " + self.use

    def analyze(self, scratch):
        """Run and return the results of the costumes plugin."""          
        for sprite in scratch.sprites:
            self.total += len(sprite.costumes)
            self.sprites += 1
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if name == 'switch costume to %s' or name == 'next costume':
                    self.use = "Yes"
                    break
            if self.use == "Yes":
                break

class BlockCounts(HairballPlugin):

    """Plugin that keeps track of the number of blocks in a project."""

    def __init__(self):
        super(BlockCounts, self).__init__()
        self.blocks = 0

    def finalize(self):
        """Output the aggregate block count results."""
        print("Number of blocks %i" % self.blocks)

    def analyze(self, scratch):
        """Run and return the results from the BlockCounts plugin."""
        for script in self.iter_scripts(scratch):
            for block in self.iter_blocks(script.blocks):
                self.blocks += 1

class Chance(HairballPlugin):

    """Plugin that keeps track of the number of random number generator blocks in a project."""

    def __init__(self):
        super(Chance, self).__init__()
        self.total = 0

    def finalize(self):
        """Output the aggregate random block count results."""
        print("Number of random blocks: %i" % self.total)

    def analyze(self, scratch):
        """Run and return the results from the Chance plugin."""
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if name == 'pick random %s to %s':
                    self.total += 1

class UserInteractivity(HairballPlugin):

    """Plugin that keeps track of the types of user inteactivity in a project."""

    def __init__(self):
        super(UserInteractivity, self).__init__()
        self.mouseClick = 0
        self.mouseMove = 0
        self.pressKey = 0
        self.answer = 0
        self.media = 0

    def finalize(self):
        """Output the results"""
        print "Types of user interactivity that appear in the project:"
        if self.mouseClick > 0:
            print "Mouse - clicks"
        if self.mouseMove > 0:
            print "Mouse - movements"
        if self.pressKey > 0:
            print "Keyboard - keys pressed"
        if self.answer > 0:
            print "Answer questions"
        if self.media > 0:
            print "Sound or video"

    def analyze(self, scratch):
        """Run and return the results from the UserInteractivity plugin."""
        for script in self.iter_scripts(scratch):
            for name, _, block in self.iter_blocks(script.blocks):
                if name == 'video %s on %s' or name == 'when %s > %s' or name == 'loudness':
                    self.media += 1
                elif name == 'when %s key pressed' or name == 'key %s pressed?':
                    self.pressKey += 1
                elif name == 'ask %s and wait' or name == 'answer':
                    self.answer += 1
                elif name == 'when this sprite clicked' or name == 'mouse down?':
                    self.mouseClick += 1
                elif ((name == 'touching %s?' or name == 'go to %s') and block.args[0] == 'mouse-pointer'):
                    self.mouseMove += 1

class Colors(HairballPlugin):

    """Plugin that keeps track of the colors of the stage images."""

    def __init__(self):
        self.colors ={}

    def finalize(self):
        """Output the aggregate block count results."""
        print self.colors

    def compute_average_image_color(self, img):
        """
            Compute the most frequent color in img.
            Code adapted from 
            http://blog.zeevgilovitz.com/detecting-dominant-colours-in-python/
        """
        image = Image.open(img)
        w, h = image.size
        pixels = image.getcolors(w * h)
        most_frequent_pixel = pixels[0]
        for count, colour in pixels:
            if count > most_frequent_pixel[0]:
                most_frequent_pixel = (count, colour)
        rgb = []
        for i in range(3):
            rgb.append (most_frequent_pixel[1][i])
        trgb = tuple(rgb)
        trgb = '#%02x%02x%02x' % trgb #Transform rgb to Hex color (HTML)
        return trgb

    def analyze(self, scratch):
        """Run and return the results from the BlockCounts plugin."""
        #ToDo: get the images from stage and characters
        print "Still in development"

class Ending(HairballPlugin):

    """Plugin that checks if the project seems to end."""

    def __init__(self):
        super(Ending, self).__init__()
        self.total = 0

    def finalize(self):
        """Output whether the project seems to end or not."""
        if self.total > 0:
            print "The game seems to end at some point"
        else:
            print "The game seems to not ever end"

    def analyze(self, scratch):
        """Run and return the results of the Ending plugin."""          
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                if name == "stop %s":
                    self.total
                    all_scripts = list(self.iter_scripts(scratch))

class Beginning(HairballPlugin):

    """
        Plugin that checks if the project seems to show instructions or a menu
        when the project is launched.
    """

    def __init__(self):
        super(Beginning, self).__init__()
        self.backdropWhenGreenFlag = 0
        self.spritesHidden = []
        self.spritesShown = 0
        self.actions = []

    def finalize(self):
        """Output whether the project seems to have beginning instructions"""
        if (self.backdropWhenGreenFlag > 0 
            and len (self.spritesHidden) > 0
            and self.spritesShown >0
            and len(self.actions) > 0):
            print "The game seems to present instructions or a menu when launched"
        else:
            print "The game seems to NOT present instructions nor a menu when launched"

    def backdropGreenFlag (self, all_scripts):
        """
            Check if a specific backdrop is displayed when green flag
        """
        backdropWhenGreenFlag = 0
        for script in all_scripts:
            if self.script_start_type(script) == self.HAT_GREEN_FLAG:
                for name, _, block in self.iter_blocks(script.blocks):
                    if name == 'switch backdrop to %s':
                        backdropWhenGreenFlag = block.args[0].lower()
                        break
            if backdropWhenGreenFlag != 0:
                break
        return backdropWhenGreenFlag

    def getHiddenSprites (self, scratch):
        """
            Check if there are sprites that are hidden when green flag
        """
        spritesHidden = []
        for sprite in scratch.sprites:
            hide = 0
            wait = 0
            for script in sprite.scripts:
                if not isinstance(script, kurt.Comment):
                    if self.script_start_type(script) == self.HAT_GREEN_FLAG:
                        for name, _, _ in self.iter_blocks(script.blocks):
                            if name == 'hide':
                                spritesHidden.append(sprite)
                                hide = 1
                            elif name == 'wait %s secs' and hide == 1:
                                wait = 1
                            elif name == 'show' and hide == 1 and wait == 1:
                                spritesHidden.remove(sprite)
        return spritesHidden

    def getActions (self, scratch):
        """
            Find messages sent or backdrops displayed or variables modified
            right after an user action (press key or mouse click)
        """
        actions = []
        for sprite in scratch.sprites:
            if sprite not in self.spritesHidden: 
                for script in sprite.scripts:
                    if (self.script_start_type(script) == self.HAT_MOUSE
                        or self.script_start_type(script) == self.HAT_KEY):
                        for name, _, block in self.iter_blocks(script.blocks):
                            if (name == 'switch backdrop to %s' 
                                or name == 'switch backdrop to %s and wait' 
                                or name == 'change %s by %s' 
                                or name == 'set %s to %s' 
                                #or name == 'when %s key pressed' 
                                or name == 'broadcast %s' 
                                or name == 'broadcast %s and wait'):
                                    actions.append(block.args[0].lower())
                    ### para aniadir vars modificadas tras un "si tecla x pulsada"
        for script in scratch.stage.scripts:
            if (self.script_start_type(script) == self.HAT_MOUSE
                or self.script_start_type(script) == self.HAT_KEY):
                for name, _, block in self.iter_blocks(script.blocks):
                    if (name == 'switch backdrop to %s' 
                        or name == 'switch backdrop to %s and wait'
                        or name == 'change %s by %s' 
                        or name == 'set %s to %s' 
                        #or name == 'when %s key pressed' 
                        or name == 'broadcast %s' 
                        or name == 'broadcast %s and wait'):
                            actions.append(block.args[0].lower())
                    elif name =='next backdrop' and self.backdropWhenGreenFlag != 0:
                        backs = []
                        for back in scratch.stage.backgrounds:
                            backs.append(back.name.lower())
                        #print backs
                        if (backs.index(self.backdropWhenGreenFlag) + 1 < len (backs)):
                            actions.append(backs[backs.index(self.backdropWhenGreenFlag) + 1])
                        elif len(backs) > 0:
                            actions.append(backs[0])
        #ToDo: En ocasiones en lugar de "al presionar" se usa un "esperar hasta que tecla x pulsada"
        #ToDo: En ocasiones en lugar de "al hacer click sobre este objeto" se usa un "tocando mouse"
        return actions

    def getShownSprites (self, scratch):
        """
            Check if there are sprites that are shown after one of the actions
        """
        spritesShown = 0
        for sprite in scratch.sprites:
            if sprite in self.spritesHidden:
                for script in sprite.scripts:
                    if not isinstance(script, kurt.Comment):
                        if (self.script_start_type(script) == self.HAT_BACKDROP 
                            or self.script_start_type(script) == self.HAT_WHEN_I_RECEIVE
                            or self.script_start_type(script) == self.HAT_KEY):
                            if script.blocks[0].args[0].lower() in self.actions:
                                for name, _, _ in self.iter_blocks(script.blocks):
                                    if name == 'show':
                                        spritesShown += 1
                                        break
                        #ToDo: comprobar que el show esta despues que la variable
                        elif self.script_start_type(script) == self.HAT_GREEN_FLAG:
                            variableAction = 0
                            show = 0
                            for name, _, block in self.iter_blocks(script.blocks):
                                if name == '%s' and block.args[0].lower() in self.actions:
                                    variableAction += 1
                                    break
                                elif name == 'show':
                                    spritesShown += 1
                            if variableAction > 0 and show > 0:
                                spritesShown += 1
                        #ToDo: check if clones are created after action, and clones are in turn shown
        return spritesShown

    def analyze(self, scratch):
        """Run and return the results of the Beginning plugin."""          
        all_scripts = list(self.iter_scripts(scratch))
        self.backdropWhenGreenFlag = self.backdropGreenFlag(all_scripts)
        self.spritesHidden = self.getHiddenSprites(scratch)
        #ToDo: Check if there are variables and lists and if so check if they are hidden when launched
        self.actions = self.getActions(scratch)
        self.spritesShown = self.getShownSprites(scratch)
        #ToDo: Check if there are variables and lists and if so check if they are shown after actions

class ModelOfReality(HairballPlugin):

    """Plugin that detects reinforcing feedback loops in a project."""

    def __init__(self):
        super(ModelOfReality, self).__init__()
        self.vars = []
        self.sprites = []

    def findSetter(self, scratch, var):
        """Return the initial value of var ('na' if not found)"""
        for script in self.iter_scripts(scratch):
            for name, _, block in self.iter_blocks(script.blocks):
                if (name == 'set %s to %s' and block.args[0] == var):
                    if type(block.args[1]) is not kurt.Block:
                        return block.args[1]
                    else:
                        return block.args[1].stringify()
        return 'na'

    def findRelationships(self, scratch, var):
        """Return the variables that affect var('na' if not found)"""
        relationships = []
        r = []
        for sprite in scratch.sprites:
            for script in sprite.scripts:
                for name, depth, block in self.iter_blocks(script.blocks):
                    if (name == 'change %s by %s' and block.args[0] == var):
                        for v in self.vars:
                            if str(v[0] != var):
                                r = []
                                if type(block.args[1]) is kurt.Block:
                                    if str(v[0]) in block.args[1].stringify():
                                        r.append(v[0])
                                        r.append(block.args[1].stringify())
                                        r.append(sprite.name)
                                else:
                                    r.append("---")
                                    r.append(str(block.args[1]))
                                    r.append(sprite.name)
                                if len(r) > 0:
                                    if len(relationships) == 0 or r not in relationships:
                                        relationships.append(r)
                                    if self.isUserOperated(scratch,sprite.name):
                                        if sprite.name not in self.sprites:
                                            self.sprites.append(sprite.name)
        for script in scratch.stage.scripts:
            for name, depth, block in self.iter_blocks(script.blocks):
                    if (name == 'change %s by %s' and block.args[0] == var):
                        for v in self.vars:
                            if str(v[0] != var):
                                r = []
                                if type(block.args[1]) is kurt.Block:
                                    if str(v[0]) in block.args[1].stringify():
                                        r.append(v[0])
                                        r.append(block.args[1].stringify())
                                        r.append('Stage')
                                        if len(relationships) == 0 or v[1] not in zip(*relationships)[1]:
                                            relationships.append(r)
                                else:
                                    r.append("---")
                                    r.append(str(block.args[1]))
                                    r.append('Stage')
                                    if len(relationships) == 0 or r not in relationships:
                                        relationships.append(r)
        if len(relationships) > 0:
            return relationships
        else:
            return ['na']

    def isUserOperated(self, scratch, sprite):
        """Return True if sprite is is handled by the user """
        for character in scratch.sprites:
            if character.name == sprite: 
                for script in character.scripts:
                    for name, _, _ in self.iter_blocks(script.blocks):
                        if (name == 'when %s key pressed' or
                            name == 'when this sprite clicked' or
                            name == 'mouse down?' or
                            name == 'key %s pressed?' or
                            name == 'ask %s and wait' or
                            name == 'answer' or
                            name == 'video %s on %s' or
                            name == 'when %s > %s' or
                            name == 'loudness'):
                            return True
        return False

    def finalize(self):
        """Output the the variables and their relationships in a project."""
        if len(self.vars) > 0:
            for v in self.vars:
                print 'Variable: ' + str(v[0])
                print '  - Initial value: ' + str(v[1])
                if v[2] != ['na']:
                    #print v[2]
                    for r in list(v[2]):
                        if r[0] != '---':
                            print '  - Modified in ' + r[2] + ' by variable ' + r[0] + ' with following operation: ' + r[1]
                        else:
                            print '  - Modified in ' + r[2] + ' with following operand: ' + r[1]
            if len(self.sprites) > 0:
                print "List of sprites where vars are modified that are handled by the user:"
                for sprite in self.sprites:
                    print "  - " + sprite
        else:
            print "No variables"

    def analyze(self, scratch):
        """Run and return the results of the ModelOfReality plugin."""          
        for var in scratch.variables:
            v = []
            v. append(str(var))
            v.append(self.findSetter(scratch,var))            
            self.vars.append(v)
        for sprite in scratch.sprites:
            for var in sprite.variables:
                v = []
                v. append(str(var))
                v.append(self.findSetter(scratch,var))            
                self.vars.append(v)
        for var in self.vars:
            var.append(self.findRelationships(scratch,var[0]))