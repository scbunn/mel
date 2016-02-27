#!/usr/bin/env python
"""Management script for MEL"""

import os
from app import create_app
from flask.ext.script import Manager

app = create_app(os.getenv('MEL_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def test():
    """Run unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
