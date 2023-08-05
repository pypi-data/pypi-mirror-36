"""These are the actual Sphinx directives we provide, but they are skeletal.

The real meat is in their parallel renderer classes, in renderers.py. The split
is due to the unfortunate trick we need here of having functions return the
directive classes after providing them the ``app`` symbol, where we store the
LUADoc output, via closure. The renderer classes, able to be top-level classes,
can access each other and collaborate.

"""
from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import flag

from .renderers import AutoFunctionRenderer, AutoClassRenderer, AutoAttributeRenderer


class LuaDirective(Directive):
    """Abstract directive which knows how to pull things out of LUADoc output"""

    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    option_spec = {
        'short-name': flag
    }


def auto_function_directive_bound_to_app(app):
    class AutoFunctionDirective(LuaDirective):
        """lua:autofunction directive, which spits out a lua:function directive

        Takes a single argument which is a LUA function name combined with an
        optional formal parameter list, all mashed together in a single string.

        """
        def run(self):
            return AutoFunctionRenderer.from_directive(self, app).rst_nodes()

    return AutoFunctionDirective


def auto_class_directive_bound_to_app(app):
    class AutoClassDirective(LuaDirective):
        """lua:autoclass directive, which spits out a lua:class directive

        Takes a single argument which is a LUA class name combined with an
        optional formal parameter list for the constructor, all mashed together
        in a single string.

        """
        option_spec = LuaDirective.option_spec.copy()
        option_spec.update({
            'members': lambda members: ([m.strip() for m in members.split(',')]
                                        if members else []),
            'exclude-members': _members_to_exclude,
            'private-members': flag})

        def run(self):
            return AutoClassRenderer.from_directive(self, app).rst_nodes()

    return AutoClassDirective


def auto_attribute_directive_bound_to_app(app):
    class AutoAttributeDirective(LuaDirective):
        """lua:autoattribute directive, which spits out a lua:attribute directive

        Takes a single argument which is a LUA attribute name.

        """
        def run(self):
            return AutoAttributeRenderer.from_directive(self, app).rst_nodes()

    return AutoAttributeDirective


def _members_to_exclude(arg):
    """Return a set of members to exclude given a comma-delim list them.

    Exclude none if none are passed. This differs from autodocs' behavior,
    which excludes all. That seemed useless to me.

    """
    return set(a.strip() for a in (arg or '').split(','))
