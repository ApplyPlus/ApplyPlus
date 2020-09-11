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
        patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2014-8172.patch")
        patch_file.getPatch()

        result = context.context_changes(patch_file.patches[0])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[1])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[2])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[3])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[4])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[5])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[6])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[7])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[8])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[9])
        # print(result.messages)
        self.assertFalse(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[10])
        self.assertFalse(result.status)
        self.assertFalse(result.is_comment)

    def test_patch_CVE_2015_0572(self):
        patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2015-0572.patch")
        patch_file.getPatch()

        result = context.context_changes(patch_file.patches[0])
        self.assertFalse(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[1])
        self.assertFalse(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[2])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[3])
        # print(result.messages)
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[4])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[5])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[6])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[7])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[8])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

    def test_patch_CVE_2012_2390(self):
        patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2012-2390.patch")
        patch_file.getPatch()

        result = context.context_changes(patch_file.patches[0])
        self.assertFalse(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[1])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[2])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[3])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[4])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

    def test_patch_CVE_2015_8845(self):
        patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2015-8845.patch")
        patch_file.getPatch()

        result = context.context_changes(patch_file.patches[0])
        self.assertFalse(result.status)
        self.assertFalse(result.is_comment)

    def test_patch_CVE_2013_7348(self):
        patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2013-7348.patch")
        patch_file.getPatch()

        result = context.context_changes(patch_file.patches[0])
        self.assertFalse(result.status)
        self.assertFalse(result.is_comment)

    def test_patch_CVE_2013_7281(self):
        patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2013-7281.patch")
        patch_file.getPatch()

        # Patch has already been applied
        result = context.context_changes(patch_file.patches[0])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # No context changes
        result = context.context_changes(patch_file.patches[1])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # No context changes
        result = context.context_changes(patch_file.patches[2])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Context has changed a little
        result = context.context_changes(patch_file.patches[3])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Context has changed a little
        result = context.context_changes(patch_file.patches[4])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[5])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[6])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)
        
        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[7])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[8])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[9])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[10])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[11])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[12])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[13])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[14])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[15])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)
        
        result = context.context_changes(patch_file.patches[16])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)
    
    def test_patch_CVE_2014_8481(self):
        patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2014-8481.patch")
        patch_file.getPatch()

        # Look into why it fails!
        result = context.context_changes(patch_file.patches[0])
        print(result.messages)
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

    def test_patch_CVE_2014_9710(self):
        patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2014-9710.patch")
        patch_file.getPatch()

        # Subpatch has been applied - look into why it fails!
        result = context.context_changes(patch_file.patches[0])
        print(result.messages)
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[1])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[2])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[3])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[4])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[5])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[6])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[7])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

    def test_patch_CVE_2014_9644(self):
        patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2014-9644.patch")
        patch_file.getPatch()

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[0])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[1])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[2])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[3])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[4])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[5])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[5])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[6])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[7])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[8])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[9])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Subpatch has been applied
        result = context.context_changes(patch_file.patches[10])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

       # Subpatch has been applied
        result = context.context_changes(patch_file.patches[11])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

       # Subpatch has been applied
        result = context.context_changes(patch_file.patches[12])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

       # Subpatch has been applied
        result = context.context_changes(patch_file.patches[13])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

       # Subpatch has been applied
        result = context.context_changes(patch_file.patches[14])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

       # Subpatch has been applied
        result = context.context_changes(patch_file.patches[15])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

       # Subpatch has been applied
        result = context.context_changes(patch_file.patches[16])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

       # This file has been deleted.
       # result = context.context_changes(patch_file.patches[17])
       # self.assertTrue(result.status)

       # Subpatch has been applied
        result = context.context_changes(patch_file.patches[18])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

       # Subpatch has been applied
        result = context.context_changes(patch_file.patches[19])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

       # Subpatch has been applied
        result = context.context_changes(patch_file.patches[20])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

       # Subpatch has been applied
        result = context.context_changes(patch_file.patches[21])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

       # Subpatch has been applied
        result = context.context_changes(patch_file.patches[22])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

       # Subpatch has been applied
        result = context.context_changes(patch_file.patches[23])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

    def test_patch_CVE_2015_3212(self):
        patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2015-3212.patch")
        patch_file.getPatch()

        result = context.context_changes(patch_file.patches[0])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[1])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[2])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[3])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[4])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[5])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Function name was changed
        result = context.context_changes(patch_file.patches[6])
        # print(result.messages)
        self.assertFalse(result.status)
        self.assertFalse(result.is_comment)

        result = context.context_changes(patch_file.patches[7])
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Something was probably added in the middle and the line scope changed. Try to expand the search.
        result = context.context_changes(patch_file.patches[8], True)
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

        # Something was probably added in the middle and the line scope changed. Try to expand the search.
        result = context.context_changes(patch_file.patches[9], True)
        self.assertTrue(result.status)
        self.assertFalse(result.is_comment)

if __name__ == "__main__":
    unittest.main()
