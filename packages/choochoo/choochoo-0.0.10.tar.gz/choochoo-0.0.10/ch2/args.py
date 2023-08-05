
from argparse import ArgumentParser
from genericpath import exists
from os import makedirs
from os.path import dirname, expanduser, realpath, normpath, relpath, join
from re import compile, sub
from typing import Mapping

PROGNAME = 'ch2'
COMMAND = 'command'
TOPIC = 'topic'

ADD_ACTIVITY = 'add-activity'
ADD_FTHR = 'add-fthr'
ADD_PLAN = 'add-plan'
ADD_SUMMARY = 'add-summary'
CREATE_DATABASE = 'create-database'
DATA = 'data'
DIARY = 'diary'
DUMP_FIT = 'dump-fit'
EDIT_ACTIVITIES = 'edit-activities'
EDIT_INJURIES = 'edit-injuries'
EDIT_SCHEDULES = 'edit-schedules'
HELP = 'help'
PACKAGE_FIT_PROFILE = 'package-fit-profile'

ACTIVITY = 'activity'
AFTER = 'after'
ALL_MESSAGES = 'all-messages'
ALL_FIELDS = 'all-fields'
CSV = 'csv'
DATABASE = 'database'
DATE = 'date'
DEV = 'dev'
DUMP_FORMAT = 'dump_format'
FIELDS = 'fields'
FINISH = 'finish'
FTHR = 'fthr'
FORCE, F = 'force', 'f'
LIMIT = 'limit'
LOGS = 'logs'
LIST = 'list'
MESSAGES = 'messages'
MONTH = 'month'
PATH = 'path'
PLAN = 'plan'
RECORD, R = 'record', 'r'
RECORDS = 'records'
ROOT = 'root'
START = 'start'
TABLES = 'tables'
V, VERBOSITY = 'v', 'verbosity'
VERSION = 'version'
WARN, W = 'warn', 'w'
YEAR = 'year'


def mm(name): return '--' + name
def m(name): return '-' + name


VARIABLE = compile(r'(.*(?:[^$]|^))\${(\w+)\}(.*)')
MEMORY  = ':memory:'


class NamespaceWithVariables(Mapping):

    def __init__(self, ns):
        self._dict = vars(ns)

    def __getitem__(self, name):
        name = sub('-', '_', name)
        value = self._dict[name]
        try:
            match = VARIABLE.match(value)
            while match:
                value = match.group(1) + self[match.group(2)] + match.group(3)
                match = VARIABLE.match(value)
            return sub(r'\$\$', '$', value)
        except TypeError:
            return value

    def path(self, name, index=None, rooted=True):
        # special case sqlite3 in-memory database
        if self[name] == MEMORY: return self[name]
        path = self[name]
        if index is not None: path = path[index]
        path = expanduser(path)
        if rooted and relpath(path) and name != ROOT:
            path = join(self.path(ROOT), path)
        return realpath(normpath(path))

    def file(self, name, index=None, rooted=True):
        file = self.path(name, index=index, rooted=rooted)
        # special case sqlite3 in-memory database
        if file == MEMORY: return file
        path = dirname(file)
        if not exists(path):
            makedirs(path)
        return file

    def dir(self, name, index=None, rooted=True):
        path = self.path(name, index=index, rooted=rooted)
        if not exists(path):
            makedirs(path)
        return path

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self.__dict__)


def parser():

    parser = ArgumentParser(prog=PROGNAME)

    parser.add_argument(mm(DATABASE), action='store', default='${root}/database.sqld', metavar='FILE',
                        help='the database file')
    parser.add_argument(mm(DEV), action='store_true', help='enable development mode')
    parser.add_argument(mm(LOGS), action='store', default='logs', metavar='DIR',
                        help='the directory for logs')
    parser.add_argument(mm(ROOT), action='store', default='~/.ch2', metavar='DIR',
                        help='the root directory for the default configuration')
    parser.add_argument(m(V), mm(VERBOSITY), action='store', nargs=1, default=None, type=int, metavar='VERBOSITY',
                        help='output level for stderr (0: silent; 5:noisy)')
    parser.add_argument(mm(VERSION), action='version', version='0.0.10',
                        help='display version and exit')

    subparsers = parser.add_subparsers()

    add_activity = subparsers.add_parser(ADD_ACTIVITY,
                                         help='add a new activity - see `%s %s -h` for more details' % (PROGNAME, ADD_ACTIVITY))
    add_activity_period = add_activity.add_mutually_exclusive_group()
    add_activity_period.add_argument(mm(MONTH), action='store_true', help='generate monthly summary')
    add_activity_period.add_argument(mm(YEAR), action='store_true', help='generate yearly summary')
    add_activity.add_argument(m(F), mm(FORCE), action='store_true', help='re-read file and delete existing data')
    add_activity.add_argument(ACTIVITY, action='store', metavar='ACTIVITY', nargs=1,
                              help='an activity name')
    add_activity.add_argument(PATH, action='store', metavar='PATH', nargs=1,
                              help='a fit file or directory containing fit files')
    add_activity.set_defaults(command=ADD_ACTIVITY)

    add_fthr = subparsers.add_parser(ADD_FTHR,
                                     help='define a new set of HR zones - see `%s %s -h` for more details' % (PROGNAME, ADD_FTHR))
    add_fthr.add_argument(FTHR, action='store', metavar='FTHR', nargs=1, type=int,
                          help='the FTHR')
    add_fthr.add_argument(DATE, action='store', metavar='DATE', nargs='?',
                          help='an optional date')
    add_fthr.set_defaults(command=ADD_FTHR)

    add_plan = subparsers.add_parser(ADD_PLAN,
                                     help='training plans - see `%s %s -h` for more details' % (PROGNAME, ADD_PLAN))
    add_plan.add_argument(mm(LIST), action='store_true',
                          help='list available plans')
    add_plan.add_argument(PLAN, action='store', metavar='PARAM', nargs='*',
                          help='the plan name and possible parameters')
    add_plan.set_defaults(command=ADD_PLAN)

    add_summary = subparsers.add_parser(ADD_SUMMARY,
                                        help='create a new summary (or summaries) - see `%s %s -h` for more details' % (PROGNAME, ADD_SUMMARY))
    add_summary.add_argument(m(F), mm(FORCE), action='store_true', help='re-generate existing summary statistics')
    add_summary_period = add_summary.add_mutually_exclusive_group()
    add_summary_period.add_argument(mm(MONTH), action='store_true', help='generate monthly summary (no start / finish)')
    add_summary_period.add_argument(mm(YEAR), action='store_true', help='generate yearly summary (no start / fininsh)')
    add_summary.add_argument(ACTIVITY, action='store', metavar='ACTIVITY', nargs=1,
                             help='an activity name')
    add_summary.add_argument(START, action='store', metavar='DATE', nargs='?',
                             help='start date (inclusive)')
    add_summary.add_argument(FINISH, action='store', metavar='DATE', nargs='?',
                             help='finish date (inclusive)')
    add_summary.set_defaults(command=ADD_SUMMARY)

    data = subparsers.add_parser(DATA,
                                 help='used within jupyter (no-op from cmd line)')
    data.set_defaults(command=DATA)

    diary = subparsers.add_parser(CREATE_DATABASE,
                                  help='create the database if missing')
    diary.set_defaults(command=CREATE_DATABASE)

    diary = subparsers.add_parser(DIARY,
                                  help='daily diary - see `%s %s -h` for more details' % (PROGNAME, DIARY))
    diary.add_argument(DATE, action='store', metavar='DATE', nargs='?',
                       help='an optional date to display (default is today)')
    diary.set_defaults(command=DIARY)

    dump_fit = subparsers.add_parser(DUMP_FIT,
                                     help='display contents of fit file - ' +
                                          'see `%s %s -h` for more details' % (PROGNAME, DUMP_FIT))
    dump_fit.add_argument(PATH, action='store', metavar='FIT-FILE', nargs=1,
                          help='the path to the fit file')
    dump_fit.add_argument(mm(AFTER), action='store', nargs=1, type=int, metavar='N', default=[0],
                          help='skip initial messages')
    dump_fit.add_argument(mm(LIMIT), action='store', nargs=1, type=int, metavar='N', default=[-1],
                          help='limit number of messages displayed')
    dump_fit_format = dump_fit.add_mutually_exclusive_group()
    dump_fit_format.add_argument(mm(RECORDS), action='store_const', dest=DUMP_FORMAT, const=RECORDS,
                                 help='show high-level structure (ordered by time)')
    dump_fit_format.add_argument(mm(TABLES), action='store_const', dest=DUMP_FORMAT, const=TABLES,
                                 help='show high-level structure (default: grouped in tables)')
    dump_fit_format.add_argument(mm(CSV), action='store_const', dest=DUMP_FORMAT, const=CSV,
                                 help='show med-level structure (CSV format)')
    dump_fit_format.add_argument(mm(MESSAGES), action='store_const', dest=DUMP_FORMAT, const=MESSAGES,
                                 help='show low-level message structure')
    dump_fit_format.add_argument(mm(FIELDS), action='store_const', dest=DUMP_FORMAT, const=FIELDS,
                                 help='show low-level field structure (more details)')
    dump_fit.add_argument(mm(ALL_FIELDS), action='store_true',
                          help='display undocumented fields (for %s, %s)' % (mm(RECORDS), mm(TABLES)))
    dump_fit.add_argument(mm(ALL_MESSAGES), action='store_true',
                          help='display undocumented messages (for %s, %s)' % (mm(RECORDS), mm(TABLES)))
    dump_fit.add_argument(m(R), mm(RECORD), action='store', metavar='name',
                          help='display only named record(s) (for %s, %s)' % (mm(RECORDS), mm(TABLES)))
    dump_fit.add_argument(m(W), mm(WARN), action='store', metavar='name',
                          help='additional warning messages')
    dump_fit.set_defaults(command=DUMP_FIT, dump_format=TABLES)

    edit_activities = subparsers.add_parser(EDIT_ACTIVITIES,
                                            help='manage activity entries - see `%s %s -h` for more details' %
                                                 (PROGNAME, EDIT_ACTIVITIES))
    edit_activities.set_defaults(command=EDIT_ACTIVITIES)

    edit_injuries = subparsers.add_parser(EDIT_INJURIES,
                                          help='manage injury entries - see `%s %s -h` for more details' %
                                               (PROGNAME, EDIT_INJURIES))
    edit_injuries.set_defaults(command=EDIT_INJURIES)

    edit_schedules = subparsers.add_parser(EDIT_SCHEDULES,
                                           help='manage schedules - see `%s %s -h` for more details' % (PROGNAME, EDIT_SCHEDULES))
    edit_schedules.set_defaults(command=EDIT_SCHEDULES)

    help = subparsers.add_parser(HELP,
                                 help='display help - ' + 'see `%s %s -h` for more details' % (PROGNAME, HELP))
    help.add_argument(TOPIC, action='store', nargs='?', metavar=TOPIC,
                      help='the subject for help')
    help.set_defaults(command=HELP)

    package_fit_profile = subparsers.add_parser(PACKAGE_FIT_PROFILE,
                                                help='parse and save the global fit profile (dev only) - ' +
                                                     'see `%s %s -h` for more details' % (PROGNAME, PACKAGE_FIT_PROFILE))
    package_fit_profile.add_argument(PATH, action='store', metavar='PROFILE', nargs=1,
                                     help='the path to the profile (Profile.xlsx)')
    package_fit_profile.add_argument(m(W), mm(WARN), action='store', metavar='name',
                                     help='additional warning messages')
    package_fit_profile.set_defaults(command=PACKAGE_FIT_PROFILE)

    return parser

