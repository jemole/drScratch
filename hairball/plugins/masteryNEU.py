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
        self.user_interactivity(file_blocks)
        self.parallelization(scratch)
        return {'types': file_blocks}
    
    def synchronization(self, file_blocks):
        """Assign the Syncronization skill result"""
        basic = 0
        developing = 0
        proficiency = 0
        if (file_blocks["wait until %s"] or 
            file_blocks["when backdrop switches to %s"] or
            file_blocks["broadcast %s and wait"]):
            proficiency = 1
        if (file_blocks["broadcast %s"] or file_blocks["when I receive %s"] or
            file_blocks["stop %s"]):
            developing = 1
        if file_blocks["wait %s secs"]:
            basic = 1
        self.concepts['Synchronization'] = basic + developing + proficiency
    
    def flow_control(self, file_blocks, scratch):
        """Assign the Flow Control skill result"""
        basic = 0
        developing = 0
        proficiency = 0
        if file_blocks["repeat until %s%s"]:
            proficiency = 1
        if (file_blocks["repeat %s%s"] or 
            file_blocks["forever%s"]):
            developing = 1
        for script in self.iter_scripts(scratch):
            if self.count_blocks(script) > 1: 
                basic = 1
                break
        self.concepts['FlowControl'] = basic + developing + proficiency
        
    def abstraction(self, file_blocks, scratch):
        """Assign the Abstraction skill result"""
        basic = 0
        developing = 0
        proficiency = 0
        if file_blocks["when I start as a clone"]:
            proficiency = 1
        if file_blocks["define %s"]: 
            developing = 1
        scripts = 0
        for script in self.iter_scripts(scratch):
            if self.script_start_type(script) != self.NO_HAT:
                scripts += 1
                if scripts > 1:
                    basic = 1
                    break
        self.concepts['Abstraction'] = basic + developing + proficiency
        
    def data(self, file_blocks):
        """Assign the Data representation skill result"""
        basic = 0
        developing = 0
        proficiency = 0
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
                proficiency = 1
                break
        if file_blocks["change %s by %s"] or file_blocks["set %s to %s"]:
            developing = 1
        for modifier in modifiers:
            if file_blocks[modifier]:
                basic = 1
                break
        self.concepts['DataRepresentation'] = basic + developing + proficiency

    def user_interactivity(self, file_blocks):
        """Assign the User Interactivity skill result"""
        basic = 0
        developing = 0
        proficiency = 0
        proficient = {'turn video %s', 'video %s on %s', 'when %s > %s', 
            'set video transparency to %s%%', 'loudness'}
        development = {'when %s key pressed', 'when this sprite clicked', 
            'mouse down?', 'key %s pressed?', 'ask %s and wait', 
            'answer' }
        for item in proficient:
            if file_blocks[item]:
                proficiency = 1
                break
        for item in development:
            if file_blocks[item]:
                developing = 1
                break
        if file_blocks['when @greenFlag clicked']:
            basic = 1
        self.concepts['UserInteractivity'] = basic + developing + proficiency
        
        
    def logic (self, file_blocks):
        """Assign the Logic skill result"""
        operations = {'%s and %s', '%s or %s', 'not %s'}
        basic = 0
        developing = 0
        proficiency = 0
        for operation in operations:
            if file_blocks[operation]:
                proficiency = 1
                break
        if file_blocks["if %s then%selse%s"]:
            developing = 1
        if file_blocks["if %s then%s"]: 
            basic = 1
        self.concepts['Logic'] = basic + developing + proficiency
    
    def parallelization (self, scratch):
        """Assign the Parallelization skill result"""
        basic = 0
        developing = 0
        proficiency = 0
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
                    proficiency = 1
                else:
                    messages.append(message)
            # 2 Scripts start on the same backdrop change
            if self.script_start_type(script) == self.HAT_BACKDROP and self.count_blocks(script) > 1:
                backdrop = script.blocks[0].args[0].lower()
                if backdrop in backdrops:
                    proficiency = 1
                else:
                    backdrops.append(backdrop)
            # 2 Scripts start on the same multimedia (video, audio, timer) event
            if self.script_start_type(script) == self.HAT_MULTIMEDIA and self.count_blocks(script) > 1:
                multi = script.blocks[0].args[0], script.blocks[0].args[1]
                if multi in multimedia:
                    proficiency = 1
                else:
                    multimedia.append(multi)
            # use of clones
            #Se podria comprobar si 2 scripts del mismo personaje comienzan con HAT_CLONE
            #elif self.script_start_type(script) == self.HAT_CLONE:
            #    self.concepts['Parallelization'] = 3
            #    return
            # 2 Scripts start on the same key pressed
            if self.script_start_type(script) == self.HAT_KEY and self.count_blocks(script) > 1:
                key = script.blocks[0].args[0]
                if key in keys:
                    developing = 1
                else:
                    keys.append(key)
            # 2 scripts on green flag
            if self.script_start_type(script) == self.HAT_GREEN_FLAG and self.count_blocks(script) > 1:
                green_flag += 1
                if green_flag > 1:
                    basic = 1
            # Sprite with 2 scripts on clicked
            sprites = list(self.iter_sprites(scratch))
            for sprite in sprites:
                clicked = 0
                for script in sprite.scripts:
                    if self.script_start_type(script) == self.HAT_MOUSE and self.count_blocks(script) > 1:
                        clicked += 1
                    if clicked > 1:
                        #self.concepts['Parallelization'] = 2
                        developing = 1
                        #return
        self.concepts['Parallelization'] = basic + developing + proficiency
