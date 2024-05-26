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

"""Tiny wrapper to generate the BaDinka reference docs"""


import pdoc
import loguru

def write_module(name, html):
  path = f'docs/public/{name}.html'
  loguru.logger.info(f'{name} -> {path}')
  with open(path, 'w') as f:
    f.write(html)

def main():
  context = pdoc.Context()
  mod = pdoc.Module('badinka', context=context)
  write_module('index', mod.html())

if __name__ == '__main__':
  main()

# vim: ft=python sw=2 ts=2 sts=2 tw=120
