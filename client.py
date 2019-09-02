# -*- coding: utf-8 -*-

import os
import sys
import json
import time
import base64
import requests

IWEBHOOK_BASE_URL           = os.getenv("IWEBHOOK_BASE_URL"          , "")
IWEBHOOK_SLACK_URL          = os.getenv("IWEBHOOK_SLACK_URL"         , "")
IWEBHOOK_SLACK_CHANNEL      = os.getenv("IWEBHOOK_SLACK_CHANNEL"     , "")
IWEBHOOK_DINGTALK_TOKEN     = os.getenv("IWEBHOOK_DINGTALK_TOKEN"    , "")
IWEBHOOK_DINGTALK_ATMOBILES = os.getenv("IWEBHOOK_DINGTALK_ATMOBILES", "")

csr_webhook = {
    "slack"     : "%s/ali/csr/webhook?slackin=%s&channel=%s" % (IWEBHOOK_BASE_URL, base64.b64encode(IWEBHOOK_SLACK_URL), IWEBHOOK_SLACK_CHANNEL),
    "dingtalk"  : "%s/ali/csr/webhook?dingtoken=%s&at_mobiles=%s" % (IWEBHOOK_BASE_URL, IWEBHOOK_DINGTALK_TOKEN, IWEBHOOK_DINGTALK_ATMOBILES),
    "bearychat" : "", # TODO:
    "wechat"    : "", # TODO:
}

csr_pushdata = {
    "push_data": {
        "digest": "sha256:14bf0c9f483bd75e51ea68689103k89da6e51db75ef30b8564fe8d3cc",
        "pushed_at": "2019-09-02 15:02:58",
        "tag": "latest"
    },
    "repository": {
        "date_created": "2019-09-02 12:37:44",
        "name": "iwebhook",
        "namespace": "icmdb",
        "region": "cn-hongkong",
        "repo_authentication_type": "NO_CERTIFIED",
        "repo_full_name": "icmdb/iwebhook",
        "repo_origin_type": "NO_CERTIFIED",
        "repo_type": "PUBLIC"
    }
}

csr_slack = requests.post(csr_webhook["slack"], data=json.dumps(csr_pushdata))
print(" csr_slack ".center(56, "*"))
print(csr_slack.url, csr_slack.ok)
print(csr_slack.content)

time.sleep(3)

csr_dingtalk = requests.post(csr_webhook["dingtalk"], data=json.dumps(csr_pushdata))
print(" csr_dingtalk ".center(56, "*"))
print(csr_dingtalk.url, csr_dingtalk.ok)
print(csr_dingtalk.content)

time.sleep(3)

#cms_slack = requests.post()
