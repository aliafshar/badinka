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



from dataclasses import dataclass, field

import jinja2
import ollama
import datetime


@dataclass
class Options:
  output_tokens: int = 128

  def as_dict(self):
    return {
        'num_predict': self.output_tokens,
    }

@dataclass
class Prompt:
  template: str

  def render(self, **kw):
    t = jinja2.Template(self.template)
    return t.render(**kw)


@dataclass
class Injection:
  n_results: int = 10

@dataclass
class Instruction:

  prompt: Prompt

  inject: Injection = None

  role: str = None
  tone: str = None
  context: str = None
  query: str = None
  template: Prompt = field(
      default_factory=lambda: Prompt(template=default_instruction_template)
  )

  def render_query(self, **kw):
    return self.prompt.render(**kw)

  def render(self, **kw):
    q = self.render_query(**kw)
    p = self.template.render(
        role = self.role,
        tone = self.tone,
        context = self.context,
        query = q,
    )
    return p



@dataclass
class Reply:
  content: str
  model_name: str
  date: datetime.datetime
  duration: int
  eval_duration: int
  load_duration: int
  prompt_duration: int

  @classmethod
  def from_response(cls, resp):
    return cls(
        content=resp['response'],
        date=datetime.datetime.fromisoformat(resp['created_at']),
        model_name=resp['model'],
        duration=resp['total_duration'],
        eval_duration=resp['eval_duration'],
        load_duration=resp['load_duration'],
        prompt_duration=resp['prompt_eval_duration'],
    )


class Generator:

  def __init__(self, config):
    self.config = config

  def generate_from_text(self, text: str, options: Options = None):
    if not options:
      options = Options()
    self.config.log.debug(text)
    resp = ollama.generate(
        model=self.config.generation_model_name,
        prompt=text,
        options=options.as_dict(),
    )
    reply = Reply.from_response(resp)
    self.config.log.debug(reply)
    return reply

  def generate_from_prompt(self, prompt: Prompt,
      options: Options=None,
      **prompt_params):
    t = prompt.render(**prompt_params)
    return self.generate_from_text(text=t, options=options)

  def generate_from_instruction(self, instruction: Instruction,
      options: Options=None,
      **prompt_params):
    t = instruction.render(**prompt_params)
    return self.generate_from_text(text=t, options=options)


default_instruction_template = """
{%- if role %}
You should behave as {{role}}.
{%- endif %}
{%- if tone %}
You should adopt a tone that is {{tone}}.
{%- endif %}
{%- if context %}
Using only the following context, answer the question below:

Context: {{context}}
{%- endif %}
{%- if check %}
Check your work and don't answer if you don't know.
{%- endif %}

{{query}}
"""

# vim: ft=python sw=2 ts=2 sts=2 tw=80
