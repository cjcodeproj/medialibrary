#!/usr/bin/env python

#
# Copyright 2024 Chris Josephes
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
List out all movies (or a random sample of all movies),
one entry per line.
"""

# pylint: disable=R0801

from media.fileops.filenames import FilenameMatches
from media.fileops.repo import Repo
from media.tools.movies.common import (
                                       Controller,
                                       MovieReport)


def main_cli():
    '''
    Entry point for script.

    Steps:
      1. Argument parsing/environment setup
      2. Repository loading
      3. Batch processing
      4. Listing
    '''
    controller = Controller()
    controller.setup()

    repo = Repo(controller.mediapath)
    repo.scan()
    repo.load(FilenameMatches.All_Media)
    movies = repo.get_movies()
    movie_report = MovieReport()
    movie_report.set_movies(movies)
    movie_report.params_from_controller(controller)
    print(movie_report.report())


if __name__ == '__main__':
    main_cli()
