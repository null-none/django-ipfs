django-ipfs
===================


Uploads are added and pinned to the configured IPFS node,
which returns the IPFS Content ID (a hash of the contents).
This hash is the name that is saved to your database.
Duplicate content will also have the same address,
saving disk space.

Because of this only file creation and reading is supported.

Other IPFS users access and reseed a piece of content 
through its unique content ID.
Differently-distributed (i.e. normal HTTP) users
can access the uploads through an HTTP → IPFS gateway.


Installation
------------

```bash
pip install django-ipfs
```


Configuration
-------------

By default `ipfs_storage` adds and pins content to an IPFS daemon running on localhost
and returns URLs pointing to the public <https://ipfs.io/ipfs/> HTTP Gateway

To customise this, set the following variables in your `settings.py`:

- `IPFS_STORAGE_API_URL`: defaults to `'http://localhost:5001/api/v0/'`. 
- `IPFS_GATEWAY_API_URL`: defaults to `'https://ipfs.io/ipfs/'`.
  
Set `IPFS_GATEWAY_API_URL` to `'http://localhost:8080/ipfs/'` to serve content
through your local daemon's HTTP gateway.


Usage
-----

There are two ways to use a Django storage backend.

### As default backend

Use IPFS as [Django's default file storage backend](https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-DEFAULT_FILE_STORAGE):

```python
# settings.py

DEFAULT_FILE_STORAGE = 'ipfs_storage.InterPlanetaryFileSystemStorage'

IPFS_STORAGE_API_URL = 'http://localhost:5001/api/v0/'
IPFS_STORAGE_GATEWAY_URL = 'http://localhost:8080/ipfs/'
```  


### For a specific FileField

Alternatively, you may only want to use the IPFS storage backend for a single field:

```python
from django.db import models

from django_ipfs.storage import InterPlanetaryFileSystemStorage


class MyModel(models.Model):
    # …
    file_stored_on_ipfs = models.FileField(storage=InterPlanetaryFileSystemStorage())
    other_file = models.FileField()  # will still use DEFAULT_FILE_STORAGE
```

Don't forget the brackets to instantiate `InterPlanetaryFileSystemStorage()` with the default arguments!
