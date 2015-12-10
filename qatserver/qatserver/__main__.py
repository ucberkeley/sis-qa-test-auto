#!/usr/bin/env python3

import os

from tornado.ioloop import IOLoop
from tornado.web import Application

from .server import TestsExecsListHandler, ExecuteHandler, StatusHandler
from .executor import TestExecResultsManager, TestsExecutor
from . import TEST_DIR

__author__ = "Dibyo Majumdar"
__email__ = "dibyo.majumdar@gmail.com"


if __name__ == '__main__':
    import sys
    port = sys.argv[1] if len(sys.argv) >= 2 else 8421

    os.chdir(TEST_DIR)

    with TestExecResultsManager() as manager:
        with TestsExecutor(results_manager=manager) as executor:
            init_kwargs = dict(executor=executor)
            app = Application([
                (r'/', TestsExecsListHandler, init_kwargs),
                (r'/execute', ExecuteHandler, init_kwargs),
                (r'/status/(.*)', StatusHandler, init_kwargs)
            ])
            app.listen(port)
            print('Server ready!')
            IOLoop.current().start()
