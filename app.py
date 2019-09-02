# -*- coding: utf-8 -*-

import os
import json

from flask import Flask, request
from islack import slack_incoming
from idingtalk import dingtalk_incoming
from ibearychat import bearychat_incoming
from ialicloud.csr import set_payload


APP_ADDR  = os.getenv("APP_ADDR"  , "0.0.0.0") 
APP_PORT  = os.getenv("APP_PORT"  , 8080)
APP_DEBUG = os.getenv("APP_DEBUG" , True)


app = Flask(__name__)

@app.route("/ali/csr/webhook", methods=["GET", "POST"])
def ali_csr_webhook():
    res = {}
    if request.method == "POST":
        req_args = request.args.to_dict()
        req_json = json.loads(request.get_data())
        if APP_DEBUG:
            print("req_args".center(56, "*"))
            print(req_args)
            print("req_json".center(56, "*"))
            print(req_json)

        csr = set_payload(req_json, req_args)

        if "slackin" in req_args.keys():
            res_slack = slack_incoming(
                csr.get_slack_incoming_url(),
                payload=csr.slack_payload, 
                username="ACS Registry",
                debug=APP_DEBUG
            )
            if APP_DEBUG:
                print("res_slack".center(56, "*"))
                print(res_slack)
            res["slack"] = res_slack.ok

        if "dingtoken" in req_args.keys():
            res_dingtalk = dingtalk_incoming(
                csr.get_dingtalk_token(),
                payload=csr.dingtalk_payload, 
                debug=APP_DEBUG
            )
            if APP_DEBUG:
                print("res_dingtalk".center(56, "*"))
                print(res_dingtalk)
            res["dingtalk"] = res_dingtalk.ok
    else:
        return '{"error": "1", "msg": "Should be request by post method!"}'

    if APP_DEBUG:
        return json.dumps({"req_json": req_json, "req_args": req_args, "res": res})

    return json.dumps(res)


if __name__ == "__main__":
    app.run(host=APP_ADDR, port=APP_PORT, debug=APP_DEBUG)
