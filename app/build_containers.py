# Copyright © 2022 Cerc

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

# Builds or pulls containers for the system components

# env vars:
# CERC_REPO_BASE_DIR defaults to ~/cerc

# TODO: display the available list of containers; allow re-build of either all or specific containers

import os
import sys
import argparse
from decouple import config
import subprocess
import click

# TODO: find a place for this
#    epilog="Config provided either in .env or settings.ini or env vars: CERC_REPO_BASE_DIR (defaults to ~/cerc)"

@click.command()
@click.pass_context
def command(ctx):
    '''build the set of containers required for a complete stack'''

    quiet = ctx.obj.quiet
    verbose = ctx.obj.verbose
    dry_run = ctx.obj.verbose

    dev_root_path = os.path.expanduser(config("CERC_REPO_BASE_DIR", default="~/cerc"))

    if not quiet:
        print(f'Dev Root is: {dev_root_path}')

    if not os.path.isdir(dev_root_path):
        print(f'Dev root directory doesn\'t exist, creating')

    with open("container-image-list.txt") as container_list_file:
        containers = container_list_file.read().splitlines()

    if verbose:
        print(f'Containers: {containers}')

    def process_container(container):
        if not quiet:
            print(f"Building: {container}")
        build_script_filename = os.path.join("container-build",container.replace("/","-"),"build.sh")
        if verbose:
            print(f"Script: {build_script_filename}")
        if not os.path.exists(build_script_filename):
            print(f"Error, script: {build_script_filename} doesn't exist")
            sys.exit(1)
        if not dry_run:
            # We need to export CERC_REPO_BASE_DIR
            build_result = subprocess.run(build_script_filename, shell=True, env={'CERC_REPO_BASE_DIR':dev_root_path})
            # TODO: check result in build_result.returncode
            print(f"Result is: {build_result}")

    for container in containers:
        process_container(container)
