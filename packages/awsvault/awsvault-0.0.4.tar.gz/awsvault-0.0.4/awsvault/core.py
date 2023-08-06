# -*- coding: utf-8 -*-
import os
import six
import json
import logging
import boto3
import botocore.exceptions


class Vault(object):
    """
    Helper for getting secrets from AWS secret manager
    Check the TESTs out for usage examples
    """

    def __init__(self, secrets, look_first=None, **kwargs):
        self._logger = logging.getLogger('awsvault.' + __name__)
        self._vault = {}
        self._look_first = look_first or os.environ

        if isinstance(secrets, six.text_type):
            secrets = [secrets]

        try:
            client = boto3.client('secretsmanager', **kwargs)
            for secret in secrets:
                response = client.get_secret_value(SecretId=secret)
                value = response.get('SecretString', '{}')
                self._vault.update(json.loads(value))
        except botocore.exceptions.ClientError as exc:
            self._logger.warning('AWS Secrets Manager error', exc_info=True)

    def get(self, name, default=None):
        value = None
        if callable(self._look_first):
            value = self._look_first(name)
        elif isinstance(self._look_first, dict):
            value = self._look_first.get(name)

        if value is not None:
            return value

        return self._vault.get(name, default)
