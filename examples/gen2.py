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

"""LLM generation with prompt substitution

### Rendered prompt

> Decsribe the effect of interest rates on house prices.

### Output (e.g.)

> **Interest rates have a significant impact on house prices:**
> 
> **1. Rising Interest Rates:**
> 
> * Increased borrowing costs reduce affordability.
> * Reduced demand can lead to lower house prices.
> * Investors may reduce investment in the housing market due to higher
>   borrowing costs.
> 
> 
> **2. Falling Interest Rates:**
> 
> * Lower borrowing costs increase affordability, making homeownership more
>   attainable.
> * Increased demand can drive up house prices.
> * Investors may become more active in the housing market due to lower
>   borrowing costs.
"""

import badinka as bd

def main():
  c = bd.Conductor()
  p = bd.Prompt('describe the effect of {{cause}} on {{effect}}')
  reply = c.generate(p, cause='interest rates', effect='house prices')
  print(reply.content)


if __name__ == '__main__':
  main()


# vim: ft=python sw=2 ts=2 sts=2 tw=80
