"""This module provides plugins used in the hairball paper."""

from collections import defaultdict, Counter
from hairball.plugins import HairballPlugin


class Animation(HairballPlugin):

    """Plugin that checks for instances of 'complex animation'.

    Animation should include loops, motion, timing, and costume changes.

    """

    COSTUME = frozenset(['switch to costume %l', 'next costume'])
    LOOP = frozenset(['repeat %n', 'repeat until %b', 'forever',
                      'forever if %b'])
    MOTION = frozenset(['change y by %n', 'change x by %n',
                        'glide %n secs to x:%n y:%n',
                        'move %n steps', 'go to x:%n y:%n'])
    ROTATE = frozenset(['turn cw %n degrees', 'turn ccw %n degrees',
                        'point in direction %d'])
    SIZE = frozenset(['change size by %n', 'set size to %n%'])
    TIMING = frozenset(['wait %n secs', 'glide %n secs to x:%n y:%n'])
    ANIMATION = COSTUME | LOOP | MOTION | ROTATE | SIZE | TIMING

    @staticmethod
    def check_results(tmp_):
        """Return a 3 tuple for something."""
        # TODO: Fix this to work with more meaningful names
        if tmp_['t'] > 0:
            if tmp_['l'] > 0:
                if tmp_['rr'] > 0 or tmp_['ra'] > 1:
                    print 1, 3, tmp_
                    return 3
                elif tmp_['cr'] > 0 or tmp_['ca'] > 1:
                    print 2, 3, tmp_
                    return 3
                elif tmp_['mr'] > 0 or tmp_['ma'] > 1:
                    print 3, 2, tmp_
                    return 2
            if tmp_['cr'] > 1 or tmp_['ca'] > 2:
                print 4, 2, tmp_
                return 2
            if tmp_['mr'] > 0 or tmp_['ma'] > 1:
                if tmp_['cr'] > 0 or tmp_['ca'] > 1:
                    print 6, 0, tmp_
                    return 0
            if tmp_['rr'] > 1 or tmp_['ra'] > 2:
                print 7, 0, tmp_
                return 0
            if tmp_['sr'] > 1 or tmp_['sa'] > 2:
                print 8, 0, tmp_
                return 0
        if tmp_['l'] > 0:
            if tmp_['rr'] > 0 or tmp_['ra'] > 1:
                print 9, 2, tmp_
                return 2
            if tmp_['cr'] > 0 or tmp_['ca'] > 1:
                print 10, 0, tmp_
                return 0
        return -1

    def check_animation(self, last, last_level, gen):
        tmp_ = Counter()
        results = Counter()
        name, level, block = last, last_level, last
        others = False
        while name in self.ANIMATION and level >= last_level:
            if name in self.LOOP:
                if block != last:
                    count = self.check_results(tmp_)
                    if count > -1:
                        results[count] += 1
                    tmp_.clear()
                tmp_['last'] += 1

            for attribute in ('costume', 'orientation', 'position', 'size'):
                if (name, 'relative') in self.BLOCKMAPPING[attribute]:
                    tmp_[(attribute, 'relative')] += 1
                elif (name, 'absolute') in self.BLOCKMAPPING[attribute]:
                    tmp_[(attribute, 'absolute')] += 1
            if name in self.TIMING:
                tmp_['timing'] += 1

            last_level = level
            name, level, block = next(gen, ('', 0, ''))
            # allow some exceptions
            if name not in self.ANIMATION and name != '':
                if not others:
                    if block.type.flag != 't':
                        last_level = level
                        (name, level, block) = next(gen, ('', 0, ''))
                        others = True
        count = self.check_results(tmp_)
        if count > -1:
            results[count] += 1
        return gen, results

    def analyze(self, scratch):
        results = Counter()
        for script in self.iter_scripts(scratch):
            gen = self.iter_blocks(script.blocks)
            name = 'start'
            level = None
            while name != '':
                if name in self.ANIMATION:
                    gen, count = self.check_animation(name, level, gen)
                    results.update(count)
                name, level, _ = next(gen, ('', 0, ''))
        return {'animation': results}


class BroadcastReceive(HairballPlugin):

    """Plugin that checks for proper usage of broadcast and receive blocks."""

    def get_receive(self, script_list):
        """Return a list of received events contained in script_list."""
        events = defaultdict(set)
        for script in script_list:
            if self.script_start_type(script) == self.HAT_WHEN_I_RECEIVE:
                event = script.blocks[0].args[0].lower()
                events[event].add(script)
        return events

    def analyze(self, scratch):
        all_scripts = list(self.iter_scripts(scratch))
        results = defaultdict(set)
        broadcast = dict((x, self.get_broadcast_events(x))  # Events by script
                         for x in all_scripts)
        correct = self.get_receive(all_scripts)
        results['never broadcast'] = set(correct.keys())

        for script, events in broadcast.items():
            for event in events.keys():
                if event is True:  # Remove dynamic broadcasts
                    results['dynamic broadcast'].add(script.morph.name)
                    del events[event]
                elif event in correct:
                    results['never broadcast'].discard(event)
                else:
                    results['never received'].add(event)

        # remove events from correct dict that were never broadcast
        for event in correct.keys():
            if event in results['never broadcast']:
                del correct[event]

        # Find scripts that have more than one broadcast event on any possible
        # execution path through the program
        # TODO: Permit mutually exclusive broadcasts
        for events in broadcast.values():
            if len(events) > 1:
                for event in events:
                    if event in correct:
                        results['parallel broadcasts'].add(event)
                        del correct[event]

        # Find events that have two (or more) receivers in which one of the
        # receivers has a "delay" block
        for event, scripts in correct.items():
            if len(scripts) > 1:
                for script in scripts:
                    for _, _, block in self.iter_blocks(script.blocks):
                        if block.type.flag == 't':
                            results['multiple receivers with delay'].add(event)
                            if event in correct:
                                del correct[event]

        results['success'] = set(correct.keys())
        return {'broadcast': results}


class SaySoundSync(HairballPlugin):

    """Plugin that checks for synchronization between say and sound blocks.

    The order should be:
    Say "___",
    Play sound "___" until done,
    Say ""

    """

    CORRECT = -1
    ERROR = 0
    INCORRECT = 1
    HACKISH = 2

    SAY_THINK = ('say %s', 'think %s')
    SAY_THINK_DURATION = ('say %s for %n secs', 'think %s for %n secs')
    ALL_SAY_THINK = SAY_THINK + SAY_THINK_DURATION

    @staticmethod
    def is_blank(word):
        """Return True if the string is empty, or only whitespace."""
        return not word or word.isspace()

    def analyze(self, scratch):
        """Categorize instances of attempted say and sound synchronization."""
        errors = Counter()
        for script in self.iter_scripts(scratch):
            prev_name, prev_depth, prev_block = '', 0, script.blocks[0]
            gen = self.iter_blocks(script.blocks)
            for name, depth, block in gen:
                if prev_depth == depth:
                    if prev_name in self.SAY_THINK:
                        if name == 'play sound %S until done':
                            if not self.is_blank(prev_block.args[0]):
                                errors += self.check(gen)
                        # TODO: What about play sound?
                    elif prev_name in self.SAY_THINK_DURATION and \
                            'play sound %S' in name:
                        errors['1'] += 1
                    elif prev_name == 'play sound %S':
                        if name in self.SAY_THINK:
                            errors[self.INCORRECT] += 1
                        elif name in self.SAY_THINK_DURATION:
                            if self.is_blank(block.args[0]):
                                errors[self.ERROR] += 1
                            else:
                                errors[self.HACKISH] += 1
                    elif prev_name == 'play sound %S until done' and \
                            name in self.ALL_SAY_THINK:
                        if not self.is_blank(block.args[0]):
                            errors[self.INCORRECT] += 1
                        # TODO: Should there be an else clause here?
                prev_name, prev_depth, prev_block = name, depth, block
        return {'sound': errors}

    def check(self, gen):
        """Check that the last part of the chain matches.

        TODO: Fix to handle the following situation that appears to not work

        say 'message 1'
        play sound until done
        say 'message 2'
        say 'message 3'
        play sound until done
        say ''

        """
        retval = Counter()
        name, _, block = next(gen, ('', 0, ''))
        if name in self.SAY_THINK:
            if self.is_blank(block.args[0]):
                retval[self.CORRECT] += 1
            else:
                name, _, block = next(gen, ('', 0, ''))
                if name == 'play sound %S until done':
                    # Increment the correct count because we have at least
                    # one successful instance
                    retval[self.CORRECT] += 1
                    # This block represents the beginning of a second
                    retval += self.check(gen)
                else:
                    retval[self.INCORRECT] += 1
        else:
            retval[self.INCORRECT] += 1
        return retval
