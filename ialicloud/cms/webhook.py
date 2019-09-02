# -*- coding: utf-8 -*-
#
# @reference:
#

import json
import base64

"""cms_data
/ali/cms/webhook?im=slack,bearychat,wechat&slackin=xxxxxxxx&at_mobile=18600000000,18500000000&channel=temp
/ali/cms/webhook?appgroup=ap-test

Content-Length: 544
User-Agent: Apache-HttpClient/4.4.1 (Java/1.7.0_65)
Connection: Keep-Alive
Host: 58.87.67.36:8888
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Accept-Encoding: gzip,deflate

{
    "alertName": "IOPS",
    "alertState": "ALERT",
    "curValue": "0.1",
    "dimensions": "{userId=xxxxxxxxxxxx, instanceId=rm-xxxxxxxxxxxx}",
    "expression": "$Average<=0.1",
    "instanceName": "rds-xxxx-xxxx",
    "metricName": "IOPS\\u4f7f\\u7528\\u7387",
    "metricProject": "acs_rds",
    "namespace": "acs_rds",
    "preTriggerLevel": "null",
    "ruleId": "applyTemplatef82fdbfd-bc24-45de-870a-d321eb463ad4",
    "signature": "OWjhogKrD2pTt9j2M8ianpqevvc=",
    "timestamp": "1565882760000",
    "triggerLevel": "INFO",
    "userId": "xxxxxxxxxxxxxxx"
}

{
    "alertName": "diskusage_utilization_95.0",
    "alertState": "ALERT",
    "curValue": "95",
    "dimensions": "{userId=xxxxxxxxxxxxxx, device=/dev/vda1, instanceId=i-xxxxxxxxxxxxxxxxxx}",
    "expression": "$Average>=95",
    "instanceName": "xx-xx-xx-xx-xx-xx/x.x.x.x",
    "metricName": "\u78c1\u76d8\u4f7f\u7528\u7387",
    "metricProject": "acs_ecs",
    "namespace": "acs_ecs",
    "preTriggerLevel": "INFO",
    "ruleId": "applyTemplateGroupf9e25e03-1fff-4bff-8bd1-f5f8a69c3b13",
    "signature": "in5UgQ6xNdobMty9m9UDvn6gFUw=",
    "timestamp": "1566382980000",
    "triggerLevel": "INFO",
    "userId": "xxxxxxxxxxx"
}
"""

req_data = {
    "alertName": "IOPS",
    "alertState": "ALERT",
    "curValue": "0.1",
    "dimensions": "{userId=xxxxxxxxxxxx, instanceId=rm-xxxxxxxxxxx}",
    "expression": "$Average<=0.1",
    "instanceName": "apr-flash-\\u5c0f\\u5e01\\u79cd",
    "metricName": "IOPS\\u4f7f\\u7528\\u7387",
    "metricProject": "acs_rds",
    "namespace": "acs_rds",
    "preTriggerLevel": "null",
    "ruleId": "applyTemplatef82fdbfd-bc24-45de-870a-d321eb463ad4",
    "signature": "OWjhogKrD2pTt9j2M8ianpqevvc=",
    "timestamp": "1565882760000",
    "triggerLevel": "INFO",
    "userId": "xxxxxxxxxxxxxxx"
}

class CmsWebhook(object):
    def __init__(self, req_data, req_args):
        self.slack_payload = {}
        self.bearychat_payload = {}
        self.data = req_data
        for k in req_args:
            self.data[k] = req_args[k]

    def set_slack_payload(self, username="AliCloudMonit", color="#2db67c", icon_url=""):
        pretext   = u"[阿里云监控] 应用分组-%s-发生%s，触发规则：%s" % (self.data["channel"], self.data["alertState"], self.data["alertName"])
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
                            "title" : "Instance: %s"   % (self.data["instanceName"]),
                            "value" : "\n".join([
                                "*UserID*: _%s_"   % (self.data["userId"]),
                                "*Instance*: _%s_" % (self.data["instanceName"]),
                                "*Metric*: _%s_"   % (self.data["metricName"]),
                                "*Status*: _%s_"   % (self.data["alertState"]),
                                "*Value*: _%s_"    % (self.data["curValue"]),
                                "*rule*: _%s_"     % (self.data["expression"].lower()),
                                "*time*: _%s_"     % (self.data["timestamp"]),
                            ]),
                            "short" : "false"
                        }
                    ]
                }
            ]
        }
        return self.slack_payload

    def set_bearychat_payload(self):
        self.bearychat_self.payload = {
            "text"        : "%s" % (self.data["instanceName"]),
            "attachments" : [
                {
                    "title"   : "This is the title.",
                    "markdown": "true",
                    "url"     : "",
                    "color"   : "#70cc29",
                    "text"    : "This is the first line.\n This is the second line."
                }
            ]
        }

    def get_slack_incoming(self):
        if "slackin" in self.data.keys():
            return base64.b64decode(self.data["slackin"])
        return None

    def get_bearychat_incoming(self):
        if "bearychatin" in self.data.keys():
            return base64.b64decode(self.data["bearychatin"])
        return None


def set_payload(req_data, req_args):
    cms = CmsWebhook(req_data, req_args)
    pass


if __name__ == "__maini__":
    cms = CmsWebhook(req_data, req_args)
    print(cms.set_slack_payload())
