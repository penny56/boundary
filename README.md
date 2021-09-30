# Regression-27

This repository derived from Regression-V1, adapted for Python 2.7, removed the HTMLTestRunner and add a wrapper to make it suit for command line.

This script deployed in rhel/YJ-rhel7-vm:/root/git/regression27, just enter the repo directory and 'git pull' to get the latest code.


## Installation

### Issues

#### ImportError: No module named pbr.version

    [yj@liwbj regression27]$ ./regWrapper-R41.sh hmc1-t90.cfg
    Traceback (most recent call last):
      File "./src/regression_R41.py", line 9, in <module>
        from testCaseCollection import testCaseCollection
      File "/home/yj/git/regression27/src/testCaseCollection.py", line 15, in <module>
        from dpm import dpm
      File "/home/yj/git/regression27/src/dpm.py", line 8, in <module>
        import zhmcclient
      File "/home/yj/git/regression27/src/zhmcclient/__init__.py", line 24, in <module>
        from ._version import *       # noqa: F401
      File "/home/yj/git/regression27/src/zhmcclient/_version.py", line 23, in <module>
        import pbr.version
    ImportError: No module named pbr.version

#### Fix

    [yj@liwbj regression27]$ sudo pip install pbr --ignore-installed

#### ImportError: No module named stomp

    [yj@liwbj regression27]$ ./regWrapper-R41.sh hmc1-t90.cfg
    Traceback (most recent call last):
      File "./src/regression_R41.py", line 9, in <module>
        from testCaseCollection import testCaseCollection
      File "/home/yj/git/regression27/src/testCaseCollection.py", line 15, in <module>
        from dpm import dpm
      File "/home/yj/git/regression27/src/dpm.py", line 8, in <module>
        import zhmcclient
      File "/home/yj/git/regression27/src/zhmcclient/__init__.py", line 43, in <module>
        from ._notification import *  # noqa: F401
      File "/home/yj/git/regression27/src/zhmcclient/_notification.py", line 69, in <module>
        import stomp
    ImportError: No module named stomp

#### Fix

    [yj@liwbj regression27]$ pip install stomp.py

