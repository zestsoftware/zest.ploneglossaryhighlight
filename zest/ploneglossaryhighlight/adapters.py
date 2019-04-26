from Acquisition import aq_inner
from Acquisition import aq_parent
from Products.CMFPlone.utils import base_hasattr
from Products.PloneGlossary.interfaces import IOptionalHighLight


# Define the valid values for the field.
YES = "yes"
NO = "no"
PARENT = "parent"


class BaseOptionalHighLight(object):
    """Adapter that gets the 'highlight' attribute from an object.

    It takes care of determining whether this object wants highlighting,
    including looking at parent settings if needed.
    """

    # This is expected to be overridden in sub classes.
    highlight = None

    def __init__(self, context):
        self.context = context

    def do_highlight(self, default=None):
        value = self.highlight
        if value == PARENT:
            parent = aq_parent(aq_inner(self.context))
            optional = IOptionalHighLight(parent, None)
            if optional is not None:
                return optional.do_highlight(default)
            return default
        if value == YES:
            return True
        if value == NO:
            return False
        return default
