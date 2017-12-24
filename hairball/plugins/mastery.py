"""This module provides plugins for measuring programming mastery"""

from collections import Counter
from hairball.plugins import HairballPlugin


class Mastery(HairballPlugin):

    """
        Plugin that measures programming mastery of a project
        in terms of Abstraction, Syncronization, Parallelism,
        Logic, Flow Control, Data representation and
        User Interactivity.
    """

    def __init__(self):
        super(Mastery, self).__init__()
        self.blocks = Counter()
        self.concepts = {} # CT concepts or capabilities

    def finalize(self):
        """Output the overall programming competence"""
        print self.concepts
        total = 0
        for i in self.concepts.items():
            total += i[1]
        print ("Total mastery points: %d/21" % total)
        average =  float (total) / 7
        print ("Average mastery points: %.2f/3" % average)
        if average > 2:
            print "Overall programming competence: Proficiency"
        elif average > 1:
            print "Overall programming competence: Developing"
        else:
            print "Overall programming competence: Basic"
    def analyze(self, scratch):
        """Run and return the results from the Mastery plugin."""
        file_blocks = Counter()
        for script in self.iter_scripts(scratch):
            if self.script_start_type(script) != self.NO_HAT:
                for name, _, _ in self.iter_blocks(script.blocks):
                    file_blocks[name] += 1
        self.blocks.update(file_blocks)  # Update the overall count
        self.flow_control(file_blocks, scratch)
        self.synchronization(file_blocks)
        self.abstraction(file_blocks, scratch)
        self.data(file_blocks)
        self.logic(file_blocks)
        self.user_interactivity(file_blocks, scratch)
        self.parallelization(scratch)
        return {'types': file_blocks}

    def synchronization(self, file_blocks):
        """Assign the Syncronization skill result"""
        if (file_blocks["wait until %s"] or
            file_blocks["when backdrop switches to %s"] or
            file_blocks["broadcast %s and wait"]):
            score = 3
        elif (file_blocks["broadcast %s"] or file_blocks["when I receive %s"] or
            file_blocks["stop %s"]):
            score = 2
        elif file_blocks["wait %s secs"]:
            score = 1
        else:
            score = 0
        self.concepts['Synchronization'] = score

    def flow_control(self, file_blocks, scratch):
        """Assign the Flow Control skill result"""
        score = 0
        if file_blocks["repeat until %s%s"]:
            score = 3
        elif (file_blocks["repeat %s%s"] or
            file_blocks["forever%s"]):
            score = 2
        else:
            for script in self.iter_scripts(scratch):
                if self.count_blocks(script) > 1:
                    score = 1
                    break
        self.concepts['FlowControl'] = score

    def abstraction(self, file_blocks, scratch):
        """Assign the Abstraction skill result"""
        score = 0
        if file_blocks["when I start as a clone"]:
            score = 3
        elif file_blocks["define %s"]:
            score = 2
        else:
            scripts = 0
            for script in self.iter_scripts(scratch):
                if self.script_start_type(script) != self.NO_HAT:
                    scripts += 1
                    if scripts > 1:
                        score = 1
                        break
        self.concepts['Abstraction'] = score

    def data(self, file_blocks):
        """Assign the Data representation skill result"""
        score = 0
        modifiers = {'switch backdrop to %s', 'next backdrop',
            'switch costume to %s', 'next costume',
            'turn @turnRight %s degrees',
            'turn @turnLeft %s degrees', 'point in direction %s',
            'point towards %s', 'move %s steps', 'go to x:%s y:%s',
            'go to %s', 'glide %s secs to x:%s y:%s',
            'change x by %s', 'set x to %s', 'change y by %s',
            'set y to %s', 'change size by %s', 'set size to %s%%',
            'hide', 'show', 'set %s effect to %s',
            'change %s effect by %s'}
        lists = {'length of %s', 'show list %s',
            'insert %s at %s of %s', 'delete %s of %s', 'add %s to %s',
            'replace item %s of %s with %s', '%s contains %s',
            'hide list %s', 'item %s of %s'}
        for item in lists:
            if file_blocks[item]:
                self.concepts['DataRepresentation'] = 3
                return
        if file_blocks["change %s by %s"] or file_blocks["set %s to %s"]:
            score = 2
        else:
            for modifier in modifiers:
                if file_blocks[modifier]:
                    score = 1
        self.concepts['DataRepresentation'] = score

    def check_mouse(self, scratch):
        """Check whether there is a block 'go to mouse' or 'touching mouse-pointer?' """
        for script in self.iter_scripts(scratch):
            for name, _, block in self.iter_blocks(script.blocks):
                if name == 'go to %s' and block.args[0] == 'mouse-pointer':
                    return 1
                if name == 'touching %s?' and block.args[0] == 'mouse-pointer':
                    return 1
        return 0

    def user_interactivity(self, file_blocks, scratch):
        """Assign the User Interactivity skill result"""
        score = 0
        proficiency = {'turn video %s', 'video %s on %s', 'when %s > %s',
            'set video transparency to %s%%', 'loudness'}
        developing = {'when %s key pressed', 'when this sprite clicked',
            'mouse down?', 'key %s pressed?', 'ask %s and wait',
            'answer',  }
        for item in proficiency:
            if file_blocks[item]:
                self.concepts['UserInteractivity'] = 3
                return
        for item in developing:
            if file_blocks[item]:
                self.concepts['UserInteractivity'] = 2
                return
        if file_blocks['go to %s']:
            if self.check_mouse(scratch) == 1:
                self.concepts['UserInteractivity'] = 2
                return
        if file_blocks['touching %s?']:
            if self.check_mouse(scratch) == 1:
                self.concepts['UserInteractivity'] = 2
                return
        if file_blocks['when @greenFlag clicked']:
            score = 1
        self.concepts['UserInteractivity'] = score


    def logic (self, file_blocks):
        """Assign the Logic skill result"""
        operations = {'%s and %s', '%s or %s', 'not %s'}
        score = 0
        for operation in operations:
            if file_blocks[operation]:
                self.concepts['Logic'] = 3
                return
        if file_blocks["if %s then%selse%s"]:
            score = 2
        elif file_blocks["if %s then%s"]:
            score = 1
        self.concepts['Logic'] = score

    def parallelization (self, scratch):
        """Assign the Parallelization skill result"""
        score = 0
        all_scripts = list(self.iter_scripts(scratch))

        messages = []
        backdrops = []
        multimedia = []
        keys = []
        green_flag = 0
        num_blocks = 0 # quitar
        for script in all_scripts:
            # 2 Scripts start on the same received message
            if self.script_start_type(script) == self.HAT_WHEN_I_RECEIVE and self.count_blocks(script) > 1:
                message = script.blocks[0].args[0].lower()
                if message in messages:
                    self.concepts['Parallelization'] = 3
                    return
                else:
                    messages.append(message)
            # 2 Scripts start on the same backdrop change
            elif self.script_start_type(script) == self.HAT_BACKDROP and self.count_blocks(script) > 1:
                backdrop = script.blocks[0].args[0].lower()
                if backdrop in backdrops:
                    self.concepts['Parallelization'] = 3
                    return
                else:
                    backdrops.append(backdrop)
            # 2 Scripts start on the same multimedia (video, audio, timer) event
            elif self.script_start_type(script) == self.HAT_MULTIMEDIA and self.count_blocks(script) > 1:
                multi = script.blocks[0].args[0], script.blocks[0].args[1]
                if multi in multimedia:
                    self.concepts['Parallelization'] = 3
                    return
                else:
                    multimedia.append(multi)
            # use of clones
            #Se podria comprobar si 2 scripts del mismo personaje comienzan con HAT_CLONE
            #elif self.script_start_type(script) == self.HAT_CLONE:
            #    self.concepts['Parallelization'] = 3
            #    return
            # 2 Scripts start on the same key pressed
            elif self.script_start_type(script) == self.HAT_KEY and self.count_blocks(script) > 1:
                key = script.blocks[0].args[0]
                if key in keys:
                    score = 2
                else:
                    keys.append(key)
            # 2 scripts on green flag
            elif self.script_start_type(script) == self.HAT_GREEN_FLAG and self.count_blocks(script) > 1:
                green_flag += 1
                if green_flag > 1 and score == 0:
                    score = 1
            # Sprite with 2 scripts on clicked
            sprites = list(self.iter_sprites(scratch))
            for sprite in sprites:
                clicked = 0
                for script in sprite.scripts:
                    if self.script_start_type(script) == self.HAT_MOUSE and self.count_blocks(script) > 1:
                        clicked += 1
                    if clicked > 1:
                        #self.concepts['Parallelization'] = 2
                        score = 2
                        #return
        self.concepts['Parallelization'] = score
