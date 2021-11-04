import copy
import glob
import os
import subprocess
import unittest

class TestNetCDFBuild(unittest.TestCase):
    def _build_file(infile):
        outfile = infile.replace('.cdl', '.nc')
        acall = ['ncgen', '-4', '-o', outfile, infile]
        print(' '.join(acall))
        subprocess.check_call(acall)

for f in glob.glob('**/*.cdl', recursive=True):
    def make_a_test(inf):
        infile = copy.copy(inf)
        outfile = f.replace('.cdl', '.nc')
        def test_ncgen(self):
            self._build_file
            self.assertTrue(os.path.exists(outfile),
                            msg='{} does not exist, ncgen failed'.format(outfile))
        return test_ncgen
    tname = 'test_{}'.format(f)
    setattr(TestNetCDFBuild, tname, make_a_test(f))


if __name__ == '__main__':
    unittest.main()
