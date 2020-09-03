import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "."))
import scripts.patch_context.context_changes as context
import scripts.patch_apply.patchParser as parse


class TestContextChanges(unittest.TestCase):
    """
    TestContextChanges contains tests for patches
    the name of the tests describe which patch is
    being tests

    ex: test_patch_CVE_2014_8172 has tests for the
    CVE-2014-8172 patch
    """

    def test_patch_CVE_2014_8172(self):
        # patch_file = parse.PatchFile("..vulnerableforks/patches/CVE-2014-8172.patch")
        patch_file = parse.PatchFile("/Users/yuvika/Desktop/URA/vulnerableforks/patches/CVE-2014-8172.patch")
        patch_file.getPatch()

        result = context.context_changes(patch_file.patches[0])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[1])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[2])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[3])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[4])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[5])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[6])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[7])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[8])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[9])
        print(result.messages)
        self.assertFalse(result.status)

        result = context.context_changes(patch_file.patches[10])
        self.assertFalse(result.status)

    def test_patch_CVE_2015_0572(self):
        # patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2014-8172.patch")
        patch_file = parse.PatchFile("/Users/yuvika/Desktop/URA/vulnerableforks/patches/CVE-2014-8172.patch")
        patch_file.getPatch()

        result = context.context_changes(patch_file.patches[0])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[1])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[2])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[3])
        print(result.messages)
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[4])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[5])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[6])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[7])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[8])
        self.assertTrue(result.status)

    def test_patch_CVE_2012_2390(self):
        # patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2012-2390.patch")
        patch_file = parse.PatchFile("/Users/yuvika/Desktop/URA/vulnerableforks/patches/CVE-2012-2390.patch")
        patch_file.getPatch()

        result = context.context_changes(patch_file.patches[0])
        self.assertFalse(result.status)

        result = context.context_changes(patch_file.patches[1])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[2])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[3])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[4])
        self.assertTrue(result.status)

    def test_patch_CVE_2015_8845(self):
        # patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2015-8845.patch")
        patch_file = parse.PatchFile("/Users/yuvika/Desktop/URA/vulnerableforks/patches/CVE-2015-8845.patch")
        patch_file.getPatch()

        result = context.context_changes(patch_file.patches[0])
        self.assertFalse(result.status)


if __name__ == "__main__":
    unittest.main()
