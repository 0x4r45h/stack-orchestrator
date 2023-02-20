# Copyright © 2022, 2023 Cerc

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http:#www.gnu.org/licenses/>.

import os
from abc import ABC, abstractmethod

def get_stack(config, stack):
    if stack == "package-registry":
        return package_registry_stack(config, stack)
    else:
        return base_stack(config, stack)


class base_stack(ABC):

    def __init__(self, config, stack):
        self.config = config
        self.stack = stack

    @abstractmethod
    def ensure_available(self):
        pass

    @abstractmethod
    def get_url(self):
        pass


class package_registry_stack(base_stack):

    def ensure_available(self):
        self.url = "<no registry url set>"
        # Check if we were given an external registry URL
        url_from_environment = os.environ.get("CERC_NPM_REGISTRY_URL")
        if url_from_environment:
            if self.config.verbose:
                print(f"Using package registry url from CERC_NPM_REGISTRY_URL: {url_from_environment}")
            self.url = url_from_environment
        else:
            # Otherwise we expect to use the local package-registry stack
            # First check if the stack is up
            # If not, print a message about how to start it and return fail to the caller
            return False
            # If it is available, get its mapped port and construct its URL
            self.url = "http://gitea.local:3000/api/packages/cerc-io/npm/"
        return True

    def get_url(self):
        return self.url

# Temporary helper functions while we figure out a good interface to the stack deploy code


def _is_stack_running(stack):
    return True


def _get_stack_mapped_port(stack, service, exposed_port):
    return 3000
