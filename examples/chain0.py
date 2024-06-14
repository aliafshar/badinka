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

"""Basic chaining generation

### Input / Output (e.g.)

> > pick a 4-letter word
>
> Yard
>
> > describe this word: Yard
>
> A yard is a unit of measurement commonly used to describe length or
> distance. It is equal to 3 feet or 0.914 meters. Yards are often used
> to measure the size of lawns, gardens, fields, or other outdoor
> spaces.
>
> > You should behave as a poet.
> > rephrase this: A yard is a unit of measurement commonly used to
> > describe length or distance. It is equal to 3 feet or 0.914 meters.
> > Yards are often used to measure the size of lawns, gardens, fields, or
> > other outdoor spaces.
>
> A yard, a measure of length untold,
> Three feet it stands, a story bold.
> From lawn to field, a verdant trace,
> Each yard a canvas, time and space.
"""

import badinka as bd


def main():
  c = bd.Conductor()
  reply = c.generate(bd.Chain([
    bd.Instruction(prompt='pick a 4-letter word'),
    bd.Instruction(prompt='describe this word: {{reply.data}}'),
    bd.Instruction(role='a poet', prompt='rephrase this: {{reply.data}}'),
  ]))
  print(reply.content)


if __name__ == '__main__':
  main()


# vim: ft=python sw=2 ts=2 sts=2 tw=80
