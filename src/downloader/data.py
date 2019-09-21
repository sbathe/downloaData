#!/usr/bin/env python
import sys

class data:
    def __init__(self):
        pass
    def fetch(self, institution):
        '''fetch the data for the institution
        @param: institution, for now, only amfi
        This method is supposed to be overridden by the child class
        for given institution'''
        try:
            from downloader import 