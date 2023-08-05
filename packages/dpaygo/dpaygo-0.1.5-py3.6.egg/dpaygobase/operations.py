from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import int, str
from dpaygographenebase.py23 import bytes_types, integer_types, string_types, text_type
from collections import OrderedDict
import json
from dpaygographenebase.types import (
    Uint8, Int16, Uint16, Uint32, Uint64,
    Varint32, Int64, String, Bytes, Void,
    Array, PointInTime, Signature, Bool,
    Set, Fixed_array, Optional, Static_variant,
    Map, Id
)
from .objects import GrapheneObject, isArgsThisClass
from dpaygographenebase.account import PublicKey
from .operationids import operations
from .objects import (
    Operation,
    Memo,
    Amount,
    Extension,
    Price,
    WitnessProps,
    Permission,
    ExchangeRate,
    Beneficiaries,
    Beneficiary,
    CommentOptionExtensions,
)

default_prefix = "DWB"


def check_for_class(self, args):
    if isArgsThisClass(self, args):
            self.data = args[0].data
            return True
    else:
        return False


class Transfer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        prefix = kwargs.get("prefix", default_prefix)
        if "memo" not in kwargs:
            kwargs["memo"] = ""
        if isinstance(kwargs["memo"], dict):
            kwargs["memo"]["prefix"] = prefix
            memo = Optional(Memo(**kwargs["memo"]))
        elif isinstance(kwargs["memo"], string_types):
            memo = (String(kwargs["memo"]))
        else:
            memo = Optional(Memo(kwargs["memo"]))

        super(Transfer, self).__init__(OrderedDict([
            ('from', String(kwargs["from"])),
            ('to', String(kwargs["to"])),
            ('amount', Amount(kwargs["amount"])),
            ('memo', memo),
        ]))


class Vote(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Vote, self).__init__(OrderedDict([
            ('voter', String(kwargs["voter"])),
            ('author', String(kwargs["author"])),
            ('permlink', String(kwargs["permlink"])),
            ('weight', Int16(kwargs["weight"])),
        ]))


class Transfer_to_vesting(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Transfer_to_vesting, self).__init__(OrderedDict([
            ('from', String(kwargs["from"])),
            ('to', String(kwargs["to"])),
            ('amount', Amount(kwargs["amount"])),
        ]))


class Withdraw_vesting(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Withdraw_vesting, self).__init__(OrderedDict([
            ('account', String(kwargs["account"])),
            ('vesting_shares', Amount(kwargs["vesting_shares"])),
        ]))


class Account_witness_vote(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Account_witness_vote, self).__init__(OrderedDict([
            ('account', String(kwargs["account"])),
            ('witness', String(kwargs["witness"])),
            ('approve', Bool(bool(kwargs["approve"]))),
        ]))


class Account_witness_proxy(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Account_witness_proxy, self).__init__(OrderedDict([
            ('account', String(kwargs["account"])),
            ('proxy', String(kwargs["proxy"])),
        ]))


class Custom(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Custom, self).__init__(OrderedDict([
            ('required_auths',
                Array([String(o) for o in kwargs["required_auths"]])),
            ('id', Uint16(int(kwargs["id"]))),
            ('data', String(kwargs["data"])),
        ]))


class Custom_binary(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Custom_binary, self).__init__(OrderedDict([
            ('id', Uint16(int(kwargs["id"]))),
            ('data', String(kwargs["data"])),
        ]))


class Op_wrapper(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Op_wrapper, self).__init__(OrderedDict([
            ('op', Operation(kwargs["op"])),
        ]))


class Account_create(GrapheneObject):

    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        prefix = kwargs.get("prefix", default_prefix)

        if not len(kwargs["new_account_name"]) <= 16:
            raise AssertionError("Account name must be at most 16 chars long")

        meta = ""
        if "json_metadata" in kwargs and kwargs["json_metadata"]:
            if isinstance(kwargs["json_metadata"], dict):
                meta = json.dumps(kwargs["json_metadata"])
            else:
                meta = kwargs["json_metadata"]

        super(Account_create, self).__init__(OrderedDict([
            ('fee', Amount(kwargs["fee"])),
            ('creator', String(kwargs["creator"])),
            ('new_account_name', String(kwargs["new_account_name"])),
            ('owner', Permission(kwargs["owner"], prefix=prefix)),
            ('active', Permission(kwargs["active"], prefix=prefix)),
            ('posting', Permission(kwargs["posting"], prefix=prefix)),
            ('memo_key', PublicKey(kwargs["memo_key"], prefix=prefix)),
            ('json_metadata', String(meta)),
        ]))


class Account_create_with_delegation(GrapheneObject):

    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        prefix = kwargs.get("prefix", default_prefix)

        if not len(kwargs["new_account_name"]) <= 16:
            raise AssertionError("Account name must be at most 16 chars long")

        meta = ""
        if "json_metadata" in kwargs and kwargs["json_metadata"]:
            if isinstance(kwargs["json_metadata"], dict):
                meta = json.dumps(kwargs["json_metadata"])
            else:
                meta = kwargs["json_metadata"]

        super(Account_create_with_delegation, self).__init__(OrderedDict([
            ('fee', Amount(kwargs["fee"])),
            ('delegation', Amount(kwargs["delegation"])),
            ('creator', String(kwargs["creator"])),
            ('new_account_name', String(kwargs["new_account_name"])),
            ('owner', Permission(kwargs["owner"], prefix=prefix)),
            ('active', Permission(kwargs["active"], prefix=prefix)),
            ('posting', Permission(kwargs["posting"], prefix=prefix)),
            ('memo_key', PublicKey(kwargs["memo_key"], prefix=prefix)),
            ('json_metadata', String(meta)),
            ('extensions', Array([])),
        ]))


class Account_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        prefix = kwargs.get("prefix", default_prefix)

        if "owner" in kwargs:
            owner = Optional(Permission(kwargs["owner"], prefix=prefix))
        else:
            owner = Optional(None)

        if "active" in kwargs:
            active = Optional(Permission(kwargs["active"], prefix=prefix))
        else:
            active = Optional(None)

        if "posting" in kwargs:
            posting = Optional(Permission(kwargs["posting"], prefix=prefix))
        else:
            posting = Optional(None)

        meta = ""
        if "json_metadata" in kwargs and kwargs["json_metadata"]:
            if isinstance(kwargs["json_metadata"], dict):
                meta = json.dumps(kwargs["json_metadata"])
            else:
                meta = kwargs["json_metadata"]

        super(Account_update, self).__init__(OrderedDict([
            ('account', String(kwargs["account"])),
            ('owner', owner),
            ('active', active),
            ('posting', posting),
            ('memo_key', PublicKey(kwargs["memo_key"], prefix=prefix)),
            ('json_metadata', String(meta)),
        ]))


class Witness_update(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        prefix = kwargs.pop("prefix", default_prefix)

        if "block_signing_key" in kwargs and kwargs["block_signing_key"]:
            block_signing_key = (PublicKey(kwargs["block_signing_key"], prefix=prefix))
        else:
            block_signing_key = PublicKey(
                prefix + "1111111111111111111111111111111114T1Anm", prefix=prefix)

        super(Witness_update, self).__init__(OrderedDict([
            ('owner', String(kwargs["owner"])),
            ('url', String(kwargs["url"])),
            ('block_signing_key', block_signing_key),
            ('props', WitnessProps(kwargs["props"])),
            ('fee', Amount(kwargs["fee"])),
        ]))


class Comment(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        meta = ""
        if "json_metadata" in kwargs and kwargs["json_metadata"]:
            if (isinstance(kwargs["json_metadata"], dict) or isinstance(kwargs["json_metadata"], list)):
                meta = json.dumps(kwargs["json_metadata"])
            else:
                meta = kwargs["json_metadata"]

        super(Comment, self).__init__(
            OrderedDict([
                ('parent_author', String(kwargs["parent_author"])),
                ('parent_permlink', String(kwargs["parent_permlink"])),
                ('author', String(kwargs["author"])),
                ('permlink', String(kwargs["permlink"])),
                ('title', String(kwargs["title"])),
                ('body', String(kwargs["body"])),
                ('json_metadata', String(meta)),
            ]))


class Custom_json(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        if "json" in kwargs and kwargs["json"]:
            if (isinstance(kwargs["json"], dict) or isinstance(kwargs["json"], list)):
                js = json.dumps(kwargs["json"])
            else:
                js = kwargs["json"]

        if len(kwargs["id"]) > 32:
            raise Exception("'id' too long")

        super(Custom_json, self).__init__(
            OrderedDict([
                ('required_auths',
                 Array([String(o) for o in kwargs["required_auths"]])),
                ('required_posting_auths',
                 Array([
                     String(o) for o in kwargs["required_posting_auths"]
                 ])),
                ('id', String(kwargs["id"])),
                ('json', String(js)),
            ]))


class Comment_options(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]

        # handle beneficiaries
        if "beneficiaries" in kwargs and kwargs['beneficiaries']:
            kwargs['extensions'] = [[0, {'beneficiaries': kwargs['beneficiaries']}]]

        extensions = Array([])
        if "extensions" in kwargs and kwargs["extensions"]:
            extensions = Array([CommentOptionExtensions(o) for o in kwargs["extensions"]])

        super(Comment_options, self).__init__(
            OrderedDict([
                ('author', String(kwargs["author"])),
                ('permlink', String(kwargs["permlink"])),
                ('max_accepted_payout',
                 Amount(kwargs["max_accepted_payout"])),
                ('percent_dpay_dollars',
                 Uint16(int(kwargs["percent_dpay_dollars"]))),
                ('allow_votes', Bool(bool(kwargs["allow_votes"]))),
                ('allow_curation_rewards',
                 Bool(bool(kwargs["allow_curation_rewards"]))),
                ('extensions', extensions),
            ]))


class Delete_comment(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Delete_comment, self).__init__(
            OrderedDict([
                ('author', String(kwargs["author"])),
                ('permlink', String(kwargs["permlink"])),
            ]))


class Feed_publish(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Feed_publish, self).__init__(
            OrderedDict([
                ('publisher', String(kwargs["publisher"])),
                ('exchange_rate', ExchangeRate(kwargs["exchange_rate"])),
            ]))


class Convert(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Convert, self).__init__(
            OrderedDict([
                ('owner', String(kwargs["owner"])),
                ('requestid', Uint32(kwargs["requestid"])),
                ('amount', Amount(kwargs["amount"])),
            ]))


class Set_withdraw_vesting_route(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Set_withdraw_vesting_route, self).__init__(
            OrderedDict([
                ('from_account', String(kwargs["from_account"])),
                ('to_account', String(kwargs["to_account"])),
                ('percent', Uint16((kwargs["percent"]))),
                ('auto_vest', Bool(kwargs["auto_vest"])),
            ]))


class Limit_order_cancel(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Limit_order_cancel, self).__init__(
            OrderedDict([
                ('owner', String(kwargs["owner"])),
                ('orderid', Uint32(kwargs["orderid"])),
            ]))


class Prove_authority(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Prove_authority, self).__init__(
            OrderedDict([
                ('challenged', String(kwargs["challenged"])),
                ('require_owner', Bool(kwargs["require_owner"])),
            ]))


class Delegate_vesting_shares(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Delegate_vesting_shares, self).__init__(
            OrderedDict([
                ('delegator', String(kwargs["delegator"])),
                ('delegatee', String(kwargs["delegatee"])),
                ('vesting_shares', Amount(kwargs["vesting_shares"])),
            ]))


class Limit_order_create(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Limit_order_create, self).__init__(
            OrderedDict([
                ('owner', String(kwargs["owner"])),
                ('orderid', Uint32(kwargs["orderid"])),
                ('amount_to_sell', Amount(kwargs["amount_to_sell"])),
                ('min_to_receive', Amount(kwargs["min_to_receive"])),
                ('fill_or_kill', Bool(kwargs["fill_or_kill"])),
                ('expiration', PointInTime(kwargs["expiration"])),
            ]))


class Limit_order_create2(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Limit_order_create2, self).__init__(
            OrderedDict([
                ('owner', String(kwargs["owner"])),
                ('orderid', Uint32(kwargs["orderid"])),
                ('amount_to_sell', Amount(kwargs["amount_to_sell"])),
                ('fill_or_kill', Bool(kwargs["fill_or_kill"])),
                ('exchange_rate', ExchangeRate(kwargs["exchange_rate"])),
                ('expiration', PointInTime(kwargs["expiration"])),
            ]))


class Change_recovery_account(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Change_recovery_account, self).__init__(
            OrderedDict([
                ('account_to_recover', String(kwargs["account_to_recover"])),
                ('new_recovery_account', String(kwargs["new_recovery_account"])),
                ('extensions', Array([])),
            ]))


class Transfer_from_savings(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        if "memo" not in kwargs:
            kwargs["memo"] = ""

        super(Transfer_from_savings, self).__init__(
            OrderedDict([
                ('from', String(kwargs["from"])),
                ('request_id', Uint32(kwargs["request_id"])),
                ('to', String(kwargs["to"])),
                ('amount', Amount(kwargs["amount"])),
                ('memo', String(kwargs["memo"])),
            ]))


class Cancel_transfer_from_savings(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Cancel_transfer_from_savings, self).__init__(
            OrderedDict([
                ('from', String(kwargs["from"])),
                ('request_id', Uint32(kwargs["request_id"])),
            ]))


class Claim_reward_balance(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Claim_reward_balance, self).__init__(
            OrderedDict([
                ('account', String(kwargs["account"])),
                ('reward_dpay', Amount(kwargs["reward_dpay"])),
                ('reward_bbd', Amount(kwargs["reward_bbd"])),
                ('reward_vests', Amount(kwargs["reward_vests"])),
            ]))


class Transfer_to_savings(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        if "memo" not in kwargs:
            kwargs["memo"] = ""
        super(Transfer_to_savings, self).__init__(
            OrderedDict([
                ('from', String(kwargs["from"])),
                ('to', String(kwargs["to"])),
                ('amount', Amount(kwargs["amount"])),
                ('memo', String(kwargs["memo"])),
            ]))


class Request_account_recovery(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        prefix = kwargs.get("prefix", default_prefix)
        new_owner = Permission(kwargs["new_owner_authority"], prefix=prefix)
        super(Request_account_recovery, self).__init__(
            OrderedDict([
                ('recovery_account', String(kwargs["recovery_account"])),
                ('account_to_recover', String(kwargs["account_to_recover"])),
                ('new_owner_authority', new_owner),
                ('extensions', Array([])),
            ]))


class Recover_account(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        prefix = kwargs.get("prefix", default_prefix)
        new_owner = Permission(kwargs["new_owner_authority"], prefix=prefix)
        recent_owner = Permission(kwargs["recent_owner_authority"], prefix=prefix)
        super(Recover_account, self).__init__(
            OrderedDict([
                ('account_to_recover', String(kwargs["account_to_recover"])),
                ('new_owner_authority', new_owner),
                ('recent_owner_authority', recent_owner),
                ('extensions', Array([])),
            ]))


class Escrow_transfer(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        meta = ""
        if "json_meta" in kwargs and kwargs["json_meta"]:
            if (isinstance(kwargs["json_meta"], dict) or isinstance(kwargs["json_meta"], list)):
                meta = json.dumps(kwargs["json_meta"])
            else:
                meta = kwargs["json_meta"]
        super(Escrow_transfer, self).__init__(
            OrderedDict([
                ('from', String(kwargs["from"])),
                ('to', String(kwargs["to"])),
                ('agent', String(kwargs["agent"])),
                ('escrow_id', Uint32(kwargs["escrow_id"])),
                ('bbd_amount', Amount(kwargs["bbd_amount"])),
                ('dpay_amount', Amount(kwargs["dpay_amount"])),
                ('fee', Amount(kwargs["fee"])),
                ('ratification_deadline', PointInTime(kwargs["ratification_deadline"])),
                ('escrow_expiration', PointInTime(kwargs["escrow_expiration"])),
                ('json_meta', String(meta)),
            ]))


class Escrow_dispute(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Escrow_dispute, self).__init__(
            OrderedDict([
                ('from', String(kwargs["from"])),
                ('to', String(kwargs["to"])),
                ('who', String(kwargs["who"])),
                ('escrow_id', Uint32(kwargs["escrow_id"])),
            ]))


class Escrow_release(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Escrow_release, self).__init__(
            OrderedDict([
                ('from', String(kwargs["from"])),
                ('to', String(kwargs["to"])),
                ('who', String(kwargs["who"])),
                ('escrow_id', Uint32(kwargs["escrow_id"])),
                ('bbd_amount', Amount(kwargs["bbd_amount"])),
                ('dpay_amount', Amount(kwargs["dpay_amount"])),
            ]))


class Escrow_approve(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Escrow_approve, self).__init__(
            OrderedDict([
                ('from', String(kwargs["from"])),
                ('to', String(kwargs["to"])),
                ('agent', String(kwargs["agent"])),
                ('who', String(kwargs["who"])),
                ('escrow_id', Uint32(kwargs["escrow_id"])),
                ('approve', Bool(kwargs["approve"])),
            ]))


class Decline_voting_rights(GrapheneObject):
    def __init__(self, *args, **kwargs):
        if check_for_class(self, args):
            return
        if len(args) == 1 and len(kwargs) == 0:
            kwargs = args[0]
        super(Decline_voting_rights, self).__init__(
            OrderedDict([
                ('account', String(kwargs["account"])),
                ('decline', Bool(kwargs["decline"])),
            ]))
