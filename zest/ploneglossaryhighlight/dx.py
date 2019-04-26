from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.PloneGlossary.interfaces import IOptionalHighLight
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider

from zest.ploneglossaryhighlight.adapters import BaseOptionalHighLight
from zest.ploneglossaryhighlight.adapters import YES
from zest.ploneglossaryhighlight.adapters import NO
from zest.ploneglossaryhighlight.adapters import PARENT
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
        description=u"",
        required=False,
        default=PARENT,
        # vocabulary=HIGHLIGHT_VOCAB,
        # widget=SelectionWidget(),
    )


@implementer(IOptionalHighLight)
@adapter(IOptionalHighLightBehavior)
class OptionalHighLightAdapter(BaseOptionalHighLight):
    """Adapter that looks up the 'highlight' field on a DX object.
    """

    @property
    def highlight(self):
        return self.context.highlight

    @highlight.setter
    def highlight(self, value):
        self.context.highlight = value
