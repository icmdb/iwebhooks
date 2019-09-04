# -*- coding: utf-8 -*-
#
# @reference:
#   https://api.slack.com/incoming-webhooks
#   https://api.slack.com/tools/block-kit-builder
#   https://yq.aliyun.com/articles/64921
#   https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq
#

import base64

csr_slack_args    = {'slackin': u'xxx', 'channel': u'temp'}
csr_dingtalk_args = {'dingtoken': u'xxx', 'at_mobiles': '18600000000,18500000000'}
csr_pushdata = {
    "push_data": {
        "digest": "sha256:14bf0c9f45293f4783bd75e51ea68689103k89da6e51db75ef30b8564fe8d3cc",
        "pushed_at": "2019-08-03 15:02:58",
        "tag": "latest"
    },
    "repository": {
        "date_created": "2019-08-03 12:37:44",
        "name": "iwebhook",
        "namespace": "icmdb",
        "region": "cn-hongkong",
        "repo_authentication_type": "NO_CERTIFIED",
        "repo_full_name": "icmdb/iwebhook",
        "repo_origin_type": "NO_CERTIFIED",
        "repo_type": "PUBLIC"
    }
}


class CsrWebook(object):
    def __init__(self, req_json, req_args):
        self.slack_payload = {}
        self.dingtalk_payload = {}
        self.data = {
            "digest"                   : req_json["push_data"]["digest"],
            "pushed_at"                : req_json["push_data"]["pushed_at"],
            "tag"                      : req_json["push_data"]["tag"],
            "data_create"              : req_json["repository"]["date_created"],
            "name"                     : req_json["repository"]["name"],
            "namespace"                : req_json["repository"]["namespace"],
            "region"                   : req_json["repository"]["region"],
            "repo_authentication_type" : req_json["repository"]["repo_authentication_type"],
            "repo_full_name"           : req_json["repository"]["repo_full_name"],
            "repo_origin_type"         : req_json["repository"]["repo_origin_type"],
            "repo_type"                : req_json["repository"]["repo_type"],
        }
        for k in req_args:
            self.data[k] = req_args[k]
        self.data["image"]             = "/".join([self.data["namespace"], self.data["name"]])
        
    def set_slack_payload(self, username="AliCloud CS Registry", color="#2db67c", icon_url=""):
        pretext   = "Image [<https://cr.console.aliyun.com/repository/%s/%s/details|%s>] pushed sucessfully!" % (self.data["region"], self.data["image"], self.data["image"])
        if not icon_url:
            icon_url  = "https://s3-us-west-2.amazonaws.com/slack-files2/bot_icons/2019-08-03/703942552627_48.png"

        self.slack_payload = {
            "channel" : "#%s" % (self.data["channel"]),
            "username": "%s"  % (username),
            "icon_url":  "%s" % (icon_url),
            "attachments": [
                {
                    "fallback": "%s"  % (pretext),
                    "pretext" : "%s"  % (pretext),
                    "color"   : "%s"  % (color),
                    "fields"  : [
                        {
                            "title" : "image: %s"   % (self.data["image"]),
                            "value" : "\n".join([
                                "*pushed_at*: _%s_" % (self.data["pushed_at"]),
                                "*region*: _%s_"    % (self.data["region"]),
                                "*type*: _%s_"      % (self.data["repo_type"].lower()),
                                "*tag*: _%s_"       % (self.data["tag"]),
                            ]),
                            "short" : "false"
                        }
                    ]
                }
            ]
        }
        return self.slack_payload

    def get_slack_incoming_url(self):
        if "slackin" in self.data:
            return base64.b64decode(self.data["slackin"])
        return None

    def set_dingtalk_payload(self, text_list=[], at_mobiles=[], is_all=False):
        title = "**Image [[%s](https://cr.console.aliyun.com/repository/%s/%s/details|%s)] pushed sucessfully!**" % (self.data["image"], self.data["region"], self.data["image"], self.data["image"])
        at_mobiles = at_mobiles or self.data["at_mobiles"].split(",")
        self.dingtalk_payload = {
                "msgtype" : "markdown",
                "markdown": {
                    "title": title,
                    "text" : "\n\n".join([
                        " %s"              % (title),
                        "> **image**: %s"     % (self.data["image"]),
                        "> **pushed_at**: %s" % (self.data["pushed_at"]),
                        "> **region**: %s"    % (self.data["region"]),
                        "> **tag**: %s"       % (self.data["tag"]),
                    ])
                },
                "at" : {
                    "atMobiles": at_mobiles,
                    "isAll": is_all
                }
            }
        return self.dingtalk_payload

    def get_dingtalk_token(self):
        if "dingtoken" in self.data:
            return self.data["dingtoken"]
        return None
        

def set_payload(csr_pushdata, csr_dingtalk_args):
    csr = CsrWebook(csr_pushdata, csr_dingtalk_args)
    if "slackin" in csr.data.keys():
        csr.set_slack_payload()
    if "dingtoken" in csr.data.keys():
        csr.set_dingtalk_payload()
    return csr



if __name__ == "__main__":
    from islack import slack_incoming
    from idingtalk import dingtalk_incoming

    csr = AcrWebook(csr_pushdata, csr_dingtalk_args)
    print(csr.set_dingtalk_payload())
    print(csr.set_slack_payload())
    print(dingtalk_incoming(csr.get_dingtalk_token(), payload=csr.dingtalk_payload, debug=True))
    print(slack_incoming(csr.get_slack_incoming_url(), payload=csr.slack_payload, username="ACS Registry", debug=True))

