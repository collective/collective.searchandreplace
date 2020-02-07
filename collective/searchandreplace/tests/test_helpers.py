import unittest


class TestFormHelpers(unittest.TestCase):
    """Test some helper methods from the utility."""

    def test_parseItems(self):
        from collective.searchandreplace.browser.searchreplaceform import parseItems

        # parseItems parses lines of format 'line:pos:path'.  line is title or
        # description or fieldname plus space plus line number.
        items = [
            "title:0:path1",
            "text 2:10:path2",
            "description 1:4:path1",
            "description 1:42:path1",
            "new 1:7:path2",
            "new 4:63:path2",
        ]
        result = parseItems(items)
        self.assertEqual(len(result), 2)
        self.assertTrue("path1" in result)
        self.assertTrue("path2" in result)
        self.assertTrue("title" in result["path1"])
        self.assertTrue("description" in result["path1"])
        self.assertTrue("text" in result["path2"])
        self.assertTrue("new" in result["path2"])
        self.assertEqual(result["path1"]["title"], [0])
        self.assertEqual(result["path1"]["description"], [4, 42])
        self.assertEqual(result["path2"]["text"], [10])
        self.assertEqual(result["path2"]["new"], [7, 63])

    def test_parseItems_broken(self):
        from collective.searchandreplace.browser.searchreplaceform import parseItems

        # We ignore broken instructions.
        items = [
            "title:0:path1",
            "too many spaces 2:10:path2",
            "okay 1:4:path3",
            "more:than:2:colons",
            "not:enoughcolons",
            "bad_position:a:path6",
            "no_space:63:path7",
            "okay_again 20:3000:path8",
        ]
        result = parseItems(items)
        # paths with broken instructions may end up in the result, but the
        # instructions will be empty.
        self.assertTrue(result)
        self.assertEqual(result.get("path1"), {"title": [0]})
        self.assertFalse(result.get("path2"))
        self.assertEqual(result.get("path3"), {"okay": [4]})
        self.assertFalse(result.get("colons"))
        self.assertFalse(result.get("enoughcolons"))
        self.assertFalse(result.get("path6"))
        self.assertFalse(result.get("path7"))
        self.assertEqual(result.get("path8"), {"okay_again": [3000]})
