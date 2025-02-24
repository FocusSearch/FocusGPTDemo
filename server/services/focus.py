# -*- coding: utf-8 -*-
# @Time    : 2025/2/24 10:52
# @Author  : ShaoJK
# @File    : focusgpt.py
# @Remark  :
import uuid

from flask import request
from services.http import post, get


def __check_datasource_param(params, key):
    param = params.get(key)
    if param:
        return param
    else:
        raise ValueError("如果连接外部数据源，%s参数是必填项。" % key.capitalize())


def __parse_datasource_config(params) -> dict:
    if not params:
        return None
    db_type = params.get("type")
    if not db_type:
        return None
    name = params.get("name")
    if not name:
        name = "%s-%s" % (db_type, str(uuid.uuid4())[:8])
    host = __check_datasource_param(params, "host")
    port = __check_datasource_param(params, "port")
    user = __check_datasource_param(params, "user")
    password = __check_datasource_param(params, "password")
    db = __check_datasource_param(params, "db")
    return {
        "type": db_type,
        "name": name,
        "description": params.get("description"),
        "schemaName": params.get("schema"),
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "db": db,
        "jdbcSuffix": params.get("jdbc")
    }


def list_tables():
    """获取表列表"""
    datasource = __parse_datasource_config(request.json.get("datasource"))
    tbl_name = request.args.get("name", "")
    if datasource:
        return post("/df/rest/datasource/tables", params={"name": tbl_name}, body=datasource)
    else:
        return get("/df/rest/table/list", params={"name": tbl_name})


def init():
    params = request.json
    """初始化FocusGPT上下文"""
    language = params.get("language", "chinese").lower()
    tbl_name = params.get("name")
    datasource = __parse_datasource_config(params.get("datasource"))
    body = {"language": language}
    if datasource:
        body["dataSource"] = datasource
    if tbl_name:
        body["names"] = [tbl_name]
    else:
        raise KeyError("TableName不可以为空.")
    return post("/df/rest/gpt/init", body=body)


def chat():
    params = request.json
    query = params.get("query")
    chat_id = params.get("chatId")
    if chat_id:
        if query:
            return post("/df/rest/gpt/data", body={"input": query, "chatId": chat_id})
        else:
            raise KeyError("query不可以是空")
    else:
        raise KeyError("chatId不可以是空")
