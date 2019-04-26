import unittest

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.PloneGlossary.interfaces import IOptionalHighLight

from zest.ploneglossaryhighlight.adapters import YES, NO, PARENT
from zest.ploneglossaryhighlight.testing import (
    PLONEGLOSSARYHIGHLIGHT_DEXTERITY_INTEGRATION_TESTING,
)


class BaseDexterityTestCase(unittest.TestCase):

    layer = PLONEGLOSSARYHIGHLIGHT_DEXTERITY_INTEGRATION_TESTING

    def _add_one(self, context=None, enabled=True, portal_type=None):
        if context is None:
            context = self.layer["portal"]
        if portal_type is None:
            if enabled:
                portal_type = "enabledtype"
            else:
                portal_type = "disabledtype"
        new_id = context.invokeFactory(portal_type, "some-id")
        return context[new_id]

    def get_tool(self):
        portal = self.layer["portal"]
        return getToolByName(portal, "portal_glossary")


class TestDexterityBehaviorDisabled(BaseDexterityTestCase):
    def add_one(self, context=None, enabled=False, portal_type=None):
        return self._add_one(context=context, enabled=enabled, portal_type=portal_type)

    def testHasNoField(self):
        folder = self.add_one()
        self.assertFalse(base_hasattr(folder, "highlight"))

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


class TestDexterityBehaviorEnabled(BaseDexterityTestCase):
    def add_one(self, context=None, enabled=True, portal_type=None):
        return self._add_one(context=context, enabled=enabled, portal_type=portal_type)

    def testHasField(self):
        folder = self.add_one()
        self.assertTrue(base_hasattr(folder, "highlight"))

    def testDefaultValue(self):
        folder = self.add_one()
        self.assertEqual(folder.highlight, PARENT)

    def testHighlightDoc(self):
        doc = self.add_one()
        gtool = self.get_tool()
        self.assertTrue(gtool.highlightContent(doc))

    def testHighlightDocOff(self):
        doc = self.add_one()
        gtool = self.get_tool()
        doc.highlight = NO
        self.assertFalse(gtool.highlightContent(doc))

    def testHighlightBadValue(self):
        doc = self.add_one()
        gtool = self.get_tool()
        doc.highlight = "hello kitty"
        self.assertIsNone(IOptionalHighLight(doc).do_highlight())
        self.assertEqual(IOptionalHighLight(doc).do_highlight("foo"), "foo")
        # The tool will fall back to its own default.
        self.assertTrue(gtool.highlightContent(doc))
        gtool.highlight_content = False
        self.assertFalse(gtool.highlightContent(doc))

    def testHighlightDocOffFolderOn(self):
        gtool = self.get_tool()
        folder = self.add_one()
        doc = self.add_one(folder)
        folder.highlight = YES
        self.assertTrue(IOptionalHighLight(folder).do_highlight())
        self.assertTrue(gtool.highlightContent(folder))
        self.assertTrue(IOptionalHighLight(doc).do_highlight())
        self.assertTrue(gtool.highlightContent(doc))
        doc.highlight = NO
        self.assertFalse(IOptionalHighLight(doc).do_highlight())
        self.assertFalse(gtool.highlightContent(doc))

    def testHighlightDocOnFolderOff(self):
        gtool = self.get_tool()
        folder = self.add_one()
        doc = self.add_one(folder)
        folder.highlight = NO
        self.assertFalse(IOptionalHighLight(folder).do_highlight())
        self.assertFalse(gtool.highlightContent(folder))
        self.assertFalse(IOptionalHighLight(doc).do_highlight())
        self.assertFalse(gtool.highlightContent(doc))
        doc.highlight = YES
        self.assertTrue(IOptionalHighLight(doc).do_highlight())
        self.assertTrue(gtool.highlightContent(doc))

    def testHighlightRootParent(self):
        gtool = self.get_tool()
        doc = self.add_one()
        doc.highlight = PARENT
        self.assertIsNone(IOptionalHighLight(doc).do_highlight())
        self.assertEqual(IOptionalHighLight(doc).do_highlight("foo"), "foo")
        # Default of the tool is still true.
        self.assertTrue(gtool.highlightContent(doc))
        gtool.highlight_content = False
        self.assertFalse(gtool.highlightContent(doc))
