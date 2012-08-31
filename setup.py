#!/usr/bin/python
import os
from distutils.core import setup

setup(
  name="django-hosttags",
  version="0.0.1",
  author="Dwight Hubbard",
  author_email="d@dhub.me",
  url="http://computing.dwighthubbard.info",
  license="LICENSE.txt",
  packages=["hosttags_project"],
  data_files=[('/usr/lib/hostlists/plugins',['hostlists_plugins/hosttags.py'])],
  long_description=open('README.txt').read(),
  description="A simple host database",
  requires=['sshmap','hostlists','django-piston','django-taggit'],
)
