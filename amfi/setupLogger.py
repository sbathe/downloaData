#!/usr/bin/env python
import sys
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.DEBUG,
                     handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)