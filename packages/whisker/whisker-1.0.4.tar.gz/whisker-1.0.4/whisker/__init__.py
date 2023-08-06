#!/usr/bin/env/python
# whisker/__init__.py

"""
===============================================================================

    Copyright (C) 2011-2018 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of the Whisker Python client library.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

===============================================================================
"""

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# http://eric.themoritzfamily.com/learning-python-logging.html
# http://stackoverflow.com/questions/12296214/python-logging-with-a-library-namespaced-packages  # noqa
