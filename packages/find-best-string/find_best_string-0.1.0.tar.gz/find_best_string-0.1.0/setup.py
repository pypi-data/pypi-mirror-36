#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Setup documentation:
# https://setuptools.readthedocs.io/en/latest/setuptools.html
#
from __future__ import absolute_import
from __future__ import print_function
from glob import glob
from setuptools import setup, find_packages
from os.path import abspath, basename, dirname, join, splitext
import re

HERE = abspath(dirname(__file__))
NAME = basename(HERE)


def read(*parts):
    with open(join(HERE, *parts), "r", encoding="utf-8") as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    # This is the name of your project. The first time you publish this
    # package, this name will be registered for you. It will determine how
    # users can install this project, e.g.:
    #
    # $ pip install sampleproject
    #
    # And where it will live on PyPI: https://pypi.org/project/sampleproject/
    #
    # There are some restrictions on what makes a valid project name
    # specification here:
    # https://packaging.python.org/specifications/core-metadata/#name
    #
    # Required
    name=NAME,

    # Versions should comply with PEP 440:
    # https://www.python.org/dev/peps/pep-0440/
    #
    # For a discussion on single-sourcing the version across setup.py and the
    # project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    #
    # Required
    version=find_version("src", NAME, "__init__.py"),

    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    #
    # Required
    description="Finds the best matching string in a larger string.",

    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    #
    # Often, this is the same as your README, so you can just read it in from
    # that file directly (as we have already done above)
    #
    # This field corresponds to the "Description" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    #
    # Optional
    long_description=read("README.md"),

    # Denotes that our long_description is in Markdown; valid values are
    # text/plain, text/x-rst, and text/markdown
    #
    # Optional if long_description is written in reStructuredText (rst) but
    # required for plain-text or Markdown; if unspecified, "applications should
    # attempt to render [the long_description] as text/x-rst; charset=UTF-8 and
    # fall back to text/plain if it is not valid rst" (see link below)
    #
    # This field corresponds to the "Description-Content-Type" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    #
    # Optional (see note above)
    long_description_content_type="text/markdown",

    # This should be a valid link to your project"s main homepage.
    #
    # This field corresponds to the "Home-Page" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#home-page-optional
    #
    # Optional
    url="https://github.com/alexseitsinger/{}".format(NAME),

    # This should be your name or the name of the organization which owns the
    # project.
    #
    # Optional
    author="Alex Seitsinger",

    # This should be a valid email address corresponding to the author listed
    # above.
    #
    # Optional
    author_email="alexseitsinger@gmail.com",

    # Classifiers help users find your project by categorizing it.
    #
    # classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    #
    # Optional
    classifiers=[
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",
        # "Environment :: Console",
        # "Environment :: Console :: Curses",
        # "Environment :: Console :: Framebuffer",
        # "Environment :: Console :: Newt",
        # "Environment :: Console :: svgalib",
        # "Environment :: Handhelds/PDA's",
        # "Environment :: MacOS X",
        # "Environment :: MacOS X :: Aqua",
        # "Environment :: MacOS X :: Carbon",
        # "Environment :: MacOS X :: Cocoa",
        # "Environment :: No Input/Output (Daemon)",
        # "Environment :: OpenStack",
        # "Environment :: Other Environment",
        # "Environment :: Plugins",
        # "Environment :: Web Environment",
        # "Environment :: Web Environment :: Buffet",
        # "Environment :: Web Environment :: Mozilla",
        # "Environment :: Web Environment :: ToscaWidgets",
        # "Environment :: Win32 (MS Windows)",
        # "Environment :: X11 Applications",
        # "Environment :: X11 Applications :: Gnome",
        # "Environment :: X11 Applications :: GTK",
        # "Environment :: X11 Applications :: KDE",
        # "Environment :: X11 Applications :: Qt",
        # "Framework :: AsyncIO",
        # "Framework :: BFG",
        # "Framework :: Bob",
        # "Framework :: Bottle",
        # "Framework :: Buildout",
        # "Framework :: Buildout :: Extension",
        # "Framework :: Buildout :: Recipe",
        # "Framework :: CastleCMS",
        # "Framework :: CastleCMS :: Theme",
        # "Framework :: Chandler",
        # "Framework :: CherryPy",
        # "Framework :: CubicWeb",
        # "Framework :: Django",
        # "Framework :: Django :: 1.10",
        # "Framework :: Django :: 1.11",
        # "Framework :: Django :: 1.4",
        # "Framework :: Django :: 1.5",
        # "Framework :: Django :: 1.6",
        # "Framework :: Django :: 1.7",
        # "Framework :: Django :: 1.8",
        # "Framework :: Django :: 1.9",
        # "Framework :: Django :: 2.0",
        # "Framework :: Django :: 2.1",
        # "Framework :: Flake8",
        # "Framework :: Flask",
        # "Framework :: IDLE",
        # "Framework :: IPython",
        # "Framework :: Jupyter",
        # "Framework :: Lektor",
        # "Framework :: Odoo",
        # "Framework :: Opps",
        # "Framework :: Paste",
        # "Framework :: Pelican",
        # "Framework :: Pelican :: Plugins",
        # "Framework :: Pelican :: Themes",
        # "Framework :: Plone",
        # "Framework :: Plone :: 3.2",
        # "Framework :: Plone :: 3.3",
        # "Framework :: Plone :: 4.0",
        # "Framework :: Plone :: 4.1",
        # "Framework :: Plone :: 4.2",
        # "Framework :: Plone :: 4.3",
        # "Framework :: Plone :: 5.0",
        # "Framework :: Plone :: 5.1",
        # "Framework :: Plone :: 5.2",
        # "Framework :: Plone :: Theme",
        # "Framework :: Pylons",
        # "Framework :: Pyramid",
        # "Framework :: Pytest",
        # "Framework :: Review Board",
        # "Framework :: Robot Framework",
        # "Framework :: Robot Framework :: Library",
        # "Framework :: Robot Framework :: Tool",
        # "Framework :: Scrapy",
        # "Framework :: Setuptools Plugin",
        # "Framework :: Sphinx",
        # "Framework :: Sphinx :: Extension",
        # "Framework :: Sphinx :: Theme",
        # "Framework :: tox",
        # "Framework :: Trac",
        # "Framework :: Trio",
        # "Framework :: Tryton",
        # "Framework :: TurboGears",
        # "Framework :: TurboGears :: Applications",
        # "Framework :: TurboGears :: Widgets",
        # "Framework :: Twisted",
        # "Framework :: Wagtail",
        # "Framework :: Wagtail :: 1",
        # "Framework :: Wagtail :: 2",
        # "Framework :: ZODB",
        # "Framework :: Zope",
        # "Framework :: Zope2",
        # "Framework :: Zope :: 2",
        # "Framework :: Zope3",
        # "Framework :: Zope :: 3",
        # "Framework :: Zope :: 4",
        # "Intended Audience :: Customer Service",
        "Intended Audience :: Developers",
        # "Intended Audience :: Education",
        # "Intended Audience :: End Users/Desktop",
        # "Intended Audience :: Financial and Insurance Industry",
        # "Intended Audience :: Healthcare Industry",
        # "Intended Audience :: Information Technology",
        # "Intended Audience :: Legal Industry",
        # "Intended Audience :: Manufacturing",
        # "Intended Audience :: Other Audience",
        # "Intended Audience :: Religion",
        # "Intended Audience :: Science/Research",
        # "Intended Audience :: System Administrators",
        # "Intended Audience :: Telecommunications Industry",
        # "License :: Aladdin Free Public License (AFPL)",
        # "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        # "License :: CeCILL-B Free Software License Agreement (CECILL-B)",
        # "License :: CeCILL-C Free Software License Agreement (CECILL-C)",
        # "License :: DFSG approved",
        # "License :: Eiffel Forum License (EFL)",
        # "License :: Free For Educational Use",
        # "License :: Free For Home Use",
        # "License :: Free for non-commercial use",
        # "License :: Freely Distributable",
        # "License :: Free To Use But Restricted",
        # "License :: Freeware",
        # "License :: GUST Font License 1.0",
        # "License :: GUST Font License 2006-09-30",
        # "License :: Netscape Public License (NPL)",
        # "License :: Nokia Open Source License (NOKOS)",
        # "License :: OSI Approved",
        # "License :: OSI Approved :: Academic Free License (AFL)",
        # "License :: OSI Approved :: Apache Software License",
        # "License :: OSI Approved :: Apple Public Source License",
        # "License :: OSI Approved :: Artistic License",
        # "License :: OSI Approved :: Attribution Assurance License",
        # "License :: OSI Approved :: Boost Software License 1.0 (BSL-1.0)",
        "License :: OSI Approved :: BSD License",
        # "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
        # "License :: OSI Approved :: Common Development and Distribution License 1.0 (CDDL-1.0)",
        # "License :: OSI Approved :: Common Public License",
        # "License :: OSI Approved :: Eclipse Public License 1.0 (EPL-1.0)",
        # "License :: OSI Approved :: Eclipse Public License 2.0 (EPL-2.0)",
        # "License :: OSI Approved :: Eiffel Forum License",
        # "License :: OSI Approved :: European Union Public Licence 1.0 (EUPL 1.0)",
        # "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        # "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        # "License :: OSI Approved :: GNU Affero General Public License v3",
        # "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        # "License :: OSI Approved :: GNU Free Documentation License (FDL)",
        # "License :: OSI Approved :: GNU General Public License (GPL)",
        # "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        # "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        # "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        # "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        # "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        # "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        # "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        # "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        # "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        # "License :: OSI Approved :: IBM Public License",
        # "License :: OSI Approved :: Intel Open Source License",
        # "License :: OSI Approved :: ISC License (ISCL)",
        # "License :: OSI Approved :: Jabber Open Source License",
        # "License :: OSI Approved :: MirOS License (MirOS)",
        # "License :: OSI Approved :: MIT License",
        # "License :: OSI Approved :: MITRE Collaborative Virtual Workspace License (CVW)",
        # "License :: OSI Approved :: Motosoto License",
        # "License :: OSI Approved :: Mozilla Public License 1.0 (MPL)",
        # "License :: OSI Approved :: Mozilla Public License 1.1 (MPL 1.1)",
        # "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        # "License :: OSI Approved :: Nethack General Public License",
        # "License :: OSI Approved :: Nokia Open Source License",
        # "License :: OSI Approved :: Open Group Test Suite License",
        # "License :: OSI Approved :: PostgreSQL License",
        # "License :: OSI Approved :: Python License (CNRI Python License)",
        # "License :: OSI Approved :: Python Software Foundation License",
        # "License :: OSI Approved :: Qt Public License (QPL)",
        # "License :: OSI Approved :: Ricoh Source Code Public License",
        # "License :: OSI Approved :: SIL Open Font License 1.1 (OFL-1.1)",
        # "License :: OSI Approved :: Sleepycat License",
        # "License :: OSI Approved :: Sun Industry Standards Source License (SISSL)",
        # "License :: OSI Approved :: Sun Public License",
        # "License :: OSI Approved :: Universal Permissive License (UPL)",
        # "License :: OSI Approved :: University of Illinois/NCSA Open Source License",
        # "License :: OSI Approved :: Vovida Software License 1.0",
        # "License :: OSI Approved :: W3C License",
        # "License :: OSI Approved :: X.Net License",
        # "License :: OSI Approved :: zlib/libpng License",
        # "License :: OSI Approved :: Zope Public License",
        # "License :: Other/Proprietary License",
        # "License :: Public Domain",
        # "License :: Repoze Public License",
        # "Natural Language :: Afrikaans",
        # "Natural Language :: Arabic",
        # "Natural Language :: Bengali",
        # "Natural Language :: Bosnian",
        # "Natural Language :: Bulgarian",
        # "Natural Language :: Cantonese",
        # "Natural Language :: Catalan",
        # "Natural Language :: Chinese (Simplified)",
        # "Natural Language :: Chinese (Traditional)",
        # "Natural Language :: Croatian",
        # "Natural Language :: Czech",
        # "Natural Language :: Danish",
        # "Natural Language :: Dutch",
        # "Natural Language :: English",
        # "Natural Language :: Esperanto",
        # "Natural Language :: Finnish",
        # "Natural Language :: French",
        # "Natural Language :: Galician",
        # "Natural Language :: German",
        # "Natural Language :: Greek",
        # "Natural Language :: Hebrew",
        # "Natural Language :: Hindi",
        # "Natural Language :: Hungarian",
        # "Natural Language :: Icelandic",
        # "Natural Language :: Indonesian",
        # "Natural Language :: Italian",
        # "Natural Language :: Japanese",
        # "Natural Language :: Javanese",
        # "Natural Language :: Korean",
        # "Natural Language :: Latin",
        # "Natural Language :: Latvian",
        # "Natural Language :: Macedonian",
        # "Natural Language :: Malay",
        # "Natural Language :: Marathi",
        # "Natural Language :: Norwegian",
        # "Natural Language :: Panjabi",
        # "Natural Language :: Persian",
        # "Natural Language :: Polish",
        # "Natural Language :: Portuguese",
        # "Natural Language :: Portuguese (Brazilian)",
        # "Natural Language :: Romanian",
        # "Natural Language :: Russian",
        # "Natural Language :: Serbian",
        # "Natural Language :: Slovak",
        # "Natural Language :: Slovenian",
        # "Natural Language :: Spanish",
        # "Natural Language :: Swedish",
        # "Natural Language :: Tamil",
        # "Natural Language :: Telugu",
        # "Natural Language :: Thai",
        # "Natural Language :: Tibetan",
        # "Natural Language :: Turkish",
        # "Natural Language :: Ukrainian",
        # "Natural Language :: Urdu",
        # "Natural Language :: Vietnamese",
        # "Operating System :: Android",
        # "Operating System :: BeOS",
        # "Operating System :: iOS",
        # "Operating System :: MacOS",
        # "Operating System :: MacOS :: MacOS 9",
        # "Operating System :: MacOS :: MacOS X",
        # "Operating System :: Microsoft",
        # "Operating System :: Microsoft :: MS-DOS",
        # "Operating System :: Microsoft :: Windows",
        # "Operating System :: Microsoft :: Windows :: Windows 10",
        # "Operating System :: Microsoft :: Windows :: Windows 3.1 or Earlier",
        # "Operating System :: Microsoft :: Windows :: Windows 7",
        # "Operating System :: Microsoft :: Windows :: Windows 8",
        # "Operating System :: Microsoft :: Windows :: Windows 8.1",
        # "Operating System :: Microsoft :: Windows :: Windows 95/98/2000",
        # "Operating System :: Microsoft :: Windows :: Windows CE",
        # "Operating System :: Microsoft :: Windows :: Windows NT/2000",
        # "Operating System :: Microsoft :: Windows :: Windows Server 2003",
        # "Operating System :: Microsoft :: Windows :: Windows Server 2008",
        # "Operating System :: Microsoft :: Windows :: Windows Vista",
        # "Operating System :: Microsoft :: Windows :: Windows XP",
        # "Operating System :: OS/2",
        # "Operating System :: OS Independent",
        # "Operating System :: Other OS",
        # "Operating System :: PalmOS",
        # "Operating System :: PDA Systems",
        # "Operating System :: POSIX",
        # "Operating System :: POSIX :: AIX",
        # "Operating System :: POSIX :: BSD",
        # "Operating System :: POSIX :: BSD :: BSD/OS",
        # "Operating System :: POSIX :: BSD :: FreeBSD",
        # "Operating System :: POSIX :: BSD :: NetBSD",
        # "Operating System :: POSIX :: BSD :: OpenBSD",
        # "Operating System :: POSIX :: GNU Hurd",
        # "Operating System :: POSIX :: HP-UX",
        # "Operating System :: POSIX :: IRIX",
        # "Operating System :: POSIX :: Linux",
        # "Operating System :: POSIX :: Other",
        # "Operating System :: POSIX :: SCO",
        # "Operating System :: POSIX :: SunOS/Solaris",
        # "Operating System :: Unix",
        # "Programming Language :: Ada",
        # "Programming Language :: APL",
        # "Programming Language :: ASP",
        # "Programming Language :: Assembly",
        # "Programming Language :: Awk",
        # "Programming Language :: Basic",
        # "Programming Language :: C",
        # "Programming Language :: C#",
        # "Programming Language :: C++",
        # "Programming Language :: Cold Fusion",
        # "Programming Language :: Cython",
        # "Programming Language :: Delphi/Kylix",
        # "Programming Language :: Dylan",
        # "Programming Language :: Eiffel",
        # "Programming Language :: Emacs-Lisp",
        # "Programming Language :: Erlang",
        # "Programming Language :: Euler",
        # "Programming Language :: Euphoria",
        # "Programming Language :: Forth",
        # "Programming Language :: Fortran",
        # "Programming Language :: Haskell",
        # "Programming Language :: Java",
        # "Programming Language :: JavaScript",
        # "Programming Language :: Lisp",
        # "Programming Language :: Logo",
        # "Programming Language :: ML",
        # "Programming Language :: Modula",
        # "Programming Language :: Objective C",
        # "Programming Language :: Object Pascal",
        # "Programming Language :: OCaml",
        # "Programming Language :: Other",
        # "Programming Language :: Other Scripting Engines",
        # "Programming Language :: Pascal",
        # "Programming Language :: Perl",
        # "Programming Language :: PHP",
        # "Programming Language :: Pike",
        # "Programming Language :: Pliant",
        # "Programming Language :: PL/SQL",
        # "Programming Language :: PROGRESS",
        # "Programming Language :: Prolog",
        "Programming Language :: Python",
        # "Programming Language :: Python :: 2",
        # "Programming Language :: Python :: 2.3",
        # "Programming Language :: Python :: 2.4",
        # "Programming Language :: Python :: 2.5",
        # "Programming Language :: Python :: 2.6",
        # "Programming Language :: Python :: 2.7",
        # "Programming Language :: Python :: 2 :: Only",
        "Programming Language :: Python :: 3",
        # "Programming Language :: Python :: 3.0",
        # "Programming Language :: Python :: 3.1",
        # "Programming Language :: Python :: 3.2",
        # "Programming Language :: Python :: 3.3",
        # "Programming Language :: Python :: 3.4",
        # "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        # "Programming Language :: Python :: 3.7",
        # "Programming Language :: Python :: 3 :: Only",
        # "Programming Language :: Python :: Implementation",
        # "Programming Language :: Python :: Implementation :: CPython",
        # "Programming Language :: Python :: Implementation :: IronPython",
        # "Programming Language :: Python :: Implementation :: Jython",
        # "Programming Language :: Python :: Implementation :: MicroPython",
        # "Programming Language :: Python :: Implementation :: PyPy",
        # "Programming Language :: Python :: Implementation :: Stackless",
        # "Programming Language :: REBOL",
        # "Programming Language :: Rexx",
        # "Programming Language :: Ruby",
        # "Programming Language :: Rust",
        # "Programming Language :: Scheme",
        # "Programming Language :: Simula",
        # "Programming Language :: Smalltalk",
        # "Programming Language :: SQL",
        # "Programming Language :: Tcl",
        # "Programming Language :: Unix Shell",
        # "Programming Language :: Visual Basic",
        # "Programming Language :: XBasic",
        # "Programming Language :: YACC",
        # "Programming Language :: Zope",
        # "Topic :: Adaptive Technologies",
        # "Topic :: Artistic Software",
        # "Topic :: Communications",
        # "Topic :: Communications :: BBS",
        # "Topic :: Communications :: Chat",
        # "Topic :: Communications :: Chat :: ICQ",
        # "Topic :: Communications :: Chat :: Internet Relay Chat",
        # "Topic :: Communications :: Chat :: Unix Talk",
        # "Topic :: Communications :: Conferencing",
        # "Topic :: Communications :: Email",
        # "Topic :: Communications :: Email :: Address Book",
        # "Topic :: Communications :: Email :: Email Clients (MUA)",
        # "Topic :: Communications :: Email :: Filters",
        # "Topic :: Communications :: Email :: Mailing List Servers",
        # "Topic :: Communications :: Email :: Mail Transport Agents",
        # "Topic :: Communications :: Email :: Post-Office",
        # "Topic :: Communications :: Email :: Post-Office :: IMAP",
        # "Topic :: Communications :: Email :: Post-Office :: POP3",
        # "Topic :: Communications :: Fax",
        # "Topic :: Communications :: FIDO",
        # "Topic :: Communications :: File Sharing",
        # "Topic :: Communications :: File Sharing :: Gnutella",
        # "Topic :: Communications :: File Sharing :: Napster",
        # "Topic :: Communications :: Ham Radio",
        # "Topic :: Communications :: Internet Phone",
        # "Topic :: Communications :: Telephony",
        # "Topic :: Communications :: Usenet News",
        # "Topic :: Database",
        # "Topic :: Database :: Database Engines/Servers",
        # "Topic :: Database :: Front-Ends",
        # "Topic :: Desktop Environment",
        # "Topic :: Desktop Environment :: File Managers",
        # "Topic :: Desktop Environment :: Gnome",
        # "Topic :: Desktop Environment :: GNUstep",
        # "Topic :: Desktop Environment :: K Desktop Environment (KDE)",
        # "Topic :: Desktop Environment :: K Desktop Environment (KDE) :: Themes",
        # "Topic :: Desktop Environment :: PicoGUI",
        # "Topic :: Desktop Environment :: PicoGUI :: Applications",
        # "Topic :: Desktop Environment :: PicoGUI :: Themes",
        # "Topic :: Desktop Environment :: Screen Savers",
        # "Topic :: Desktop Environment :: Window Managers",
        # "Topic :: Desktop Environment :: Window Managers :: Afterstep",
        # "Topic :: Desktop Environment :: Window Managers :: Afterstep :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: Applets",
        # "Topic :: Desktop Environment :: Window Managers :: Blackbox",
        # "Topic :: Desktop Environment :: Window Managers :: Blackbox :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: CTWM",
        # "Topic :: Desktop Environment :: Window Managers :: CTWM :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: Enlightenment",
        # "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Epplets",
        # "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR15",
        # "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR16",
        # "Topic :: Desktop Environment :: Window Managers :: Enlightenment :: Themes DR17",
        # "Topic :: Desktop Environment :: Window Managers :: Fluxbox",
        # "Topic :: Desktop Environment :: Window Managers :: Fluxbox :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: FVWM",
        # "Topic :: Desktop Environment :: Window Managers :: FVWM :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: IceWM",
        # "Topic :: Desktop Environment :: Window Managers :: IceWM :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: MetaCity",
        # "Topic :: Desktop Environment :: Window Managers :: MetaCity :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: Oroborus",
        # "Topic :: Desktop Environment :: Window Managers :: Oroborus :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: Sawfish",
        # "Topic :: Desktop Environment :: Window Managers :: Sawfish :: Themes 0.30",
        # "Topic :: Desktop Environment :: Window Managers :: Sawfish :: Themes pre-0.30",
        # "Topic :: Desktop Environment :: Window Managers :: Waimea",
        # "Topic :: Desktop Environment :: Window Managers :: Waimea :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: Window Maker",
        # "Topic :: Desktop Environment :: Window Managers :: Window Maker :: Applets",
        # "Topic :: Desktop Environment :: Window Managers :: Window Maker :: Themes",
        # "Topic :: Desktop Environment :: Window Managers :: XFCE",
        # "Topic :: Desktop Environment :: Window Managers :: XFCE :: Themes",
        # "Topic :: Documentation",
        # "Topic :: Documentation :: Sphinx",
        # "Topic :: Education",
        # "Topic :: Education :: Computer Aided Instruction (CAI)",
        # "Topic :: Education :: Testing",
        # "Topic :: Games/Entertainment",
        # "Topic :: Games/Entertainment :: Arcade",
        # "Topic :: Games/Entertainment :: Board Games",
        # "Topic :: Games/Entertainment :: First Person Shooters",
        # "Topic :: Games/Entertainment :: Fortune Cookies",
        # "Topic :: Games/Entertainment :: Multi-User Dungeons (MUD)",
        # "Topic :: Games/Entertainment :: Puzzle Games",
        # "Topic :: Games/Entertainment :: Real Time Strategy",
        # "Topic :: Games/Entertainment :: Role-Playing",
        # "Topic :: Games/Entertainment :: Side-Scrolling/Arcade Games",
        # "Topic :: Games/Entertainment :: Simulation",
        # "Topic :: Games/Entertainment :: Turn Based Strategy",
        # "Topic :: Home Automation",
        # "Topic :: Internet",
        # "Topic :: Internet :: File Transfer Protocol (FTP)",
        # "Topic :: Internet :: Finger",
        # "Topic :: Internet :: Log Analysis",
        # "Topic :: Internet :: Name Service (DNS)",
        # "Topic :: Internet :: Proxy Servers",
        # "Topic :: Internet :: WAP",
        # "Topic :: Internet :: WWW/HTTP",
        # "Topic :: Internet :: WWW/HTTP :: Browsers",
        # "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        # "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        # "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",
        # "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Message Boards",
        # "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
        # "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Page Counters",
        # "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Wiki",
        # "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        # "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        # "Topic :: Internet :: WWW/HTTP :: Session",
        # "Topic :: Internet :: WWW/HTTP :: Site Management",
        # "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
        # "Topic :: Internet :: WWW/HTTP :: WSGI",
        # "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        # "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        # "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
        # "Topic :: Internet :: XMPP",
        # "Topic :: Internet :: Z39.50",
        # "Topic :: Multimedia",
        # "Topic :: Multimedia :: Graphics",
        # "Topic :: Multimedia :: Graphics :: 3D Modeling",
        # "Topic :: Multimedia :: Graphics :: 3D Rendering",
        # "Topic :: Multimedia :: Graphics :: Capture",
        # "Topic :: Multimedia :: Graphics :: Capture :: Digital Camera",
        # "Topic :: Multimedia :: Graphics :: Capture :: Scanners",
        # "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
        # "Topic :: Multimedia :: Graphics :: Editors",
        # "Topic :: Multimedia :: Graphics :: Editors :: Raster-Based",
        # "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
        # "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        # "Topic :: Multimedia :: Graphics :: Presentation",
        # "Topic :: Multimedia :: Graphics :: Viewers",
        # "Topic :: Multimedia :: Sound/Audio",
        # "Topic :: Multimedia :: Sound/Audio :: Analysis",
        # "Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
        # "Topic :: Multimedia :: Sound/Audio :: CD Audio",
        # "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Playing",
        # "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Ripping",
        # "Topic :: Multimedia :: Sound/Audio :: CD Audio :: CD Writing",
        # "Topic :: Multimedia :: Sound/Audio :: Conversion",
        # "Topic :: Multimedia :: Sound/Audio :: Editors",
        # "Topic :: Multimedia :: Sound/Audio :: MIDI",
        # "Topic :: Multimedia :: Sound/Audio :: Mixers",
        # "Topic :: Multimedia :: Sound/Audio :: Players",
        # "Topic :: Multimedia :: Sound/Audio :: Players :: MP3",
        # "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        # "Topic :: Multimedia :: Sound/Audio :: Speech",
        # "Topic :: Multimedia :: Video",
        # "Topic :: Multimedia :: Video :: Capture",
        # "Topic :: Multimedia :: Video :: Conversion",
        # "Topic :: Multimedia :: Video :: Display",
        # "Topic :: Multimedia :: Video :: Non-Linear Editor",
        # "Topic :: Office/Business",
        # "Topic :: Office/Business :: Financial",
        # "Topic :: Office/Business :: Financial :: Accounting",
        # "Topic :: Office/Business :: Financial :: Investment",
        # "Topic :: Office/Business :: Financial :: Point-Of-Sale",
        # "Topic :: Office/Business :: Financial :: Spreadsheet",
        # "Topic :: Office/Business :: Groupware",
        # "Topic :: Office/Business :: News/Diary",
        # "Topic :: Office/Business :: Office Suites",
        # "Topic :: Office/Business :: Scheduling",
        # "Topic :: Other/Nonlisted Topic",
        # "Topic :: Printing",
        # "Topic :: Religion",
        # "Topic :: Scientific/Engineering",
        # "Topic :: Scientific/Engineering :: Artificial Intelligence",
        # "Topic :: Scientific/Engineering :: Artificial Life",
        # "Topic :: Scientific/Engineering :: Astronomy",
        # "Topic :: Scientific/Engineering :: Atmospheric Science",
        # "Topic :: Scientific/Engineering :: Bio-Informatics",
        # "Topic :: Scientific/Engineering :: Chemistry",
        # "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        # "Topic :: Scientific/Engineering :: GIS",
        # "Topic :: Scientific/Engineering :: Human Machine Interfaces",
        # "Topic :: Scientific/Engineering :: Image Recognition",
        # "Topic :: Scientific/Engineering :: Information Analysis",
        # "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        # "Topic :: Scientific/Engineering :: Mathematics",
        # "Topic :: Scientific/Engineering :: Medical Science Apps.",
        # "Topic :: Scientific/Engineering :: Physics",
        # "Topic :: Scientific/Engineering :: Visualization",
        # "Topic :: Security",
        # "Topic :: Security :: Cryptography",
        # "Topic :: Sociology",
        # "Topic :: Sociology :: Genealogy",
        # "Topic :: Sociology :: History",
        # "Topic :: Software Development",
        # "Topic :: Software Development :: Assemblers",
        # "Topic :: Software Development :: Bug Tracking",
        # "Topic :: Software Development :: Build Tools",
        # "Topic :: Software Development :: Code Generators",
        # "Topic :: Software Development :: Compilers",
        # "Topic :: Software Development :: Debuggers",
        # "Topic :: Software Development :: Disassemblers",
        # "Topic :: Software Development :: Documentation",
        # "Topic :: Software Development :: Embedded Systems",
        # "Topic :: Software Development :: Internationalization",
        # "Topic :: Software Development :: Interpreters",
        # "Topic :: Software Development :: Libraries",
        # "Topic :: Software Development :: Libraries :: Application Frameworks",
        # "Topic :: Software Development :: Libraries :: Java Libraries",
        # "Topic :: Software Development :: Libraries :: Perl Modules",
        # "Topic :: Software Development :: Libraries :: PHP Classes",
        # "Topic :: Software Development :: Libraries :: Pike Modules",
        # "Topic :: Software Development :: Libraries :: pygame",
        # "Topic :: Software Development :: Libraries :: Python Modules",
        # "Topic :: Software Development :: Libraries :: Ruby Modules",
        # "Topic :: Software Development :: Libraries :: Tcl Extensions",
        # "Topic :: Software Development :: Localization",
        # "Topic :: Software Development :: Object Brokering",
        # "Topic :: Software Development :: Object Brokering :: CORBA",
        # "Topic :: Software Development :: Pre-processors",
        # "Topic :: Software Development :: Quality Assurance",
        # "Topic :: Software Development :: Testing",
        # "Topic :: Software Development :: Testing :: Acceptance",
        # "Topic :: Software Development :: Testing :: BDD",
        # "Topic :: Software Development :: Testing :: Mocking",
        # "Topic :: Software Development :: Testing :: Traffic Generation",
        # "Topic :: Software Development :: Testing :: Unit",
        # "Topic :: Software Development :: User Interfaces",
        # "Topic :: Software Development :: Version Control",
        # "Topic :: Software Development :: Version Control :: Bazaar",
        # "Topic :: Software Development :: Version Control :: CVS",
        # "Topic :: Software Development :: Version Control :: Git",
        # "Topic :: Software Development :: Version Control :: Mercurial",
        # "Topic :: Software Development :: Version Control :: RCS",
        # "Topic :: Software Development :: Version Control :: SCCS",
        # "Topic :: Software Development :: Widget Sets",
        # "Topic :: System",
        # "Topic :: System :: Archiving",
        # "Topic :: System :: Archiving :: Backup",
        # "Topic :: System :: Archiving :: Compression",
        # "Topic :: System :: Archiving :: Mirroring",
        # "Topic :: System :: Archiving :: Packaging",
        # "Topic :: System :: Benchmark",
        # "Topic :: System :: Boot",
        # "Topic :: System :: Boot :: Init",
        # "Topic :: System :: Clustering",
        # "Topic :: System :: Console Fonts",
        # "Topic :: System :: Distributed Computing",
        # "Topic :: System :: Emulators",
        # "Topic :: System :: Filesystems",
        # "Topic :: System :: Hardware",
        # "Topic :: System :: Hardware :: Hardware Drivers",
        # "Topic :: System :: Hardware :: Mainframes",
        # "Topic :: System :: Hardware :: Symmetric Multi-processing",
        # "Topic :: System :: Installation/Setup",
        # "Topic :: System :: Logging",
        # "Topic :: System :: Monitoring",
        # "Topic :: System :: Networking",
        # "Topic :: System :: Networking :: Firewalls",
        # "Topic :: System :: Networking :: Monitoring",
        # "Topic :: System :: Networking :: Monitoring :: Hardware Watchdog",
        # "Topic :: System :: Networking :: Time Synchronization",
        # "Topic :: System :: Operating System",
        # "Topic :: System :: Operating System Kernels",
        # "Topic :: System :: Operating System Kernels :: BSD",
        # "Topic :: System :: Operating System Kernels :: GNU Hurd",
        # "Topic :: System :: Operating System Kernels :: Linux",
        # "Topic :: System :: Power (UPS)",
        # "Topic :: System :: Recovery Tools",
        # "Topic :: System :: Shells",
        # "Topic :: System :: Software Distribution",
        # "Topic :: System :: Systems Administration",
        # "Topic :: System :: Systems Administration :: Authentication/Directory",
        # "Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP",
        # "Topic :: System :: Systems Administration :: Authentication/Directory :: NIS",
        # "Topic :: System :: System Shells",
        # "Topic :: Terminals",
        # "Topic :: Terminals :: Serial",
        # "Topic :: Terminals :: Telnet",
        # "Topic :: Terminals :: Terminal Emulators/X Terminals",
        # "Topic :: Text Editors",
        # "Topic :: Text Editors :: Documentation",
        # "Topic :: Text Editors :: Emacs",
        # "Topic :: Text Editors :: Integrated Development Environments (IDE)",
        # "Topic :: Text Editors :: Text Processing",
        # "Topic :: Text Editors :: Word Processors",
        # "Topic :: Text Processing",
        # "Topic :: Text Processing :: Filters",
        # "Topic :: Text Processing :: Fonts",
        "Topic :: Text Processing :: General",
        # "Topic :: Text Processing :: Indexing",
        # "Topic :: Text Processing :: Linguistic",
        # "Topic :: Text Processing :: Markup",
        # "Topic :: Text Processing :: Markup :: HTML",
        # "Topic :: Text Processing :: Markup :: LaTeX",
        # "Topic :: Text Processing :: Markup :: SGML",
        # "Topic :: Text Processing :: Markup :: VRML",
        # "Topic :: Text Processing :: Markup :: XML",
        "Topic :: Utilities",
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Optional
    keywords=[
        # eg:
        #   "sample", "test"
    ],

    py_modules=[
        splitext(basename(path))[0] for path in glob("src/*.py")
    ],

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    # Required
    packages=find_packages("src"),

    # Tell distutils packages are under "./src"
    # Required if we store packages under a "src" directory.
    #
    # Optional
    package_dir={"": "src"},

    # A file or a string to specify the type of license for this package.
    #
    # Optional
    license="BSD 2-Clause License",

    # Whether the project can be safely installed and run from a zip file. If
    # this argument is not supplied, the bdist_egg command will have to
    # analyze all of your project’s contents for possible problems each time
    # it builds an egg.
    #
    # Optional
    zip_safe=False,

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip"s requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    #
    # Optional
    install_requires=[
        # eg:
        #   "six", or "six>=1.7",
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    #
    # Optional
    extras_require={
        # eg:
        #   "rst": ["docutils>=0.11"],
        #   ":python_version=="2.6"": ["argparse"],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    #
    # If using Python 2.6 or earlier, then these have to be included in
    # MANIFEST.in as well.
    #
    # You do not need to use this option if you are using
    # include_package_data, unless you need to add e.g. files that are
    # generated by your setup script and build process. (And are therefore not
    # in source control or are files that you don’t want to include in your
    # source distribution.)
    #
    # Optional
    package_data={
        # eg:
        #   "sample": ["package_data.dat"],
    },

    # This tells setuptools to automatically include any data files it finds
    # inside your package directories that are specified by your MANIFEST.in
    # file.
    include_package_data=True,

    # Although "package_data" is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    #
    # In this case, "data_file" will be installed into "<sys.prefix>/my_data"
    #
    # Optional
    data_files=[
        # eg:
        #   ("my_data", ["data/data_file"]),
    ],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    #
    # Optional
    entry_points={
        # eg:
        #   "console_scripts": [
        #       "sample=sample:main",
        #   ],
    },

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what"s used to render the link text on PyPI.
    #
    # Optional
    project_urls={
        # eg:
        #   "Bug Reports": "https://github.com/pypa/sampleproject/issues",
        #   "Funding": "https://donate.pypi.org",
        #   "Say Thanks!": "http://saythanks.io/to/example",
        #   "Source": "https://github.com/pypa/sampleproject/",
    },
)
