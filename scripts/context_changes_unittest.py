import unittest
import context_changes as context
import patchParser as parse

class TestContextChanges(unittest.TestCase:)

def test_subpatch(self) :
    patch_file = parse.PatchFile("../vulnerableforks/patches/CVE-2014-8172.patch")
    patch_file.getPatch()
    result = context.context_changes(patch_file.patches[0])
    self.assertTrue(result.status)


if __name__ == '__main__':
    unittest.main()