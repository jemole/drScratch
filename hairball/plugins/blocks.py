"""This module provides plugins for basic block statistics."""

from collections import Counter
from hairball.plugins import HairballPlugin


class BlockCounts(HairballPlugin):

    """Plugin that keeps track of how often each block is used."""

    def __init__(self):
        super(BlockCounts, self).__init__()
        self.blocks = Counter()

    def finalize(self):
        """Output the aggregate block count results."""
        for name, count in sorted(self.blocks.items(), key=lambda x: x[1]):
            print('{0:3} {1}'.format(count, name))
        print('{0:3} total'.format(sum(self.blocks.values())))

    def analyze(self, scratch):
        """Run and return the results from the BlockCounts plugin."""
        file_blocks = Counter()
        for script in self.iter_scripts(scratch):
            for name, _, _ in self.iter_blocks(script.blocks):
                file_blocks[name] += 1
        self.blocks.update(file_blocks)  # Update the overall count
        return {'types': file_blocks}


class DeadCode(HairballPlugin):

    """Plugin that indicates unreachable code in Scratch files."""

    def __init__(self):
        super(DeadCode, self).__init__()
        self.total_instances = 0
        self.dead_code_instances = 0

    def analyze(self, scratch):
        """Run and return the results form the DeadCode plugin.

        The variable_event indicates that the Scratch file contains at least
        one instance of a broadcast event based on a variable. When
        variable_event is True, dead code scripts reported by this plugin that
        begin with a "when I receive" block may not actually indicate dead
        code.

        """
        self.total_instances += 1
        sprites = {}
        for sprite, script in self.iter_sprite_scripts(scratch):
            if not script.reachable:
                blocks_list = []
                for name, _, _ in self.iter_blocks(script.blocks):
                    blocks_list.append(name)
                sprites.setdefault(sprite, []).append(blocks_list)
        if sprites:
            self.dead_code_instances += 1
            import pprint
            pprint.pprint(sprites)
        variable_event = any(True in self.get_broadcast_events(x) for x in
                             self.iter_scripts(scratch))
        return {'dead_code': {'sprites': sprites,
                              'variable_event': variable_event}}

    def finalize(self):
        """Output the number of instances that contained dead code."""
        
        if self.total_instances > 1:
            print('{0} of {1} instances contained dead code.'
                  .format(self.dead_code_instances, self.total_instances))
