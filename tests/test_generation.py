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


import datetime
import pytest
import badinka



example_response = {
 'context': [106,
             108],
 'created_at': '2024-05-23T08:34:32.980570344Z',
 'done': True,
 'eval_count': 16,
 'eval_duration': 2157026000,
 'load_duration': 3495130037,
 'model': 'gemma:2b',
 'prompt_eval_count': 15,
 'prompt_eval_duration': 1510910000,
 'response': 'The sky appears blue due to Rayleigh scattering.\n'
             '\n'
             '**Rayleigh Scattering:**\n'
             '\n',
 'total_duration': 7163785403
}

example_date = datetime.datetime(
    2024, 5, 23, 8, 34, 32, 980570,
    tzinfo=datetime.timezone.utc)

def test_template():
  p = badinka.Prompt(template='why is the sky {{q}}?')
  assert 'why is the sky blue?' == p.render(q='blue')

@pytest.mark.skipif("not config.getoption('integration')")
def test_generate_from_prompt():
  p = badinka.Prompt(template='why is the sky {{q}}?')
  g = badinka.Generator(badinka.Config(
    generation_model='orca-mini',
  ))
  g.generate_from_prompt(p, q='blue')

@pytest.mark.skipif("not config.getoption('integration')")
def test_generate_from_instruction():
  i = badinka.Instruction(
      prompt = badinka.Prompt(
        template='why is the sky {{q}}?'
      ),
      role = 'comedian',
      tone = 'amusing',
  )
  g = badinka.Generator(badinka.Config(
    generation_model='orca-mini',
  ))
  g.generate_from_instruction(i, q='blue')

@pytest.mark.skipif("not config.getoption('integration')")
def test_generate_from_instruction_context():
  i = badinka.Instruction(
      prompt = badinka.Prompt(
        template='how do you stay {{q}}?'
      ),
      role = 'a scientist',
      tone = 'classical like virgil',
      context = 'an apple a day keeps the doctor away',
  )
  g = badinka.Generator(badinka.Config(
    generation_model='orca-mini',
  ))
  g.generate_from_instruction(i, q='healthy')

def test_reply_from_response():
  repl = badinka.Reply.from_response(example_response)
  assert example_response['response'] == repl.content
  assert example_date == repl.date

# vim: ft=python sw=2 ts=2 sts=2 tw=120
