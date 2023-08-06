import os
import sys
import click

import pkg_resources

from cumulusci.core.config import YamlGlobalConfig
from cumulusci.core.exceptions import ConfigError
from cumulusci.core.exceptions import NotInProject
from cumulusci.core.exceptions import OrgNotFound
from cumulusci.core.exceptions import ProjectConfigNotFound
from cumulusci.core.utils import import_class


class CliConfig(object):
    def __init__(self):
        self.global_config = None
        self.project_config = None
        self.keychain = None

        self._load_global_config()
        self._load_project_config()
        self._load_keychain()
        self._add_repo_to_path()

    def _add_repo_to_path(self):
        if self.project_config:
            sys.path.append(self.project_config.repo_root)

    def _load_global_config(self):
        self.global_config = YamlGlobalConfig()

    def _load_project_config(self):
        try:
            self.project_config = self.global_config.get_project_config()
        except ProjectConfigNotFound:
            pass
        except NotInProject as e:
            raise click.UsageError(e.message)
        except ConfigError as e:
            raise click.UsageError("Config Error: {}".format(e.message))

    def _load_keychain(self):
        self.keychain_key = os.environ.get("CUMULUSCI_KEY")
        if self.project_config:
            keychain_class = os.environ.get(
                "CUMULUSCI_KEYCHAIN_CLASS", self.project_config.cumulusci__keychain
            )
            self.keychain_class = import_class(keychain_class)
            self.keychain = self.keychain_class(self.project_config, self.keychain_key)
            self.project_config.set_keychain(self.keychain)

    def get_org(self, org_name=None, fail_if_missing=True):
        if org_name:
            org_config = self.keychain.get_org(org_name)
        else:
            org_name, org_config = self.keychain.get_default_org()
        if org_config:
            org_config = self.check_org_expired(org_name, org_config)
        elif fail_if_missing:
            raise click.UsageError("No org specified and no default org set.")
        return org_name, org_config

    def check_org_expired(self, org_name, org_config):
        if org_config.scratch and org_config.date_created and org_config.expired:
            click.echo(click.style("The scratch org is expired", fg="yellow"))
            if click.confirm("Attempt to recreate the scratch org?", default=True):
                self.keychain.create_scratch_org(
                    org_name, org_config.config_name, org_config.days
                )
                click.echo(
                    "Org config was refreshed, attempting to recreate scratch org"
                )
                org_config = self.keychain.get_org(org_name)
                org_config.create_org()
            else:
                raise click.ClickException(
                    "The target scratch org is expired.  You can use cci org remove {} "
                    "to remove the org and then recreate the config manually".format(
                        org_name
                    )
                )

        return org_config

    def check_org_overwrite(self, org_name):
        try:
            org = self.keychain.get_org(org_name)
            if org.scratch:
                if org.created:
                    raise click.ClickException(
                        "Scratch org has already been created. "
                        "Use `cci org scratch_delete {}`".format(org_name)
                    )
            else:
                raise click.ClickException(
                    "Org {} already exists.  Use `cci org remove` to delete it.".format(
                        org_name
                    )
                )
        except OrgNotFound:
            pass
        return True

    def check_keychain(self):
        self.check_project_config()
        if self.keychain and self.keychain.encrypted and not self.keychain_key:
            raise click.UsageError(
                "You must set the environment variable CUMULUSCI_KEY "
                "with the encryption key to be used for storing org credentials"
            )

    def check_project_config(self):
        if not self.project_config:
            raise click.UsageError(
                'No project configuration found.  You can use the "project init" '
                "command to initilize the project for use with CumulusCI"
            )

    def check_cumulusci_version(self):
        if self.project_config:
            min_cci_version = self.project_config.minimum_cumulusci_version
            if min_cci_version:
                parsed_version = pkg_resources.parse_version(min_cci_version)
                if get_installed_version() < parsed_version:
                    raise click.UsageError(
                        "This project requires CumulusCI version {} or later. "
                        "Please upgrade using pip install -U cumulusci".format(
                            min_cci_version
                        )
                    )


def get_installed_version():
    """ returns the version name (e.g. 2.0.0b58) that is installed """
    req = pkg_resources.Requirement.parse("cumulusci")
    dist = pkg_resources.WorkingSet().find(req)
    return pkg_resources.parse_version(dist.version)
