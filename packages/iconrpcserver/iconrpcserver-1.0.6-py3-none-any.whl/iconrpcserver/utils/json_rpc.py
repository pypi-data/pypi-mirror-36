# Copyright 2018 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import json
import aiohttp

from jsonrpcclient.aiohttp_client import aiohttpClient

from ..default_conf.icon_rpcserver_constant import ConfigKey, ApiVersion
from ..utils.message_queue.stub_collection import StubCollection
from ..utils.icon_service.converter_v2 import convert_params, ParamType
from ..protos import message_code


async def redirect_request_to_rs(message, rs_target, version=ApiVersion.v3.name):
    method_name = "icx_sendTransaction"
    subscribe_use_https = StubCollection().conf[ConfigKey.SUBSCRIBE_USE_HTTPS]
    rs_url = f"{'https' if subscribe_use_https else 'http'}://{rs_target}/api/{version}"
    async with aiohttp.ClientSession() as session:
        result = await aiohttpClient(session, rs_url).request(method_name, message)

    return result


async def get_block_v2_by_params(block_height=None, block_hash="", with_commit_state=False):
    channel_name = StubCollection().conf[ConfigKey.CHANNEL]
    channel_stub = StubCollection().channel_stubs[channel_name]
    response_code, block_hash, block_data_json, tx_data_json_list = \
        await channel_stub.async_task().get_block_v2(
            block_height=block_height,
            block_hash=block_hash,
            block_data_filter="",
            tx_data_filter=""
        )
    block = json.loads(block_data_json)  # if fail, block = {}

    if block:
        block = convert_params(block, ParamType.get_block)

    result = {
        'response_code': response_code,
        'block': block
    }

    if 'commit_state' in result['block'] and not with_commit_state:
        del result['block']['commit_state']

    return block_hash, result


async def get_block_by_params(block_height=None, block_hash="", with_commit_state=False):
    channel_name = StubCollection().conf[ConfigKey.CHANNEL]
    block_data_filter = "prev_block_hash, height, block_hash, merkle_tree_root_hash," \
                        " time_stamp, peer_id, signature"
    tx_data_filter = "icx_origin_data"
    channel_stub = StubCollection().channel_stubs[channel_name]
    response_code, block_hash, block_data_json, tx_data_json_list = \
        await channel_stub.async_task().get_block(
            block_height=block_height,
            block_hash=block_hash,
            block_data_filter=block_data_filter,
            tx_data_filter=tx_data_filter
        )

    try:
        block = json.loads(block_data_json) if response_code == message_code.Response.success else {}
    except Exception as e:
        logging.error(f"get_block_by_params error caused by : {e}")
        block = {}

    result = {
        'response_code': response_code,
        'block': block
    }

    if 'commit_state' in result['block'] and not with_commit_state:
        del result['block']['commit_state']

    return block_hash, result
