"""Template Provider Module."""

from openbb_core.provider.abstract.provider import Provider

# import openbb_template.models import TemplateFetcher
template_provider = Provider(
    name="template",
    website="https://template.source",
    description=(
        "This is a template provider. Please replace this with the actual text."
    ),
    fetcher_dict={
        # "StandardModel": "TemplateFetcher",
    },
)
