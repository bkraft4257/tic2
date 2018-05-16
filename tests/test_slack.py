# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import json
import requests

from tic_core import slack


def test_get_webhook():

    webhook_url = slack.get_webhook()
    print(webhook_url)


def test_webhook():
    """
    Test the Slack API to send a message to cl-wf-data-monitor
    :return:

    In order to send messages to Slack you need a webhook.  Obtaining a webhook is easy.  You
    open the Slack App and install the Incoming WebHooks App. This will ask you which channel
    you want to add a WebHook.  You select the channel it will the post the URL.

    Copy this URL.  The WebHook should not be stored in any of the TIC code on GitHub. The WebHook
    and other confidential information should be added to the tic_configuration.json file in the
    .tic directory.  This configuration file should never be added to the TIC core code. Instead, it should
    be manually passed from TIC members and configured for their individual needs.

    """

    # webhook_url = slack.get_webhook()
    webhook_url = 'https://hooks.slack.com/services/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'
    slack_data = {'text': "Sup! We're slacking now."}

    response = requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
    )

    print(response)

    assert response.status_code == 200
