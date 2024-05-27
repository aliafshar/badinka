# BaDinka

**Minimalist AI orchestration library for local LLMs**


## What is a minimalist orchestration framework

BaDinka provides the following:

1. Model generation with Gemma (or other Ollama models)
2. Document storage with Chromadb

and simplifies the connection between them in order to prompt the LLM with
instructions.




# Examples


## Basic LLM generation
View/Download source: [gen0.py](examples/gen0.py)
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
View/Download source: [rag0.py](examples/rag0.py)
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


# Motivation

(obligatory stream of consciousness)

Most orchestration frameworks are built to integrate every possible combination
of models, databases, etc. possible and are very good at making it possible to
swap components out. BaDinka is not that framework.

BaDinka doesn't particularly focus on the concept or arbitrary pipelines either.
I found, while using Langchain and Haystack (two excellent frameworks you should
probably check out if you are using Python) that things became overly complex,
but overly un-granular, and in an effort to support *everything*, that *nothing*
was particularly well supported. This is not a criticism, but a common effect of
generalization in software development - the lowest common denominator effect.



