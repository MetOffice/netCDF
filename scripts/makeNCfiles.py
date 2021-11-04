import copy
import glob
import os
import subprocess
import unittest

class TestNetCDFBuild(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestNetCDFBuild, self).__init__(*args, **kwargs)
        self.files = []


    def _build_file(self, infile):
        outfile = infile.replace('.cdl', '.nc')
        acall = ['ncgen', '-4', '-o', outfile, infile]
        try:
            subprocess.check_output(acall, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            raise ValueError(' '.join(acall) + '\n{}'.format(e.output))
        finally:
            if os.path.exists(outfile):
                self.files.append(outfile)

    def tearDown(self):
        for outfile in self.files:
            if os.path.exists(outfile):
                os.remove(outfile)


for f in glob.glob('**/*.cdl', recursive=True):
    def make_a_test(inf):
        infile = copy.copy(inf)
        outfile = f.replace('.cdl', '.nc')
        def test_ncgen(self):
            self._build_file(infile)
            self.assertTrue(os.path.exists(outfile),
                            msg='{} does not exist, ncgen failed'.format(outfile))
        return test_ncgen
    tname = 'test_{}'.format(f)
    setattr(TestNetCDFBuild, tname, make_a_test(f))


if __name__ == '__main__':
    unittest.main()
