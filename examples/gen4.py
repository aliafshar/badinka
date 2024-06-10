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

"""LLM generation with JSON output

### Rendered prompt

> Name some things in the sky, and their color, in JSON

### Output (e.g.)

```json
{
  "sky_elements": [
    {
      "name": "Sun",
      "color": "#FFD700"
    },
    {
      "name": "Moon",
      "color": "#FFFFFF"
    }
  ]
}
```
"""

import badinka as bd

def main():
  c = bd.Conductor()
  reply = c.generate(
      'Name some things in the sky, and their colour, in JSON',
      options=bd.Options(
        json=True,
        tokens=1024,
      ),
  )
  print(reply.content)


if __name__ == '__main__':
  main()


# vim: ft=python sw=2 ts=2 sts=2 tw=80
