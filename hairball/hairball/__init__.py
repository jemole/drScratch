"""A plugin-able framework for the static analysis of Scratch projects."""

import kurt
import os
import sys
from imp import load_source
from optparse import OptionParser
from hairball.plugins import HairballPlugin


__version__ = '0.1rc3'


class Hairball(object):

    """The Hairball exeuction class.

    This class is responsible for parsing command line arguments, loading the
    plugins, and running the plugins on the specified scratch files.

    """

    def __init__(self, argv):
        self.plugins = []
        description = ('PATH can be either the path to a scratch file, or a '
                       'directory containing scratch files. Multiple PATH '
                       'arguments can be provided.')
        parser = OptionParser(usage='%prog -p PLUGIN_NAME [options] PATH...',
                              description=description,
                              version='%prog {0}'.format(__version__))
        parser.add_option('-d', '--plugin-dir', metavar='DIR',
                          help=('Specify the path to a directory containing '
                                'plugins. Plugins in this directory take '
                                'precedence over similarly named plugins '
                                'included with Hairball.'))
        parser.add_option('-p', '--plugin', action='append',
                          help=('Use the named plugin to perform analysis. '
                                'This option can be provided multiple times.'))
        parser.add_option('-k', '--kurt-plugin', action='append',
                          help=('Include the named file containing Kurt '
                                'plugin. This file should contain a '
                                'load_hairball method. '
                                'This option can be provided multiple times.'))
        self.options, self.args = parser.parse_args(argv)

        if not self.options.plugin:
            parser.error('At least one plugin must be specified via -p.')
        if not self.args:
            parser.error('At least one PATH must be provided.')

        if self.options.plugin_dir:
            if os.path.isdir(self.options.plugin_dir):
                sys.path.append(self.options.plugin_dir)
            else:
                parser.error('`{0}` is not a directory'
                             .format(self.options.plugin_dir))

        if self.options.kurt_plugin:
            for kurt_plugin in self.options.kurt_plugin:
                module = os.path.splitext(os.path.basename(kurt_plugin))[0]
                load_source(module, kurt_plugin)

        self.extensions = [x.extension for x in
                           kurt.plugin.Kurt.plugins.values()]

    def finalize(self):
        """Indicate that analysis is complete.

        Calling finalize  will call the finalize method of all plugins thus
        allowing them to output any aggregate results or perform any clean-up.

        """
        for plugin in self.plugins:
            plugin.finalize()

    def initialize_plugins(self):
        """Attempt to Load and initialize all the plugins.

        Any issues loading plugins will be output to stderr.

        """
        for plugin_name in self.options.plugin:
            parts = plugin_name.split('.')
            if len(parts) > 1:
                module_name = '.'.join(parts[:-1])
                class_name = parts[-1]
            else:
                # Use the titlecase format of the module name as the class name
                module_name = parts[0]
                class_name = parts[0].title()

            # First try to load plugins from the passed in plugins_dir and then
            # from the hairball.plugins package.
            plugin = None
            for package in (None, 'hairball.plugins'):
                if package:
                    module_name = '{0}.{1}'.format(package, module_name)
                try:
                    module = __import__(module_name, fromlist=[class_name])
                    # Initializes the plugin by calling its constructor
                    plugin = getattr(module, class_name)()

                    # Verify plugin is of the correct class
                    if not isinstance(plugin, HairballPlugin):
                        sys.stderr.write('Invalid type found for plugin `{0}` '
                                         '{1}\n'.format(plugin_name,
                                                        type(plugin)))
                        plugin = None
                    else:
                        break
                except (ImportError, AttributeError):
                    pass
            if plugin:
                self.plugins.append(plugin)
            else:
                sys.stderr.write('Cannot find plugin `{0}`\n'
                                 .format(plugin_name))
        if not self.plugins:
            sys.stderr.write('No plugins loaded. Goodbye!\n')
            sys.exit(1)

    def process(self):
        """Start the analysis."""
        scratch_files = []
        while self.args:
            filename = self.args.pop()
            _, ext = os.path.splitext(filename)
            # Interatively traverse directories
            if os.path.isdir(filename):
                for temp in os.listdir(filename):
                    if temp not in ('.', '..'):
                        self.args.append(os.path.join(filename, temp))
            elif ext in self.extensions and os.path.isfile(filename):
                scratch_files.append(filename)

        # Run all the plugins on a single file at at time so we only have to
        # open the file once.
        for filename in sorted(scratch_files):
            print(filename)
            scratch = kurt.Project.load(filename)
            for plugin in self.plugins:
                plugin._process(scratch)  # pylint: disable-msg=W0212

def main():
    """The entrypoint for the `hairball` command installed via setup.py."""
    hairball = Hairball(sys.argv[1:])
    hairball.initialize_plugins()
    hairball.process()
    hairball.finalize()
