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

"""All the gemmas

Run a query using the 4 gemma chat models.

### Output trace

**`gemma:2b`**
I You should behave as a gullible person.
I Using only the following context, answer the question below:
I Context: the sky is blue because of fairies
I why is the sky blue?
O The context does not provide information about why the sky is blue due
O to fairies, so I cannot answer this question from the context.

**`gemma`**
I You should behave as a gullible person.
I Using only the following context, answer the question below:
I Context: the sky is blue because of fairies
I why is the sky blue?
O The sky is blue because of fairies! They're tiny little creatures that
O sprinkle the sky with their magical dust, and that's what makes it
O blue.

**`gemma2`**
I You should behave as a gullible person.
I Using only the following context, answer the question below:
I Context: the sky is blue because of fairies
I why is the sky blue?
O Because of the fairies! They make it blue with their magic. ✨

**`gemma2:27b`**
I You should behave as a gullible person.
I Using only the following context, answer the question below:
I Context: the sky is blue because of fairies
I why is the sky blue?
O The sky is blue because... fairies? 🧚‍♀️✨
O They paint it every night with their magic wands, making sure it's
O nice and bright for the morning! 🌈☀️
"""

import badinka as bd

def main():
  c = bd.Conductor()
  # You would usually create the database in a separate step and reuse it.
  # Here we create it on the fly.
  c.docs.append(
      bd.Document(content='the sky is blue because of fairies'),
  )
  instruction = bd.Instruction(
      role = 'a gullible person', # The AI is too smart otherwise.
      prompt = bd.Prompt('why is the sky blue?'),
      # Performs a document search and inserts the results into the context.
      inject = bd.Injection(n_results=1),
  )
  for model in ['gemma:2b', 'gemma', 'gemma2', 'gemma2:27b']:
    print(f'**`{model}`**')
    reply = c.generate(
      instruction,
      options=bd.Options(
        model=model,
        tokens=64,
      ),
    )


if __name__ == '__main__':
  main()


# vim: ft=python sw=2 ts=2 sts=2 tw=80
