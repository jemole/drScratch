"""This module provides plugins for checking initialization."""

import kurt
from hairball.plugins import HairballPlugin


def partition_scripts(scripts, start_type1, start_type2):
    """Return two lists of scripts out of the original `scripts` list.

    Scripts that begin with a `start_type1` or `start_type2` blocks
    are returned first. All other scripts are returned second.

    """
    match, other = [], []
    for script in scripts:
        if HairballPlugin.script_start_type(script) == start_type1:
            match.append(script)
        elif HairballPlugin.script_start_type(script) == start_type2:
            match.append(script)
        else:
            other.append(script)
    return match, other


class AttributeInitialization(HairballPlugin):

    """Plugin that checks if modified attributes are properly initialized."""

    ATTRIBUTES = ('background', 'costume', 'orientation', 'position', 'size',
                  'visibility')

    STATE_NOT_MODIFIED = 0
    STATE_MODIFIED = 1
    STATE_INITIALIZED = 2

    @classmethod
    def attribute_result(cls, sprites):
        """Return mapping of attributes to if they were initialized or not."""
        retval = dict((x, True) for x in cls.ATTRIBUTES)
        for properties in sprites.values():
            for attribute, state in properties.items():
                retval[attribute] &= state != cls.STATE_MODIFIED
        return retval

    @classmethod
    def attribute_state(cls, scripts, attribute):
        """Return the state of the scripts for the given attribute.

        If there is more than one `when green flag clicked` script and they
        both modify the attribute, then the attribute is considered to not be
        initialized.

        """
        green_flag, other = partition_scripts(scripts, cls.HAT_GREEN_FLAG, cls.HAT_CLONE)
#	add_scripts(green_flag, other, cls.HAT_CLONE)
        block_set = cls.BLOCKMAPPING[attribute]
        state = cls.STATE_NOT_MODIFIED
        # TODO: Any regular broadcast blocks encountered in the initialization
        # zone should be added to this loop for conflict checking.
        for script in green_flag:
            in_zone = True
            for name, level, _ in cls.iter_blocks(script.blocks):
                if name == 'broadcast %e and wait':
                    # TODO: Follow the broadcast and wait scripts that occur in
                    # the initialization zone
                    in_zone = False
                if (name, 'absolute') in block_set:
                    if in_zone and level == 0:  # Success!
                        if state == cls.STATE_NOT_MODIFIED:
                            state = cls.STATE_INITIALIZED
                        elif HairballPlugin.script_start_type(script) == cls.HAT_GREEN_FLAG:
                            # Multiple when green flag clicked conflict
                            state = cls.STATE_MODIFIED
                    elif in_zone:
                        continue  # Conservative ignore for nested absolutes
                    else:
                        state = cls.STATE_MODIFIED
                    break  # The state of the script has been determined
                elif (name, 'relative') in block_set:
                    state = cls.STATE_MODIFIED
                    break
        if state != cls.STATE_NOT_MODIFIED:
            return state
        # Check the other scripts to see if the attribute was ever modified
        for script in other:
            if not isinstance(script, kurt.Comment):
                for name, _, _ in cls.iter_blocks(script.blocks):
                    if name in [x[0] for x in block_set]:
                        return cls.STATE_MODIFIED
        return cls.STATE_NOT_MODIFIED

    @classmethod
    def output_results(cls, sprites):
        """Output whether or not each attribute was correctly initialized.

        Attributes that were not modified at all are considered to be properly
        initialized.

        """
        print(' '.join(cls.ATTRIBUTES))
        format_strs = ['{{{0}!s:^{1}}}'.format(x, len(x)) for x in
                       cls.ATTRIBUTES]
        print(' '.join(format_strs).format(**cls.attribute_result(sprites)))

    @classmethod
    def sprite_changes(cls, sprite):
        """Return a mapping of attributes to their initilization state."""
        retval = dict((x, cls.attribute_state(sprite.scripts, x)) for x in
                      (x for x in cls.ATTRIBUTES if x != 'background'))
        return retval

    def analyze(self, scratch):
        """Run and return the results of the AttributeInitialization plugin."""
        changes = dict((x.name, self.sprite_changes(x)) for x in
                       scratch.sprites)
        changes['stage'] = {
            'background': self.attribute_state(scratch.stage.scripts,
                                               'costume')}
        #self.output_results(changes)
        print changes
        return {'initialized': changes}


class VariableInitialization(HairballPlugin):

    """Plugin that checks if modified variables are properly initialized."""

    STATE_NOT_MODIFIED = 0
    STATE_MODIFIED = 1
    STATE_INITIALIZED = 2

    @classmethod
    def variable_state(cls, scripts, variables):
        """Return the initialization state for each variable in variables.

        The state is determined based on the scripts passed in via the scripts
        parameter.

        If there is more than one `when green flag clicked` script and they
        both modify the attribute, then the attribute is considered to not be
        initialized.

        """

        def conditionally_set_not_modified():
            """Set the variable to modified if it hasn't been altered."""
            state = variables.get(block.args[0], None)
            if state == cls.STATE_NOT_MODIFIED:
                variables[block.args[0]] = cls.STATE_MODIFIED

        green_flag, other = partition_scripts(scripts, cls.HAT_GREEN_FLAG)
        variables = dict((x, cls.STATE_NOT_MODIFIED) for x in variables)
        for script in green_flag:
            in_zone = True
            for name, level, block in cls.iter_blocks(script.blocks):
                #if name == 'broadcast %e and wait':
                if name == 'broadcast %s and wait':###cambiar
                    in_zone = False
                #if name == 'set %v to %s':
                if name == 'set %s to %s':
                    state = variables.get(block.args[0], None)
                    if state is None:
                        continue  # Not a variable we care about
                    if in_zone and level == 0:  # Success!
                        if state == cls.STATE_NOT_MODIFIED:
                            state = cls.STATE_INITIALIZED
                        else:  # Multiple when green flag clicked conflict
                            # TODO: Need to allow multiple sets of a variable
                            # within the same script
                            #print 'CONFLICT', script
                            state = cls.STATE_MODIFIED
                    elif in_zone:
                        continue  # Conservative ignore for nested absolutes
                    elif state == cls.STATE_NOT_MODIFIED:
                        state = cls.STATE_MODIFIED
                    variables[block.args[0]] = state
                #elif name == 'change %v by %n':
                elif name == 'change %s by %s':
                    conditionally_set_not_modified()
        for script in other:
            for name, _, block in cls.iter_blocks(script.blocks):
                #if name in ('change %v by %n', 'set %v to %s'):
                if name in ('change %s by %s', 'set %s to %s'):
                    conditionally_set_not_modified()
        return variables

    def analyze(self, scratch):
        """Run and return the results of the VariableInitialization plugin."""

        variables = dict((x, self.variable_state(x.scripts, scratch.variables))### he cambiado x.variables por scratch.variables
                         for x in scratch.sprites)
        variables['global'] = self.variable_state(self.iter_scripts(scratch),
                                                  scratch.stage.variables)
        # Output for now
        import pprint
        pprint.pprint(variables)
        return {'variables': variables}
