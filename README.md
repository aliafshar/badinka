# BaDinka




# Examples


## Basic LLM generation

[view file: gen0.py](examples/gen0.py)

### Rendered prompt

> why is the sky blue?

### Output example

> Reply(content='**The sky is blue due to two main factors:**

**1. Ra...'
>       model_name='gemma',
>       date=datetime.datetime(2024, 5, 26, 16, 47, 56, 317100,
>           tzinfo=datetime.timezone.utc),
>       duration=72159197130,
>       eval_duration=63221428000,
>       load_duration=4498268186,
>       prompt_duration=4437450000)

### Code

```python
def main():
  c = bd.Conductor()
  reply = c.generate('why is the sky blue?')
  print(reply)


if __name__ == '__main__':
  main()
```



## rag0.py a hello world of retrieval augmented generation.

[view file: rag0.py](examples/rag0.py)

# Rendered prompt

> You should behave as a gullible person.
> Using only the following context, answer the question below:
>
> Context: the sky is blue because of fairies
>
> why is the sky blue?

# Output example

> Because of fairies, of course! They must be sprinkling
> the clouds with magical glitter that makes them all blue.

### Code

```python
import badinka as bd

def main():
  c = bd.Conductor()
  # You would usually create the database in a separate step and reuse it.
  # Here we create it on the fly.
  c.docs.append(
      bd.Document(content='the sky is blue because of fairies'),
  )
  reply = c.generate(
    bd.Instruction(
      role = 'a gullible person', # The AI is too smart otherwise.
      prompt = bd.Prompt('why is the sky blue?'),
      # Performs a document search and inserts the results into the context.
      inject = bd.Injection(),
    ),
    options = bd.Options(
      output_tokens=32,
    ),
  )
  print(reply.content)


if __name__ == '__main__':
  main()
```





