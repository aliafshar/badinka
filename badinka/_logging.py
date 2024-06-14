# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Logging for minimal in-memory use cases."""

import os
import sys
import enum
import inspect
import atexit
import pprint
import textwrap
from datetime import timedelta, datetime
from dataclasses import dataclass, field


class Ansi:
  """Handle ANSI color codes """
  YELLOW = "\033[1;33m"
  RED = "\033[1;31m"
  GREEN = "\033[1;32m"
  BLUE = "\033[1;34m"
  PURPLE = "\033[1;35m"
  CYAN = "\033[1;36m"
  WHITE = "\033[1;37m"
  ITALIC = "\033[3m"
  UNDERLINE = "\033[4m"
  FAINT = "\033[2m"
  BOLD = "\033[1m"
  END = "\033[0m"

  def __call__(self, text, color):
    return f'{color}{text}{Colors.END}'

ansi = Ansi()

class Colors:
  """Handle ANSI color codes """
  YELLOW = "\033[1;33m"
  RED = "\033[1;31m"
  GREEN = "\033[1;32m"
  BLUE = "\033[1;34m"
  PURPLE = "\033[1;35m"
  CYAN = "\033[1;36m"
  WHITE = "\033[1;37m"
  ITALIC = "\033[3m"
  UNDERLINE = "\033[4m"
  FAINT = "\033[2m"
  BOLD = "\033[1m"
  END = "\033[0m"

  @staticmethod
  def colored(text, style):
    return f'{style}{text}{Colors.END}'


@dataclass
class LogConfig:
  immediate: bool = False
  dump_at_exit: bool = False


class LogLevel(enum.Enum):
  SYSTEM = 0
  DEBUG = 1
  INFO = 2
  WARNING = 3
  ERROR = 4


@dataclass
class LogEntry:
  level: LogLevel
  message: str
  caller: str
  callfile: str
  parameters: dict[str, any] = field(default_factory=dict)
  date: datetime = field(default_factory=datetime.now)
  since: timedelta = field(default_factory=timedelta)

  @property
  def p_color(self):
    return {
        LogLevel.SYSTEM: Colors.FAINT,
        LogLevel.DEBUG: Colors.GREEN,
        LogLevel.INFO: Colors.BLUE,
        LogLevel.WARNING: Colors.YELLOW,
        LogLevel.ERROR: Colors.RED,
    }[self.level]

  @property
  def p_time(self):
    return Colors.colored(f'{self.since.seconds:>4}', Colors.CYAN)

  @property
  def p_level(self):
    return Colors.colored(f'{self.level.name:>7}', self.p_color)

  @property
  def p_caller(self):
    return Colors.colored(f'{self.caller}', Colors.WHITE)

  @property
  def p_callfile(self):
    return Colors.colored(f'{self.callfile}', Colors.ITALIC)

  @property
  def p_parameters(self):
    if not self.parameters:
      return ''
    raw = pprint.pformat(self.parameters).split('\n')
    lines = ['']
    for l in raw:
      c = Colors.colored(l, Colors.PURPLE)
      lines.append(f'     | {c}')
    return '\n'.join(lines)

  @property
  def p_message(self):
    return Colors.colored(f'{self.message}', self.p_color)


  def printable(self):
    return (f'{self.p_time:>4} | {self.p_level} | '
            f'{self.p_caller} {self.p_callfile} | '
            f'{self.p_message}{self.p_parameters}')

class Log:

  def __init__(self, config: LogConfig=None):
    self.config = config or LogConfig()
    self.entries: list[Log] = []
    atexit.register(self.exit)
    self.system('logging begins')

  def exit(self):
    if self.config.dump_at_exit:
      self.dump()

  def log(self, level, message='', **kw):
    frame = inspect.stack()[2]
    fn = os.path.basename(frame.filename)
    e = LogEntry(
          level=level,
          message=message,
          parameters=kw,
          caller=frame.function,
          callfile=f'{fn}:{frame.lineno}',
    )
    self.entries.append(e)
    if self.config.immediate:
      print(e.printable())

  def system(self, message='', **kw):
    self.log(LogLevel.SYSTEM, message, **kw)

  def debug(self, message='', **kw):
    self.log(LogLevel.DEBUG, message, **kw)

  def info(self, message='', **kw):
    self.log(LogLevel.INFO, message, **kw)

  def warning(self, message='', **kw):
    self.log(LogLevel.WARNING, message, **kw)

  def error(self, message='', **kw):
    self.log(LogLevel.ERROR, message, **kw)

  def message(self, block, prefix):
    blines = block.strip().splitlines()
    olines = []
    for line in blines:
      for wline in textwrap.wrap(line, 70):
        olines.append(f'{prefix} {wline}')
    print('\n'.join(olines))

  def in_message(self, block):
    self.message(block, ansi('I', Ansi.GREEN))

  def out_message(self, block):
    self.message(block, ansi('O', Ansi.BLUE))



  @property
  def p_date(self):
    return Colors.colored(self.entries[0].date, Colors.CYAN)

  @property
  def p_name(self):
    return Colors.colored(f'badinka', Colors.PURPLE)

  @property
  def p_intro(self):
    d = f' {self.p_name}@{self.p_date} '
    g = ' ' * len(d)
    return f'{g}\n{d}\n{g}'

  def dump(self):
    print(self.p_intro)
    for e in self.entries:
      print(e.printable())



if __name__ == '__main__':
    log = Log()
    log.debug('I am a debug')
    log.info('I am an info')
    log.warning('I am a warning')
    log.error('I am an error')
    log.print()


# vim: ft=python sw=2 ts=2 sts=2 tw=80
