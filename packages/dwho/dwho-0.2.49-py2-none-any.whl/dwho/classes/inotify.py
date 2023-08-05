# -*- coding: utf-8 -*-
"""dwho inotify"""

__author__  = "Adrien DELLE CAVE <adc@doowan.net>"
__license__ = """
    Copyright (C) 2017-2018  doowan

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..
"""

import abc
import copy
import glob
import logging
import os
import pyinotify
import Queue
import sys

from dwho.classes.errors import DWhoConfigurationError, DWhoInotifyError
from dwho.classes.inoplugs import CACHE_EXPIRE, INOPLUGS, LOCK_TIMEOUT
from sonicprobe import helpers
from sonicprobe.libs.workerpool import WorkerPool
from threading import Thread

LOG             = logging.getLogger('dwho.inotify')

DWHO_INOQ       = Queue.Queue()

MODE_ADD        = 'MODE_ADD'
MODE_REM        = 'MODE_REM'

MAX_WORKERS     = 5

ALL_EVENTS      = ('access',
                   'attrib',
                   'create',
                   'close_write',
                   'close_nowrite',
                   'delete',
                   'delete_self',
                   'modify',
                   'move_self',
                   'moved_from',
                   'moved_to',
                   'open')

DEFAULT_CONFIG  = {'plugins':   dict(zip(INOPLUGS.keys(),
                                         [False] * len(INOPLUGS.keys()))),
                   'events':    ['create',
                                 'close_write',
                                 'move_self',
                                 'moved_to',
                                 'moved_from']}


class DWhoInotifyCfgPath(object):
    def __init__(self,
                 path,
                 event_mask     = 0,
                 plugins        = None,
                 do_glob        = False,
                 exclude_filter = None):
        self.path           = path
        self.event_mask     = event_mask
        self.plugins        = plugins
        self.do_glob        = do_glob
        self.exclude_filter = exclude_filter


class DWhoInotifyConfig(object):
    def __call__(self, notifier, conf):
        if not conf.has_key('plugins'):
            conf['plugins'] = DEFAULT_CONFIG['plugins'].copy()

        if not conf.has_key('events'):
            conf['events'] = list(DEFAULT_CONFIG['events'])

        if conf.has_key('exclude_files'):
            if isinstance(conf['exclude_files'], basestring):
                conf['exclude_files'] = [conf['exclude_files']]
            elif not isinstance(conf['exclude_files'], list):
                LOG.error('Invalid %s type. (%s: %r, section: %r)',
                          'exclude_files',
                          'exclude_files',
                          conf['exclude_files'],
                          'inotify')
                conf['exclude_files'] = []
        else:
            conf['exclude_files'] = []

        if not conf.has_key('paths') or not isinstance(conf['paths'], dict):
            raise DWhoConfigurationError("Missing paths configuration")

        for path, value in conf['paths'].iteritems():
            if not value.has_key('plugins'):
                value['plugins'] = conf['plugins'].copy()

            value['event_masks']    = 0

            if not value.has_key('events'):
                value['events'] = list(conf['events'])
            else:
                for event in value['events']:
                    if not event.startswith('-'):
                        continue
                    event = event[1:]
                    if event in value['events']:
                        value['events'].remove(event)

            if not value['events']:
                raise DWhoConfigurationError("Invalid configured events. (events: %r, path: %r)"
                                             % (value['events'], path))
            else:
                for event in value['events']:
                    if not self.valid_event(event):
                        raise DWhoConfigurationError("Invalid configured event: %r. (path: %r)"
                                                     % (event, path))
                    value['event_masks'] |= DWhoInotify.get_flag_value(event)

            if not value.has_key('exclude_files'):
                value['exclude_files'] = list(conf['exclude_files'])
            else:
                if isinstance(value['exclude_files'], basestring):
                    value['exclude_files'] = [value['exclude_files']]
                elif not isinstance(value['exclude_files'], list):
                    raise DWhoConfigurationError("Invalid exclude_files type. (exclude_files: %r, path: %r)"
                                                 % (value['exclude_files'], path))

                for exclude_file in value['exclude_files']:
                    if not exclude_file.startswith('-'):
                        continue
                    exclude_file = exclude_file[1:]
                    if exclude_file in value['exclude_files']:
                        value['exclude_files'].remove(exclude_file)

            value['exclude_patterns']   = set()

            if value['exclude_files']:
                for x in value['exclude_files']:
                    pattern = helpers.load_patterns_from_file(x)
                    if not pattern:
                        raise DWhoConfigurationError("Unable to load exclude patterns from %r. (path: %r)"
                                                     % (x, path))

                    value['exclude_patterns'].update(pattern)

            if value['exclude_patterns']:
                value['exclude_patterns'] = pyinotify.ExcludeFilter(list(value['exclude_patterns']))
            else:
                value['exclude_patterns'] = None

        for path, value in conf['paths'].iteritems():
            plugins     = []
            if value['plugins']:
                for plugin, options in value['plugins'].iteritems():
                    if not options:
                        continue
                    if INOPLUGS.has_key(plugin):
                        plugins.append(INOPLUGS[plugin])

            if not os.path.exists(path):
                helpers.make_dirs(path)

            notifier.add(DWhoInotifyCfgPath(path,
                                            value['event_masks'],
                                            plugins,
                                            value.get('glob'),
                                            value['exclude_patterns']))
        return conf

    @staticmethod
    def valid_event(event):
        return event in ALL_EVENTS


class DWhoInotifyWatchManager(pyinotify.WatchManager):
    def __init__(self, exclude_filter=lambda path: False):
        pyinotify.WatchManager.__init__(self, exclude_filter)

    def __format_path(self, path):
        """
        Format path to its internal (stored in watch manager) representation.
        """
        # Unicode strings are converted back to strings, because it seems
        # that inotify_add_watch from ctypes does not work well when
        # it receives an ctypes.create_unicode_buffer instance as argument.
        # Therefore even wd are indexed with bytes string and not with
        # unicode paths.
        if isinstance(path, unicode):
            path = path.encode(sys.getfilesystemencoding())
        return os.path.normpath(path)

    def __add_watch(self, path, mask, proc_fun, auto_add, exclude_filter):
        """
        Add a watch on path, build a Watch object and insert it in the
        watch manager dictionary. Return the wd value.
        """
        path = self.__format_path(path)
        if auto_add and not mask & pyinotify.IN_CREATE:
            mask |= pyinotify.IN_CREATE
        wd = self._inotify_wrapper.inotify_add_watch(self._fd, path, mask)
        if wd < 0:
            return wd
        watch = pyinotify.Watch(wd=wd, path=path, mask=mask, proc_fun=proc_fun,
                                auto_add=auto_add, exclude_filter=exclude_filter)
        self._wmd[wd] = watch
        LOG.debug('Added watch on path: %r', watch)
        return wd

    def __glob(self, path, do_glob):
        if do_glob:
            return glob.iglob(path)
        else:
            return [path]

    def add_watch(self, path, mask, proc_fun=None, rec=False,
                  auto_add=False, do_glob=False, quiet=True,
                  exclude_filter=None):
        """
        Add watch(s) on the provided |path|(s) with associated |mask| flag
        value and optionally with a processing |proc_fun| function and
        recursive flag |rec| set to True.
        Ideally |path| components should not be unicode objects. Note that
        although unicode paths are accepted there are converted to byte
        strings before a watch is put on that path. The encoding used for
        converting the unicode object is given by sys.getfilesystemencoding().
        If |path| is already watched it is ignored, but if it is called with
        option rec=True a watch is put on each one of its not-watched
        subdirectory.

        @param path: Path to watch, the path can either be a file or a
                     directory. Also accepts a sequence (list) of paths.
        @type path: string or list of strings
        @param mask: Bitmask of events.
        @type mask: int
        @param proc_fun: Processing object.
        @type proc_fun: function or ProcessEvent instance or instance of
                        one of its subclasses or callable object.
        @param rec: Recursively add watches from path on all its
                    subdirectories, set to False by default (doesn't
                    follows symlinks in any case).
        @type rec: bool
        @param auto_add: Automatically add watches on newly created
                         directories in watched parent |path| directory.
                         If |auto_add| is True, IN_CREATE is ored with |mask|
                         when the watch is added.
        @type auto_add: bool
        @param do_glob: Do globbing on pathname (see standard globbing
                        module for more informations).
        @type do_glob: bool
        @param quiet: if False raises a WatchManagerError exception on
                      error. See example not_quiet.py.
        @type quiet: bool
        @param exclude_filter: predicate (boolean function), which returns
                               True if the current path must be excluded
                               from being watched. This argument has
                               precedence over exclude_filter passed to
                               the class' constructor.
        @type exclude_filter: callable object
        @return: dict of paths associated to watch descriptors. A wd value
                 is positive if the watch was added sucessfully,
                 otherwise the value is negative. If the path was invalid
                 or was already watched it is not included into this returned
                 dictionary.
        @rtype: dict of {str: int}
        """
        ret_ = {} # return {path: wd, ...}

        if exclude_filter is None:
            exclude_filter = self._exclude_filter

        # normalize args as list elements
        for npath in self.__format_param(path):
            # unix pathname pattern expansion
            for apath in self.__glob(npath, do_glob):
                # recursively list subdirs according to rec param
                for rpath in self.__walk_rec(apath, rec, exclude_filter):
                    if not exclude_filter(rpath):
                        wd = ret_[rpath] = self.__add_watch(rpath, mask,
                                                            proc_fun,
                                                            auto_add,
                                                            exclude_filter)
                        if wd < 0:
                            err = ('add_watch: cannot watch %s WD=%d, %s' % \
                                       (rpath, wd,
                                        self._inotify_wrapper.str_errno()))
                            if quiet:
                                LOG.error(err)
                            else:
                                raise pyinotify.WatchManagerError(err, ret_)
                    else:
                        # Let's say -2 means 'explicitely excluded
                        # from watching'.
                        ret_[rpath] = -2
        return ret_

    def __get_sub_rec(self, lpath):
        """
        Get every wd from self._wmd if its path is under the path of
        one (at least) of those in lpath. Doesn't follow symlinks.

        @param lpath: list of watch descriptor
        @type lpath: list of int
        @return: list of watch descriptor
        @rtype: list of int
        """
        for d in lpath:
            root = self.get_path(d)
            if root is not None:
                # always keep root
                yield d
            else:
                # if invalid
                continue

            # nothing else to expect
            if not os.path.isdir(root):
                continue

            # normalization
            root = os.path.normpath(root)
            # recursion
            lend = len(root)
            for iwd in self._wmd.items():
                cur = iwd[1].path
                pref = os.path.commonprefix([root, cur])
                if root == os.sep or (len(pref) == lend and \
                                      len(cur) > lend and \
                                      cur[lend] == os.sep):
                    yield iwd[1].wd

    def __format_param(self, param):
        """
        @param param: Parameter.
        @type param: string or int
        @return: wrap param.
        @rtype: list of type(param)
        """
        if isinstance(param, list):
            for p_ in param:
                yield p_
        else:
            yield param

    def __walk_rec(self, top, rec, exclude_filter):
        if not rec or os.path.islink(top) or not os.path.isdir(top):
            yield top
        else:
            for root, dirs, files in os.walk(top, topdown = True):
                if exclude_filter(root):
                    dirs[:] = []
                yield root


class DWhoInotify(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.config      = None
        self.killed      = False
        self.cfg_paths   = {}
        self.name        = 'inotify'
        self.notifier    = None
        self.wm          = None
        self.workerpool  = None

    def init(self, config):
        self.config     = config
        self.workerpool = WorkerPool(max_workers = int(config['inotify'].get('max_workers') or MAX_WORKERS),
                                     life_time   = config['inotify'].get('worker_lifetime'),
                                     name        = 'inoworker')

        return self

    @staticmethod
    def add(cfg_path):
        DWHO_INOQ.put((MODE_ADD, cfg_path))

    @staticmethod
    def rem(cfg_path):
        DWHO_INOQ.put((MODE_REM, cfg_path))

    @staticmethod
    def get_flag_value(name):
        if pyinotify.EventsCodes.ALL_FLAGS.has_key(name):
            return pyinotify.EventsCodes.ALL_FLAGS.get(name)

        if not isinstance(name, basestring):
            return

        uname   = name.upper()
        if pyinotify.EventsCodes.ALL_FLAGS.has_key(uname):
            return pyinotify.EventsCodes.ALL_FLAGS.get(uname)

        uname   = "IN_%s" % uname
        if pyinotify.EventsCodes.ALL_FLAGS.has_key(uname):
            return pyinotify.EventsCodes.ALL_FLAGS.get(uname)

    @staticmethod
    def valid_flag(name):
        return DWhoInotify.get_flag_value(name) is not None

    def get_cfg_path(self, path):
        if self.cfg_paths.has_key(path):
            LOG.debug("path: %r, wd_path: %r, common: %r",
                      path,
                      path.rstrip(os.sep),
                      os.path.commonprefix([path, path]))
            return self.cfg_paths[path]

        try:
            cfg_paths = self.cfg_paths.copy()
            for wd_path in cfg_paths.iterkeys():
                if os.path.commonprefix([path, wd_path]) == wd_path.rstrip(os.sep):
                    LOG.debug("path: %r, wd_path: %r, common: %r",
                              path,
                              wd_path.rstrip(os.sep),
                              os.path.commonprefix([path, wd_path]))
                    return self.cfg_paths[wd_path]
        finally:
            cfg_paths = None

    def __add_watch(self, cfg_path):
        LOG.debug("Add watch. (path: %r, mask: %r, plugins: %r, glob: %r)",
                  cfg_path.path,
                  cfg_path.event_mask,
                  cfg_path.plugins,
                  cfg_path.do_glob)

        try:
            wdd = self.wm.add_watch(cfg_path.path,
                                    cfg_path.event_mask,
                                    rec             = True,
                                    auto_add        = True,
                                    quiet           = False,
                                    do_glob         = cfg_path.do_glob,
                                    exclude_filter  = cfg_path.exclude_filter)

            for wpath, wcode in wdd.iteritems():
                if wcode == -2:
                    LOG.debug("Path excluded. (path: %r, code: %r)", wpath, wcode)
                elif wcode < 0:
                    LOG.error("Unable to monitor. (path: %r, code: %r)", wpath, wcode)
                else:
                    self.cfg_paths[wpath] = cfg_path
        except pyinotify.WatchManagerError, e:
            LOG.exception("Unable to monitor. (path: %r, reason: %r)", cfg_path.path, e)
        finally:
            wdd = None

    def __rem_watch(self, cfg_path):
        if not self.cfg_paths.has_key(cfg_path.path):
            return

        LOG.debug("Remove watch. (path: %r, mask: %r, plugins: %r, glob: %r)",
                  cfg_path.path,
                  cfg_path.event_mask,
                  cfg_path.plugins,
                  cfg_path.do_glob)

        try:
            self.wm.rm_watch(cfg_path.path, rec = True, quiet = False)
        except pyinotify.WatchManagerError, e:
            LOG.exception("Unable to unmonitor. (path: %r, reason: %r)", cfg_path.path, e)
        else:
            del self.cfg_paths[cfg_path.path]

    def run(self):
        self.wm         = DWhoInotifyWatchManager()
        self.notifier   = pyinotify.ThreadedNotifier(self.wm,
                                                     DWhoInotifyEventHandler(**{'dw_inotify': self}))
        self.notifier.start()

        while not self.killed:
            try:
                (mode, cfg_path) = DWHO_INOQ.get(True, 0.5)
                if mode == MODE_ADD:
                    self.__add_watch(cfg_path)
                elif mode == MODE_REM:
                    self.__rem_watch(cfg_path)
                else:
                    raise DWhoInotifyError("Invalid mode: %r" % mode)
            except Queue.Empty:
                pass

        self.notifier.stop()

    def stop(self):
        self.killed = True
        self.workerpool.killall(0)


class DWhoInotifyPlugs(Thread):
    THREADNAME = 'inoplugs'

    def __init__(self, config, cfg_path, event, filepath):
        Thread.__init__(self)

        self.cache_expire = config['inotify'].get('cache_expire', CACHE_EXPIRE)
        self.config       = config
        self.cfg_path     = cfg_path
        self.event        = event
        self.filepath     = filepath
        self.timeout      = config['inotify'].get('lock_timeout', LOCK_TIMEOUT)
        self.server_id    = config['general']['server_id']
        self.name         = self.THREADNAME

    def run(self):
        for plugin in self.cfg_path.plugins:
            plug = None
            try:
                plug      = copy.copy(plugin)
                self.name = "%s:%s" % (self.THREADNAME, plug.PLUGIN_NAME)

                LOG.debug("Starting plugin %s. (filename: %r, thread: %r)",
                          plug.PLUGIN_NAME,
                          self.filepath,
                          self.name)

                plug(self.cfg_path, self.event, self.filepath)

                LOG.debug("Stopping plugin %s. (filename: %r, thread: %r)",
                          plug.PLUGIN_NAME,
                          self.filepath,
                          self.name)

                self.name = self.THREADNAME
            except Exception, e:
                LOG.exception("Error during plugin. (error: %r, filename: %r)",
                              e,
                              self.filepath)
            finally:
                if plug:
                    del plug

    def __call__(self):
        return self.run()


class DWhoInotifyEventHandler(pyinotify.ProcessEvent):
    def my_init(self, dw_inotify, plugs_class = DWhoInotifyPlugs, workerpool = None):
        self.dw_inotify  = dw_inotify
        self.workerpool  = workerpool or dw_inotify.workerpool
        self.plugs_class = plugs_class

    def call_plugins(self, cfg_path, event, include_plugins = [], exclude_filter = None):
        if not cfg_path.plugins:
            LOG.warning("No plugin enabled")
            return

        if not include_plugins:
            conf_path = cfg_path
        else:
            conf_path = copy.copy(cfg_path)
            plugins   = list(conf_path.plugins)
            for plugin in plugins:
                if plugin.PLUGIN_NAME not in include_plugins:
                    conf_path.plugins.remove(plugin)

        if not conf_path.plugins:
            LOG.warning("No plugin included")
            return

        if not hasattr(event, 'pathname'):
            LOG.warning("Missing pathname in Event. (event: %r)", event)
            return

        filepath = event.pathname

        try:
            os.path.isfile(filepath)
        except UnicodeEncodeError:
            LOG.exception("Encoding error file: %r", filepath)
            return

        if exclude_filter is not False:
            if exclude_filter:
                if exclude_filter(filepath):
                    LOG.debug("Exclude file from scan. (filepath: %r)", filepath)
                    return
            elif conf_path.exclude_filter and conf_path.exclude_filter(filepath):
                LOG.debug("Exclude file from scan. (filepath: %r)", filepath)
                return

        self.workerpool.run(self.plugs_class(self.dw_inotify.config, conf_path, event, filepath))

    def process_IN_ACCESS(self, event):
        cfg_path  = self.dw_inotify.get_cfg_path(event.path)
        if cfg_path:
            self.call_plugins(cfg_path, event)

        LOG.debug("DWhoInotifyEvent reports that an ACCESS event has occurred. (event: %r)", event)

    def process_IN_ATTRIB(self, event):
        cfg_path  = self.dw_inotify.get_cfg_path(event.path)
        if cfg_path:
            self.call_plugins(cfg_path, event)

        LOG.debug("DWhoInotifyEvent reports that an ATTRIB event has occurred. (event: %r)", event)

    def process_IN_CREATE(self, event):
        cfg_path  = self.dw_inotify.get_cfg_path(event.path)
        if cfg_path:
            self.call_plugins(cfg_path, event)

        LOG.debug("DWhoInotifyEvent reports that a CREATE event has occurred. (event: %r)", event)

    def process_IN_CLOSE_WRITE(self, event):
        cfg_path  = self.dw_inotify.get_cfg_path(event.path)
        if cfg_path:
            self.call_plugins(cfg_path, event)

        LOG.debug("DWhoInotifyEvent reports that a CLOSE_WRITE event has occurred. (event: %r)", event)

    def process_IN_CLOSE_NOWRITE(self, event):
        cfg_path  = self.dw_inotify.get_cfg_path(event.path)
        if cfg_path:
            self.call_plugins(cfg_path, event)

        LOG.debug("DWhoInotifyEvent reports that a CLOSE_NOWRITE event has occurred. (event: %r)", event)

    def process_IN_DELETE(self, event):
        cfg_path  = self.dw_inotify.get_cfg_path(event.path)
        if cfg_path:
            self.call_plugins(cfg_path, event)

        LOG.debug("DWhoInotifyEvent reports that a DELETE event has occurred. (event: %r)", event)

    def process_IN_DELETE_SELF(self, event):
        cfg_path  = self.dw_inotify.get_cfg_path(event.path)
        if cfg_path:
            self.call_plugins(cfg_path, event)

        LOG.debug("DWhoInotifyEvent reports that a DELETE_SELF event has occurred. (event: %r)", event)

    def process_IN_MODIFY(self, event):
        cfg_path  = self.dw_inotify.get_cfg_path(event.path)
        if cfg_path:
            self.call_plugins(cfg_path, event)

        LOG.debug("DWhoInotifyEvent reports that a MODIFY event has occurred. (event: %r)", event)

    def process_IN_MOVE_SELF(self, event):
        cfg_path  = self.dw_inotify.get_cfg_path(event.path)
        if cfg_path:
            self.call_plugins(cfg_path, event)

        LOG.debug("DWhoInotifyEvent reports that a MOVE_SELF event has occurred. (event: %r)", event)

    def process_IN_MOVED_FROM(self, event):
        cfg_path  = self.dw_inotify.get_cfg_path(event.path)
        if cfg_path:
            self.call_plugins(cfg_path, event)

        LOG.debug("DWhoInotifyEvent reports that a MOVED_FROM event has occurred. (event: %r)", event)

    def process_IN_MOVED_TO(self, event):
        cfg_path  = self.dw_inotify.get_cfg_path(event.path)
        if cfg_path:
            self.call_plugins(cfg_path, event)

        LOG.debug("DWhoInotifyEvent reports that a MOVED_TO event has occurred. (event: %r)", event)

    def process_IN_OPEN(self, event):
        cfg_path  = self.dw_inotify.get_cfg_path(event.path)
        if cfg_path:
            self.call_plugins(cfg_path, event)

        LOG.debug("DWhoInotifyEvent reports that an OPEN event has occurred. (event: %r)", event)

    def process_IN_Q_OVERFLOW(self, event):
        LOG.debug("DWhoInotifyEvent reports that a Q_OVERFLOW event has occurred. (event: %r)", event)

    def process_default(self, event):
        LOG.debug("DWhoInotifyEvent reports that an unsupported event has occurred. (event: %r)", event)
