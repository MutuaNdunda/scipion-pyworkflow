# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se) [1]
# *
# * [1] SciLifeLab, Stockholm University
# *
# * This program is free software: you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation, either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program.  If not, see <https://www.gnu.org/licenses/>.
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************
import ast
import os
import sys
import importlib
import types

# This variable is useful to determinate the plugins compatibility with the
# current Scipion core release.
# This version does not need to change with future scipion releases
# if plugins are still compatible, so future hot fixes releases or even micros
# or minor release should not change this CORE_VERSION. Only, when a new release
# will break existing plugins, this number needs to be incremented.
CORE_VERSION = '3.0.0'

# Versions
VERSION_1 = '1.0.0'
VERSION_1_1 = '1.1.0'
VERSION_1_2 = '1.2.0'
VERSION_2_0 = '2.0.0'
VERSION_3_0 = '3.0.0'

# For a new release, define a new constant and assign it to LAST_VERSION
# The existing one has to be added to OLD_VERSIONS list.
LAST_VERSION = VERSION_3_0
OLD_VERSIONS = (VERSION_1, VERSION_1_1, VERSION_1_2, VERSION_2_0)

# Define pyworkflow version in a standard way, as proposed by:
# https://www.python.org/dev/peps/pep-0396/
__version__ = LAST_VERSION + 'a1'

HOME = os.path.abspath(os.path.dirname(__file__))
PYTHON = os.environ.get("SCIPION_PYTHON", 'python3')

# Variable constants, probably we can have a constants module
SCIPION_LAUNCH_CMD = 'SCIPION_LAUNCH_CMD'
NOTES_HEADING_MSG = \
     '############################################  SCIPION NOTES  ##############################################' + \
     '\n\nThis document can be used to store your notes within your project from Scipion framework.\n\n' + \
     'Scipion notes behaviour can be managed in the Scipion config file by creating or editing, if they\n' + \
     'already exist, the following variables:\n\n' + \
     '\t-SCIPION_NOTES_FILE is used to store the file name (default is {})\n' + \
     '\t-SCIPION_NOTES_PROGRAM is used to select the program which will be used to open the notes file. If \n' + \
     '\t empty, it will use the default program used by your OS to open that type of file.\n' + \
     '\t-SCIPION_NOTES_ARGS is used to add input arguments that will be used in the calling of the program\n' + \
     '\t specified in SCIPION_NOTES_PROGRAM.\n\n' + \
     'These lines can be removed if desired.\n\n' + \
     '###########################################################################################################' + \
     '\n\nPROJECT NOTES:'

# Following are a set of functions to centralize the way to get
# files from several scipion folder such as: config or apps
def getPWPath(*paths):
    return os.path.join(os.path.dirname(__file__), *paths)


def getAppsPath():
    return os.path.join(getPWPath(), 'apps')


def getSyncDataScript():
    return os.path.join(getAppsPath(), 'pw_sync_data.py')


def getScheduleScript():
    return os.path.join(getAppsPath(), 'pw_schedule_run.py')


def getPwProtMpiRunScript():
    return os.path.join(getAppsPath(), 'pw_protocol_mpirun.py')


def getTestsScript():
    return os.path.join(getAppsPath(), 'pw_run_tests.py')


def getViewerScript():
    return os.path.join(getAppsPath(), 'pw_viewer.py')


class Config:
    """ Main Config for pyworkflow. It contains the main configuration values
    providing default values or, if present, taking them from the environment.
    It has SCIPION_HOME, SCIPION_USER_DATA ...
    Necessary value is SCIPION_HOME and has to be present in the environment"""

    __get = os.environ.get  # shortcut

    # SCIPION PATHS
    SCIPION_HOME = __get('SCIPION_HOME', '') # Home for scipion
    # Location for scipion projects
    SCIPION_USER_DATA = __get('SCIPION_USER_DATA',
                              os.path.expanduser('~/ScipionUserData'))
    # Path for Scipion logs
    SCIPION_LOGS = __get('SCIPION_LOGS', os.path.join(SCIPION_USER_DATA,'logs'))

    # Get general log file path
    LOG_FILE = os.path.join(SCIPION_LOGS, 'scipion.log')

    # Where is the input data for tests...also where it will be downloaded
    SCIPION_TESTS = __get('SCIPION_TESTS',
                          os.path.join(SCIPION_HOME, 'data', 'tests'))

    # Where to install software
    SCIPION_SOFTWARE = __get('SCIPION_SOFTWARE',
                            os.path.join(SCIPION_HOME, 'software'))
    # General purpose scipion tmp folder
    SCIPION_TMP = __get('SCIPION_TMP',
                            os.path.join(SCIPION_USER_DATA, 'tmp'))


    SCIPION_SUPPORT_EMAIL = __get('SCIPION_SUPPORT_EMAIL',
                                  'scipion@cnb.csic.es')
    SCIPION_LOGO = __get('SCIPION_LOGO',
                         'scipion_logo.gif')

    # Where the output of the tests will be stored
    SCIPION_TESTS_OUTPUT = __get('SCIPION_TESTS_OUTPUT',
                                 os.path.join(SCIPION_USER_DATA, 'Tests'))

    SCIPION_CONFIG = __get('SCIPION_CONFIG', 'scipion.conf')
    SCIPION_LOCAL_CONFIG = __get('SCIPION_LOCAL_CONFIG', SCIPION_CONFIG)
    SCIPION_HOSTS = __get('SCIPION_HOSTS', 'hosts.conf')
    SCIPION_PROTOCOLS = __get('SCIPION_PROTOCOLS', 'protocols.conf')

    SCIPION_PLUGIN_JSON = __get('SCIPION_PLUGIN_JSON', None)
    SCIPION_PLUGIN_REPO_URL = __get('SCIPION_PLUGIN_REPO_URL',
                                    'http://scipion.i2pc.es/getplugins/')

    # REMOTE Section
    SCIPION_URL = __get('SCIPION_URL' , 'http://scipion.cnb.csic.es/downloads/scipion')
    SCIPION_URL_SOFTWARE = __get('SCIPION_URL_SOFTWARE', SCIPION_URL + '/software')
    SCIPION_URL_TESTDATA = __get('SCIPION_URL_TESTDATA', SCIPION_URL + '/data/tests')

    # Scipion Notes
    SCIPION_NOTES_FILE = __get('SCIPION_NOTES_FILE', 'notes.txt')
    SCIPION_NOTES_PROGRAM = __get('SCIPION_NOTES_PROGRAM', None)
    SCIPION_NOTES_ARGS = __get('SCIPION_NOTES_ARGS', None)

    # Aspect
    SCIPION_FONT_NAME = __get('SCIPION_FONT_NAME', "Helvetica")
    SCIPION_FONT_SIZE = int(__get('SCIPION_FONT_SIZE', 10))

    # Notification
    SCIPION_NOTIFY = __get('SCIPION_NOTIFY', 'True')

    try:
        VIEWERS = ast.literal_eval(__get('VIEWERS', "{}"))
    except Exception as e:
        VIEWERS = {}
        print("ERROR loading preferred viewers, VIEWERS variable will be ignored")
        print(e)

    SCIPION_DOMAIN = __get('SCIPION_DOMAIN', None)
    SCIPION_LAUNCH_CMD = __get(SCIPION_LAUNCH_CMD, getTestsScript())

    @classmethod
    def getVariableDict(cls):
        """ fill environment with own values"""
        myDict = dict()
        # For each attribute
        for name, value in vars(cls).items():
            # Skip methods, only str objects
            if isinstance(value, str):
                # Skip starting with __ : __doc__, __module__
                if not name.startswith("__"):
                    # Update environment
                    myDict[name] =value

        return myDict

    @classmethod
    def getDomain(cls):
        """ Import domain module from path or name defined in SCIPION_DOMAIN. """
        value = cls.SCIPION_DOMAIN

        if not value:
            return None

        if os.path.isdir(value):
            dirname, value = os.path.split(value)
            sys.path.append(dirname)

        return importlib.import_module(value).Domain

    @classmethod
    def setDomain(cls, moduleOrNameOrPath):
        if isinstance(moduleOrNameOrPath, types.ModuleType):
            value = os.path.abspath(moduleOrNameOrPath.__path__[0])
        else:
            value = moduleOrNameOrPath
        cls.SCIPION_DOMAIN = value
        os.environ['SCIPION_DOMAIN'] = value

    @staticmethod
    def getPythonLibFolder():
        from sysconfig import get_paths
        return join(get_paths()['data'], "lib")

    @staticmethod
    def debugOn(*args):
        from pyworkflow.utils import envVarOn
        return bool(envVarOn("SCIPION_DEBUG", *args))

    @staticmethod
    def toggleDebug():

        newValue = not Config.debugOn()

        os.environ["SCIPION_DEBUG"] = str(newValue)

def join(*paths):
    """ join paths from HOME . """
    return os.path.join(HOME, *paths)


__resourcesPath = [join('resources')]


def findResource(filename):
    from .utils.path import findFile

    return findFile(filename, *__resourcesPath)

def genNotesHeading():
    return NOTES_HEADING_MSG.format(Config.SCIPION_NOTES_FILE)
