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

"""Calling an external tool from a prompt

### Rendered prompt

> You have the following tools available, if, and only if, you need to use
> one of them, format your answer as :T:toolname:arguments, the arguments
> should be in strict JSON format with an example provided for each tool, e.g.
> for a tool called "name":"mytool", with "arguments":{"name": "string"}
> 
> :T:mytool:{"name":"string"}.
> 
> The format is very important because a computer will parse it strictly.
> If you do not find a tool as the most appropriate way to reply, reply without
> the use of the tool, using any other knowledge you have.
> {
>   "arguments": {
>     "command": "string"
>   },
>   "description": "execute a shell command",
>   "name": "exec"
> }
> 
> execute the command "fortune"


### Output (e.g.)

> O, what a tangled web we weave, When first we practice to deceive.
>	              -- Sir Walter Scott, "Marmion"
"""

import subprocess
import badinka as bd

class ExecTool(bd.Tool):
  """A tool to execute arbitrary shell commands (!)"""

  name = 'exec'
  description = 'execute a shell command'
  arguments = {'command': 'string'}

  def do(self, **kw):
    return subprocess.check_output(
        kw['command'], shell=True, encoding='utf-8')


def main():
  c = bd.Conductor(bd.Config())
  reply = c.generate(
      bd.Instruction(
        query='execute the command "fortune"',
        tools=[ExecTool()]
      ),
  )
  print(reply.content)
  print(reply.data)



if __name__ == '__main__':
  main()


# vim: ft=python sw=2 ts=2 sts=2 tw=80
