# python-lyrebird--vocal-avatar

`python-lyrebird-vocal-avatar` is the Python SDK for [Lyrebird.ai](http://lyrebird.ai).

## Install

Using `pip`:
```bash
pip install lyrebird-vocal-avatar
```

From source:
```bash
git clone https://github.com/lyrebird-ai/python-vocal-avatar
pip install .
```

## Usage

See the `examples` folder for examples.

## API

### Overview

`lyrebird-vocal-avatar` provides a Lyrebird class with the following methods:
* `generate` - the Lyrebird Vocal Avatar [generate endpoint](http://docs.lyrebird.ai/reference-avatar/api.html#tag/Audio/paths/~1generate/post)
* `generated` - the Lyrebird Vocal Avatar [generated endpoint](http://docs.lyrebird.ai/reference-avatar/api.html#tag/Audio/paths/~1generated/get)

### Lyrebird class

The Lyrebird constructor takes the following parameters:
* `access_token` - the Access Token of your Lyrebird instance

A minimal example looks like this:

```python
from lyrebird import Lyrebird

client = Lyrebird(access_token)
client.generate('Hello World')
```

### .generate()

The Lyrebird Vocal Avatar [generate endpoint](http://docs.lyrebird.ai/reference-avatar/api.html#tag/Audio/paths/~1generate/post)

Takes the following parameters:
* `text` - the text you want the Lyrebird Vocal Avatar to synthethize

Example:
```python
resp = client.generate('Hello World')
with open('hello_world.wav', "w+") as audio_file:
    audio_file.write(resp.content)
```

### .generated()

the Lyrebird Vocal Avatar [generated endpoint](http://docs.lyrebird.ai/reference-avatar/api.html#tag/Audio/paths/~1generated/get)

Takes the following parameters:
* `offset` - the offset of the first returned paginated element from the beginning of the result set, defaults to 0
* `limit` - the maximum count of returned paginated elements, defaults to 10

Example:
```python
# Get the last two generated utterances
generated_resp = client.generated(0, 2)
generated_resp_json = generated_resp.json()
```

See the [docs](http://docs.lyrebird.ai/) for more information.


### Logging

Default logging is to `STDOUT` with `INFO` level.

You can set your logging level as follows:
``` python
from lyrebird import Lyrebird
import logging

logging.basicConfig()
logger = logging.getLogger('logger')

client = Lyrebird(acces_token, logger)
client.logger.setLevel(logging.WARNING)
```

You can also specify a custom logger object in the Lyrebird constructor:
``` python
from lyrebird import Lyrebird
client = Lyrebird(access_token=access_token, logger=custom_logger)
```

See the [logging module](https://docs.python.org/2/library/logging.html) and
[logging.config](https://docs.python.org/2/library/logging.config.html#module-logging.config) docs for more information.
