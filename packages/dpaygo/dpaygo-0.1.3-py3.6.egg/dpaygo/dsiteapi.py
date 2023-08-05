# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import hashlib
import base64
import json
import random
import requests
import struct
from datetime import datetime
from binascii import hexlify
from .instance import shared_dpay_instance
from .account import Account
from dpaygographenebase.py23 import py23_bytes
from dpaygographenebase.ecdsasig import sign_message
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class DSiteAPI(object):
    """ Class to access dSite DSiteAPI instances:
        https://github.com/dsites/dsiteapi

        Description from the official documentation:

        * Feature flags: "Feature flags allows our apps (condenser mainly) to
          hide certain features behind flags."
        * User data: "DSiteAPI is the central point for storing sensitive user
          data (email, phone, etc). No other services should store this data
          and should instead query for it here every time."
        * User tags: "Tagging mechanism for other services, allows defining and
          assigning tags to accounts (or other identifiers) and querying for
          them."

        Not contained in the documentation, but implemented and working:

        * Draft handling: saving, listing and removing post drafts
          consisting of a post title and a body.

        The underlying RPC authentication and request signing procedure is
        described here: https://github.com/dpays/dpay-rpc-auth

    """

    def __init__(self, url="https://api.dsite.io",
                 dpay_instance=None):
        """ Initialize a DSiteAPI instance
            :param str url: (optional) URL to the dSite API, defaults to
                https://api.dsite.io
            :param dpaygo.dpay.DPay dpay_instance: DPay instance

        """

        self.url = url
        self.dpay = dpay_instance or shared_dpay_instance()
        self.id = 0
        self.ENCODING = 'utf-8'
        self.TIMEFORMAT = '%Y-%m-%dT%H:%M:%S.%f'
        self.K = hashlib.sha256(py23_bytes('dpay_jsonrpc_auth',
                                           self.ENCODING)).digest()

    def prehash_message(self, timestamp, account, method, params, nonce):
        """ Prepare a hash for the dSite API request with SHA256 according
            to https://github.com/dpays/dpay-rpc-auth
            Hashing of `second` is then done inside `ecdsasig.sign_message()`.

            :param str timestamp: valid iso8601 datetime ending in "Z"
            :param str account: valid dPay blockchain account name
            :param str method: DSiteAPI method name to be called
            :param bytes param: base64 encoded request parameters
            :param bytes nonce: random 8 bytes

        """
        first = hashlib.sha256(py23_bytes(timestamp + account + method +
                                          params, self.ENCODING))
        return self.K + first.digest() + nonce

    def _request(self, account, method, params, key):
        """Assemble the request, hash it, sign it and send it to the DSiteAPI
            instance. Returns the server response as JSON.

            :param str account: account name
            :param str method: dSite API method name to be called
            :param dict params: request parameters as `dict`
            :param str key: dPay posting key for signing

        """
        params_bytes = py23_bytes(json.dumps(params), self.ENCODING)
        params_enc = base64.b64encode(params_bytes).decode(self.ENCODING)
        timestamp = datetime.utcnow().strftime(self.TIMEFORMAT)[:-3] + "Z"
        nonce_int = random.getrandbits(64)
        nonce_bytes = struct.pack('>Q', nonce_int)  # 64bit ULL, big endian
        nonce_str = "%016x" % (nonce_int)

        message = self.prehash_message(timestamp, account, method,
                                       params_enc, nonce_bytes)
        signature = sign_message(message, key)
        signature_hex = hexlify(signature).decode(self.ENCODING)

        request = {
            "jsonrpc": "2.0",
            "id": self.id,
            "method": method,
            "params": {
                "__signed": {
                    "account": account,
                    "nonce": nonce_str,
                    "params": params_enc,
                    "signatures": [signature_hex],
                    "timestamp": timestamp
                }
            }
        }
        r = requests.post(self.url, data=json.dumps(request))
        self.id += 1
        return r.json()

    def _dsiteapi_method(self, account, signing_account, method, params):
        """ Wrapper function to handle account and key lookups

            :param str account: name of the addressed account
            :param str signing_account: name of the account to sign the request
            :param method: DSiteAPI method name to be called
            :params dict params: request parameters as `dict`

        """
        account = Account(account, dpay_instance=self.dpay)
        if signing_account is None:
            signer = account
        else:
            signer = Account(signing_account, dpay_instance=self.dpay)
        if "posting" not in signer:
            signer.refresh()
        if "posting" not in signer:
            raise AssertionError("Could not access posting permission")
        for authority in signer["posting"]["key_auths"]:
            posting_wif = self.dpay.wallet.getPrivateKeyForPublicKey(
                authority[0])
        return self._request(account['name'], method, params,
                             posting_wif)

    def get_user_data(self, account, signing_account=None):
        """ Get the account's email address and phone number. The request has to be
            signed by the requested account or an admin account.

            :param str account: requested account
            :param str signing_account: (optional) account to sign the
                request. If unset, `account` is used.

            Example:

            .. code-block:: python

                from dpaygo import DPay
                from dpaygo.dsiteapi import DSiteAPI
                s = DPay(keys=["5JPOSTINGKEY"])
                c = DSiteAPI(dpay_instance=s)
                print(c.get_user_data('accountname'))

        """
        account = Account(account, dpay_instance=self.dpay)
        user_data = self._dsiteapi_method(account, signing_account,
                                          "dsiteapi.get_user_data",
                                          [account['name']])
        if "result" in user_data:
            return user_data["result"]
        else:
            return user_data

    def set_user_data(self, account, params, signing_account=None):
        """ Set the account's email address and phone number. The request has to be
            signed by an admin account.

            :param str account: requested account
            :param dict param: user data to be set
            :param str signing_account: (optional) account to sign the
                request. If unset, `account` is used.

            Example:

            .. code-block:: python

                from dpaygo import DPay
                from dpaygo.dsiteapi import DSiteAPI
                s = DPay(keys=["5JADMINPOSTINGKEY"])
                c = DSiteAPI(dpay_instance=s)
                userdata = {'email': 'foo@bar.com', 'phone':'+123456789'}
                c.set_user_data('accountname', userdata, 'adminaccountname')

        """
        return self._dsiteapi_method(account, signing_account,
                                     "dsiteapi.set_user_data",
                                     [params])

    def get_feature_flags(self, account, signing_account=None):
        """ Get the account's feature flags. The request has to be signed by the
            requested account or an admin account.

            :param str account: requested account
            :param str signing_account: (optional) account to sign the
                request. If unset, `account` is used.

            Example:

            .. code-block:: python

                from dpaygo import DPay
                from dpaygo.dsiteapi import DSiteAPI
                s = DPay(keys=["5JPOSTINGKEY"])
                c = DSiteAPI(dpay_instance=s)
                print(c.get_feature_flags('accountname'))

        """
        account = Account(account, dpay_instance=self.dpay)
        feature_flags = self._dsiteapi_method(account, signing_account,
                                              "dsiteapi.get_feature_flags",
                                              [account['name']])
        if "result" in feature_flags:
            return feature_flags["result"]
        else:
            return feature_flags

    def get_feature_flag(self, account, flag, signing_account=None):
        """ Test if a specific feature flag is set for an account. The request
            has to be signed by the requested account or an admin account.

            :param str account: requested account
            :param str flag: flag to be tested
            :param str signing_account: (optional) account to sign the
                request. If unset, `account` is used.

            Example:

            .. code-block:: python

                from dpaygo import DPay
                from dpaygo.dsiteapi import DSiteAPI
                s = DPay(keys=["5JPOSTINGKEY"])
                c = DSiteAPI(dpay_instance=s)
                print(c.get_feature_flag('accountname', 'accepted_tos'))

        """
        account = Account(account, dpay_instance=self.dpay)
        return self._dsiteapi_method(account, signing_account,
                                     "dsiteapi.get_feature_flag",
                                     [account['name'], flag])

    def save_draft(self, account, title, body):
        """ Save a draft in the DSiteAPI database

            :param str account: requested account
            :param str title: draft post title
            :param str body: draft post body

        """
        account = Account(account, dpay_instance=self.dpay)
        draft = {'title': title, 'body': body}
        return self._dsiteapi_method(account, None,
                                     "dsiteapi.save_draft",
                                     [account['name'], draft])

    def list_drafts(self, account):
        """ List all saved drafts from `account`

            :param str account: requested account

            Sample output:

            .. code-block:: js

                {
                    'jsonrpc': '2.0', 'id': 2, 'result': [
                        {'title': 'draft-title', 'body': 'draft-body',
                         'uuid': '06497e1e-ac30-48cb-a069-27e1672924c9'}
                    ]
                }

        """
        account = Account(account, dpay_instance=self.dpay)
        return self._dsiteapi_method(account, None,
                                     "dsiteapi.list_drafts",
                                     [account['name']])

    def remove_draft(self, account, uuid):
        """ Remove a draft from the DSiteAPI database

            :param str account: requested account
            :param str uuid: draft identifier as returned from
                `list_drafts`

        """
        account = Account(account, dpay_instance=self.dpay)
        return self._dsiteapi_method(account, None,
                                     "dsiteapi.remove_draft",
                                     [account['name'], uuid])

    def healthcheck(self):
        """ Get the DSiteAPI status

            Sample output:

            .. code-block:: js

                {
                    'ok': True, 'version': '1.1.1-4d28e36-1528725174',
                    'date': '2018-07-21T12:12:25.502Z'
                }

        """
        url = urljoin(self.url, "/.well-known/healthcheck.json")
        r = requests.get(url)
        return r.json()
