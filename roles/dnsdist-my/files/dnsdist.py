#!/usr/bin/python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from pprint import pprint 
import requests
import json

class Dnsdist():

    def __init__(self, args):
        """
        constructor
        """
        self.args = args

    class DnsdistError(Exception):
        pass

    def get(self, action = '/jsonstat', command = ''):
        try:
            headers={'Content-Type': 'application/json', 'X-API-Key': 'eon1Vai8ahth' if self.args.get('apiKey', '').__contains__('apiKey') else self.args.get('apiKey', '')}
            params={'command': command}
            resp = requests.get(self.args.get('url') + action, params=params, headers=headers)
            if not resp.status_code == 200:
                raise self.DnsdistError('ReqestPostError', 'request status code: {};\n URL:{};\n text:{}'.format(str(resp.status_code), str(resp.url), str(resp.text)))
        except requests.exceptions.ConnectionError as E:
            return None
        except Exception as E:
            raise self.DnsdistError('ReqestPostError', E)
        return resp.json()


    def get_json(self):
        data = json.loads(getattr(self, self.args.get('json_function', ''))())
        return data.get(self.args.get('json_item'))


    def get_stats(self):
        return json.dumps(self.get(command='stats'), ensure_ascii=False)


    def discovery_frontends(self):
        data = []
        for frontend in self.get(action='/api/v1/servers/localhost').get('frontends'):
            data.append({'{#FRONTEND_ID}': frontend.get('id'), '{#FRONTEND_ADDRESS}': frontend.get('address'), '{#FRONTEND_TYPE}': 'UDP' if frontend.get('udp') is True else 'TCP'})
        return json.dumps({'data': data}, ensure_ascii=False)


    def get_frontend(self):
        frontend_id = self.args.get('id')
        for frontend in self.get(action='/api/v1/servers/localhost').get('frontends'):
            if str(frontend.get('id')) == frontend_id:
                return json.dumps(frontend, ensure_ascii=False)
        return False


    def discovery_nodes(self):
        data = []
        for node in self.get(action='/api/v1/servers/localhost').get('servers'):
            data.append({'{#NODE_ID}': node.get('id'), '{#NODE_NAME}': node.get('name'), '{#NODE_ADDRESS}': node.get('address')})
        return json.dumps({'data': data}, ensure_ascii=False)


    def get_node(self):
        node_id = self.args.get('id')
        for node in self.get(action='/api/v1/servers/localhost').get('servers'):
            if str(node.get('id')) == node_id:
                return json.dumps(node, ensure_ascii=False)
        return False


    def discovery_pools(self):
        data = []
        for pool in self.get(action='/api/v1/servers/localhost').get('pools'):
            data.append({'{#POOL_ID}': pool.get('id'), '{#POOL_NAME}': pool.get('name')})
        return json.dumps({'data': data}, ensure_ascii=False)


    def get_pool(self):
        pool_id = self.args.get('id')
        for pool in self.get(action='/api/v1/servers/localhost').get('pools'):
            if str(pool.get('id')) == pool_id:
                return json.dumps(pool, ensure_ascii=False)
        return False


    def discovery_rule(self):
        data = []
        for rule in self.get(action='/api/v1/servers/localhost').get('rules'):
            data.append({'{#RULE_ID}': rule.get('id'), '{#RULE_NAME}': rule.get('rule'), '{#RULE_ACT}': rule.get('action'), '{#RULE_CREATION_ORDER}': rule.get('creationOrder')})
        return json.dumps({'data': data}, ensure_ascii=False)


    def get_rule(self):
        rule_id = self.args.get('id')
        for rule in self.get(action='/api/v1/servers/localhost').get('rules'):
            if str(rule.get('creationOrder')) == rule_id:
                return json.dumps(rule, ensure_ascii=False)
        return False


    def all_params(self):
        return self.get(action='/api/v1/servers/localhost')


def parser():
    parser = ArgumentParser()
    # parser.add_argument("", help='', metavar='', dest='', required=True)
    parser.add_argument("url", help='', metavar='URL')
    parser.add_argument("apiKey", help='', metavar='apiKey')
    parser.add_argument("function", help='', metavar='FUNCTION')
    parser.add_argument("-id", help='', metavar='ID', dest='id', required=False)
    parser.add_argument("-jf", "--json_function", help='Function for json parser', metavar='JSON_FUNCTION', dest='json_function', required=False)
    parser.add_argument("-ji", "--item", help='Item for json parser', metavar='ITEM_JSON', dest='json_item', required=False)
    args = vars(parser.parse_args())
    return args


def main(args):
# args = {'url': '', 'function': '', 'apiKey': '', 'id': None}
    dnsdist = Dnsdist(args)
    print(getattr(dnsdist, args.get('function'))())
    return True


if __name__ == "__main__":
    main(parser())
