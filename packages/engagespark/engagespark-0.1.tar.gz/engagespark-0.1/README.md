# engageSPARK python SDK

## Prerequisites

What you need are your primary keys which are `token` and `organization_id` which you can find [here](https://ui.engagespark.com/#/api/docs). You can get your engagement ids in the engagements page. Having trouble looking for them? Try looking at our [support page](https://www.engagespark.com/support/how-can-i-use-your-api/)

Technical requirements:
- `python>=3.6`. Versions on python2 are unsupported. Other python3 versions are untested.

## Usage

```python
from engagespark import Client


client = Client(token='your_token_here')
subscribed_contacts = client.engagements.subscribe(
    engagement_id=1,
    contacts=[{'fullPhoneNumber': '639480896899'}],
    try_using_existing='newest',
)
print(subscribed_contacts)
```

## Docs

Engagements

- **`engagements.subscribe`**
  - Parameters:
    - `engagement_id`.
      - Type `int`.
      - Required.
    - `contacts`.
      - Type `list` or `dict`.
      - Required.
    - `try_using_existing`.
      - Only `newest` is supported as of the moment. Defaults to empty string `''`. If not specified, will always create the contact regardless of redundancy.
      - Optional


## Tests

Requirements:

    'mock>=2.0.0'
    'pytest==3.8.0'

You can run the tests via:

    $ pytest tests.py