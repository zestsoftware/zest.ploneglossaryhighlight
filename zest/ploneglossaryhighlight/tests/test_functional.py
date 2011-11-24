import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from zest.ploneglossaryhighlight.testing import (
    PLONEGLOSSARYHIGHLIGHT_NOT_INSTALLED_INTEGRATION_TESTING,
    PLONEGLOSSARYHIGHLIGHT_INTEGRATION_TESTING,
    )


class TestNormalGlossary(unittest.TestCase):

    layer = PLONEGLOSSARYHIGHLIGHT_NOT_INSTALLED_INTEGRATION_TESTING

    def testHasNoField(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        new_id = portal.invokeFactory('Document', 'doc')
        self.assertFalse(portal[new_id].getField('highlight'))

    def testHighlightDoc(self):
        portal = self.layer['portal']
        gtool = getToolByName(portal, 'portal_glossary')
        setRoles(portal, TEST_USER_ID, ('Manager',))
        new_id = portal.invokeFactory('Document', 'doc')
        self.assertTrue(gtool.highlightContent(portal[new_id]))


class TestInstalled(unittest.TestCase):

    layer = PLONEGLOSSARYHIGHLIGHT_INTEGRATION_TESTING

    def testHasField(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        new_id = portal.invokeFactory('Document', 'doc')
        self.assertTrue(portal[new_id].getField('highlight'))

    def testHighlightDoc(self):
        portal = self.layer['portal']
        gtool = getToolByName(portal, 'portal_glossary')
        setRoles(portal, TEST_USER_ID, ('Manager',))
        new_id = portal.invokeFactory('Document', 'doc')
        self.assertTrue(gtool.highlightContent(portal[new_id]))
