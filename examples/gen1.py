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

"""LLM generation with instruction

### Rendered prompt

> You should behave as a poet.
> 
> why is the sky blue?

### Output (e.g.)

> In fields of clouds, where whispers meet,
> The sun's embrace, a gentle heat.
> Through scattered threads, a cosmic dance,
> Ray meets molecule, chance meets chance.
> 
> Blue, the hue that fills the frame,
> A symphony of scattered name.
> Rayleigh's dance, a wondrous sight,
> Explains the sky's ethereal light.
"""

import badinka as bd

def main():
  c = bd.Conductor()
  reply = c.generate(
      bd.Instruction(
        role='a poet',
        query='why is the sky blue?',
      ),
  )
  print(reply.content)


if __name__ == '__main__':
  main()


# vim: ft=python sw=2 ts=2 sts=2 tw=80
