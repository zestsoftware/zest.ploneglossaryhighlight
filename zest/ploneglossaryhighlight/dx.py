from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.PloneGlossary.interfaces import IOptionalHighLight
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from zope.schema import Choice
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from zest.ploneglossaryhighlight.adapters import BaseOptionalHighLight
from zest.ploneglossaryhighlight.adapters import YES
from zest.ploneglossaryhighlight.adapters import NO
from zest.ploneglossaryhighlight.adapters import PARENT
from zest.ploneglossaryhighlight import ZestPloneGlossaryHighlightMessageFactory as _


_terms = (
    SimpleTerm(YES, title=_(u"Yes")),
    SimpleTerm(NO, title=_(u"No")),
    SimpleTerm(PARENT, title=_(u"Use setting of parent folder")),
)
HIGHLIGHT_VOCAB = SimpleVocabulary(_terms)


@provider(IFormFieldProvider)
class IOptionalHighLightBehavior(model.Schema):
    """Behavior extender that makes highlighting the known terms optional.
    """

    model.fieldset("settings", label=_(u"Settings"), fields=["highlight"])
    highlight = Choice(
        title=_(
            (
                u"This page, or pages contained in this folder, "
                u"wants to highlight known terms from the glossary."
            )
        ),
        description=u"",
        vocabulary=HIGHLIGHT_VOCAB,
        default=PARENT,
        required=True,
        readonly=False,
    )


@implementer(IOptionalHighLight)
@adapter(IOptionalHighLightBehavior)
class OptionalHighLightAdapter(BaseOptionalHighLight):
    """Adapter that looks up the 'highlight' field on a DX object.
    """

    @property
    def highlight(self):
        return self.context.highlight

    # @highlight.setter
    # def highlight(self, value):
    #     self.context.highlight = value
