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
import datetime

import jinja2
import ollama

from ._config import Config
from ._tools import Tool, ToolParser
from ._parsing import Parser


@dataclass
class Options:
  """The options for a generation call."""

  #: The number of output tokens
  tokens: int = None

  #: The output format (only "json" is acceptable)
  json: bool = False

  #: The generation temperature
  temperature: float = None

  #: The model to use for generation
  model: str = None

  def as_dict(self, config: Config) -> dict[str, any]:
    """Generates the correct keywords for calling Ollama."""
    d = {
        'num_predict': config.generation_tokens,
        'temperature': config.generation_temperature,
        'top_p': config.generation_topp,
        'top_k': config.generation_topk,
    }
    if self.tokens is not None:
      d['num_predict'] = self.tokens
    if self.temperature is not None:
      d['temperature'] = self.temperature
    if self.json:
      d['format'] = 'json'
    return d


@dataclass
class Prompt:
  """A prompt with substitutable variables.

  BaDinka prompts use the complete [Jinja2]() templating language."""

  #: The template content as a string.
  template: str

  def render(self, **prompt_params: dict[str, any]) -> str:
    """Render the template with the given prompt parameters."""
    t = jinja2.Template(self.template)
    return t.render(**prompt_params)


@dataclass
class Injection:
  """Context injection parameters to populate the prompt context."""

  #: The number of results to populate the context.
  n_results: int = 10


@dataclass
class Instruction:
  """The instruction to generate for an LLM

  This is a high-level construct which contains a bunch of different parts to
  build a prompt for an LLM:

  * The prompt is the prompt that will generate the final query for the LLM.
    This is a jinja2 template which can be substituted with parameters during
    the render.
  * The context. You can populate this manually, or you can use the injection
    to automatically generate it from the document store based on the query.
  * The role describes how you want the LLM to behave. This can be a person,
    such as "teacher" or describe the behavioural attributes of the LLM.
  * Tools define external tools that can be called by the generation.
  * Injection defines how the context will be populated from the document store
    with the query parameters. 

  """

  #: The prompt that provides the last part of the instruction.
  prompt: Prompt|str = None

  #: The query that provides the last part of the instruction.
  #: Query is provided here as a prompt with no substitutions to save typing
  #: when a plain prompt is needed.
  query: str = ''

  #: The parameters that control whether context is injected.
  inject: Injection = None

  #: The behavioural role that the generation will take.
  role: str = None

  #: The tone that the generation should take.
  tone: str = None

  #: The detail at which to generate
  detail: str = None

  #: The prompt context. If provided, the LLM will be given the context and
  #: instructed to use it to generate its response.
  #: Note: when an injection is provided this is overriden.
  context: str = None

  #: The hard-coded text query. If the prompt is provided this will be overriden
  #: with the rendered prompt.
  query: str = None

  #: External tools to be called from the LLM
  tools: list[Tool] = field(default_factory=list)

  #: Parsers are response parsers
  parsers: list[Tool] = field(default_factory=list)

  #: The template for the complete instruction. This prompt has a default which
  #: can be overriden here.
  template: Prompt = field(
      default_factory=lambda: Prompt(
        template=default_instruction_template)
  )

  def rationalize(self):
    tool_parsers = [ToolParser(t) for t in self.tools]
    self.parsers = tool_parsers + self.parsers


  def render_query(self, **kw) -> str:
    """Renders the query part of the prompt."""
    if self.prompt:
      match self.prompt:
        case str():
          self.prompt = Prompt(self.prompt)
      return self.prompt.render(**kw)
    return self.query

  def render(self, **kw) -> str:
    """Renders the complete prompt."""
    q = self.render_query(**kw)
    p = self.template.render(
        role = self.role,
        tone = self.tone,
        detail = self.detail,
        context = self.context,
        tools = self.tools,
        query = q,
    )
    return p


@dataclass
class Reply:
  """Generated text from the LLM."""

  #: The text content of the reply.
  content: str

  #: The data is the parsed content of the reply
  data: any

  #: The model that was used for generation.
  model_name: str

  #: The date and time of the response.
  date: datetime.datetime

  #: The duration that the entire generation took.
  duration: int

  #: The duration of evaluation.
  eval_duration: int

  #: The duration of loading the model.
  load_duration: int

  #: The duration of the actual prompt.
  prompt_duration: int

  #: Tool
  tool: Tool = None

  #: Parser
  parser: Parser = None

  @classmethod
  def from_response(cls, resp):
    """Create this instance from the Ollama response."""
    return cls(
        content=resp['response'],
        data=resp['response'],
        date=datetime.datetime.fromisoformat(resp['created_at']),
        model_name=resp['model'],
        duration=resp['total_duration'],
        eval_duration=resp['eval_duration'],
        load_duration=resp['load_duration'],
        prompt_duration=resp['prompt_eval_duration'],
    )


@dataclass
class Chain:

  instructions: list[Instruction]



class Generator:
  """Generator calls LLMs and generates text."""

  def __init__(self, config: Config):
    self.config = config

  def generate_from_text(self, text: str,
      options: Options = None) -> Reply:
    """Generate a response from simple text."""
    if not options:
      options = Options()
    self.config.log.debug('generate request', prompt=text, options=options)
    self.config.log.in_message(text)
    resp = ollama.generate(
        model=options.model or self.config.generation_model,
        prompt=text,
        options=options.as_dict(self.config),
    )
    reply = Reply.from_response(resp)
    self.config.log.out_message(reply.content)
    self.config.log.debug('generate response', reply=reply)
    return reply

  def generate_from_prompt(self, prompt: Prompt,
      options: Options=None,
      **prompt_params) -> Reply:
    """Generate a response from a prompt with parameters."""
    t = prompt.render(**prompt_params)
    return self.generate_from_text(text=t, options=options)

  def generate_from_instruction(self, instruction: Instruction,
      options: Options=None,
      **prompt_params) -> Reply:
    """Generate a response from a complete instruction."""
    instruction.rationalize()
    t = instruction.render(**prompt_params)
    reply = self.generate_from_text(text=t, options=options)
    for p in instruction.parsers:
      if p.match(reply):
        reply.data = p.parse(reply)
        break
    self.config.log.debug('parsed response', reply=reply)
    return reply

  def generate_from_chain(self, chain: Chain, options: Options=None,
      **prompt_params):
    """Generate a response from a chain of instructions."""
    reply = None
    for instruction in chain.instructions:
      reply = self.generate_from_instruction(instruction, options,
          reply=reply,
          **prompt_params)
    return reply



#: The default template for an instruction.
default_instruction_template = """
{%- if role %}
You should behave as {{role}}.
{%- endif %}
{%- if tone %}
You should adopt a tone that is {{tone}}.
{%- endif %}
{%- if tools %}
You have the following tools available, if, and only if, you need to use
one of them, format your answer as :T:toolname:arguments, the arguments
should be in strict JSON format with an example provided for each tool, e.g.
for a tool called "name":"mytool", with "arguments":{"name": "string"}
:T:mytool:{"name":"string"}.
The format is very important because a computer will parse it strictly.
If you do not find a tool as the most appropriate way to reply, reply without
the use of the tool, using any other knowledge you have.
{%- for tool in tools %}
{{ tool.as_dict()|tojson(indent=2) }}
{%- endfor %}
{%- endif %}
{%- if context %}
Using only the following context, answer the question below
{%- if detail %} {{ detail }}{%- endif %}:

Context: {{context}}
{%- endif %}
{%- if check %}
Check your work and don't answer if you don't know.
{%- endif %}

{{query-}}
"""

# vim: ft=python sw=2 ts=2 sts=2 tw=80
