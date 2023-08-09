#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Mark Mercado <mmercado@digitalocean.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
---
module: sizes_info

short_description: List all of available Droplet sizes

version_added: 0.2.0

description:
  - List all of available Droplet sizes.
  - View the API documentation at (https://docs.digitalocean.com/reference/api/api-reference/#operation/sizes_list).

author: Mark Mercado (@mamercad)

requirements:
  - pydo >= 0.1.3
  - azure-core >= 1.26.1

extends_documentation_fragment:
  - digitalocean.cloud.common.documentation
"""


EXAMPLES = r"""
- name: Get Droplet sizes
  digitalocean.cloud.sizes_info:
    token: "{{ token }}"
"""


RETURN = r"""
sizes:
  description: Droplet sizes information.
  returned: always
  type: list
  elements: dict
  sample:
    - available: true
      description: Basic
      disk: 10
      memory: 512
      price_hourly: 0.00595
      price_monthly: 4.0
      regions:
        - ams3
        - fra1
        - nyc1
        - sfo3
        - sgp1
        - syd1
      slug: s-1vcpu-512mb-10gb
      transfer: 0.5
      vcpus: 1
    - ...
error:
  description: DigitalOcean API error.
  returned: failure
  type: dict
  sample:
    Message: Informational error message.
    Reason: Unauthorized
    Status Code: 401
msg:
  description: Droplet sizes result information.
  returned: always
  type: str
  sample:
    - Current Droplet sizes
    - No Droplet sizes
"""

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.digitalocean.cloud.plugins.module_utils.common import (
    DigitalOceanOptions,
    DigitalOceanFunctions,
)

import traceback

HAS_AZURE_LIBRARY = False
AZURE_LIBRARY_IMPORT_ERROR = None
try:
    from azure.core.exceptions import HttpResponseError
except ImportError:
    AZURE_LIBRARY_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_AZURE_LIBRARY = True

HAS_PYDO_LIBRARY = False
PYDO_LIBRARY_IMPORT_ERROR = None
try:
    from pydo import Client
except ImportError:
    PYDO_LIBRARY_IMPORT_ERROR = traceback.format_exc()
else:
    HAS_PYDO_LIBRARY = True


class DropletSizesInformation:
    def __init__(self, module):
        """Class constructor."""
        self.module = module
        self.client = Client(token=module.params.get("token"))
        self.state = module.params.get("state")
        if self.state == "present":
            self.present()

    def present(self):
        sizes = DigitalOceanFunctions.get_paginated(
            module=self.module,
            obj=self.client.sizes,
            meth="list",
            key="sizes",
            exc=HttpResponseError,
        )
        if sizes:
            self.module.exit_json(
                changed=False,
                msg="Current Droplet sizes",
                sizes=sizes,
            )
        self.module.exit_json(changed=False, msg="No Droplet sizes", sizes=[])


def main():
    argument_spec = DigitalOceanOptions.argument_spec()
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if not HAS_AZURE_LIBRARY:
        module.fail_json(
            msg=missing_required_lib("azure.core.exceptions"),
            exception=AZURE_LIBRARY_IMPORT_ERROR,
        )
    if not HAS_PYDO_LIBRARY:
        module.fail_json(
            msg=missing_required_lib("pydo"),
            exception=PYDO_LIBRARY_IMPORT_ERROR,
        )

    DropletSizesInformation(module)


if __name__ == "__main__":
    main()