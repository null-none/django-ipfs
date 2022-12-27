from urllib.parse import urlparse

from django.conf import settings
from django.core.files.base import File, ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
import ipfsapi


__version__ = "0.1.0"


@deconstructible
class InterPlanetaryFileSystemStorage(Storage):
    """IPFS Django storage backend.

    Only file creation and reading is supported
    due to the nature of the IPFS protocol.
    """

    def __init__(self, api_url=None, gateway_url=None):
        """Connect to Interplanetary File System daemon API to add/pin files.

        :param api_url: IPFS control API base URL.
                        Also configurable via `settings.IPFS_STORAGE_API_URL`.
                        Defaults to 'http://localhost:5001/api/v0/'.
        :param gateway_url: Base URL for IPFS Gateway (for HTTP-only clients).
                            Also configurable via `settings.IPFS_STORAGE_GATEWAY_URL`.
                            Defaults to 'https://ipfs.io/ipfs/'.
        """
        parsed_api_url = urlparse(
            api_url
            or getattr(
                settings, "IPFS_STORAGE_API_URL", "http://localhost:5001/api/v0/"
            )
        )
        self._ipfs_client = ipfsapi.connect(
            parsed_api_url.hostname, parsed_api_url.port, parsed_api_url.path.strip("/")
        )
        self.gateway_url = gateway_url or getattr(
            settings, "IPFS_STORAGE_GATEWAY_URL", "https://ipfs.io/ipfs/"
        )

    def _open(self, name: str, mode="rb") -> File:
        """Retrieve the file content identified by multihash.

        :param name: IPFS Content ID multihash.
        :param mode: Ignored. The returned File instance is read-only.
        """
        return ContentFile(self._ipfs_client.cat(name), name=name)

    def _save(self, name: str, content: File) -> str:
        """Add and pin content to IPFS daemon.

        :param name: Ignored. Provided to comply with `Storage` interface.
        :param content: Django File instance to save.
        :return: IPFS Content ID multihash.
        """
        multihash = self._ipfs_client.add_bytes(content.__iter__())
        self._ipfs_client.pin_add(multihash)
        return multihash

    def get_valid_name(self, name):
        """Returns name. Only provided for compatibility with Storage interface."""
        return name

    def get_available_name(self, name, max_length=None):
        """Returns name. Only provided for compatibility with Storage interface."""
        return name

    def size(self, name: str) -> int:
        """Total size, in bytes, of IPFS content with multihash `name`."""
        return self._ipfs_client.object_stat(name)["CumulativeSize"]

    def delete(self, name: str):
        """Unpin IPFS content from the daemon."""
        self._ipfs_client.pin_rm(name)

    def url(self, name: str):
        """Returns an HTTP-accessible Gateway URL by default.

        Override this if you want direct `ipfs://…` URLs or something.

        :param name: IPFS Content ID multihash.
        :return: HTTP URL to access the content via an IPFS HTTP Gateway.
        """
        return "{gateway_url}{multihash}".format(
            gateway_url=self.gateway_url, multihash=name
        )
