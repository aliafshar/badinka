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

"""gen0.py a hello world of generation.

# Rendered prompt

> why is the sky blue?

# Output example

> Reply(content='**The sky is blue due to two main factors:**\n\n**1. Ra...'
>       model_name='gemma',
>       date=datetime.datetime(2024, 5, 26, 16, 47, 56, 317100,
>           tzinfo=datetime.timezone.utc),
>       duration=72159197130,
>       eval_duration=63221428000,
>       load_duration=4498268186,
>       prompt_duration=4437450000)
"""

import badinka as bd


def main():
  c = bd.Conductor()
  reply = c.generate('why is the sky blue?')
  print(reply)


if __name__ == '__main__':
  main()


# vim: ft=python sw=2 ts=2 sts=2 tw=80
