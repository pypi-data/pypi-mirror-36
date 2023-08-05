
# -*- coding: utf-8 -*-

# Base class and functions for PyGeodesy tests.

# After (C) Chris Veness 2011-2015 published under the same MIT Licence,
# see <http://www.Movable-Type.co.UK/scripts/latlong-vectors.html>
# and <http://www.Movable-Type.co.UK/scripts/latlong.html>.

from inspect import isclass, isfunction, ismethod, ismodule
from os.path import abspath, basename, dirname
from platform import architecture, java_ver, mac_ver, win32_ver, uname
import sys
from time import time

try:
    import geographiclib
except ImportError:
    geographiclib = None
try:
    import numpy
except ImportError:
    numpy = None

PyGeodesy_dir = dirname(dirname(abspath(__file__)))
# extend sys.path to include the ../.. directory
if PyGeodesy_dir not in sys.path:  # Python 3+ ModuleNotFoundError
    sys.path.insert(0, PyGeodesy_dir)

from pygeodesy import version as PyGeodesy_version, \
                      iterNumpy2over, normDMS  # PYCHOK expected

__all__ = ('geographiclib', 'numpy',  # constants
           'isIntelPython', 'isiOS', 'isNix', 'isPyPy',
           'isPython2', 'isPython3', 'isWindows',
           'PyGeodesy_dir', 'Python_O',
           'TestsBase',  # classes
           'ios_ver', 'runner', 'secs2str',  # functions
           'tilde', 'type2str', 'versions')
__version__ = '18.09.14'

try:
    _Ints = int, long
    _Strs = basestring
except NameError:  # Python 3+
    _Ints = int
    _Strs = str

_os_bitstr = architecture()[0]
_pseudo_home_dir = dirname(PyGeodesy_dir or '~') or '~'

Python_O = sys.executable  # python or Pythonista path

isIntelPython = 'intelpython' in Python_O
# isiOS is used by some tests known to fail on iOS only
isiOS         = sys.platform == 'ios'  # public
isNix         = uname()[0] in ('Linux', 'linux')
isPyPy        = 'PyPy ' in sys.version  # public
isPython2     = sys.version_info[0] == 2
isPython3     = sys.version_info[0] == 3
isWindows     = sys.platform.startswith('win')

try:
    # use distro only for Linux, not macOS, etc.
    if isNix:
        import distro  # <http://PyPI.org/project/distro>
    else:
        raise ImportError

    def _2str(ustr):
        s = u = str(ustr).strip()
        for c in u:
            if not (c.isalnum() or c in '._-'):
                s = s.replace(c, ' ')
        return '_'.join(s.strip().split())

    _Nix = _2str(distro.id()).capitalize()  # .name()?

    def nix_ver():  # *nix release
        return _2str(distro.version()), _os_bitstr

except ImportError:
    _Nix = ''  # not linux?

    def nix_ver():  # PYCHOK expected
        return _Nix, _os_bitstr


class TestsBase(object):
    '''Tests based on @examples from the original JavaScript code
       and examples in <http://www.EdWilliams.org/avform.htm> or
       elsewhere as indicated.
    '''
    _file     = ''
    _name     = ''
    _iterisk  = ''
    _prefix   = '    '
    _time     = 0
    _verbose  = True  # print all tests, otherwise failures only
    _versions = ''  # cached versions() string

    failed  = 0
    known   = 0
    skipped = 0
    total   = 0

    def __init__(self, testfile, version, module=None, verbose=True):
        if not self._versions:  # get versions once
            TestsBase._versions = versions()
        self._file = testfile
        self._name = basename(testfile)
        self.title(self._name, version, module=module)
        self._time = time()
        self._verbose = verbose

    def errors(self):
        '''Return the number of tests failures,
           excluding the KNOWN failures.
        '''
        return self.failed - self.known  # new failures

    def exit(self, errors=0):
        '''Exit with the number of test failures as exist status.
        '''
        sys.exit(min(errors + self.errors(), 99))

    def iterNumpy2over(self, n=None):
        '''Set the I{iterNumpy2} threshold.

           @keyword n: Optional, new threshold value (integer).

           @return: Previous threshold (integer).
        '''
        p = iterNumpy2over(n)
        self.test('iterNumpy2over', iterNumpy2over(), n)
        return p

    def printf(self, fmt, *args, **kwds):  # nl=0, nt=0
        '''Print a formatted line to sys.stdout.
        '''
        nl = '\n' * kwds.get('nl', 0)
        nt = '\n' * kwds.get('nt', 0)
        print(''.join((nl, self._prefix, (fmt % args), nt)))

    def results(self, passed='passed', nl=1):
        '''Summarize the test results.
        '''
        s = time() - self._time
        r = passed
        t = self.total
        n = self.failed
        if n:
            k = self.known or ''
            if k:
                if k == n:
                    k = ', KNOWN' if k == 1 else (
                        ', BOTH KNOWN' if k == 2 else
                        ', ALL KNOWN')
                else:
                    k = ', incl. %s KNOWN' % (k,)
            r = '(%.1f%%) FAILED%s' % (100.0 * n / t, k)
            n = '%s of %d' % (n, t)
        elif t:
            n = 'all %d' % (t,)
        else:
            n = 'all'
        k = self.skipped or ''
        if k:
            k = ', %d skipped' % (k,)
        r = '%s%s (%s) %s' % (r, k, self._versions, secs2str(s))
        self.printf('%s %s tests %s', n, self._name, r, nl=nl)

    def skip(self, text=''):
        '''Skip this test, leave a message.
        '''
        self.skipped += 1
        if text and self._verbose:
            self.printf('test skipped (%d): %s', self.skipped, text)

    def subtitle(self, module, testing='ing', **kwds):
        '''Print the subtitle of a test suite.
        '''
        t = (basename(module.__name__), module.__version__) + \
             tuple('%s=%s' % t for t in sorted(kwds.items()))
        self.printf('test%s(%s)', testing, ', '.join(t), nl=1)

    def test(self, name, value, expect, fmt='%s', known=False, nt=0):
        '''Compare a test value with the expected one.
        '''
        if self._iterisk:
            name += self._iterisk

        if not isinstance(expect, _Strs):
            expect = fmt % (expect,)  # expect as str

        f, v = '', fmt % (value,)  # value as str
        if v != expect and v != normDMS(expect):
            self.failed += 1  # failures
            if known:  # failed before
                self.known += 1
                f = ', KNOWN'
            f = '  FAILED%s, expected %s' % (f, expect)

        self.total += 1  # tests
        if f or self._verbose:
            self.printf('test %d %s: %s%s', self.total, name, v, f, nt=nt)

    def test__(self, fmt, *args, **kwds):
        '''Print subtotal test line.
        '''
        t = '-' * len(str(self.total))
        self.printf('test %s %s', t, (fmt % args), **kwds)

    def testiter(self):
        '''Test with/-out I{iterNumpy2} threshold.
        '''
        yield iterNumpy2over(100000)
        self._iterisk = '*'
        yield iterNumpy2over(1)
        self._iterisk = ''

    def title(self, test, version, module=None):
        '''Print the title of the test suite.
        '''
        if module:
            m = ' (module %s %s)' % (basename(module.__name__),
                                     module.__version__)
        else:
            m = ''
        self.printf('testing %s %s%s', test, version, m, nl=1)


if isiOS:  # MCCABE 13

    def ios_ver(**unused):
        '''Get the iOS version information.
        '''
        t = mac_ver()
        # append 'machine' iPad, iPhone to 'release'
        r = t[0] + ' ' + t[2].split(',')[0]
        return (r,) + t[1:]

    try:  # prefer StringIO over io
        from StringIO import StringIO
    except ImportError:  # Python 3+
        from io import StringIO
    from runpy import run_path
    from traceback import format_exception

    def runner(test):
        '''Invoke one test module and return
           the exit status and console output.
        '''
        # Mimick partial behavior of function runner
        # further below because subprocess.Popen is
        # not available on iOS/Pythonista/Python.
        # One issue however, the test script is
        # imported and run in the same process.

        x = None  # no exit, no exception

        sys3 = sys.argv, sys.stdout, sys.stderr
        sys.stdout = sys.stderr = std = StringIO()
        try:
            sys.argv = [test]
            run_path(test, run_name='__main__')
        except:  # PYCHOK have to on Pythonista
            x = sys.exc_info()
            if x[0] is SystemExit:
                x = x[1].code  # exit status
            else:  # append traceback
                x = [t for t in format_exception(*x)
                             if 'runpy.py", line' not in t]
                print(''.join(map(tilde, x)).rstrip())
                x = 1  # count as a failure
        sys.argv, sys.stdout, sys.stderr = sys3

        r = std.getvalue()
        if isinstance(r, bytes):  # Python 3+
            r = r.decode('utf-8')

        std.close()
        std = None  # del std

        if x is None:  # no exit status or exception:
            # count failed tests excluding KNOWN ones
            x = r.count('FAILED, expected')
        return x, r

    Python_O = basename(Python_O)

else:  # non-iOS

    def ios_ver(**unused):  # PYCHOK expected
        '''Get the iOS version information.
        '''
        return ('', ('', '', ''), '')

    from subprocess import PIPE, STDOUT, Popen

    if not __debug__:
        Python_O += ' -O'  # optimized

    def runner(test):  # PYCHOK expected
        '''Invoke one test module and return
           the exit status and console output.
        '''
        c = Python_O.split() + [test]
        p = Popen(c, creationflags=0,
                     executable   =sys.executable,
                   # shell        =True,
                     stdin        =None,
                     stdout       =PIPE,  # XXX
                     stderr       =STDOUT)  # XXX

        r = p.communicate()[0]
        if isinstance(r, bytes):  # Python 3+
            r = r.decode('utf-8')

        # the exit status reflects the number of
        # test failures in the tested module
        return p.returncode, r


def secs2str(secs):
    '''Convert a time value to string.
    '''
    unit = ['sec', 'ms', 'us', 'ps']
    while secs < 1 and len(unit) > 1:
        secs *= 1000.0
        unit.pop(0)
    return '%.3f %s' % (secs, unit[0])


def tilde(path):
    '''Return a shortened path, especially Pythonista.
    '''
    return path.replace(_pseudo_home_dir, '~')


def type2str(obj, attr):
    '''Return the type name of an object attribute.
    '''
    t = getattr(obj, attr, None)
    if isclass(t):
        t = '() class'
    elif isinstance(t, float):
        t = ' float'
    elif ismethod(t):
        t = '() method'
    elif isfunction(t):
        if isclass(obj):
            t = '() method'
        else:
            t = '() function'
    elif isinstance(t, _Ints):
        t = ' int'
    elif ismodule(t):
        t = ' module'
    elif type(t) is property:
        t = ' property'
    elif isinstance(t, _Strs):
        t = ' str'
    else:
        t = str(type(t)).replace("'", '')
        if t.startswith('<') and t.endswith('>'):
            t = ' ' + t[1:-1]
        else:
            t = ' attribute'
    return t


def versions():
    '''Get pygeodesy, Python versions, size, OS name and release.
    '''
    t = 'Intel-' if isIntelPython else 'PyPy-' if isPyPy else ''
    vs = 'PyGeodesy', PyGeodesy_version, (t +
         'Python'), sys.version.split()[0], _os_bitstr
    if geographiclib:
        vs += 'geographiclib', geographiclib.__version__
    if numpy:
        vs += 'numpy', numpy.__version__

    # - mac_ver() returns ('10.12.5', ..., 'x86_64') on
    #   macOS and ('10.3.3', ..., 'iPad4,2') on iOS
    # - win32_ver is ('XP', ..., 'SP3', ...) on Windows XP SP3
    # - platform() returns 'Darwin-16.6.0-x86_64-i386-64bit'
    #   on macOS and 'Darwin-16.6.0-iPad4,2-64bit' on iOS
    # - sys.platform is 'darwin' on macOS, 'ios' on iOS,
    #   'win32' on Windows and 'cygwin' on Windows/Gygwin
    # - distro.id() and .name() return 'Darwin' on macOS
    for t, r in (('iOS',     ios_ver),
                 ('macOS',   mac_ver),
                 ('Windows', win32_ver),
                 (_Nix,      nix_ver),
                 ('Java',    java_ver),
                 ('uname',   uname)):
        r = r()[0]
        if r:
            vs += t, r
            break

    return ' '.join(vs)
