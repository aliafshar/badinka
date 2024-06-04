{#- This is the template that generates the README -#}

# BaDinka

**{{ subtitle }}**

Skip this, go straight to the [API Docs](https://badinka-website.web.app/).

{{ howto }}


# Examples

{% for example in examples %}
## {{ example.summary }}
View/Download source: [{{example.filename}}]({{ example.path }})
{{ example.description }}
### Code
```python
{{ example.source }}
```
{% endfor %}

{{ motivation }}



