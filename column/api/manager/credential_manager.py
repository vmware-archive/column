import logging

from column import utils


LOG = logging.getLogger(__name__)


class CredentialManager(object):
    """Column Credential Manager class

    The Credential Manager layer is to support additional logic which is needed
    to update and get credential.

    """

    def get_credential(self, cred):
        return utils.vault_decrypt(cred['value'])

    def update_credential(self, cred):
        utils.vault_encrypt(cred['value'])
