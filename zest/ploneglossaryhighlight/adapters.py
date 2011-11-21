from Acquisition import aq_inner, aq_parent
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.atapi import DisplayList
#from Products.Archetypes.interfaces import IBaseContent
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender, \
    IBrowserLayerAwareExtender
from zope.component import adapts
from zope.interface import implements, Interface

from Products.PloneGlossary.interfaces import IOptionalHighLight

# Our add-on browserlayer:
from zest.ploneglossaryhighlight.interfaces import IOptionalHighLightLayer
from zest.ploneglossaryhighlight import \
    ZestPloneGlossaryHighlightMessageFactory as _

YES = 'yes'
NO = 'no'
PARENT = 'parent'
HIGHLIGHT_VOCAB = DisplayList(data=[
    (YES, _(u"Yes")),
    (NO, _(u"No")),
    (PARENT, _(u"Use setting of parent folder")),
    ])


class MyBooleanField(ExtensionField, BooleanField):
    """A extension boolean field."""


class MyStringField(ExtensionField, StringField):
    """A extension string field."""


class HighLightExtender(object):
    """Schema extender that makes highlighting the known terms
    optional per object.
    """
    adapts(Interface)
    implements(ISchemaExtender, IBrowserLayerAwareExtender)
    # Don't do schema extending unless our add-on product is installed
    # on this Plone site.
    layer = IOptionalHighLightLayer
    fields = [
        MyStringField(
            "highlight",
            schemata='settings',
            default=PARENT,
            vocabulary=HIGHLIGHT_VOCAB,
            widget=SelectionWidget(
                label=_((u"This page, or pages contained in this folder, "
                         u"wants to highlight known terms from the glossary.")
                         ))),
            ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        """Get the fields.

        We could add a check like this, to avoid showing the fields
        unnecessarily, but then we should allow it for folderish items
        as well, so never mind.

        from Products.CMFCore.utils import getToolByName
        gtool = getToolByName(self.context, 'portal_glossary', None)
        if gtool is None:
            return []
        if not self.context.portal_type in gtool.getAllowedPortalTypes():
            return []
        """
        return self.fields


class OptionalHighLight(object):
    """Adapter that looks up the 'highlight' field on an object.
    """
    implements(IOptionalHighLight)
    adapts(Interface)

    def __init__(self, context):
        self.context = context

    def do_highlight(self, default=None):
        try:
            field = self.context.getField('highlight')
        except AttributeError:
            return default
        if not field:
            return default
        value = field.get(self.context)
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
