import unittest
import context_changes as context
import patchParser as parse

class TestContextChanges(unittest.TestCase):

    def test_patch_CVE_2014_8172(self):
        patch_file = parse.PatchFile("../patches/CVE-2014-8172.patch")
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
        self.assertFalse(result.status)

        # VERY GOOD FOR THE DEMO
        result = context.context_changes(patch_file.patches[9])
        print(result.messages)
        self.assertFalse(result.status)

        result = context.context_changes(patch_file.patches[10])
        self.assertFalse(result.status)

    def test_patch_CVE_2015_0572(self):
        patch_file = parse.PatchFile("../patches/CVE-2015-0572.patch")
        patch_file.getPatch()

        # TODO: check this patch, odd behaviour
        result = context.context_changes(patch_file.patches[0])
        self.assertFalse(result.status)

        result = context.context_changes(patch_file.patches[1])
        self.assertFalse(result.status)

        result = context.context_changes(patch_file.patches[2])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[3])
        print(result.messages)
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[4])
        self.assertFalse(result.status)

        result = context.context_changes(patch_file.patches[5])
        self.assertTrue(result.status)
        
        result = context.context_changes(patch_file.patches[6])
        self.assertTrue(result.status)
    
        result = context.context_changes(patch_file.patches[7])
        self.assertTrue(result.status)

        result = context.context_changes(patch_file.patches[8])
        self.assertTrue(result.status)







        
















        
if __name__ == '__main__':
    unittest.main()