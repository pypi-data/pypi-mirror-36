{{ header }}
{{ "-" * header_line_length }}

.. toctree::
   :maxdepth: 1

    {% for article in article_list -%}
    {{ article.title }} <{{ article.path }}>
    {% endfor -%}
