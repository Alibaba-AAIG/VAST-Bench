"""Built-in transform plugins available to profiles.

``BUILTIN_PLUGINS`` maps a plugin name to its transform class; a profile's ``plugin`` key
selects one of these by name.
"""

import acme_reverse
import acme_upper

BUILTIN_PLUGINS = {
    "acme_upper": acme_upper.Transform,
    "acme_reverse": acme_reverse.Transform,
}
