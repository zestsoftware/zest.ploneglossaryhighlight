from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from zope.configuration import xmlconfig


class PloneGlossaryHighlightNotInstalled(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.PloneGlossary
        xmlconfig.file('configure.zcml', Products.PloneGlossary,
                       context=configurationContext)
        import zest.ploneglossaryhighlight
        xmlconfig.file('configure.zcml', zest.ploneglossaryhighlight,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.PloneGlossary:default')


class PloneGlossaryHighlight(PloneGlossaryHighlightNotInstalled):

    defaultBases = (PLONE_FIXTURE,)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'Products.PloneGlossary:default')
        applyProfile(portal, 'zest.ploneglossaryhighlight:default')


PLONEGLOSSARYHIGHLIGHT_NOT_INSTALLED_FIXTURE = \
    PloneGlossaryHighlightNotInstalled()
PLONEGLOSSARYHIGHLIGHT_NOT_INSTALLED_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEGLOSSARYHIGHLIGHT_NOT_INSTALLED_FIXTURE,),
    name="PloneGlossaryHighlightNotInstalled:Integration")

PLONEGLOSSARYHIGHLIGHT_FIXTURE = PloneGlossaryHighlight()
PLONEGLOSSARYHIGHLIGHT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEGLOSSARYHIGHLIGHT_FIXTURE,),
    name="PloneGlossaryHighlight:Integration")
