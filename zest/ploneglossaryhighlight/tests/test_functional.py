import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from Products.PloneGlossary.interfaces import IOptionalHighLight

from zest.ploneglossaryhighlight.adapters import YES, NO, PARENT
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

    def testNoHighlightImage(self):
        portal = self.layer['portal']
        gtool = getToolByName(portal, 'portal_glossary')
        setRoles(portal, TEST_USER_ID, ('Manager',))
        new_id = portal.invokeFactory('Image', 'image')
        self.assertFalse(gtool.highlightContent(portal[new_id]))

    def testHighlightDocInFolder(self):
        portal = self.layer['portal']
        gtool = getToolByName(portal, 'portal_glossary')
        setRoles(portal, TEST_USER_ID, ('Manager',))
        folder_id = portal.invokeFactory('Folder', 'folder')
        folder = portal[folder_id]
        doc_id = folder.invokeFactory('Document', 'doc')
        doc = folder[doc_id]
        self.assertFalse(gtool.highlightContent(folder))
        self.assertTrue(gtool.highlightContent(doc))


class TestInstalled(unittest.TestCase):

    layer = PLONEGLOSSARYHIGHLIGHT_INTEGRATION_TESTING

    def testHasField(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        new_id = portal.invokeFactory('Document', 'doc')
        self.assertTrue(portal[new_id].getField('highlight'))

    def testDefaultValue(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))
        new_id = portal.invokeFactory('Document', 'doc')
        doc = portal[new_id]
        self.assertTrue(doc.getField('highlight').get(doc), PARENT)

    def testHighlightDoc(self):
        portal = self.layer['portal']
        gtool = getToolByName(portal, 'portal_glossary')
        setRoles(portal, TEST_USER_ID, ('Manager',))
        new_id = portal.invokeFactory('Document', 'doc')
        self.assertTrue(gtool.highlightContent(portal[new_id]))

    def testNoHighlightImage(self):
        portal = self.layer['portal']
        gtool = getToolByName(portal, 'portal_glossary')
        setRoles(portal, TEST_USER_ID, ('Manager',))
        new_id = portal.invokeFactory('Image', 'image')
        self.assertFalse(gtool.highlightContent(portal[new_id]))

    def testHighlightDocOff(self):
        portal = self.layer['portal']
        gtool = getToolByName(portal, 'portal_glossary')
        setRoles(portal, TEST_USER_ID, ('Manager',))
        new_id = portal.invokeFactory('Document', 'doc')
        doc = portal[new_id]
        doc.getField('highlight').set(doc, NO)
        self.assertFalse(gtool.highlightContent(doc))

    def testHighlightDocOffFolderOn(self):
        portal = self.layer['portal']
        gtool = getToolByName(portal, 'portal_glossary')
        setRoles(portal, TEST_USER_ID, ('Manager',))
        folder_id = portal.invokeFactory('Folder', 'folder')
        folder = portal[folder_id]
        doc_id = folder.invokeFactory('Document', 'doc')
        doc = folder[doc_id]
        folder.getField('highlight').set(folder, YES)
        self.assertTrue(IOptionalHighLight(folder).do_highlight())
        # The Folder type is still never highlighted by the tool
        self.assertFalse(gtool.highlightContent(folder))
        self.assertTrue(IOptionalHighLight(doc).do_highlight())
        self.assertTrue(gtool.highlightContent(doc))
        doc.getField('highlight').set(doc, NO)
        self.assertFalse(IOptionalHighLight(doc).do_highlight())
        self.assertFalse(gtool.highlightContent(doc))

    def testHighlightDocOnFolderOff(self):
        portal = self.layer['portal']
        gtool = getToolByName(portal, 'portal_glossary')
        setRoles(portal, TEST_USER_ID, ('Manager',))
        folder_id = portal.invokeFactory('Folder', 'folder')
        folder = portal[folder_id]
        doc_id = folder.invokeFactory('Document', 'doc')
        doc = folder[doc_id]
        folder.getField('highlight').set(folder, NO)
        self.assertFalse(IOptionalHighLight(folder).do_highlight())
        self.assertFalse(gtool.highlightContent(folder))
        self.assertFalse(IOptionalHighLight(doc).do_highlight())
        self.assertFalse(gtool.highlightContent(doc))
        doc.getField('highlight').set(doc, YES)
        self.assertTrue(IOptionalHighLight(doc).do_highlight())
        self.assertTrue(gtool.highlightContent(doc))
