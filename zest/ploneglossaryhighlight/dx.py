from Acquisition import aq_inner, aq_parent

from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider

from Products.PloneGlossary.interfaces import IOptionalHighLight

from zest.ploneglossaryhighlight.interfaces import YES
from zest.ploneglossaryhighlight.interfaces import NO
from zest.ploneglossaryhighlight.interfaces import PARENT
from zest.ploneglossaryhighlight import ZestPloneGlossaryHighlightMessageFactory as _


# TODO
HIGHLIGHT_VOCAB = (
    (YES, _(u"Yes")),
    (NO, _(u"No")),
    (PARENT, _(u"Use setting of parent folder")),
)


@provider(IFormFieldProvider)
class IOptionalHighLightBehavior(model.Schema):
    """Behavior extender that makes highlighting the known terms optional.
    """

    # TODO fix schema.
    highlight = schema.ASCIILine(
        title=_(
            (
                u"This page, or pages contained in this folder, "
                u"wants to highlight known terms from the glossary."
            )
        ),
        description=u'',
        required=False,
        default=PARENT,
        # vocabulary=HIGHLIGHT_VOCAB,
        # widget=SelectionWidget(),
    )


@implementer(IOptionalHighLightBehavior)
@adapter(IDexterityContent)
class OptionalHighLight(object):
    """Adapter that looks up the 'highlight' field on an object.
    """

    def __init__(self, context):
        self.context = context

    @property
    def highlight(self):
        return self.context.highlight

    @highlight.setter
    def highlight(self, value):
        self.context.highlight = value

    def do_highlight(self, default=None):
        value = self.highlight
        # The rest is the same for DX and AT, so could be shared.
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
