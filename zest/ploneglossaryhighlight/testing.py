from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFCore.utils import getToolByName
from zope.configuration import xmlconfig


class PloneGlossaryHighlightNotInstalled(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import Products.PloneGlossary

        xmlconfig.file(
            "configure.zcml", Products.PloneGlossary, context=configurationContext
        )
        import zest.ploneglossaryhighlight

        xmlconfig.file(
            "configure.zcml", zest.ploneglossaryhighlight, context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, "Products.PloneGlossary:default")

        # We don't care about permissions in these tests.
        setRoles(portal, TEST_USER_ID, ("Manager",))


PLONEGLOSSARYHIGHLIGHT_NOT_INSTALLED_FIXTURE = PloneGlossaryHighlightNotInstalled()
PLONEGLOSSARYHIGHLIGHT_NOT_INSTALLED_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEGLOSSARYHIGHLIGHT_NOT_INSTALLED_FIXTURE,),
    name="PloneGlossaryHighlightNotInstalled:Integration",
)


class PloneGlossaryHighlight(PloneGlossaryHighlightNotInstalled):

    defaultBases = (PLONEGLOSSARYHIGHLIGHT_NOT_INSTALLED_FIXTURE,)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "Products.PloneGlossary:default")
        applyProfile(portal, "zest.ploneglossaryhighlight:default")


PLONEGLOSSARYHIGHLIGHT_FIXTURE = PloneGlossaryHighlight()
PLONEGLOSSARYHIGHLIGHT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEGLOSSARYHIGHLIGHT_FIXTURE,), name="PloneGlossaryHighlight:Integration"
)


class PloneGlossaryHighlightDexterity(PloneGlossaryHighlight):

    defaultBases = (PLONEGLOSSARYHIGHLIGHT_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # import plone.app.dexterity
        # self.loadZCML(name='meta.zcml', package=plone.app.dexterity)
        # self.loadZCML(package=plone.app.dexterity)
        import plone.dexterity

        self.loadZCML(name="meta.zcml", package=plone.dexterity)
        self.loadZCML(package=plone.dexterity)

    def setUpPloneSite(self, portal):
        from plone.dexterity.fti import DexterityFTI

        # Create FTI with our behavior enabled.
        fti = DexterityFTI("enabledtype")
        portal.portal_types._setObject("enabledtype", fti)
        fti.klass = "plone.dexterity.content.Container"
        fti.filter_content_types = False
        fti.behaviors = (
            "zest.ploneglossaryhighlight",
            "plone.app.dexterity.behaviors.metadata.IBasic",
        )

        # Create FTI with our behavior disabled.
        fti = DexterityFTI("disabledtype")
        portal.portal_types._setObject("disabledtype", fti)
        fti.klass = "plone.dexterity.content.Container"
        fti.filter_content_types = False
        fti.behaviors = ("plone.app.dexterity.behaviors.metadata.IBasic",)

        # Enable highlighting these types by default
        gtool = getToolByName(portal, "portal_glossary")
        allowed = list(gtool.getAllowedPortalTypes())
        allowed.extend(["enabledtype", "disabledtype"])
        allowed = tuple(allowed)
        gtool.allowed_portal_types = allowed


PLONEGLOSSARYHIGHLIGHT_DEXTERITY_FIXTURE = PloneGlossaryHighlightDexterity()
PLONEGLOSSARYHIGHLIGHT_DEXTERITY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEGLOSSARYHIGHLIGHT_DEXTERITY_FIXTURE,),
    name="PloneGlossaryHighlightDexterity:Integration",
)
