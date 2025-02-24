# -*- coding: utf-8 -*-
# @Time    : 2025/2/24 13:39
# @Author  : ShaoJK
# @File    : http.py
# @Remark  :
import requests

import config


def __build_url(path):
    return config.DF_URL + path


def get(url, params: dict = None):
    headers = {"Authorization": "Bearer %s" % config.DF_APP_TOKEN}
    response = requests.get(__build_url(url), params=params, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()


def post(url, body: dict = None, params: dict = None) -> dict:
    headers = {"Authorization": "Bearer %s" % config.DF_APP_TOKEN}
    response = requests.post(__build_url(url), params=params, json=body, headers=headers, verify=False)
    response.raise_for_status()
    return response.json()
