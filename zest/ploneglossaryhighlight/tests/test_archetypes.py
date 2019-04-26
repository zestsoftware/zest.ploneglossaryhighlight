import unittest

from Products.CMFCore.utils import getToolByName
from Products.PloneGlossary.interfaces import IOptionalHighLight

from zest.ploneglossaryhighlight.adapters import YES, NO, PARENT
from zest.ploneglossaryhighlight.testing import (
    PLONEGLOSSARYHIGHLIGHT_NOT_INSTALLED_INTEGRATION_TESTING,
    PLONEGLOSSARYHIGHLIGHT_INTEGRATION_TESTING,
)


class BaseArchetypesTestCase(unittest.TestCase):

    layer = PLONEGLOSSARYHIGHLIGHT_NOT_INSTALLED_INTEGRATION_TESTING

    def add_one(self, context=None, portal_type="Document"):
        if context is None:
            context = self.layer["portal"]
        new_id = context.invokeFactory(portal_type, "some-id")
        return context[new_id]

    def get_tool(self):
        portal = self.layer["portal"]
        return getToolByName(portal, "portal_glossary")


class TestNormalGlossary(BaseArchetypesTestCase):
    def testHasNoField(self):
        doc = self.add_one()
        self.assertFalse(doc.getField("highlight"))

    def testHighlightDoc(self):
        doc = self.add_one()
        gtool = self.get_tool()
        self.assertTrue(gtool.highlightContent(doc))

    def testNoHighlightImage(self):
        image = self.add_one(portal_type="Image")
        gtool = self.get_tool()
        self.assertFalse(gtool.highlightContent(image))

    def testHighlightDocInFolder(self):
        folder = self.add_one(portal_type="Folder")
        doc = self.add_one(folder)
        gtool = self.get_tool()
        self.assertFalse(gtool.highlightContent(folder))
        self.assertTrue(gtool.highlightContent(doc))


class TestInstalled(BaseArchetypesTestCase):

    layer = PLONEGLOSSARYHIGHLIGHT_INTEGRATION_TESTING

    def testHasField(self):
        doc = self.add_one()
        self.assertTrue(doc.getField("highlight"))

    def testDefaultValue(self):
        doc = self.add_one()
        self.assertTrue(doc.getField("highlight").get(doc), PARENT)

    def testHighlightDoc(self):
        doc = self.add_one()
        gtool = self.get_tool()
        self.assertTrue(gtool.highlightContent(doc))

    def testNoHighlightImage(self):
        image = self.add_one(portal_type="Image")
        gtool = self.get_tool()
        self.assertFalse(gtool.highlightContent(image))

    def testHighlightDocOff(self):
        doc = self.add_one()
        gtool = self.get_tool()
        doc.getField("highlight").set(doc, NO)
        self.assertFalse(gtool.highlightContent(doc))

    def testHighlightBadValue(self):
        doc = self.add_one()
        gtool = self.get_tool()
        doc.getField("highlight").set(doc, "hello kitty")
        self.assertIsNone(IOptionalHighLight(doc).do_highlight())
        self.assertEqual(IOptionalHighLight(doc).do_highlight("foo"), "foo")
        # The tool will fall back to its own default.
        self.assertTrue(gtool.highlightContent(doc))
        gtool.highlight_content = False
        self.assertFalse(gtool.highlightContent(doc))

    def testHighlightDocOffFolderOn(self):
        gtool = self.get_tool()
        folder = self.add_one(portal_type="Folder")
        doc = self.add_one(folder)
        folder.getField("highlight").set(folder, YES)
        self.assertTrue(IOptionalHighLight(folder).do_highlight())
        # The Folder type is still never highlighted by the tool
        self.assertFalse(gtool.highlightContent(folder))
        self.assertTrue(IOptionalHighLight(doc).do_highlight())
        self.assertTrue(gtool.highlightContent(doc))
        doc.getField("highlight").set(doc, NO)
        self.assertFalse(IOptionalHighLight(doc).do_highlight())
        self.assertFalse(gtool.highlightContent(doc))

    def testHighlightDocOnFolderOff(self):
        gtool = self.get_tool()
        folder = self.add_one(portal_type="Folder")
        doc = self.add_one(folder)
        folder.getField("highlight").set(folder, NO)
        self.assertFalse(IOptionalHighLight(folder).do_highlight())
        self.assertFalse(gtool.highlightContent(folder))
        self.assertFalse(IOptionalHighLight(doc).do_highlight())
        self.assertFalse(gtool.highlightContent(doc))
        doc.getField("highlight").set(doc, YES)
        self.assertTrue(IOptionalHighLight(doc).do_highlight())
        self.assertTrue(gtool.highlightContent(doc))

    def testHighlightRootParent(self):
        gtool = self.get_tool()
        doc = self.add_one()
        doc.getField("highlight").set(doc, PARENT)
        self.assertIsNone(IOptionalHighLight(doc).do_highlight())
        self.assertEqual(IOptionalHighLight(doc).do_highlight("foo"), "foo")
        # Default of the tool is still true.
        self.assertTrue(gtool.highlightContent(doc))
        gtool.highlight_content = False
        self.assertFalse(gtool.highlightContent(doc))
