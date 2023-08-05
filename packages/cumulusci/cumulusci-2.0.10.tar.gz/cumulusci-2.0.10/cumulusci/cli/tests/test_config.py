from datetime import date
from datetime import timedelta
import mock
import os
import sys
import unittest

import click

import cumulusci
from ..config import CliConfig
from cumulusci.core.config import OrgConfig
from cumulusci.core.exceptions import ConfigError
from cumulusci.core.exceptions import NotInProject
from cumulusci.core.exceptions import OrgNotFound
from cumulusci.core.exceptions import ProjectConfigNotFound


class TestCliConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.chdir(os.path.dirname(cumulusci.__file__))
        os.environ["CUMULUSCI_KEY"] = "1234567890abcdef"

    def test_init(self):
        config = CliConfig()

        for key in {"cumulusci", "tasks", "flows", "services", "orgs", "project"}:
            self.assertIn(key, config.global_config.config)
        self.assertEqual("CumulusCI", config.project_config.project__name)
        for key in {"services", "orgs", "app"}:
            self.assertIn(key, config.keychain.config)
        self.assertIn(config.project_config.repo_root, sys.path)

    def test_load_project_not_in_project(self):
        config = CliConfig()
        config.global_config.get_project_config = mock.Mock(side_effect=NotInProject)

        with self.assertRaises(click.UsageError):
            config._load_project_config()

    def test_load_project_config_no_file(self):
        config = CliConfig()
        config.project_config = None
        config.global_config.get_project_config = mock.Mock(
            side_effect=ProjectConfigNotFound
        )
        config._load_project_config()
        self.assertIsNone(config.project_config)

    def test_load_project_config_error(self):
        config = CliConfig()
        config.project_config = None
        config.global_config.get_project_config = mock.Mock(side_effect=ConfigError)

        with self.assertRaises(click.UsageError):
            config._load_project_config()

    def test_get_org(self):
        config = CliConfig()
        config.keychain = mock.Mock()
        config.keychain.get_org.return_value = org_config = OrgConfig({}, "test")

        org_name, org_config_result = config.get_org("test")
        self.assertEqual("test", org_name)
        self.assertIs(org_config, org_config_result)

    def test_get_org_default(self):
        config = CliConfig()
        config.keychain = mock.Mock()
        org_config = OrgConfig({}, "test")
        config.keychain.get_default_org.return_value = ("test", org_config)

        org_name, org_config_result = config.get_org()
        self.assertEqual("test", org_name)
        self.assertIs(org_config, org_config_result)

    def test_get_org_missing(self):
        config = CliConfig()
        config.keychain = mock.Mock()
        config.keychain.get_org.return_value = None

        with self.assertRaises(click.UsageError):
            org_name, org_config_result = config.get_org("test", fail_if_missing=True)

    @mock.patch("click.confirm")
    def test_check_org_expired(self, confirm):
        config = CliConfig()
        config.keychain = mock.Mock()
        org_config = OrgConfig(
            {
                "scratch": True,
                "date_created": date.today() - timedelta(days=2),
                "expired": True,
            },
            "test",
        )
        confirm.return_value = True

        config.check_org_expired("test", org_config)
        config.keychain.create_scratch_org.assert_called_once()

    @mock.patch("click.confirm")
    def test_check_org_expired_decline(self, confirm):
        config = CliConfig()
        config.keychain = mock.Mock()
        org_config = OrgConfig(
            {
                "scratch": True,
                "date_created": date.today() - timedelta(days=2),
                "expired": True,
            },
            "test",
        )
        confirm.return_value = False

        with self.assertRaises(click.ClickException):
            config.check_org_expired("test", org_config)

    def test_check_org_overwrite_not_found(self):
        config = CliConfig()
        config.keychain.get_org = mock.Mock(side_effect=OrgNotFound)

        self.assertTrue(config.check_org_overwrite("test"))

    def test_check_org_overwrite_scratch_exists(self):
        config = CliConfig()
        config.keychain.get_org = mock.Mock(
            return_value=OrgConfig({"scratch": True, "created": True}, "test")
        )

        with self.assertRaises(click.ClickException):
            config.check_org_overwrite("test")

    def test_check_org_overwrite_non_scratch_exists(self):
        config = CliConfig()
        config.keychain.get_org = mock.Mock(
            return_value=OrgConfig({"scratch": False}, "test")
        )

        with self.assertRaises(click.ClickException):
            config.check_org_overwrite("test")

    def test_check_keychain_missing_key(self):
        config = CliConfig()
        config.keychain = mock.Mock(encrypted=True)
        config.keychain_key = None

        with self.assertRaises(click.UsageError):
            config.check_keychain()

    def test_check_project_config(self):
        config = CliConfig()
        config.project_config = None

        with self.assertRaises(click.UsageError):
            config.check_project_config()
