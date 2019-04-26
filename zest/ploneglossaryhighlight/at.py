from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import StringField
from Products.Archetypes.public import SelectionWidget
from Products.Archetypes.atapi import DisplayList

from Products.Archetypes.interfaces import IBaseContent
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import (
    ISchemaExtender,
    IBrowserLayerAwareExtender,
)
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

from Products.PloneGlossary.interfaces import IOptionalHighLight

from zest.ploneglossaryhighlight.adapters import BaseOptionalHighLight
from zest.ploneglossaryhighlight.adapters import YES
from zest.ploneglossaryhighlight.adapters import NO
from zest.ploneglossaryhighlight.adapters import PARENT

# Our add-on browserlayer:
from zest.ploneglossaryhighlight.interfaces import IOptionalHighLightLayer
from zest.ploneglossaryhighlight import ZestPloneGlossaryHighlightMessageFactory as _


HIGHLIGHT_VOCAB = DisplayList(
    data=[
        (YES, _(u"Yes")),
        (NO, _(u"No")),
        (PARENT, _(u"Use setting of parent folder")),
    ]
)


class MyBooleanField(ExtensionField, BooleanField):
    """A extension boolean field."""


class MyStringField(ExtensionField, StringField):
    """A extension string field."""


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
@adapter(Interface)
class HighLightExtender(object):
    """Schema extender that makes highlighting the known terms
    optional per object.
    """

    # Don't do schema extending unless our add-on product is installed
    # on this Plone site.
    layer = IOptionalHighLightLayer
    fields = [
        MyStringField(
            "highlight",
            schemata="settings",
            default=PARENT,
            vocabulary=HIGHLIGHT_VOCAB,
            widget=SelectionWidget(
                label=_(
                    (
                        u"This page, or pages contained in this folder, "
                        u"wants to highlight known terms from the glossary."
                    )
                )
            ),
        )
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


@implementer(IOptionalHighLight)
@adapter(IBaseContent)
class OptionalHighLight(BaseOptionalHighLight):
    """Adapter that looks up the 'highlight' field on an AT object.
    """

    def __init__(self, context):
        self.context = context

    @property
    def highlight(self):
        field = self.context.getField("highlight")
        if field:
            return field.get(self.context)
