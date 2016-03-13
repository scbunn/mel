#!/usr/bin/env python
"""Management script for MEL"""

import os
import sys
from app import create_app
from flask.ext.script import Manager

app = create_app(os.getenv('MEL_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def test():
    """Run unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    successfull = unittest.TextTestRunner(
        verbosity=2).run(tests).wasSuccessful()
    if successfull:
        sys.exit(0)
    else:
        sys.exit(1)



if __name__ == "__main__":
    manager.run()
