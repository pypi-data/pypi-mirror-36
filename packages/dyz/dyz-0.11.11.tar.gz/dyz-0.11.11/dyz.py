#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import base64
import base64 as pkg_base64
import code
import codecs
import csv
import glob
import os
import random as pkg_random
import re
import signal
import string as pkg_string
import sys
import threading
import time
import uuid as pkg_uuid
from StringIO import StringIO
from datetime import datetime, date as date_type
from decimal import Decimal
from os.path import expanduser
from pprint import pprint

import click
import odoorpc
import psycopg2
import validictory
import yaml
from dateutil import parser as dt_parser
from dateutil.relativedelta import relativedelta
from dyools import IF, Operator, Logger, File
from faker import Faker
from lxml import etree
from odoorpc.tools import v
from prettytable import PrettyTable

fake = Faker('fr_FR')

Log = Logger()

ODOO_FIELDS = ['__last_update', 'create_date', 'create_uid', 'write_date', 'write_uid']

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'

home = expanduser("~")
home = os.path.join(home, '.dyvz')

CONFIG_FILE = os.path.join(home, 'dyz.ini')

__VERSION__ = '0.11.11'

SCHEMA_GLOBAL = {
    "type": "object",
    "properties": {
        "repeat": {
            "type": "integer",
            "required": False,
            "minimum": 1,
        },
        "ignore": {
            "type": "boolean",
            "required": False,
        },
        "section": {
            "type": "string",
            "required": False,
        },
        "mode": {
            "type": "string",
            "required": False,
        },
        "port": {
            "type": "integer",
            "required": False,
        },
        "database": {
            "type": "string",
            "required": False,
        },
        "host": {
            "type": "string",
            "required": False,
        },
        "menu_delete": {
            "type": "boolean",
            "required": False,
        },
        "message": {
            "type": "object",
            "required": False,
            "properties": {
                "title": {
                    "type": "string",
                    "required": True,
                },
                "body": {
                    "type": "string",
                    "required": False,
                }
            },
        },
        "vars": {
            "required": False,
            "type": "array",
            "items": {
                "type": "object",
            },
        },
        "sleep": {
            "required": False,
            "type": "integer",
        },
        "show": {
            "required": False,
            "type": "object",
            "properties": {
                "model": {
                    "type": "string",
                },
                "fields": {
                    "type": "array",
                },
                "refs": {
                    "type": "any",
                    "required": False,
                },
                "order": {
                    "type": "string",
                    "required": False,
                },
                "limit": {
                    "type": "integer",
                    "required": False,
                },

            },
        },
        "menu": {
            "required": False,
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                },
                "code": {
                    "type": "string",
                },
                "parent_code": {
                    "type": "string",
                    "required": False,
                },
                "sequence": {
                    "type": "integer",
                    "required": False,
                },
                "action": {
                    "type": "object",
                    "required": False,
                    "properties": {
                        "model": {
                            "type": "string",
                        },
                        "context": {
                            "type": "object",
                            "required": False,
                        },
                        "domain": {
                            "type": "array",
                            "required": False,
                        },
                        "view_mode": {
                            "type": "string",
                            "required": False,
                        },
                        "views": {
                            "type": "array",
                            "required": False,
                            "items": {
                                "type": "object",
                                "required": True,
                                "properties": {
                                    "type": {
                                        "type": "string",
                                    },
                                    "sequence": {
                                        "type": "integer",
                                    },
                                    "fields": {
                                        "type": "array",
                                        "required": False
                                    },
                                    "attributes": {
                                        "type": "object",
                                        "required": False
                                    },
                                    "ref": {
                                        "type": "string",
                                        "required": False
                                    },
                                },
                            },
                        },
                    },
                },

            },
        },
        "import": {
            "required": False,
            "type": "object",
            "properties": {
                "model": {
                    "type": "string",
                },
                "path": {
                    "type": "string",
                },
                "view_ref": {
                    "type": "string",
                    "required": False,
                },
                "map": {
                    "type": "object",
                    "items": {
                        "type": "object",
                    }
                },
                "keys": {
                    "type": "array",
                    "required": False,
                    "items": {
                        "type": "string",
                    }
                },
                "number": {
                    "type": "integer",
                    "required": False,
                },
                "random": {
                    "type": "boolean",
                    "required": False,
                },
                "pick": {
                    "type": "array",
                    "required": False,
                    "items": {
                        "type": "object",
                        "required": True,
                        "patternProperties": {
                            ".*": {
                                "type": ["array", "string"],
                            },
                        },
                    }
                },
            },
        },
        "record": {
            "type": "object",
            "required": False,
            "properties": {
                "model": {
                    "type": "string",

                },
                "refs": {
                    "type": "any",
                    "required": False,

                },
                "condition": {
                    "type": "any",
                    "required": False,
                },
                "view_ref": {
                    "type": "string",
                    "required": False,

                },
                "key": {
                    "type": "string",
                    "required": False,
                },
                "order": {
                    "type": "string",
                    "required": False,

                },
                "limit": {
                    "type": "integer",
                    "required": False,
                },
                "values": {
                    "type": "array",
                    "required": False,

                },
                "show": {
                    "type": ["array", "boolean"],
                    "required": False,
                    "items": {
                        "type": "string",
                    },

                },
                "many2many": {
                    "type": "array",
                    "required": False,
                    "items": {
                        "type": "object",
                        "patternProperties": {
                            ".*": {
                                "type": 'string',
                                "enum": ['add', 'remove', 'replace']
                            }
                        }
                    },

                },
                "many2one": {
                    "type": "array",
                    "required": False,
                    "items": {
                        "type": "object",
                        "patternProperties": {
                            ".*": {
                                "type": 'array',
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "limit": {
                                            "type": "integer",
                                            "required": False,
                                        },
                                        "order": {
                                            "type": "string",
                                            "required": False,
                                        },
                                    }

                                }

                            }
                        }
                    },
                },
                "context": {
                    "type": "object",
                    "required": False,
                },
                "typology": {
                    "type": "string",
                    "required": False,
                    "enum": ['one', 'multi', 'last', 'model', 'first'],
                },

                "create": {
                    "type": "boolean",
                    "required": False,

                },
                "write": {
                    "type": "boolean",
                    "required": False,

                },
                "unlink": {
                    "type": "boolean",
                    "required": False,

                },
                "functions": {
                    "type": "array",
                    "required": False,
                    "items": {
                        "type": "object",
                        "required": False,
                        "properties": {
                            "name": {
                                "type": "string",
                            },
                            "args": {
                                "type": "object",
                                "required": False,
                            },
                            "api": {
                                "type": "string",
                                "required": False,
                                "enum": ['one', 'multi', 'model'],
                            },
                            "kwargs": {
                                "type": "boolean",
                                "required": False,
                            }
                        }
                    }
                },
                "workflows": {
                    "type": "array",
                    "required": False,

                },
                "export": {
                    "type": "array",
                    "required": False,
                    "items": {
                        "type": "object"
                    }

                },
                "pick": {
                    "type": "array",
                    "required": False,
                    "items": {
                        "type": "object",
                        "required": True,
                        "patternProperties": {
                            ".*": {
                                "type": ["array", "string"],
                            },
                        },
                    }

                },
            },
        },

        "load": {
            "type": "object",
            "required": False,
            "properties": {
                "model": {
                    "type": "string",
                },
                "repeat": {
                    "type": "integer",
                    "required": False,
                },
                "values": {
                    "type": "array",
                    "required": True,
                    "items": {
                        "type": {
                            "type": "array",
                            "items": {
                                "type": {
                                    "type": "object",
                                },
                            },
                        },
                    },

                },
            },
        }
    },
}


def validate(_data, _schema):
    try:
        validictory.validate(_data, _schema, disallow_unknown_properties=True)
    except Exception as e:
        Log.error(e.message)


try:
    os.makedirs(home)
except:
    pass

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w+') as config_file:
        pass


def raise_keyboard_interrupt(*a):
    raise KeyboardInterrupt()


class Console(code.InteractiveConsole):
    def __init__(self, locals=None, filename="<console>"):
        code.InteractiveConsole.__init__(self, locals, filename)
        try:
            import readline
            import rlcompleter
        except ImportError:
            print 'readline or rlcompleter not available, autocomplete disabled.'
        else:
            readline.set_completer(rlcompleter.Completer(locals).complete)
            readline.parse_and_bind("tab: complete")


class Shell(object):
    def init(self, args):
        signal.signal(signal.SIGINT, raise_keyboard_interrupt)

    def console(self, local_vars):
        if not os.isatty(sys.stdin.fileno()):
            exec sys.stdin in local_vars
        else:
            Console(locals=local_vars).interact()


def process_domain(ctx, name, _value):
    domain = []
    if _value:
        for d in _value:
            field, operator, value = d
            try:
                value = eval(value)
            except:
                pass
            if operator.startswith('dt'):
                operator = operator[2:]
                value = parse_date_hash(ctx, value).strftime(DATETIME_FORMAT)
            if operator.startswith('d'):
                operator = operator[1:]
                value = parse_date_hash(ctx, value).strftime(DATE_FORMAT)
            if field in ['create_date', 'write_date']:
                if value in ['today', 'yesterday']:
                    dt = datetime.now()
                    if value == 'yesterday':
                        dt = dt + relativedelta(days=-1)
                    domain.append((field, '>=', dt.strftime('%Y-%m-%d 00:00:00')))
                    domain.append((field, '<=', dt.strftime('%Y-%m-%d 23:59:59')))
                    continue
            operator = operator.replace('gte', '>=')
            operator = operator.replace('gt', '>')
            operator = operator.replace('lte', '<=')
            operator = operator.replace('lt', '<')
            operator = operator.replace('eq', '=')
            domain.append((field, operator, value))
    if ctx.obj['debug']:
        Log.debug(domain)
    return domain


def __normalize_domain(ctx, domain, ou, slug):
    domain = domain or []
    if slug:
        domain = [('id', 'in', unslugify(slug))] + domain
    if not domain:
        return domain
    if len(domain) <= 1:
        return domain
    if not ou:
        return domain
    else:
        domain = ['|'] * (len(domain) - 1) + domain
        if ctx.obj['debug']:
            Log.debug(domain)
        return domain


def __order_fields(fields):
    def f(item):
        if item == 'id':
            return 1
        elif item == 'display_name':
            return 2
        elif item == 'name':
            return 3
        elif item.startswith('name'):
            return 4
        elif item.endswith('_id'):
            return 99
        elif item.endswith('_ids'):
            return 100
        else:
            return 50

    return sorted(fields, key=f)


def parse_date_hash(ctx, hash, dt=None):
    if not dt:
        dt = datetime.now()
    pattern = re.compile("([+-])*(\d+)([MSMHmdyw])")
    values = pattern.findall(hash)
    for sign, number, code in values:
        coeff = -1 if sign == '-' else 1
        number = int(number) if number and number.isdigit() else 0
        if not code:
            Log.error('the term %s is not processed' % hash)
        years = months = weeks = days = hours = minutes = seconds = microseconds = 0
        if code == 'M':
            microseconds = coeff * number
        if code == 'S':
            seconds = coeff * number
        if code == 'M':
            minutes = coeff * number
        if code == 'H':
            hours = coeff * number
        if code == 'd':
            days = coeff * number
        if code == 'm':
            months = coeff * number
        if code == 'y':
            years = coeff * number
        if code == 'w':
            weeks = coeff * number

        dt = dt + relativedelta(
            years=years,
            months=months,
            weeks=weeks,
            days=days,
            hours=hours,
            minutes=minutes,
            seconds=seconds,
            microseconds=microseconds
        )
    return dt


@click.group()
@click.option('--database', '-d', type=click.STRING, default=None, help="The database")
@click.option('--host', '-h', type=click.STRING, default=None, help="The host of the server")
@click.option('--load', '-l', type=click.STRING, help="The name of section to load")
@click.option('--prompt-login', type=click.BOOL, is_flag=True, help="Prompt the Odoo parameters for loggin")
@click.option('--prompt-connect', type=click.BOOL, is_flag=True, help="Prompt the Odoo parameters for connection")
@click.option('--config', '-c',
              type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=True, readable=True,
                              resolve_path=True), default=CONFIG_FILE, help="The path of config")
@click.option('--port', '-p', type=click.INT, default=0, help="The port of the server")
@click.option('--user', '-u', type=click.STRING, default=None, help="The user of the database")
@click.option('--password', '-pass', type=click.STRING, default=None, help="The password of the user")
@click.option('--superuserpassword', '-s', type=click.STRING, default=None, help="The password of the super user")
@click.option('--protocol', type=click.Choice(['jsonrpc+ssl', 'jsonrpc']), default=None, help="Protocol to use")
@click.option('--mode', '-m', type=click.Choice(['test', 'dev', 'prod']), default=None, help="Database mode")
@click.option('--timeout', '-t', type=click.INT, default=60, help="Timeout in minutes")
@click.option('--yes', is_flag=True, default=False)
@click.option('--no-context', is_flag=True, default=False)
@click.option('--debug', is_flag=True, default=False)
@click.option('--workers', '-w', type=click.INT, default=0)
@click.version_option(__VERSION__, expose_value=False, is_eager=True, help="Show the version")
@click.pass_context
def cli(ctx, database, host, port, user, password, superuserpassword, protocol, timeout, config, load, mode,
        prompt_login, prompt_connect, yes, no_context, debug, workers):
    """CLI for Odoo"""
    odoo = False
    prompt_connect = prompt_login or prompt_connect

    def xml_id(record, record_id=False):
        global odoo
        if not record:
            return ''
        if not record_id:
            res_model, res_id = record._name, record.id
        else:
            res_model, res_id = record, record_id
        IrModelData = odoo.env['ir.model.data']
        data_id = IrModelData.search([('model', '=', res_model), ('res_id', '=', res_id)])
        data = IrModelData.browse(data_id)
        return data.complete_name if data else ''

    def object_from_xml_id(xmlid):
        global odoo
        if not xmlid:
            return False
        xmlid_tuple = xmlid.strip().split('.')
        module = False
        if len(xmlid_tuple) == 2:
            module, xml_name = xmlid_tuple
        else:
            xml_name = xmlid
        IrModelData = odoo.env['ir.model.data']
        model_domain = [('name', '=', xml_name)]
        if module:
            model_domain.append(('module', '=', module))
        data_id = IrModelData.search(model_domain)
        data = IrModelData.browse(data_id)
        if data:
            return odoo.env[data.model].browse(data.res_id)
        return False

    def action_connect():
        global odoo
        if mode == 'prod':
            if not yes and not click.confirm('You are in mode production, continue ?'):
                sys.exit()
        try:
            Log.info('Try to connect to the host %s:%s, database=%s, mode=%s, timeout=%smin' % (
                host, port, database, mode, timeout / 60))
            odoo = odoorpc.ODOO(host, protocol=protocol, port=port, timeout=timeout)
            odoo.config['auto_context'] = not no_context
            Log.success('Connected to host %s:%s, database=%s, version=%s, mode=%s, timeout=%smin' % (
                host, port, database, odoo.version, mode, timeout / 60))
            ctx.obj['version'] = int(
                ''.join([x for x in odoo.version.strip() if x.isdigit() or x == '.']).split('.')[0])
        except:
            Log.error('Cannot connect to host %s:%s, database=%s, mode=%s' % (host, port, database, mode))
        return odoo

    def action_login():
        global odoo
        odoo = action_connect()
        if odoo:
            odoo = odoorpc.ODOO(host, protocol=protocol, port=port, timeout=timeout)
            try:
                Log.info('Try to login to the database %s as %s' % (database, user))
                odoo.login(database, user, password)
                Log.success('Connected to the database %s as %s' % (database, user))
            except:
                Log.error('Cannot connect to the database %s as %s' % (database, user))
        return odoo

    def get_new_odoo():
        new_odoo = False
        if mode == 'prod':
            if not yes and not click.confirm('You are in mode production, continue ?'):
                sys.exit()
        try:
            Log.info('Try to connect to the host %s:%s, database=%s, mode=%s, timeout=%smin' % (
                host, port, database, mode, timeout / 60))
            new_odoo = odoorpc.ODOO(host, protocol=protocol, port=port, timeout=timeout)
            new_odoo.config['auto_context'] = not no_context
            Log.success('Connected to host %s:%s, database=%s, version=%s, mode=%s, timeout=%smin' % (
                host, port, database, new_odoo.version, mode, timeout / 60))
            ctx.obj['version'] = int(
                ''.join([x for x in new_odoo.version.strip() if x.isdigit() or x == '.']).split('.')[0])
            new_odoo = odoorpc.ODOO(host, protocol=protocol, port=port, timeout=timeout)
            Log.info('Try to login to the database %s as %s' % (database, user))
            new_odoo.login(database, user, password)
            Log.success('Connected to the database %s as %s' % (database, user))
        except:
            Log.error('Cannot connect to the database %s as %s' % (database, user))
        return new_odoo

    def update_list():
        global odoo
        if odoo:
            Log.info('Updating the list of modules ...')
            odoo.env['ir.module.module'].update_list()

    timeout *= 30

    config_obj = ConfigParser.ConfigParser()
    ctx.obj['config_obj'] = config_obj
    ctx.obj['config_path'] = config
    config_obj.read(config)
    if not load:
        for _sec in config_obj.sections():
            default = config_obj.has_option(_sec, 'default') and config_obj.getboolean(_sec, 'default') or False
            if default:
                load = _sec
    load_from_config = load and load in config_obj.sections()
    if load_from_config:
        Log.title('Loading data from the config file ...')
    ctx.obj['load'] = load
    ctx.obj['_database'] = database
    ctx.obj['_host'] = host
    ctx.obj['_port'] = port
    ctx.obj['_user'] = user
    ctx.obj['_password'] = password
    ctx.obj['_protocol'] = protocol
    ctx.obj['_superuserpassword'] = superuserpassword
    ctx.obj['_mode'] = mode
    ctx.obj['_default'] = False

    database = database or (config_obj.get(load, 'database', database) if load_from_config else database)
    host = host or (config_obj.get(load, 'host', host) if load_from_config else host)
    port = int(port) or (config_obj.getint(load, 'port') if load_from_config else port)
    user = user or (config_obj.get(load, 'user', user) if load_from_config else user)
    password = password or (config_obj.get(load, 'password', password) if load_from_config else password)
    protocol = protocol or (config_obj.get(load, 'protocol', protocol) if load_from_config else protocol)
    mode = mode or (config_obj.get(load, 'mode', mode) if load_from_config else mode)
    superuserpassword = superuserpassword or (
        config_obj.get(load, 'superuserpassword', superuserpassword) if load_from_config else superuserpassword)
    if prompt_connect:
        host = click.prompt('host', host, type=str)
        port = click.prompt('port', default=port, type=str)
        superuserpassword = click.prompt('superuserpassword', default=superuserpassword, type=str)
        protocol = click.prompt('protocol', protocol, type=str)
    ctx.obj['prompt_database'] = False
    if prompt_login:
        ctx.obj['prompt_database'] = True
        database = click.prompt('database', default=database, type=str)
        user = click.prompt('user', default=user, type=str)
        password = click.prompt('password', default=password, type=str)
        mode = click.prompt('mode', default=mode, type=str)
    ctx.obj['database'] = database
    ctx.obj['host'] = host
    ctx.obj['port'] = port
    ctx.obj['user'] = user
    ctx.obj['password'] = password
    ctx.obj['protocol'] = protocol
    ctx.obj['superuserpassword'] = superuserpassword
    ctx.obj['mode'] = mode
    ctx.obj['odoo'] = odoo
    ctx.obj['action_login'] = action_login
    ctx.obj['get_new_odoo'] = get_new_odoo
    ctx.obj['action_connect'] = action_connect
    ctx.obj['odoo'] = odoo
    ctx.obj['xml_id'] = xml_id
    ctx.obj['object_from_xml_id'] = object_from_xml_id
    ctx.obj['update_list'] = update_list
    ctx.obj['debug'] = debug and True or False
    ctx.obj['workers'] = workers

    PROD_COMMANDS_BLACKLIST = [
        'db_drop',
        'db_restore',
        'db_create',
        'func',
        'debug',
        'module_install',
        'module_upgrade',
        'module_install_all',
        'module_uninstall',
        'install',
        'upgrade',
        'install_all',
        'uninstall',
        'truncate',
        'record_update',
        'record_create',
        'record_unlink',
        'load_yaml',
        'pg_truncate',
        'pg_reset_passwords',
    ]
    if mode == 'prod' and ctx.invoked_subcommand in PROD_COMMANDS_BLACKLIST:
        Log.error('The command "%s" is not enabled in production mode !!' % ctx.invoked_subcommand)


# database functions

@cli.command()
@click.pass_context
def pg_login(ctx):
    """Login to the postgresql"""
    Log.info('Databases :')
    index = 0
    kw = {
        'host': ctx.obj['host'],
        'port': ctx.obj['port'],
        'user': ctx.obj['user'],
        'password': ctx.obj['password'],
    }
    databases = [ctx.obj['database']]
    if databases == ['all']:
        conn = psycopg2.connect(**kw)
        cur = conn.cursor()
        databses_sql = """
            SELECT datname FROM pg_database WHERE datistemplate = false;
        """
        cur.execute(databses_sql)
        databases = [x[0] for x in cur.fetchall()]
        conn.close()
    for db in databases:
        kw = dict(kw, database=db)
        conn = psycopg2.connect(**kw)
        cur = conn.cursor()
        table_sql = """
                SELECT count(*) 
                FROM pg_class
                WHERE relkind='r' 
                AND relname='res_users'
        """
        cur.execute(table_sql)
        count = cur.fetchone()[0]
        if count:
            index += 1
            Log.info(' %s -> %s' % (index, db,))
        conn.close()


@cli.command()
@click.pass_context
@click.option('--auto-commit', is_flag=True, type=click.BOOL, required=False, default=False)
@click.option('--commit', is_flag=True, type=click.BOOL, required=False, default=False)
@click.option('--yes', is_flag=True, type=click.BOOL, required=False, default=False)
def pg_reset_passwords(ctx, auto_commit, commit, yes):
    """Reset password of given databases to admin"""
    auto_commit = auto_commit or commit or False
    kw = {
        'host': ctx.obj['host'],
        'port': ctx.obj['port'],
        'user': ctx.obj['user'],
        'password': ctx.obj['password'],
    }
    databases = [ctx.obj['database']]
    if databases == ['all']:
        conn = psycopg2.connect(**kw)
        cur = conn.cursor()
        databses_sql = """
            SELECT datname FROM pg_database WHERE datistemplate = false;
        """
        cur.execute(databses_sql)
        databases = [x[0] for x in cur.fetchall()]
        conn.close()
    if not (yes or click.confirm('Continue on databases : %s' % databases)):
        Log.error('Exit')
    for db in databases:
        Log.info('Switch to the database %s' % (db,))
        kw = dict(kw, database=db)
        conn = psycopg2.connect(**kw)
        cur = conn.cursor()
        table_sql = """
                SELECT count(*) 
                FROM pg_class
                WHERE relkind='r' 
                AND relname='res_users'
        """
        cur.execute(table_sql)
        count = cur.fetchone()[0]
        if count:
            cur = conn.cursor()
            update_sql = """
                            UPDATE res_users SET password='admin';
                            UPDATE res_users SET login='admin' where id=1;
            """
            cur.execute(update_sql)
            Log.success('Data are updated in the database %s' % (db,))
        if auto_commit or click.confirm('Commit ?'):
            conn.commit()
        cur.close()
        conn.close()


@cli.command()
@click.pass_context
def pg_users(ctx):
    """Show users of given databases"""
    kw = {
        'host': ctx.obj['host'],
        'port': ctx.obj['port'],
        'user': ctx.obj['user'],
        'password': ctx.obj['password'],
    }
    databases = [ctx.obj['database']]
    if databases == ['all']:
        conn = psycopg2.connect(**kw)
        cur = conn.cursor()
        databses_sql = """
            SELECT datname FROM pg_database WHERE datistemplate = false;
        """
        cur.execute(databses_sql)
        databases = [x[0] for x in cur.fetchall()]
        conn.close()
    if not click.confirm('Continue on databases : %s' % databases):
        Log.error('Exit')
    for db in databases:
        Log.info('Switch to the database %s' % (db,))
        kw = dict(kw, database=db)
        conn = psycopg2.connect(**kw)
        cur = conn.cursor()
        table_sql = """
                SELECT count(*) 
                FROM pg_class
                WHERE relkind='r' 
                AND relname='res_users'
        """
        cur.execute(table_sql)
        count = cur.fetchone()[0]
        if count:
            cur = conn.cursor()
            update_sql = """
                    SELECT u.id, u.login, p.name, u.password
                    FROM res_users AS u
                    LEFT JOIN res_partner AS p
                    ON u.partner_id = p.id
                    
            """
            cur.execute(update_sql)
            x = x = PrettyTable()
            x.field_names = ["Id", "Login", "Name", "Password"]
            for f in x.field_names:
                x.align[f] = 'l'
            for user_id, user_login, user_name, user_password in cur.fetchall():
                x.add_row([user_id, user_login, user_name, user_password])
            Log.info(x)
        cur.close()
        conn.close()


@cli.command()
@click.pass_context
@click.argument('tables', type=click.STRING, required=False, nargs=-1)
@click.option('--auto-commit', is_flag=True, type=click.BOOL, required=False, default=False)
@click.option('--commit', is_flag=True, type=click.BOOL, required=False, default=False)
@click.option('--yes', is_flag=True, type=click.BOOL, required=False, default=False)
def pg_truncate(ctx, tables, auto_commit, commit, yes):
    """Truncate some postgresql tables"""
    auto_commit = auto_commit or commit or False
    if not tables:
        tables = [
            'mrp_production',
            'stock_picking',
            'stock_picking_wave',
            'stock_move',
            'stock_quant',
            'account_move',
            'account_move_line',
            'account_invoice',
            'account_invoice_line',
            'account_payment',
            'account_bank_statement',
            'account_batch_deposit',
            'account_analytic_line',
            'sale_order',
            'sale_order_line',
            'purchase_order',
            'purchase_order_line',
            'procurement_order',
            'stock_inventory',
            'stock_scrap',
            'stock_production_lot',
            'stock_quant_package',
            'account_batch_deposit',
            'crm_lead',
            'calendar_event',
        ]
    kw = {
        'host': ctx.obj['host'],
        'port': ctx.obj['port'],
        'user': ctx.obj['user'],
        'password': ctx.obj['password'],
    }
    databases = [ctx.obj['database']]
    if databases == ['all']:
        conn = psycopg2.connect(**kw)
        cur = conn.cursor()
        databses_sql = """
            SELECT datname FROM pg_database WHERE datistemplate = false;
        """
        cur.execute(databses_sql)
        databases = [x[0] for x in cur.fetchall()]
        conn.close()
    if not (yes or click.confirm('Continue to truncate tables %s on databases : %s' % (tables, databases))):
        Log.error('Exit')
    for db in databases:
        Log.info('Switch to the database %s' % (db,))
        kw = dict(kw, database=db)
        conn = psycopg2.connect(**kw)
        cur = conn.cursor()
        for table in tables:
            table_sql = """
                    SELECT count(*) 
                    FROM pg_class
                    WHERE relkind='r' 
                    AND relname=%s
            """
            cur.execute(table_sql, (table,))
            count = cur.fetchone()[0]
            if count:
                cur = conn.cursor()
                truncate_sql = """ TRUNCATE TABLE %s CASCADE """ % table
                cur.execute(truncate_sql)
                Log.success('The table <%s> is truncated in the database <%s>' % (table, db))
            else:
                Log.warn('The table <%s> not found in the database <%s>' % (table, db))
        if auto_commit or click.confirm('Commit ?'):
            conn.commit()
        cur.close()
        conn.close()


def __get_kwargs_from_section(ctx, section):
    config = ctx.obj['config_obj']
    vars = ['host', 'port', 'database', 'user', 'password', 'superuserpassword', 'protocol', 'mode']
    kwargs = {}
    for var in vars:
        try:
            kwargs[var] = config.get(section, var, '')
        except:
            kwargs[var] = ctx.obj[var]
    return kwargs


def __which(ctx):
    vars = ['host', 'port', 'database', 'user', 'password', 'superuserpassword', 'protocol', 'mode']
    x = PrettyTable()
    x.field_names = [var.title() for var in vars]
    kwargs = {}
    for var in vars:
        kwargs[var] = ctx.obj.get(var, '')
    x.add_row([ctx.obj.get(var, '') for var in vars])
    Log.info(x)
    Log.info('http://{host}:{port}/?db={database}   {user}/{password}'.format(**kwargs))
    Log.info('Section : {}'.format(ctx.obj['load']))


@cli.command()
@click.pass_context
def which(ctx):
    """Show actual informations"""
    __which(ctx)


def __section_create(ctx, section):
    config = ctx.obj['config_obj']
    config_path = ctx.obj['config_path']
    Log.info('Create new section %s to the config %s' % (section, config_path))
    config.read(config_path)
    if section not in config.sections():
        config.add_section(section)
    else:
        Log.error('The section %s already exists' % section)
    host = click.prompt('host', default=ctx.obj['host'], type=str)
    port = click.prompt('port', default=ctx.obj['port'], type=str)
    database = click.prompt('database', default=ctx.obj['database'], type=str)
    user = click.prompt('user', default=ctx.obj['user'], type=str)
    password = click.prompt('password', default=ctx.obj['password'], type=str)
    superuserpassword = click.prompt('superuserpassword', default=ctx.obj['superuserpassword'], type=str)
    protocol = click.prompt('protocol', default=ctx.obj['protocol'], type=str)
    mode = click.prompt('mode', default=ctx.obj['mode'], type=str)
    config.set(section, 'host', host)
    config.set(section, 'port', port)
    config.set(section, 'database', database)
    config.set(section, 'user', user)
    config.set(section, 'password', password)
    config.set(section, 'superuserpassword', superuserpassword)
    config.set(section, 'protocol', protocol)
    config.set(section, 'mode', mode)
    config.set(section, 'default', True)
    with open(ctx.obj['config_path'], 'wb') as configfile:
        config.write(configfile)
    Log.success('The section %s is created' % section)
    __use_section(ctx, section)


@cli.command()
@click.argument('section', type=click.STRING, required=True)
@click.pass_context
def create(ctx, section):
    """Create a new section"""
    __section_create(ctx, section)


def __section_update(ctx, section):
    """Update a section"""
    if not section:
        section = ctx.obj['load']
    if not section:
        Log.error('Please specify a section')
    config = ctx.obj['config_obj']
    config_path = ctx.obj['config_path']
    Log.info('Update the section %s in the config %s' % (section, config_path))
    config.read(config_path)
    if section not in config.sections():
        Log.error('The section %s does not found' % section)
        return
    host = click.prompt('host', default=config.get(section, 'host'), type=str)
    port = click.prompt('port', default=config.get(section, 'port'), type=str)
    database = click.prompt('database', default=config.get(section, 'database'), type=str)
    user = click.prompt('user', default=config.get(section, 'user'), type=str)
    password = click.prompt('password', default=config.get(section, 'password'), type=str)
    superuserpassword = click.prompt('superuserpassword', default=config.get(section, 'superuserpassword'), type=str)
    protocol = click.prompt('protocol', default=config.get(section, 'protocol'), type=str)
    mode = click.prompt('mode', default=config.get(section, 'mode'), type=str)
    config.set(section, 'host', host)
    config.set(section, 'port', port)
    config.set(section, 'database', database)
    config.set(section, 'user', user)
    config.set(section, 'password', password)
    config.set(section, 'superuserpassword', superuserpassword)
    config.set(section, 'protocol', protocol)
    config.set(section, 'mode', mode)
    config.set(section, 'default', True)
    with open(ctx.obj['config_path'], 'wb') as configfile:
        config.write(configfile)
    Log.success('The section %s is updated' % section)
    __use_section(ctx, section)


@cli.command()
@click.argument('section', type=click.STRING, required=False)
@click.pass_context
def update(ctx, section):
    """Update a section"""
    __section_update(ctx, section)


@cli.command()
@click.argument('arg', type=click.STRING, required=False)
@click.pass_context
def select(ctx, arg):
    """Select a section"""
    config = ctx.obj['config_obj']
    config_path = ctx.obj['config_path']
    config.read(config_path)
    candidates = []
    vars = ['host', 'port', 'database', 'user', 'password', 'superuserpassword', 'protocol', 'mode']
    index = 0
    for section in config.sections():
        index = index + 1
        kwargs = {_k: config.get(section, _k, '') for _k in vars}
        candidates.append((index, section, kwargs.get('database', '')))
        kwargs['index'] = index
        kwargs['section'] = section
        kwargs['section_database'] = "%s (db=%s)" % (section, kwargs.get('database', ''))
        Log.title('{index:<4} : {section_database:<40} http://{host}:{port}/?db={database}   {user}/{password}'.format(
            **kwargs))
        if arg and (section == arg or kwargs.get('database', '') == arg) or str(index) == str(arg):
            __use_section(ctx, section)
            return True
    found = False
    while True:
        if found:
            break
        section = click.prompt('Enter a section/database')
        for _c_index, _c_section, _c_database in candidates:
            if str(_c_index) == str(section) or str(_c_section) == str(section) or str(_c_database) == str(section):
                section = _c_section
                __use_section(ctx, section)
                found = True
            elif section.strip().lower() in ['exit', 'quit', 'q', 'x']:
                Log.error('Exit')


def __use_section(ctx, section):
    """Set a section"""
    config = ctx.obj['config_obj']
    config_path = ctx.obj['config_path']
    Log.info('Set the section %s in the config %s' % (section, config_path))
    config.read(config_path)
    if section not in config.sections():
        Log.error('The section %s does not found' % section)
    for _sec in config.sections():
        config.set(_sec, 'default', False)
    config.set(section, 'default', True)
    with open(ctx.obj['config_path'], 'wb') as configfile:
        config.write(configfile)
    Log.success('The section %s is default' % section)
    kwargs = __get_kwargs_from_section(ctx, section)
    Log.code('http://{host}:{port}/?db={database}   {user}/{password}'.format(**kwargs))


@cli.command()
@click.argument('section', type=click.STRING, required=False, nargs=-1)
@click.option('--yes', is_flag=True, default=False)
@click.pass_context
def delete(ctx, section, yes):
    """Delete a section"""
    if not section:
        section = [ctx.obj['load']]
    config = ctx.obj['config_obj']
    config_path = ctx.obj['config_path']
    Log.info('Delete sections %s from the config %s' % (list(section), config_path))
    config.read(config_path)
    if yes or click.confirm('Do you want to continue?'):
        for sec in section:
            if sec not in config.sections():
                Log.error('The section %s does not found' % sec)
                continue
            else:
                config.remove_section(sec)
                Log.success('The section %s is removed' % sec)
        with open(ctx.obj['config_path'], 'wb') as configfile:
            config.write(configfile)
    else:
        Log.error('Exit')


@cli.command('list')
@click.pass_context
@click.argument('arg', type=click.STRING, required=False)
@click.option('--connect', '-c', is_flag=True, type=click.BOOL, default=False, required=False)
@click.option('--login', '-l', is_flag=True, type=click.BOOL, default=False, required=False)
@click.option('--short', '-s', is_flag=True, type=click.BOOL, default=False, required=False)
@click.option('--version', '-v', is_flag=True, type=click.BOOL, default=False, required=False)
@click.option('--dev', '-d', is_flag=True, type=click.BOOL, default=False, required=False)
@click.option('--test', '-t', is_flag=True, type=click.BOOL, default=False, required=False)
@click.option('--prod', '-p', is_flag=True, type=click.BOOL, default=False, required=False)
@click.option('--host', '-h', type=click.STRING, default=False, required=False)
@click.option('--port', '-p', type=click.STRING, default=False, required=False)
@click.option('--database', '-db', type=click.STRING, default=False, required=False)
@click.option('--user', '-u', type=click.STRING, default=False, required=False)
@click.option('--password', type=click.STRING, default=False, required=False)
@click.option('--protocol', type=click.STRING, default=False, required=False)
@click.option('--local', is_flag=True, type=click.STRING, default=False, required=False)
@click.option('--remote', is_flag=True, type=click.STRING, default=False, required=False)
def __list(ctx, arg, connect, login, short, version, dev, test, prod, host, port, database, user, password, protocol,
           local, remote):
    """Show section list"""
    connect = connect or login or version
    short = short or connect
    sections = __section_filtered(ctx,
                                  dev=dev,
                                  test=test,
                                  prod=prod,
                                  host=host,
                                  port=port,
                                  database=database,
                                  user=user,
                                  password=password,
                                  protocol=protocol,
                                  local=local,
                                  remote=remote,
                                  )
    __section_list(ctx, arg, connect, login, short, version, sections)


def __section_filtered(ctx, **kwargs):
    config = ctx.obj['config_obj']
    dev, test, prod = kwargs.get('dev', None), kwargs.get('test', None), kwargs.get('prod', None)
    f_host, f_port, f_database = kwargs.get('host', None), kwargs.get('port', None), kwargs.get('database', None)
    f_user, f_password = kwargs.get('user', None), kwargs.get('password', None)
    f_protocol = kwargs.get('protocol', None)
    f_local, f_remote = kwargs.get('local', None), kwargs.get('remote', None)
    modes = []
    if dev: modes.append('dev')
    if test: modes.append('test')
    if prod: modes.append('prod')
    if not modes:
        modes = ['dev', 'test', 'prod']
    for section in config.sections():
        protocol = config.get(section, 'protocol', '')
        database = config.get(section, 'database', '')
        host = config.get(section, 'host', '')
        port = config.get(section, 'port', '')
        user = config.get(section, 'user', '')
        password = config.get(section, 'password', '')
        mode = config.get(section, 'mode', '')
        if mode not in modes:
            continue
        if f_local and host.lower().strip() not in ['localhost'] and not host.lower().strip().startswith(
                '192.') and not host.lower().strip().startswith('127.'):
            continue
        if f_remote and (host.lower().strip() in ['localhost'] or host.lower().strip().startswith(
                '192.') or host.lower().strip().startswith('127.')):
            continue
        if f_host and (host not in f_host and f_host not in host):
            continue
        if f_database and (database not in f_database and f_database not in database):
            continue
        if f_user and (user not in f_user and f_user not in user):
            continue
        if f_protocol and (protocol not in f_protocol and f_protocol not in protocol):
            continue
        if f_password and (password not in f_password and f_password not in password):
            continue
        if f_port and int(port) != int(f_port):
            continue
        yield section


def __get_connection_and_version(ctx, section, connect, login, version, section_connection):
    is_connect = is_login = is_version = False
    kwargs = __get_kwargs_from_section(ctx, section)
    protocol = kwargs['protocol']
    database = kwargs['database']
    host = kwargs['host']
    port = kwargs['port']
    user = kwargs['user']
    password = kwargs['password']
    connect = version or connect
    if connect:
        try:
            odoo_cnx = odoorpc.ODOO(host, protocol=protocol, port=port, timeout=20)
            is_connect = True
            is_version = odoo_cnx.version or ''
        except:
            pass
    if login:
        try:
            odoo_cnx.login(database, user, password)
            is_login = True
        except:
            pass
    section_connection[section] = {'connect': is_connect, 'login': is_login, 'version': is_version}


def __section_list(ctx, arg, connect, login, short, version, sections):
    sections = list(sections)
    config = ctx.obj['config_obj']
    config_path = ctx.obj['config_path']
    Log.info('List sections of the config')
    config.read(config_path)
    x = PrettyTable()
    if not arg and not short:
        field_names = ["Index", "Section", "Database", "Host", "Port", "User", "Password", "Super User Password",
                       "Protocol",
                       "Mode"]
    elif not arg and short:
        field_names = ["Index", "Section", "Path", "Mode"]
    else:
        field_names = ["Section", "Database", arg.title()]
    if connect:
        field_names.append('Connection')
    if login:
        field_names.append('Login')
    if version:
        field_names.append('Version')
    x.field_names = field_names
    for f in x.field_names:
        x.align[f] = 'l'
    section_connection = {}
    threads = []
    for index, section in enumerate(sections):
        t = threading.Thread(target=__get_connection_and_version,
                             args=(ctx, section, connect, login, version, section_connection))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    for index, section in enumerate(sections):
        section_label = "{:^3} {}".format(config.getboolean(section, 'default') and '(*)' or '', section)
        protocol = config.get(section, 'protocol', '')
        database = config.get(section, 'database', '')
        host = config.get(section, 'host', '')
        port = config.get(section, 'port', '')
        user = config.get(section, 'user', '')
        password = config.get(section, 'password', '')
        superuserpassword = config.get(section, 'superuserpassword', '')
        mode = config.get(section, 'mode', '')
        if not arg and not short:
            data = [
                str(index),
                section_label,
                database,
                host,
                port,
                user,
                password,
                superuserpassword,
                protocol,
                mode,
            ]
        elif not arg and short:
            path = "{:8} {}:{}/?db={} {}/{}".format(
                protocol,
                host,
                port,
                database,
                user,
                password,
            )
            data = [
                str(index),
                section_label,
                path,
                mode,
            ]
        else:
            data = [
                section_label,
                config.get(section, 'database', ''),
                config.get(section, arg, ''),
            ]
        odoo_version = ''
        if connect:
            if section_connection[section]['connect']:
                data.append('*')
            else:
                data.append(' ')
        if login:
            if section_connection[section]['login']:
                data.append('*')
            else:
                data.append(' ')
        if version:
            if section_connection[section]['version']:
                data.append(odoo_version)
            else:
                data.append(' ')

        x.add_row(data)
    Log.info(x)


# Misc

@cli.command()
@click.argument('length', type=click.INT, default=24, required=False)
@click.option('--nbr', '-n', type=click.INT, default=1, required=False)
@click.option('--uuid', is_flag=True, type=click.BOOL, default=False, required=False)
@click.option('--base64', is_flag=True, type=click.BOOL, default=False, required=False)
@click.pass_context
def random(ctx, length, nbr, uuid, base64):
    """Generate random strings"""
    Log.info('Some random strings')
    tab = []
    for i in range(nbr):
        if uuid:
            generated_string = str(pkg_uuid.uuid1())
        elif base64:
            generated_string = pkg_base64.b64encode(os.urandom(length))
        else:
            generated_string = ''.join(pkg_random.choice(pkg_string.letters + pkg_string.digits) for _ in range(length))
        tab.append(generated_string)
    x = PrettyTable()
    x.field_names = ["Random"]
    x.align["Random"] = "l"
    for r in tab:
        x.add_row([r])
    Log.info(x)


# Managing database

@cli.command()
@click.argument('output', type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True,
                                          resolve_path=True), required=True, default=os.getcwd())
@click.option('--zip/--no-zip', default=True, required=False)
@click.option('--key', '-k', default='', required=False)
@click.pass_context
def db_backup(ctx, output, zip, key):
    """Backup the database"""
    database = ctx.obj['database']
    key = '' if not key else '_' + key.replace(' ', '_')
    if zip:
        filename = '%s_%s%s.zip' % (database, time.strftime('%Y%m%d_%H%M%S'), key)
        _format = 'zip'
    else:
        filename = '%s_%s.backup' % (database, time.strftime('%Y%m%d_%H%M%S'), key)
        _format = 'backup'
    path = os.path.join(output, filename)
    Log.info('Backup the database %s to %s' % (database, path))
    dump = ctx.obj['action_connect']().db.dump(ctx.obj['superuserpassword'], database, format_=_format)
    f = open(path, 'wb+')
    f.write(dump.getvalue())
    f.close()
    Log.success('The backup is stored to %s [Size: %s]' % (path, File.get_size_str(path)))


@cli.command()
@click.pass_context
@click.argument('output', type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True,
                                          resolve_path=True), required=True, default=os.getcwd())
@click.option('--dev', '-d', is_flag=True, type=click.BOOL, default=False, required=False)
@click.option('--test', '-t', is_flag=True, type=click.BOOL, default=False, required=False)
@click.option('--prod', '-p', is_flag=True, type=click.BOOL, default=False, required=False)
@click.option('--host', '-h', type=click.STRING, default=False, required=False)
@click.option('--port', '-p', type=click.STRING, default=False, required=False)
@click.option('--database', '-db', type=click.STRING, default=False, required=False)
@click.option('--user', '-u', type=click.STRING, default=False, required=False)
@click.option('--password', type=click.STRING, default=False, required=False)
@click.option('--protocol', type=click.STRING, default=False, required=False)
@click.option('--local', is_flag=True, type=click.STRING, default=False, required=False)
@click.option('--remote', is_flag=True, type=click.STRING, default=False, required=False)
@click.option('--manifest/--no-manifest', default=True, required=False)
@click.option('--zip/--no-zip', default=True, required=False)
@click.option('--key', '-k', default='', required=False)
def db_backup_all(ctx, output, dev, test, prod, host, port, database, user, password, protocol, local, remote,
                  manifest, zip, key):
    """Backup all databases"""
    sections = __section_filtered(ctx,
                                  dev=dev,
                                  test=test,
                                  prod=prod,
                                  host=host,
                                  port=port,
                                  database=database,
                                  user=user,
                                  password=password,
                                  protocol=protocol,
                                  local=local,
                                  remote=remote,
                                  )
    threads = []
    key = '' if not key else '_' + key.replace(' ', '_')
    for section in sections:
        t = threading.Thread(target=__db_backup_by_section, args=(ctx, section, False, output, manifest, zip, key))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


@cli.command()
@click.pass_context
@click.argument('output', type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True,
                                          resolve_path=True), required=True, default=os.getcwd())
@click.option('--section', '-s', default=False, required=False)
@click.option('--manifest/--no-manifest', default=True, required=False)
@click.option('--zip/--no-zip', default=True, required=False)
@click.option('--key', '-k', default='', required=False)
def db_server_backup(ctx, output, section, manifest, zip, key):
    """Backup all databases on a server"""
    section = section or ctx.obj['load']
    kwargs = __get_kwargs_from_section(ctx, section)
    odoo_cnx = odoorpc.ODOO(kwargs['host'], protocol=kwargs['protocol'], port=kwargs['port'], timeout=60 * 60)
    threads = []
    for db in odoo_cnx.db.list():
        t = threading.Thread(target=__db_backup_by_section, args=(ctx, section, db, output, manifest, zip, key))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


def __db_backup_by_section(ctx, section, database, output, manifest, zip, key):
    kwargs = __get_kwargs_from_section(ctx, section)
    database = database or kwargs['database']
    host = kwargs['host']
    port = int(kwargs['port'])
    protocol = kwargs['protocol']
    superuserpassword = kwargs['superuserpassword']
    now_str = time.strftime('%Y%m%d_%H%M%S')
    output = os.path.join(output, section)
    manifest_path = os.path.join(output, 'manifest.ini')
    is_backup = False
    not_zip = not zip
    try:
        odoo_cnx = odoorpc.ODOO(host, protocol=protocol, port=port, timeout=60 * 60)
        if zip:
            try:
                Log.info('Begin to dump the database: %s, server: %s, port: %s' % (database, host, port))
                dump = odoo_cnx.db.dump(superuserpassword, database, format_='zip')
                filename = '%s_%s%s.zip' % (database, now_str, key)
            except:
                not_zip = True
                filename = '%s_%s%s.backup' % (database, now_str, key)
        if not_zip:
            dump = odoo_cnx.db.dump(superuserpassword, database, format_='backup')
            filename = '%s_%s%s.backup' % (database, now_str, key)
        path = os.path.join(output, filename)
        to_delete_output = True
        if os.path.exists(output):
            to_delete_output = False
        try:
            os.makedirs(output)
        except:
            pass
        f = open(path, 'wb+')
        f.write(dump.getvalue())
        f.close()
        if File.get_size(path) == 0:
            try:
                os.remove(path)
            except:
                pass
            if to_delete_output:
                try:
                    os.rmdir(output)
                except:
                    pass
            raise
        file_size_str = File.get_size_str(path)
        options = now_str
        config = ConfigParser.ConfigParser()
        config.read(manifest_path)
        if not config.has_section(options):
            config.add_section(options)
        config.set(options, 'host', host)
        config.set(options, 'port', port)
        config.set(options, 'database', database)
        config.set(options, 'superuserpassword', superuserpassword)
        config.set(options, 'protocol', protocol)
        config.set(options, 'filename', filename)
        config.set(options, 'size', file_size_str)
        config.set(options, 'key', key or '')
        if manifest:
            with open(manifest_path, 'wb') as configfile:
                config.write(configfile)
        is_backup = True
    except:
        pass
    if is_backup:
        Log.success('The backup of section %s is stored to %s [%s]' % (section, path, file_size_str))
    else:
        Log.error('The backup of section %s is failed' % section, exit=False)


@cli.command()
@click.argument('input', type=click.Path(exists=True, file_okay=True, dir_okay=False, writable=False, readable=True,
                                         resolve_path=True), required=True)
@click.pass_context
def db_restore(ctx, input):
    """Restore a database"""
    database = ctx.obj['database']
    Log.info('Restore the database %s from %s' % (database, input))
    with open(input, 'rb') as backup_file:
        ctx.obj['action_connect']().db.restore(ctx.obj['superuserpassword'], database, backup_file)
    Log.success('The database is restored')


@cli.command()
@click.option('--yes', is_flag=True, default=False)
@click.pass_context
def db_drop(ctx, yes):
    """Drop the database"""
    database = ctx.obj['database']
    Log.info('Drop the database %s ' % database)
    if yes or click.confirm('Do you want to continue?'):
        ctx.obj['action_connect']().db.drop(ctx.obj['superuserpassword'], database)
        Log.success('The database is dropped')
    else:
        Log.error('The database is not dropped')


@cli.command()
@click.option('--yes', is_flag=True, default=False)
@click.pass_context
def db_create(ctx, yes):
    """Create a database"""
    ctx.obj['action_connect']()
    database = ctx.obj['database']
    if not ctx.obj['prompt_database']:
        database = click.prompt('Name of the database ?', database)
    Log.info('Create the database %s ' % database)
    demo = False
    lang = click.prompt('Language ?', 'fr_FR')
    if yes or click.confirm('Load demo data ?'):
        demo = True
    if yes or click.confirm('Do you want to continue?'):
        odoo.db.create(admin_password=ctx.obj['superuserpassword'], db=database, demo=demo, lang=lang,
                       password=ctx.obj['superuserpassword'])
        Log.success('The database is created')
    else:
        Log.error('The database is not created')


@cli.command()
@click.pass_context
def db_list(ctx):
    """List databases"""
    Log.info('List databases')
    odoo = ctx.obj['action_connect']()
    x = PrettyTable()
    x.field_names = ["Name"]
    x.align["Name"] = "l"
    for db in odoo.db.list():
        x.add_row([db])
    Log.info(x)


# Access database

@cli.command()
@click.pass_context
def login(ctx):
    """Login to the database"""
    ctx.obj['action_login']()


@cli.command()
@click.pass_context
def shell(ctx):
    """Shell mode"""

    def records(model_name, args=None, limit=0, order='id asc'):
        model = odoo.env[model_name]
        if isinstance(args, (int, long)):
            return model.browse(args)
        elif hasattr(args, '__iter__'):
            if args:
                if isinstance(args[0], (int, long)):
                    return model.browse(args)
                else:
                    return model.browse(model.search(args, limit=limit, order=order))
        return model

    def model(model_name):
        return odoo.env[model_name]

    def read(model_name, domain=[], fields=[], limit=0):
        return odoo.env[model_name].search_read(domain, fields, limit=limit)

    get = records
    pp = pprint
    odoo = ctx.obj['action_login']()
    self = odoo
    env = odoo.env
    Shell().console(locals())


@cli.command()
@click.pass_context
def connect(ctx):
    """Connect to the server"""
    ctx.obj['action_connect']()


@cli.command()
@click.argument('model', type=click.STRING, required=True)
@click.option('--filter', '-f', type=click.STRING, required=False, multiple=True)
@click.option('--states', '-ss', type=click.BOOL, is_flag=True, required=False, default=False)
@click.option('--store', type=click.BOOL, is_flag=True, required=False, default=False)
@click.option('--depends', '-d', type=click.BOOL, is_flag=True, required=False, default=False)
@click.option('--required', '-r', type=click.BOOL, is_flag=True, required=False, default=False)
@click.option('--readonly', '-ro', type=click.BOOL, is_flag=True, required=False, default=False)
@click.option('--domain', type=click.BOOL, is_flag=True, required=False, default=False)
@click.option('--translate', '-t', type=click.BOOL, is_flag=True, required=False, default=False)
@click.option('--relation', type=click.BOOL, is_flag=True, required=False, default=False)
@click.option('--selection', type=click.BOOL, is_flag=True, required=False, default=False)
@click.option('--extra', '-e', '-x', 'extras', type=click.STRING, required=False, default=False, multiple=True)
@click.option('--slug', '-s', type=click.STRING, default=False, help="Slug, serie of ids (eg. 34,78,67)")
@click.pass_context
def fields(ctx, model, filter, store, states, depends, required, readonly, domain, translate, relation, selection,
           extras, slug):
    """List fields of a model"""
    Log.info('Showing the fields of the model %s' % model)
    odoo = ctx.obj['action_login']()
    Model = odoo.env[model]
    Field = odoo.env['ir.model.fields']
    ids = [int(x) for x in (slug.split(',') if slug else '') if x and x.isdigit()]
    records = False
    if ids:
        records = Model.browse(Model.search([('id', 'in', ids)]))
    x = PrettyTable()
    header = ["Name", ]
    if not records:
        header.append("Type")
        header.append("Label")
    if store:
        header.append('Store')
    if states:
        header.append('States')
    if depends:
        header.append('Depends')
    if required:
        header.append('Required')
    if readonly:
        header.append('Readonly')
    if domain:
        header.append('Domain')
    if translate:
        header.append('Translate')
    if relation:
        header.append('Relation')
    if selection:
        header.append('Selection')
    for extra in extras:
        header.append(extra.upper())
    header_values = []
    if ids:
        for i, record in enumerate(records):
            header_label = 'Value %s' % (i + 1)
            header_values.append(header_label)
            header.append(header_label)
    x.field_names = header
    x.align["Name"] = x.align["Type"] = x.align["Label"] = "l"
    for heade_value in header_values:
        x.align[heade_value] = "l"
    for key, value in sorted(Model.fields_get().iteritems(), key=lambda r: r[0]):
        if extras:
            field_line_id = Field.search([('name', '=', key), ('model_id.model', '=', model)])
            field_line = Field.browse(field_line_id)
        show = False
        if not filter:
            show = True
        elif value.get('type') in filter or key in filter or value.get('relation', False) in filter:
            show = True
        else:
            for f in filter:
                if f in value.get('type') or f in key or f in value.get('relation', ''):
                    show = True
        if show:
            tab = [key, ]
            if not records:
                tab.append(value.get('type', ''))
                tab.append(value.get('string', ''))
            if store:
                tab.append(value.get('store', ''))
            if states:
                tab.append(value.get('states', ''))
            if depends:
                tab.append(','.join([str(tmp) for tmp in value.get('depends', '')]))
            if required:
                tab.append(value.get('required', ''))
            if readonly:
                tab.append(value.get('readonly', ''))
            if domain:
                tab.append(value.get('domain', ''))
            if translate:
                tab.append(value.get('translate', ''))
            if relation:
                tab.append(value.get('relation', ''))
            if selection:
                tab.append(','.join([str(tmp[0]) for tmp in value.get('selection', '')]))
            for extra in extras:
                if extra == 'type':
                    tab.append(value.get('type', ''))
                elif extra in ('label', 'string'):
                    tab.append(value.get('string', ''))
                else:
                    tab.append(getattr(field_line, extra))
            if ids:
                for record in records:
                    if value.get('type', '') == 'binary':
                        record_value = 'binary ...'
                    else:
                        record_value = getattr(record, key, '')
                    tab.append(unicode(record_value))
            x.add_row(tab)
    Log.info(x)


@cli.command()
@click.argument('model', type=click.STRING, required=True)
@click.argument('function', type=click.STRING, required=True)
@click.option('--domain', '-d', nargs=3, help='Filter the records', multiple=True, callback=process_domain)
@click.option('--limit', '-l', type=click.INT, default=0, help="Limit of records")
@click.option('--id', default=False, type=click.STRING, required=False, multiple=True)
@click.option('--slug', '-s', type=click.STRING, default=False, help="Slug, serie of ids (eg. 34,78,67)")
@click.option('--param', '-p', default=False, nargs=2, type=click.STRING, required=False, multiple=True)
@click.option('--key', '-k', default=False, type=click.STRING, required=False, )
@click.option('--all', 'all_records', is_flag=True, default=False)
@click.option('--or', 'ou', flag_value='or')
@click.option('--api', '-a', default='multi', type=click.Choice(['multi', 'one', 'model']), required=False, )
@click.pass_context
def func(ctx, model, function, domain, limit, id, slug, param, all_records, ou, key, api):
    """Execute a function"""
    domain = __normalize_domain(ctx, domain, ou, slug)
    odoo = ctx.obj['action_login']()
    for function in function.split(','):
        Log.info('Execute the function %s of the model %s' % (function, model))
        ids = []
        Model = odoo.env[model]
        if id:
            ids += [int(x) for x in id]
        if domain:
            ids += Model.search(domain, limit=limit)
        if all_records:
            ids += Model.search([], limit=limit)
        if ids:
            if limit:
                ids = ids[:limit]
        args = {}
        for p_key, p_value in param:
            try:
                p_value = eval(p_value)
            except:
                pass
            args[p_key] = p_value
        if api == 'model':
            Log.info('ids=%s, args=%s' % (ids, args))
            res = getattr(Model, function)(**args)
            if key:
                res = res.get(key)
            Log.info(res)
        elif api == 'multi':
            records = Model.browse(ids)
            Log.info('ids=%s, args=%s' % (ids, args))
            res = getattr(records, function)(**args)
            if key:
                res = res.get(key)
            Log.info(res)
        else:
            for item_id in ids:
                Model = Model.browse(item_id)
                Log.info('id=%s, args=%s' % (item_id, args))
                res = getattr(Model, function)(**args)
                if key:
                    res = res.get(key)
                Log.info(res)


@cli.command()
@click.argument('model', type=click.STRING, required=True, nargs=-1)
@click.option('--metadata/--no-metadata', help='Show metadata in the view tree')
@click.option('--menu/--no-menu', help='Show menu apps')
@click.option('--delete', is_flag=True, default=False, help='Combine with menu and metadata')
@click.pass_context
def debug(ctx, model, metadata, menu, delete):
    """Debug tree views of the given models"""
    models = model
    Log.info('Debug the models : %s' % ([x for x in models],))
    odoo = ctx.obj['action_login']()
    odoo.env.context.update({
        'ir.ui.menu.full_list': True,
    })
    View = odoo.env['ir.ui.view']
    Menu = odoo.env['ir.ui.menu']
    Action = odoo.env['ir.actions.act_window']
    fields_to_debug = ['create_date', 'id']
    parser = etree.XMLParser(remove_blank_text=True)
    if metadata:
        invisible, visible = "1", "0"
        if delete:
            invisible, visible = "0", "1"
        for model in models:
            hits = 0
            nbr_trees = 0
            tree_ids = View.search([
                ('model', '=', model),
                ('type', '=', 'tree'),
                ('mode', '=', 'primary'),
            ])
            for tree_id in tree_ids:
                tree_arch = View.browse(tree_id).arch
                file_tree = StringIO(tree_arch)
                root = etree.parse(file_tree, parser)
                tree_node = root.xpath('//tree')[0] if len(root.xpath('//tree')) == 1 else False
                if tree_node is not None:
                    nbr_trees += 1
                    for field_to_debug in fields_to_debug:
                        founds = root.xpath('//field[@name=\'%s\']' % field_to_debug)
                        if len(founds) > 0:
                            for found in founds:
                                if found.attrib.get('invisible', visible) != visible:
                                    found.attrib['invisible'] = visible
                                    if visible == "1" and 'default_order' in found.attrib:
                                        found.attrib.pop('default_order')
                                    else:
                                        found.attrib['default_order'] = 'create_date desc'
                                    hits += 1
                        else:
                            tree_node.insert(0, etree.Element('field', name=field_to_debug, invisible=visible))
                            if visible == '0':
                                tree_node[0].attrib['default_order'] = 'create_date desc'
                            hits += 1
                arch_res = etree.tostring(root, pretty_print=True)
                View.write([tree_id], {'arch': arch_res})
            if hits:
                Log.success('%s trees, %s fields modified on the model : %s' % (hits, nbr_trees, model))
            else:
                Log.warn('%s trees, no views modified on the model : %s' % (nbr_trees, model,))
    if menu:
        main_menu_id = Menu.search([('name', '=', 'DEBUG_MENUS')])
        if not main_menu_id:
            main_menu_id = Menu.create({'name': 'DEBUG_MENUS'})
        else:
            main_menu_id = main_menu_id[0]
        main_menu = Menu.browse(main_menu_id)
        nbr_delete = 0
        nbr_added = 0
        for model in models:
            if delete:
                menu_to_delete_ids = Menu.search([
                    ('parent_id', '=', main_menu.id),
                    ('name', '=', model),
                ])
                menu_to_delete_ids += Menu.search([
                    ('parent_id', 'in', menu_to_delete_ids),
                ])
                nbr_delete += len(list(set(menu_to_delete_ids)))
                Menu.unlink(list(set(menu_to_delete_ids)))
                continue
            model_menu_id = Menu.search([
                ('parent_id', '=', main_menu.id),
                ('name', '=', model),
            ])
            if not model_menu_id:
                model_menu_id = Menu.create({
                    'parent_id': main_menu.id,
                    'name': model,
                })
            else:
                model_menu_id = model_menu_id[0]
            model_menu = Menu.browse(model_menu_id)
            action_ids = Action.search([
                ('res_model', '=', model),
                ('src_model', '=', False)
            ])
            actions = Action.browse(action_ids)
            action_done_names = []
            for action in actions:
                if action.name in action_done_names:
                    continue
                else:
                    action_done_names.append(action.name)
                model_menu_action_id = Menu.search([
                    ('parent_id', '=', model_menu.id),
                    ('name', '=', action.name),
                ])
                if not model_menu_action_id:
                    model_menu_action_id = Menu.create({
                        'parent_id': model_menu.id,
                        'name': action.name,
                    })
                    nbr_added += 1
                else:
                    model_menu_action_id = model_menu_action_id[0]
                model_menu_action = Menu.browse(model_menu_action_id)
                model_menu_action.action = 'ir.actions.act_window,%s' % action.id
        Log.success('%s menus added, %s menus deleted' % (nbr_added, nbr_delete))


@cli.command()
@click.pass_context
def update_list(ctx):
    """Update list of modules"""
    ctx.obj['action_login']()
    ctx.obj['update_list']()
    Log.success('The list of module is updated')


def __module_install(ctx, modules, module, update_list):
    odoo = ctx.obj['action_login']()
    if update_list:
        ctx.obj['update_list']()
    for module in Operator.unique([x.strip() for x in Operator.split_and_flat(',', modules, module)]):
        Log.info('Installing the module : %s ' % module)
        Module = odoo.env['ir.module.module']
        module_id = Module.search([('name', '=', module)])
        if module_id:
            Module.button_immediate_install(module_id)
            Log.success('The module %s is installed' % module)
        else:
            Log.error('The module %s is not installed' % module)


@cli.command()
@click.argument('modules', nargs=-1, type=click.STRING, required=True)
@click.option('--module', '-m', type=click.STRING, multiple=True)
@click.option('--update-list', is_flag=True, default=False, type=click.BOOL)
@click.pass_context
def install(ctx, modules, module, update_list):
    """Install modules"""
    __module_install(ctx, modules, module, update_list)


def __module_install_all(ctx, path, update_list):
    odoo = ctx.obj['action_login']()
    if update_list:
        ctx.obj['update_list']()
    modules = []
    for root, dirnames, filenames in os.walk(path):
        for dirname in dirnames:
            for _root, _dirnames, _filenames in os.walk(os.path.join(root, dirname)):
                for filename in _filenames:
                    if filename in ['__openerp__.py', '__manifest__.py']:
                        modules.append(dirname)

    for module in modules:
        Log.info('Installing the module : %s ' % module)
        Module = odoo.env['ir.module.module']
        module_id = Module.search([('name', '=', module)])
        if module_id:
            Module.button_immediate_install(module_id)
            Log.success('The module %s is installed' % module)
        else:
            Log.error('The module %s is not installed' % module)


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=False, readable=True,
                                        resolve_path=True), default=home)
@click.option('--update-list', is_flag=True, default=False, type=click.BOOL)
@click.pass_context
def install_all(ctx, path, update_list):
    """Install modules"""
    __module_install_all(ctx, path, update_list)


def __module_upgrade(ctx, modules, module, update_list):
    odoo = ctx.obj['action_login']()
    if update_list:
        ctx.obj['update_list']()
    for module in Operator.unique([x.strip() for x in Operator.split_and_flat(',', modules, module)]):
        Log.info('Updating the module : %s ' % module)
        Module = odoo.env['ir.module.module']
        module_id = Module.search([('name', '=', module)])
        if module_id:
            Module.button_immediate_upgrade(module_id)
            Log.success('The module %s is upgraded' % module)
        else:
            Log.error('The module %s is not upgraded' % module)


@cli.command()
@click.argument('modules', nargs=-1, type=click.STRING, required=True)
@click.option('--module', '-m', type=click.STRING, multiple=True)
@click.option('--update-list', is_flag=True, default=False, type=click.BOOL)
@click.pass_context
def upgrade(ctx, modules, module, update_list):
    """Upgrade modules"""
    __module_upgrade(ctx, modules, module, update_list)


@cli.command()
@click.argument('model', type=click.STRING, required=True, nargs=-1)
@click.option('--domain', '-d', nargs=3, help='Filter the records', multiple=True, callback=process_domain)
@click.option('--yes', is_flag=True, default=False, help="All as yes")
@click.option('--slug', '-s', type=click.STRING, default=False, help="Slug, serie of ids (eg. 34,78,67)")
@click.option('--batch-mode', is_flag=True, default=False, help="Batch mode")
@click.option('--or', 'ou', flag_value='or')
@click.pass_context
def truncate(ctx, model, domain, yes, slug, batch_mode, ou):
    """Truncate an object"""
    domain = __normalize_domain(ctx, domain, ou, slug)
    models = model
    odoo = ctx.obj['action_login']()
    for model in models:
        Model = odoo.env[model]
        model_ids = Model.search(domain)
        if yes or click.confirm('Are you sure you want to delete %s records from %s with the domain %s' % (
                len(model_ids), model, domain)):
            success, error = 0, 0
            if batch_mode:
                try:
                    Model.unlink(model_ids)
                    Log.success('the records are deleted')
                    success += len(model_ids)
                except:
                    Log.error('the records can not be deleted')
                    error += len(model_ids)

            else:
                for model_id in model_ids:
                    try:
                        Model.unlink(model_id)
                        Log.success('the record #%s is deleted' % model_id)
                        success += 1
                    except:
                        Log.error('the record #%s can not deleted' % model_id)
                        error += 1
            Log.info('success: %s, error: %s' % (success, error))
        else:
            Log.error('The truncate is aborted !')


def __module_uninstall(ctx, modules, module, update_list):
    odoo = ctx.obj['action_login']()
    if update_list:
        ctx.obj['update_list']()
    for module in Operator.unique([x.strip() for x in Operator.split_and_flat(',', modules, module)]):
        Log.info('Uninstalling the module : %s ' % module)
        Module = odoo.env['ir.module.module']
        module_id = Module.search([('name', '=', module)])
        if module_id:
            Module.button_uninstall(module_id)
            Log.success('The module %s is uninstalled' % module)
        else:
            Log.error('The module %s is not uninstalled' % module)


@cli.command()
@click.argument('modules', nargs=-1, type=click.STRING, required=True)
@click.option('--module', '-m', type=click.STRING, multiple=True)
@click.option('--update-list', is_flag=True, default=False, type=click.BOOL)
@click.pass_context
def uninstall(ctx, modules, module, update_list):
    """Uninstall modules"""
    __module_uninstall(ctx, modules, module, update_list)


@cli.command()
@click.argument('model', type=click.STRING, required=True)
@click.argument('params', type=click.STRING, required=False)
@click.pass_context
def refs(ctx, model, params):
    """Searching the XML-IDS related to the model"""
    Log.info('Inspect the XML-IDS of the model %s ' % model)
    if '=' in model or '&' in model:
        params = model
    action_param = menu_param = view_type_param = record_id_param = False
    if params:
        for param_expression in params.split('&'):
            param_tuple = param_expression.split('=')
            if len(param_tuple) == 2:
                _k = param_tuple[0].split('#')[-1]
                _v = param_tuple[1].isdigit() and int(param_tuple[1]) or param_tuple[1]
                if _k == 'menu_id': menu_param = _v
                if _k == 'action': action_param = _v
                if _k == 'view_type': view_type_param = _v
                if _k == 'id': record_id_param = _v
                if _k == 'model': model = _v
    odoo = ctx.obj['action_login']()
    xml_id = ctx.obj['xml_id']
    Action = odoo.env['ir.actions.act_window']
    Menu = odoo.env['ir.ui.menu']
    View = odoo.env['ir.ui.view']
    view_domain = [('model', '=', model)]
    if view_type_param:
        view_domain.append(('type', '=', view_type_param))
    view_ids = View.search(view_domain)
    blacklist = []
    action_domain = [('res_model', '=', model)]
    if action_param:
        action_domain.append(('id', '=', action_param))
    action_ids = Action.search(action_domain)
    if record_id_param:
        Log.info('')
        Log.code('Data XML-ID')
        x = PrettyTable()
        x.field_names = ["DATA XML-ID"]
        for f in x.field_names:
            x.align[f] = 'l'
        x.add_row([xml_id(odoo.env[model].browse(int(record_id_param)))])
        Log.info(x)

    x = PrettyTable()
    x_menu = PrettyTable()
    x.field_names = ["Action Name", "Action ID", "Action XML-ID", "Menu Name", "Menu ID", "Menu XML-ID"]
    x_menu.field_names = ["ID", "Menu Name", "Full Path"]
    for f in x.field_names:
        x.align[f] = 'l'
    for f in x_menu.field_names:
        x_menu.align[f] = 'l'
    for action in Action.browse(action_ids):
        if v(odoo.version) < v('9.0'):
            menu_domain = [('value', '=', 'ir.actions.act_window,%s' % action.id)]
            if menu_param:
                menu_domain.append(('res_id', '=', menu_param))
            values = odoo.env['ir.values'].search_read(menu_domain, ['res_id'])
            menu_ids = [_x.get('res_id') for _x in values]
        else:
            menu_domain = [('action', '=', 'ir.actions.act_window,%s' % action.id)]
            if menu_param:
                menu_domain.append(('id', '=', menu_param))
            menu_ids = Menu.search(menu_domain)
        menu_data = []
        menu_ids = [_x for _x in menu_ids if _x > 0]
        for menu in Menu.browse(menu_ids):
            menu_data.append({'name': menu.name, 'id': menu.id, 'xml_id': xml_id(menu)})
            x_menu.add_row([menu.id, menu.name, menu.complete_name])
        if not menu_ids:
            menu_data.append({'name': '', 'id': '', 'xml_id': '', 'complete_name': ''})
        first_line = True
        for menu_line in menu_data:
            if first_line:
                x.add_row([action.name, action.id, xml_id(action), menu_line.get('name'), menu_line.get('id'),
                           menu_line.get('xml_id'), ])
                first_line = False
            else:
                x.add_row(['', '', '', menu_line.get('name'), menu_line.get('id'), menu_line.get('xml_id')])
    Log.info('')
    Log.code('Menus')
    Log.info(x_menu)
    Log.info('')
    Log.code('Action and menus XML-IDS')
    Log.info(x)

    for action in Action.browse(action_ids):
        Log.info('')
        Log.code('Associated views to the action : %s, xml-id : %s' % (action.name, xml_id(action)))
        Log.code('Context : %s' % action.context)
        Log.code('Domain : %s' % action.domain)
        associated_views = []
        x2 = PrettyTable()
        x2.field_names = ["View name", "View Type", "XML-ID"]
        for f in x2.field_names:
            x2.align[f] = 'l'
        if action.search_view_id:
            if not view_type_param or view_type_param == action.search_view_id.type:
                associated_views.append(action.search_view_id.id)
                blacklist.append(action.search_view_id.id)
        if action.view_id:
            if not view_type_param or view_type_param == action.view_id.type:
                associated_views.append(action.view_id.id)
                blacklist.append(action.view_id.id)
        for view in action.view_ids:
            if view.view_id:
                if not view_type_param or view_type_param == view.view_id.type:
                    associated_views.append(view.view_id.id)
                    blacklist.append(view.view_id.id)
        views = View.browse(list(set(associated_views)))
        for view in views:
            x2.add_row([view.name, view.type, xml_id(view)])
        Log.info(x2)

    Log.info('')
    Log.code('Other views')
    other_views = list(set(view_ids) - set(blacklist))
    views = View.browse(list(set(other_views)))
    x3 = PrettyTable()
    x3.field_names = ["View name", "View Type", "XML-ID"]
    for f in x3.field_names:
        x3.align[f] = 'l'
    for view in views:
        x3.add_row([view.name, view.type, xml_id(view)])
    Log.info(x3)


def show_slug(__data):
    Log.title("-s %s" % slugify(__data))


def slugify(__data):
    return ",".join([str(x.get('id')) if isinstance(x, dict) else str(x.id) for x in __data if x])


def unslugify(__ids):
    return [int(x) for x in __ids.split(',')]


@cli.command()
@click.argument('expr', type=click.STRING, required=True)
@click.option('--model', '-m', type=click.STRING, required=False, multiple=True)
@click.option('--type', '-t', type=click.STRING, required=False, multiple=True)
@click.pass_context
def search_expr(ctx, expr, model, type):
    """Searching for the expression in the views"""
    Log.info('Search for the expression <%s> on the views of the models %s types %s' % (expr, model, type))
    odoo = ctx.obj['action_login']()
    xml_id = ctx.obj['xml_id']
    View = odoo.env['ir.ui.view']
    view_domain = [('arch_db', 'like', expr)]
    if model:
        view_domain.append(('model', 'in', model), )
    if type:
        view_domain.append(('type', 'in', type), )
    Log.debug(view_domain)
    view_ids = View.search(view_domain)
    views = View.browse(view_ids)
    x = PrettyTable()
    x.field_names = ["ID", "View name", "View Type", "Model", "XML-ID", "Mode"]
    for f in x.field_names:
        x.align[f] = 'l'
    for view in views:
        x.add_row([view.id, view.name, view.type, view.model or '', xml_id(view), view.mode])
    Log.info(x)
    Log.info("Total : %s" % len(views))
    show_slug(views)


@cli.command()
@click.argument('term', type=click.STRING, required=True)
@click.argument('lang', type=click.STRING, required=False)
@click.argument('module', type=click.STRING, required=False)
@click.option('--exact', is_flag=True, type=click.BOOL, default=False, required=False)
@click.pass_context
def trans_search(ctx, term, lang, module, exact):
    """Searching for the term in the translation table"""
    Log.info('Search for the term %s in the translation table' % term)
    odoo = ctx.obj['action_login']()
    Translation = odoo.env['ir.translation']
    view_domain = []
    if lang:
        view_domain += [('lang', '=', lang)]
    if module:
        view_domain += [('module', '=', module)]
    if exact:
        view_domain += ['|', ('value', '=', term), ('src', '=', term)]
    else:
        view_domain += ['|', ('value', 'ilike', term), ('src', 'ilike', term)]
    item_ids = Translation.search(view_domain)
    items = Translation.browse(item_ids)
    x = PrettyTable()
    x.field_names = ["Src", "Value", "Module", "Lang", "Type", "Name"]
    for f in x.field_names:
        x.align[f] = 'l'
    for item in items:
        x.add_row([item.src, item.value, item.module, item.lang, item.type, item.name])
    Log.info(x)
    Log.info("Total : %s" % len(items))


@cli.command()
@click.argument('view', type=click.STRING, required=True)
@click.pass_context
def arch(ctx, view):
    """Cat the arch of the view"""
    Log.info('Show the arch of the view %s ' % view)
    odoo = ctx.obj['action_login']()
    object_from_xml_id = ctx.obj['object_from_xml_id']
    View = odoo.env['ir.ui.view']
    if view.isdigit():
        view_domain = [('id', '=', int(view))]
    else:
        view_xml_id = object_from_xml_id(view)
        if not view_xml_id:
            Log.error('XML-ID not found')
        view_domain = [('id', '=', view_xml_id.id)]
    view_ids = View.search(view_domain)
    views = View.browse(view_ids)
    for view in views:
        Log.info(view.arch)


@cli.command()
@click.argument('model', type=click.STRING, required=True)
@click.option('--fields', '-f', type=click.STRING, help='Fields to show', multiple=True)
@click.option('--domain', '-d', nargs=3, help='Filter the records', multiple=True, callback=process_domain)
@click.option('--limit', '-l', type=click.INT, default=0, help="Limit of records")
@click.option('--order', '-o', type=click.STRING, default='id asc', help="Expression to sort the records")
@click.option('--slug', '-s', type=click.STRING, default=False, help="Slug, serie of ids (eg. 34,78,67)")
@click.option('--xmlid', is_flag=True, type=click.BOOL, default=False, help="Show XML-ID column")
@click.option('--or', 'ou', flag_value='or')
@click.option('--all-fields', is_flag=True, type=click.BOOL, default=False, help="Show all fields")
@click.option('--metadata', is_flag=True, type=click.BOOL, default=False, help="Show all metadata")
@click.pass_context
def records(ctx, model, fields, domain, limit, order, slug, xmlid, ou, all_fields, metadata):
    """Show the data of a model"""
    domain = __normalize_domain(ctx, domain, ou, slug)
    Log.info('Show the data of the model %s ' % model)
    odoo = ctx.obj['action_login']()
    xml_id = ctx.obj['xml_id']
    Model = odoo.env[model]
    if all_fields:
        fields = filter(lambda r: r not in ODOO_FIELDS, [x[0] for x in Model.fields_get().iteritems()])
    elif metadata:
        xmlid = True
        fields = ['id', 'display_name'] + ODOO_FIELDS
    else:
        fields = ['display_name'] if not fields else fields
    records = Model.search_read(domain or [], fields, limit=limit, order=order)
    if records:
        fields = records[0].keys()
    fields = __order_fields(fields)
    x = PrettyTable()
    if xmlid:
        x.field_names = fields + ['XML-ID']
    else:
        x.field_names = fields
    for f in x.field_names:
        x.align[f] = 'l'
    for record in records:
        y = [record.get(f) for f in fields]
        if xmlid:
            y += [xml_id(model, record.get('id'))]
        x.add_row(y)
    Log.info(x)
    show_slug(records)


@cli.command()
@click.argument('model', type=click.STRING, required=True)
@click.option('--fields', '-f', type=click.STRING, help='Fields to show', multiple=True)
@click.option('--domain', '-d', nargs=3, help='Filter the records', multiple=True, callback=process_domain)
@click.option('--limit', '-l', type=click.INT, default=0, help="Limit of records")
@click.option('--order', '-o', type=click.STRING, default='id asc', help="Expression to sort the records")
@click.option('--slug', '-s', type=click.STRING, default=False, help="Slug, serie of ids (eg. 34,78,67)")
@click.option('--or', 'ou', flag_value='or')
@click.option('--edit', '-e', type=click.STRING, help='Fields to edit', multiple=True, required=True, )
@click.pass_context
def prompt(ctx, model, fields, domain, limit, order, slug, ou, edit):
    """Edit the data of a model by promting"""
    domain = __normalize_domain(ctx, domain, ou, slug)
    Log.info('Edit the data of the model %s ' % model)
    odoo = ctx.obj['action_login']()
    Model = odoo.env[model]
    fields = ['id', 'display_name', 'active'] if not fields else fields
    records = Model.search_read(domain or [], list(fields) + list(edit), limit=limit, order=order)
    if records:
        fields = records[0].keys()
    fields = __order_fields(fields)
    for record in records:
        x = PrettyTable()
        x.field_names = fields
        for f in x.field_names:
            x.align[f] = 'l'
        y = [record.get(f) for f in fields]
        x.add_row(y)
        Log.info(x)
        vals = {}
        for field_to_edit in edit:
            field_value = click.prompt('Enter a new value for the field <%s>' % field_to_edit,
                                       record.get(field_to_edit), type=str)
            try:
                field_value = eval(field_value)
            except:
                pass
            vals[field_to_edit] = field_value
        if Model.write([record.get('id')], vals):
            Log.success("the record is updated")
        else:
            Log.error("There are an error when updating the record")


@cli.command()
@click.argument('model', type=click.STRING, required=True)
@click.option('--values', '-v', nargs=2, type=click.STRING, help='Values to apply', multiple=True)
@click.option('--domain', '-d', nargs=3, help='Filter the records', multiple=True, callback=process_domain)
@click.option('--batch-mode', is_flag=True, default=False, help="Batch mode")
@click.option('--yes', is_flag=True, default=False)
@click.option('--slug', '-s', type=click.STRING, default=False, help="Slug, serie of ids (eg. 34,78,67)")
@click.option('--or', 'ou', flag_value='or')
@click.pass_context
def record_update(ctx, model, values, domain, batch_mode, yes, slug, ou):
    """Update the data of a model"""
    domain = __normalize_domain(ctx, domain, ou, slug)
    Log.info('Update the data of the model %s ' % model)
    _values = {}
    for _k, _v in values:
        try:
            _v = eval(_v)
        except:
            pass
        _values[_k] = _v
    values = _values
    odoo = ctx.obj['action_login']()
    Model = odoo.env[model]
    model_ids = Model.search(domain)
    if yes or click.confirm('Are you sure you want to update %s records from %s with the values %s' % (
            len(model_ids), model, values)):
        success, error = 0, 0
        if batch_mode:
            try:
                Model.write(model_ids, values)
                Log.success('%s records are updated' % len(model_ids))
                success += len(model_ids)
            except:
                Log.error('%s records can not be updated' % len(model_ids))
                error += len(model_ids)
        else:
            for model_id in model_ids:
                try:
                    Model.write([model_id], values)
                    Log.success('the record #%s is updated' % model_id)
                    success += 1
                except:
                    Log.error('the record #%s can not be updated' % model_id)
                    error += 1
        Log.info('success: %s, error: %s' % (success, error))


@cli.command()
@click.argument('model', type=click.STRING, required=True)
@click.option('--values', '-v', nargs=2, type=click.STRING, help='Values to apply', multiple=True)
@click.option('--yes', is_flag=True, default=False)
@click.pass_context
def record_create(ctx, model, values, yes):
    """Create the data to a model"""
    Log.info('Create the data of the model %s ' % model)
    _values = {}
    for _k, _v in values:
        try:
            _v = eval(_v)
        except:
            pass
        _values[_k] = _v
    values = _values
    odoo = ctx.obj['action_login']()
    Model = odoo.env[model]
    if yes or click.confirm('Are you sure you want to create a record with values %s' % values):
        try:
            model_id = Model.create(values)
            Log.success('the record #%s is created' % model_id)
        except:
            Log.error('the record can not be created')


@cli.command()
@click.argument('model', type=click.STRING, required=True)
@click.option('--domain', '-d', nargs=3, help='Filter the records', multiple=True, callback=process_domain)
@click.option('--slug', '-s', type=click.STRING, default=False, help="Slug, serie of ids (eg. 34,78,67)")
@click.option('--or', 'ou', flag_value='or')
@click.pass_context
def count(ctx, model, domain, slug, ou):
    """Count the records on a model"""
    domain = __normalize_domain(ctx, domain, ou, slug)
    Log.info('Count the number of records on the model %s ' % model)
    odoo = ctx.obj['action_login']()
    Model = odoo.env[model]
    nbr = Model.search_count(domain or [])
    x = PrettyTable()
    x.field_names = ['Count']
    x.align['Count'] = 'l'
    x.add_row([nbr])
    Log.info(x)


@cli.command()
@click.argument('model', type=click.STRING, required=True)
@click.option('--user', '-u', type=click.STRING, required=False, multiple=True)
@click.pass_context
def crud(ctx, model, user):
    """List users access to the givenmodel"""
    Log.info('List the users access to the model %s ' % model)
    Log.code('')
    Log.code('CRUD')
    odoo = ctx.obj['action_login']()
    User = odoo.env['res.users']
    IrRule = odoo.env['ir.rule']
    IrModelAccess = odoo.env['ir.model.access']
    ir_rule_ids = IrRule.search([('model_id.model', '=', model)])
    rule_lines = IrRule.read(ir_rule_ids)
    ir_model_access_ids = IrModelAccess.search([('model_id.model', '=', model)])
    crud_lines = IrModelAccess.read(ir_model_access_ids)
    user_ids = User.search([]) if not user else User.search([('login', 'in', user)])
    x = PrettyTable()
    x.field_names = ["Name", "Read", "Write", "Create", "Unlink"]
    x.align["Name"] = "l"
    x.align["Read"] = x.align["Write"] = x.align["Create"] = x.align["Unlink"] = "c"
    for user in User.browse(user_ids):
        name = user.name
        group_ids = map(lambda r: r.id, user.groups_id)
        filtered_crud_lines = filter(lambda r: not r.get('group_id') or r.get('group_id')[0] in group_ids, crud_lines)
        create = write = unlink = read = False
        for crud_line in filtered_crud_lines:
            read = crud_line.get('perm_read', False) or read
            write = crud_line.get('perm_write', False) or write
            unlink = crud_line.get('perm_unlink', False) or unlink
            create = crud_line.get('perm_create', False) or create
        x.add_row([name, read and 'X' or '', write and 'X' or '', create and 'X' or '', unlink and 'X' or ''])
    Log.info(x)
    Log.code('')
    Log.code('Global domains')
    filtered_gloabl_rule_lines = filter(lambda r: r.get('global') == True, rule_lines)
    x2 = PrettyTable()
    x2.field_names = ["Domain", "Domain Force"]
    x2.align["Domain"] = x2.align["Domain Force"] = "l"
    for line in filtered_gloabl_rule_lines:
        x2.add_row([line.get('domain', ''), line.get('domain_force', '')])
    Log.info(x2)
    Log.code('')
    Log.code('Rules')
    x3 = PrettyTable()
    x3.field_names = ["Name", "Domain", "Domain force", "Read", "Write", "Create", "Unlink"]
    x3.align["Name"] = x3.align["Domain"] = "l"
    x3.align["Read"] = x3.align["Write"] = x3.align["Create"] = x3.align["Unlink"] = "c"
    for user in User.browse(user_ids):
        name = user.name
        group_ids = map(lambda r: r.id, user.groups_id)
        filtered_rule_lines = filter(
            lambda r: r.get('global') == False and set(r.get('groups')).intersection(group_ids), rule_lines)
        for rule_line in filtered_rule_lines:
            domain = rule_line.get('domain', '')
            domain_force = rule_line.get('domain_force', '')
            read = rule_line.get('perm_read', False)
            write = rule_line.get('perm_write', False)
            unlink = rule_line.get('perm_unlink', False)
            create = rule_line.get('perm_create', False)
            x3.add_row([name, domain, domain_force, read and 'X' or '', write and 'X' or '', create and 'X' or '',
                        unlink and 'X' or ''])
    Log.info(x3)


@cli.command()
@click.argument('model', type=click.STRING, required=True)
@click.option('--show', '-s', is_flag=True, type=click.BOOL, default=False)
@click.option('--duplicates', '-d', is_flag=True, type=click.BOOL, default=False)
@click.option('--fields', '-f', is_flag=True, type=click.BOOL, default=False)
@click.option('--buttons', '-b', is_flag=True, type=click.BOOL, default=False)
@click.option('--pages', '-p', is_flag=True, type=click.BOOL, default=False)
@click.option('--xpath', '-x', nargs=3, help='Find xpath', multiple=False)
@click.option('--view_id', '-v', type=click.STRING, default=None)
@click.option('--view_type', '-t', type=click.STRING, default='form')
@click.option('--expr', '-e', type=click.STRING, help='Execute xpath', multiple=False)
@click.option('--attrs', '-a', type=click.STRING, default=False, multiple=True)
@click.pass_context
def view(ctx, model, show, duplicates, fields, buttons, pages, xpath, view_id, view_type, expr, attrs):
    """Execute fields_view_get on the given model
    Extract: duplicates, xpath, buttons, pages, etc"""
    if xpath:
        xpath = '//%s[@%s=\'%s\']' % xpath

    def node_attrs(node):
        _node_attrs = []
        for _k, _v in node.attrib.iteritems():
            if _k in attrs:
                _node_attrs.append('%s=%s' % (_k, _v))
        return '   '.join(_node_attrs)

    def parent_xpath(node, j, node_number):
        xpath_list = []
        first = True
        while True:
            tag = node.tag
            if node.get('name'):
                tag += '[@name=\'%s\']' % node.get('name')
            if node_number > 1 and first:
                tag += '[%s]' % (j + 1)
            xpath_list.append(tag)
            node = node.getparent()
            first = False
            if node is None:
                break
        return '//' + '/'.join(xpath_list[::-1])

    """Execute fields_view_get on the given model"""
    Log.info(
        'execute the function fields_view_get on the model %s with print=%s duplicates=%s' % (model, show, duplicates))
    odoo = ctx.obj['action_login']()
    object_from_xml_id = ctx.obj['object_from_xml_id']
    Model = odoo.env[model]
    fvg_args = {'view_type': view_type}
    if view_id:
        view_id = int(view_id) if view_id.isdigit() else view_id
        view_id = object_from_xml_id(view_id).id if isinstance(view_id, basestring) else view_id
        fvg_args.update({'view_id': view_id})
    xml = Model.fields_view_get(**fvg_args).get('arch')
    root = etree.fromstring(xml)
    model_fields = [f.attrib['name'] for f in root.xpath('//field') if 'name' in f.attrib]
    _fields = []
    if duplicates:
        Log.code('')
        Log.code('Show duplicate fields')
        _duplicates = []
        for f in model_fields:
            if f in _fields:
                _duplicates.append(f)
            _fields.append(f)
        x1 = PrettyTable()
        x1.field_names = ["Name"]
        x1.align["Name"] = "l"
        for _d in _duplicates:
            x1.add_row([_d])
        Log.info(x1)
    if show:
        Log.code('')
        Log.code('Show XML')
        Log.info(etree.tostring(root, pretty_print=True, encoding='utf-8'))
    if fields:
        Log.code('')
        Log.code('Show fields')
        x2 = PrettyTable()
        x2.field_names = ["Name", "String", "Attributes"]
        x2.align["Name"] = x2.align["Attributes"] = x2.align["String"] = "l"
        for field_item in root.xpath('//field'):
            x2.add_row([field_item.attrib.get('name', ''), field_item.attrib.get('string', ''), node_attrs(field_item)])
        Log.info(x2)
    if buttons:
        Log.code('')
        Log.code('Show buttons')
        x3 = PrettyTable()
        x3.field_names = ["Name", "String", "Attributes"]
        x3.align["Name"] = x3.align["Attributes"] = x3.align["String"] = "l"
        for field_item in root.xpath('//button'):
            x3.add_row([field_item.attrib.get('name', ''), field_item.attrib.get('string', ''), node_attrs(field_item)])
        Log.info(x3)
    if pages:
        Log.title('')
        Log.title('Show pages')
        x4 = PrettyTable()
        x4.field_names = ["Name", "String", "Attributes"]
        x4.align["Name"] = x4.align["Attributes"] = x4.align["String"] = "l"
        for field_item in root.xpath('//page'):
            x4.add_row([field_item.attrib.get('name', ''), field_item.attrib.get('string', ''), node_attrs(field_item)])
        Log.info(x4)
    if xpath:
        Log.code('')
        Log.code('Show XPATH')
        x5 = PrettyTable()
        x5.field_names = ["Tag", "Name", "String", "Parent XPATH"]
        x5.align["Tag"] = x5.align["Name"] = x5.align["Parent XPATH"] = x5.align["String"] = "l"
        nbr = len(root.xpath(xpath)) if root.xpath(xpath) is not None else 0
        for i, node_xpath in enumerate(root.xpath(xpath)):
            x5.add_row([node_xpath.tag, node_xpath.attrib.get('name', ''), node_xpath.attrib.get('string'),
                        parent_xpath(node_xpath, i, nbr)])
        if not show:
            Log.info(x5)
    if expr:
        Log.code('')
        Log.code('Execute XPATH')
        nbr = len(root.xpath(expr)) if root.xpath(expr) is not None else 0
        Log.title('Found : %s' % nbr)
        for i, node_xpath in enumerate(root.xpath(expr)):
            Log.title('*' * 80)
            Log.info(etree.tostring(node_xpath, pretty_print=True, encoding='utf-8'))
            Log.title('*' * 80)
        Log.title('Found : %s' % nbr)


@cli.command('qweb')
@click.argument('xmlid', type=click.STRING, required=True)
@click.option('--show', '-s', is_flag=True, type=click.BOOL, default=False)
@click.option('--divs', '-d', is_flag=True, type=click.BOOL, default=False)
@click.option('--xpath', '-x', type=click.STRING, help='Find Xpath', multiple=False)
@click.option('--expr', '-e', type=click.STRING, help='Execute Xpath', multiple=False)
@click.option('--first-class', 'first_class', is_flag=True, type=click.BOOL, default=False,
              help='Choose the first class', multiple=False)
@click.option('--last-class', 'last_class', is_flag=True, type=click.BOOL, default=False, help='Choose the last class',
              multiple=False)
@click.option('--all-classes', 'all_classes', is_flag=True, type=click.BOOL, default=False,
              help='Choose the last class', multiple=False)
@click.pass_context
def __qweb(ctx, xmlid, show, divs, xpath, expr, first_class, last_class, all_classes):
    """Qweb inspection"""

    def parent_xpath(node, j, node_number, first_class, last_class, all_classes):
        last_class = True if not any([first_class, last_class, all_classes]) else False
        xpath_list = []
        first = True
        while True:
            tag = node.tag
            classes = tuple(node.get('class').split(' ')) if node.get('class') else ()
            if classes:
                if all_classes:
                    first_class = last_class = False
                if first_class:
                    classes = (classes[0],)
                elif last_class:
                    classes = (classes[-1],)
            if node.get('name'):
                tag += '[@name=\'%s\']' % node.get('name')
            elif node.get('t-if'):
                tag += '[@t-if=\'%s\']' % node.get('t-if')
            elif node.get('t-as'):
                tag += '[@t-as=\'%s\']' % node.get('t-as')
            elif node.get('t-call'):
                tag += '[@t-call=\'%s\']' % node.get('t-call')
            elif classes:
                tag += '[contains(@class,\'%s\')]' % ','.join(classes)
            xpath_list.append(tag)
            node = node.getparent()
            if node is None:
                break
        return '//' + '/'.join(xpath_list[::-1])

    xpath = expr or xpath
    expr = xpath or expr

    Log.info('Inspect the sweb with xmlid=%s' % (xmlid,))
    ctx.obj['action_login']()
    object_from_xml_id = ctx.obj['object_from_xml_id']
    view = object_from_xml_id(xmlid)
    xml = view.read_combined(['arch'])['arch']
    root = etree.fromstring(xml)
    show = show or not (xpath or expr or divs)
    if show:
        Log.code('')
        Log.code('Show XML')
        Log.info(etree.tostring(root, pretty_print=True, encoding='utf-8'))

    if divs:
        Log.code('')
        Log.code('Show divs')
        x2 = PrettyTable()
        x2.field_names = ["Name", "Classes", "IF"]
        x2.align["Name"] = x2.align["Classes"] = x2.align["IF"] = "l"
        for field_item in root.xpath('//div'):
            x2.add_row([field_item.attrib.get('name', ''), field_item.attrib.get('class', ''),
                        field_item.attrib.get('t-if', '')])
        Log.info(x2)

    if expr:
        Log.code('')
        Log.code('Execute XPATH')
        nbr = len(root.xpath(expr)) if root.xpath(expr) is not None else 0
        Log.title('Found : %s' % nbr)
        for i, node_xpath in enumerate(root.xpath(expr)):
            Log.title('*' * 80)
            Log.info(etree.tostring(node_xpath, pretty_print=True, encoding='utf-8'))
            Log.title('*' * 80)
        Log.title('Found : %s' % nbr)

    if xpath:
        Log.code('')
        Log.code('Show XPATH')
        x5 = PrettyTable()
        x5.field_names = ["Tag", "Parent XPATH"]
        x5.align["Tag"] = x5.align["Parent XPATH"] = "l"
        nbr = len(root.xpath(xpath)) if root.xpath(xpath) is not None else 0
        for i, node_xpath in enumerate(root.xpath(expr)):
            x5.add_row([node_xpath.tag, parent_xpath(node_xpath, i, nbr, first_class, last_class, all_classes)])
        Log.info(x5)


def __check_yaml_access(ctx, data):
    database = data.get('database', False)
    host = data.get('host', False)
    port = data.get('port', False)
    load = data.get('section', False)
    mode = data.get('mode', False)
    err = False
    if database and ctx.obj['database'] and database != ctx.obj['database']:
        err = ('database', database, ctx.obj['database'])
    if host and ctx.obj['host'] and host != ctx.obj['host']:
        err = ('host', host, ctx.obj['host'])
    if port and ctx.obj['port'] and port != ctx.obj['port']:
        err = ('port', port, ctx.obj['port'])
    if mode and ctx.obj['mode'] and ctx.obj['mode'] not in str(mode).split('|'):
        err = ('mode', mode, ctx.obj['mode'])
    if load and ctx.obj['load'] and load != ctx.obj['load']:
        err = ('load', load, ctx.obj['load'])
    if err:
        Log.error("Constraint %s (%s<=>%s) violated" % err)


def __pass_yaml_index(ctx, path, start, stop, indexes):
    first_item = os.path.basename(path).split('_')[0]
    if not first_item.isdigit():
        return True
    first_item = int(first_item)
    if start and first_item < start:
        Log.warn('File <%s> ignored ! <%s> not in range(%s, %s)' % (path, first_item, start, stop))
        return False
    if stop and first_item > stop:
        Log.warn('File <%s> ignored ! <%s> not in range(%s, %s)' % (path, first_item, start, stop))
        return False
    if indexes and first_item not in indexes:
        Log.warn('File <%s> ignored ! <%s> not in indexes %s' % (path, first_item, indexes))
        return False
    return True


def process_yamls(ctx, paths, cmd_repeat):
    start, stop, indexes, to_delete = 0, 0, [], []
    for x_path in paths:
        if ':' in x_path:
            start, stop = [int(x) if x.isdigit() else 0 for x in x_path.split(':')]
            to_delete.append(x_path)
        if ',' in x_path:
            indexes += [int(x) for x in x_path.split(',') if x.isdigit()]
            to_delete.append(x_path)
    if to_delete:
        Log.warn('some paths will ignored: %s' % to_delete)
    paths = [x for x in paths if x not in to_delete]
    Log.title("Processing yaml params, start=%s, stop=%s, indexes=%s" % (start, stop, indexes))
    contents = u""
    nbr_files = 0

    def append(contents, content, __path):
        datas = [x for x in yaml.load_all(content) if x]
        repeat = cmd_repeat or 1
        ignore = False
        ignored = False
        for data in datas:
            data_repeat = data.get('repeat', 0)
            repeat = data_repeat > repeat and data_repeat or repeat
            repeat = cmd_repeat > 1 and cmd_repeat or repeat
            __check_yaml_access(ctx, data)
            ignore = ignore or data.get('ignore', False)
        repeat_total = repeat
        repeat_index = 1
        if not ignore:
            while repeat:
                repeat_str = u'\n---\nvars:\n  - repeat_index: %s\n  - repeat_total: %s\n---\n' % (
                    repeat_index, repeat_total)
                contents += (u'\n---\n%s\n---\n' % repeat_str) + content
                repeat -= 1
                repeat_index += 1
        else:
            Log.warn('File <%s> ignored !' % __path)
            ignored = True
        return contents, ignored

    for path in paths:
        if os.path.isfile(path):
            if not __pass_yaml_index(ctx, path, start, stop, indexes):
                continue
            with codecs.open(path, encoding='utf8', mode='r') as yaml_file:
                contents, ignored = append(contents, yaml_file.read(), path)
                if not ignored:
                    nbr_files += 1
        elif os.path.isdir(path):
            new_paths = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    filename = os.path.join(root, file)
                    if os.path.splitext(filename)[1].lower() in ['.yml', '.yaml']:
                        new_paths.append(filename)
            new_paths = sorted(new_paths, key=lambda k: k.strip().lower())
            for new_path in new_paths:
                if not __pass_yaml_index(ctx, path, start, stop, indexes):
                    continue
                with codecs.open(new_path, encoding='utf8', mode='r') as yaml_file:
                    contents, ignored = append(contents, yaml_file.read(), new_path)
                    if not ignored:
                        nbr_files += 1
        else:
            Log.error('Can not process the path %s' % path)
    Log.code('%s yaml files processed' % nbr_files)
    return yaml.load_all(contents)


def yaml_eval(value, context, before_eval=False):
    tmp_ctx = context.copy()
    if '__builtins__' in tmp_ctx:
        tmp_ctx.pop('__builtins__')
    if not isinstance(value, basestring):
        return value
    pattern1 = re.compile("(\$\{[^}]+})")
    values1 = pattern1.findall(value)
    pattern2 = re.compile("(\$[^$]+\$)")
    values2 = pattern2.findall(value)
    pattern3 = re.compile("rand_([\s\*\$=+\.\d\w]+)_(\d+)")
    values3 = pattern3.findall(value)
    if not values1 and not values2 and not values3:
        return value
    for v_value in values1:
        main_v = v_value
        v_value = v_value[2:-1]
        try:
            v_value = unicode(eval(v_value, context))
        except:
            Log.error('Can not process %s in the context %s' % (v_value, tmp_ctx))
            sys.exit(-1)
        value = value.replace(main_v, v_value)
    for v_value in values2:
        main_v = v_value
        v_value = v_value[1:-1]
        try:
            v_value = eval(v_value, context)
            if callable(v_value):
                v_value = v_value()
            v_value = unicode(v_value)
        except:
            Log.error('Can not process %s in the context %s' % (v_value, tmp_ctx))
            sys.exit(-1)
        value = value.replace(main_v, v_value)
    for v_value in values3:
        main_v = 'rand_%s_%s' % v_value
        v_value = ''.join([pkg_random.choice(v_value[0]) for x in range(int(v_value[1]))])
        if not v_value:
            Log.error('Can not process %s' % main_v)
            sys.exit(-1)
        value = value.replace(main_v, v_value)
    if before_eval:
        return value
    if value:
        if not (re.match('^\d{4}-\d{2}-\d{2}$', value)):
            try:
                value = eval(value, context)
            except:
                pass
    if callable(value):
        value = value()
    return value


def __get_ref_records(ctx, odoo, model, ref, order, limit, context):
    kwargs = {}
    if limit:
        kwargs.update({'limit': limit})
    if order:
        kwargs.update({'order': order})
    object_from_xml_id = ctx.obj['object_from_xml_id']
    if not ref and not hasattr(ref, '__iter__'):
        return model.browse([])
    if ref == '__ALL' or (not ref and hasattr(ref, '__iter__')):
        return model.browse(model.search([], **kwargs))
    if isinstance(ref, basestring):
        ref = yaml_eval(ref, context)
    if isinstance(ref, (list, tuple)):
        new_ref = []
        for item_tuple in ref:
            x_tuple = []
            if isinstance(item_tuple, (list, tuple)):
                item_tuple_tab = []
                for sub_item_tuple in item_tuple:
                    if isinstance(sub_item_tuple, (list, tuple)):
                        xs_item = []
                        for xs_item_tuple in sub_item_tuple:
                            xs_item.append(yaml_eval(xs_item_tuple, context))
                        item_tuple_tab.append(xs_item)
                    else:
                        item_tuple_tab.append(yaml_eval(sub_item_tuple, context))
                x_tuple.append(item_tuple_tab)
            else:
                x_tuple.append(yaml_eval(item_tuple, context))
            new_ref += x_tuple
        ref = new_ref
    Log.code('Processing reference to : %s' % ref)
    if isinstance(ref, (int, long)):
        return model.browse([ref])
    if isinstance(ref, (list, tuple)) and isinstance(ref[0], (int, long)):
        return model.browse(ref)
    if isinstance(ref, (list, tuple)) and (ref[0] in ['&', '|', '!'] or isinstance(ref[0], (list, tuple))):
        return model.browse(model.search(ref, **kwargs))
    if IF.is_xmlid(ref):
        record = object_from_xml_id(ref)
        if not record:
            Log.error('The XML-ID %s is not found' % ref)
        return record
    if isinstance(ref, (list, tuple)) and isinstance(ref[0], basestring) and '.' in ref[0]:
        ids = []
        for tmp_ref in ref:
            record = object_from_xml_id(tmp_ref)
            if not record:
                Log.error('The XML-ID %s is not found' % tmp_ref)
            ids.append(record.id)
        return model.browse(ids)
    if isinstance(ref, basestring):
        return model.browse(model.search([('name', '=', ref)], **kwargs))
    Log.error('Can not process the reference %s' % ref)


INT, CHAR, TEXT, HTML, FLOAT, BOOL, SELECTION = 'integer', 'char', 'text', 'html', 'float', 'boolean', 'selection'
M2O, M2M, O2M = 'many2one', 'many2many', 'one2many'
DATE, DATETIME = 'date', 'datetime'
BINARY = 'binary'


def _onchange_spec(model, view_info=None):
    result = {}
    onchanges = []
    view_fields = []

    def process(node, info, prefix):
        if node.tag == 'field':
            name = node.attrib['name']
            names = "%s.%s" % (prefix, name) if prefix else name
            view_fields.append(name)
            if not result.get(names):
                result[names] = node.attrib.get('on_change')
                if node.attrib.get('on_change'):
                    onchanges.append(name)
            # traverse the subviews included in relational fields
            for subinfo in info['fields'][name].get('views', {}).itervalues():
                process(etree.fromstring(subinfo['arch']), subinfo, names)
        else:
            for child in node:
                process(child, info, prefix)

    if view_info is None:
        view_info = model.fields_view_get()
    process(etree.fromstring(view_info['arch']), view_info, '')
    return result, onchanges, view_fields


def __onchange_values(model, values, field_name, field_onchange):
    values = model.onchange([], values, field_name, field_onchange)
    if values and 'value' in values:
        values = values.get('value', {})
        for k, v in values.iteritems():
            if v and isinstance(v, (list, tuple)):
                v = v[0]
            values[k] = v
    return values


def __process_values(ctx, odoo, model, mode, values, fields, many2many, many2one, view_info, context):
    assert not values or isinstance(values, list), 'The values should be a list, found %s' % type(values)

    def wrap_m2m(_f, _v):
        if _f not in many2many:
            return [(6, 0, _v)]
        else:
            if many2many[_f] == 'add':
                return [(4, _x) for _x in _v]
            elif many2many[_f] == 'remove':
                return [(3, _x) for _x in _v]
            elif many2many[_f] == 'replace':
                return [(6, 0, _v)]

    vals = {}
    spec_fields, onchange_fields, view_fields = _onchange_spec(model, view_info)
    final_values = {}
    if mode == 'create':
        final_values = model.default_get(fields.keys())
    for field, value in values:
        kwargs = {}
        if field in many2one:
            kwargs = many2one.get(field)
        if field not in fields:
            Log.error('The field %s does not exists in the model %s' % (field, model._name))
        field_type = fields.get(field).get('type')
        field_relation = fields.get(field).get('relation')
        field_selection = fields.get(field).get('selection')
        # PROCESSINg CHAR AND TEXT
        if isinstance(value, basestring):
            value = yaml_eval(value, context)
        if field_type in [CHAR, TEXT, HTML]:
            vals[field] = unicode(value)
        elif field_type in [SELECTION]:
            for _select_key, _select_value in field_selection:
                if _select_value == value:
                    value = _select_key
            if value not in [x[0] for x in field_selection]:
                Log.error('Can not get the selection value for field %s on model %s (value: %s, allowed: %s)' % (
                    field, model._name, value, [x[0] for x in field_selection]))
            vals[field] = value
        elif field_type in [BOOL]:
            try:
                value = eval(value)
            except Exception as e:
                pass
            vals[field] = bool(value)
        elif field_type in [INT]:
            vals[field] = int(value)
        elif field_type in [FLOAT]:
            vals[field] = float(value)
        elif field_type in [BINARY]:
            if not os.path.isfile(value):
                Log.error('The file %s for the field %s on model %s not found' % (value, field, model._name))
            with open(value, "rb") as binary_file:
                vals[field] = base64.b64encode(binary_file.read())
        elif field_type in [DATE]:
            if isinstance(value, date_type):
                vals[field] = value.strftime(DATE_FORMAT)
            else:
                vals[field] = dt_parser.parse(str(value), dayfirst=True, fuzzy=True).strftime(DATE_FORMAT)
        elif field_type in [DATETIME]:
            if isinstance(value, datetime):
                vals[field] = value.strftime(DATETIME_FORMAT)
            else:
                vals[field] = dt_parser.parse(str(value), dayfirst=True, fuzzy=True).strftime(DATETIME_FORMAT)
        elif field_type == M2O:
            if isinstance(value, (int, long)):
                vals[field] = value
            elif isinstance(value, basestring):
                if value == '__ALL':
                    ids = odoo.env[field_relation].search([], **kwargs)
                else:
                    ids = odoo.env[field_relation].search([('name', '=', value)], **kwargs)
                if len(ids) == 1:
                    vals[field] = ids[0]
                else:
                    Log.error('Can not get values for %s on the field %s, model %s got %s ids' % (
                        value, field, field_relation, ids))
            elif isinstance(value, (list, tuple)):
                domain = []
                for line in value:
                    if len(line) != 3 and line not in ['&', '|', '!']:
                        Log.error(
                            'The tuple %s of the domain on the model %s can not be processed' % (line, model._name), )
                    else:
                        if len(line) == 3:
                            domain.append((line[0], line[1], yaml_eval(line[2], context)))
                        else:
                            domain.append(line)
                ids = odoo.env[field_relation].search(domain, **kwargs)
                if len(ids) == 1:
                    vals[field] = ids[0]
                else:
                    Log.error('Can not get values for %s on the field %s, model %s got %s ids' % (
                        domain, field, field_relation, ids))
        elif field_type == M2M:
            if isinstance(value, (int, long)):
                vals[field] = wrap_m2m(field, [value])
            elif isinstance(value, basestring):
                if value == '__ALL':
                    ids = odoo.env[field_relation].search([], **kwargs)
                    if ids:
                        vals[field] = wrap_m2m(field, ids)
                else:
                    ids = odoo.env[field_relation].search([('name', '=', value)], **kwargs)
                    if ids:
                        vals[field] = wrap_m2m(field, ids)
                    else:
                        Log.error('Can not get values for %s on the field %s, model %s got %s ids' % (
                            value, field, field_relation, ids))
            elif isinstance(value, (list, tuple)):
                domain = []
                for line in value:
                    if len(line) != 3 and line not in ['&', '|', '!']:
                        Log.error(
                            'The tuple %s of the domain on the model %s can not be processed' % (line, model._name))
                    else:
                        if len(line) == 3:
                            domain.append((line[0], line[1], yaml_eval(line[2], context)))
                        else:
                            domain.append(line)
                ids = odoo.env[field_relation].search(domain, **kwargs)
                if ids:
                    vals[field] = wrap_m2m(field, ids)
                else:
                    Log.error('Can not get values for %s on the field %s, model %s got %s ids' % (
                        value, field, field_relation, ids))
        else:
            Log.error('The type of the field %s as %s is not implemented' % (field, field_type))
        final_values[field] = vals[field]
        if field in onchange_fields:
            onchange_values = dict.fromkeys(view_fields, '')
            onchange_values.update(final_values)
            final_values.update(
                __onchange_values(model, onchange_values, field, spec_fields)
            )

    if ctx.obj['debug']:
        Log.debug(final_values)
    return final_values


def __process_load(ctx, odoo, record, context):
    datas = record.get('load', [])
    model = datas.get('model')
    repeat = datas.get('repeat', 1)
    values = datas.get('values', []) * repeat
    fields = []
    data = []
    for value in values:
        if not fields:
            fields = map(lambda r: r.keys()[0], value)
        value = {k: yaml_eval(v, context) for item in value for k, v in item.items()}
        data.append([value.get(f, '') for f in fields])
    if ctx.obj['debug']:
        Log.debug("model=%s repeat=%s fields=%s" % (model, repeat, fields))
        Log.debug("data=%s" % data)
    res = odoo.env[model].load(fields, data)
    Log.info(res)
    return context


def __process_vars(ctx, odoo, record, context):
    datas = record.get('vars', [])
    for item in datas:
        for key, value in item.items():
            context.update({key: yaml_eval(value, context)})
    return context


def __process_sleep(ctx, odoo, record, context):
    datas = record.get('sleep', 0)
    Log.info('Sleep %s seconds' % datas)
    time.sleep(datas)
    return context


def __process_message(ctx, odoo, record, context):
    datas = record.get('message', [])
    title = datas.get('title', '')
    if title:
        title = yaml_eval(title, context)
        title = ' %s ' % unicode(title).upper()
    body = datas.get('body', '')
    Log.code(title.center(80, '*'))
    if body:
        Log.code(yaml_eval(body, context))
        Log.code('*' * 80)
    return context


def __process_show(ctx, odoo, record, context):
    datas = record.get('show', [])
    model_name = datas.get('model')
    model = odoo.env[model_name]
    limit = datas.get('limit', False)
    order = datas.get('order', False)
    fields = datas.get('fields', [])
    ref = datas.get('refs', False)
    records = __get_ref_records(ctx, odoo, model, ref or '__ALL', order, limit, context)
    x = PrettyTable()
    x.field_names = [f.title() for f in fields if f]
    for f in x.field_names:
        x.align[f] = "l"
    for record in records:
        x.add_row([str(getattr(record, f, '-')) for f in fields if f])
    Log.info(x)
    return context


def __process_delete_menu(ctx, odoo, record, context):
    Menu = odoo.env['ir.ui.menu']
    View = odoo.env['ir.ui.view']
    Action = odoo.env['ir.actions.act_window']
    action_to_delete_ids = context.get('action_to_delete_ids', [])
    menu_to_delete_ids = context.get('menu_to_delete_ids', [])
    view_to_delete_ids = context.get('view_to_delete_ids', [])
    for action_id in action_to_delete_ids:
        action = Action.browse(action_id)
        action_name = action.name
        action.unlink()
        Log.success('The action [%s] is deleted' % action_name)
    for menu_id in menu_to_delete_ids:
        menu = Menu.browse(menu_id)
        menu_name = menu.name
        menu.unlink()
        Log.success('The menu [%s] is deleted' % menu_name)
    for view_id in view_to_delete_ids:
        view = View.browse(view_id)
        view_name = view.name
        view.unlink()
        Log.success('The view [%s] is deleted' % view_name)
    return context


def __process_menu(ctx, odoo, record, context):
    Menu = odoo.env['ir.ui.menu']
    View = odoo.env['ir.ui.view']
    Action = odoo.env['ir.actions.act_window']
    object_from_xml_id = ctx.obj['object_from_xml_id']
    datas = record.get('menu', [])
    name = datas.get('name')
    code = datas.get('code')
    parent = datas.get('parent_code', False)
    menu_seq = datas.get('sequence', 1)
    action_datas = datas.get('action', {})
    menu_created_nbr = 0
    parser = etree.XMLParser(remove_blank_text=True)
    if parent:
        if not context.get(parent, False):
            Log.error('Can not find the menu code : %s' % code)
    if not parent:
        menu_id = Menu.search([('name', '=', name)])
        if not menu_id:
            menu_id = Menu.create({'name': name, 'sequence': menu_seq})
            menu_created_nbr += 1
        else:
            menu_id = menu_id[0]
    else:
        menu_id = Menu.search([
            ('name', '=', name),
            ('parent_id', '=', context.get(parent)),
        ])
        if menu_id:
            menu_id = menu_id[0]
        else:
            menu_id = Menu.create({
                'name': name,
                'parent_id': context.get(parent),
                'sequence': menu_seq,
            })
            menu_created_nbr += 1
    context[code] = menu_id
    Log.success('[%s] %s menu created' % (name, menu_created_nbr,))
    context['menu_to_delete_ids'] = context.get('menu_to_delete_ids', []) + [menu_id]
    menu = Menu.browse(menu_id)
    if action_datas:
        action_model = action_datas.get('model', False)
        action_domain = action_datas.get('domain', [])
        action_context = action_datas.get('context', {})
        action_view_mode = action_datas.get('view_mode', False)
        action_views = action_datas.get('views', [])
        action_data = {
            'name': name,
            'res_model': action_model,
            'context': str(action_context),
            'domain': str(action_domain),
        }
        if not any([action_views, action_view_mode]):
            Log.error('Please provide <view_mode> or <views> on action')
        if action_view_mode:
            action_data.update({
                'view_mode': action_view_mode,
                'view_ids': [(5, 0, 0)],
            })
        else:
            view_datas = []
            view_mode_tab = []
            for _x in action_views:
                _x_data = {
                    'sequence': _x.get('sequence', 1),
                    'view_mode': _x.get('type'),
                }
                view_mode_tab.append(_x.get('type', 'tree'))
                if _x.get('ref', False):
                    view_obj = object_from_xml_id(_x.get('ref'))
                    if not view_obj:
                        Log.error('XML-ID not found [%s]' % _x.get('ref'))
                    _x_data['view_id'] = view_obj.id
                elif _x.get('fields', []):
                    attributes = {'string': name}
                    attributes.update(_x.get('attributes', {}))
                    root = etree.Element(_x.get('type', 'tree'), **attributes)
                    fields = _x.get('fields')
                    for field in fields:
                        field_args = field.values()[0] if isinstance(field, dict) else {}
                        field_name = field.keys()[0] if isinstance(field, dict) else field
                        field_args['name'] = field_name
                        etree.SubElement(root, 'field', **field_args)
                    arch_res = etree.tostring(root, pretty_print=True)
                    file_tree = StringIO(arch_res)
                    root = etree.parse(file_tree, parser)
                    arch_res = etree.tostring(root, pretty_print=True)
                    tree_name = "%s.%s.%s" % (action_model, _x.get('type', 'tree'), name)
                    tree_id = View.search([
                        ('model', '=', action_model),
                        ('type', '=', _x.get('type', 'tree')),
                        ('name', '=', tree_name),
                    ])
                    if tree_id:
                        tree_id = tree_id[0]
                        View.write([tree_id], {'arch_base': arch_res})
                        Log.success('The architecture XML of the view #%s %s is updated' % (tree_id, tree_name))
                    else:
                        tree_id = View.create({
                            'model': action_model,
                            'type': _x.get('type', 'tree'),
                            'name': tree_name,
                            'arch_base': arch_res,
                            'priority': 999,
                        })
                        Log.success('New view #%s created with fields %s' % (tree_id, _x.get('fields', [])))
                    _x_data['view_id'] = tree_id
                    context['view_to_delete_ids'] = context.get('view_to_delete_ids', []) + [tree_id]

                view_datas.append(_x_data)
            action_data.update({
                'view_mode': action_view_mode or ','.join(view_mode_tab),
                'view_ids': [(5, 0, 0)] + [(0, 0, view_data) for view_data in view_datas],
            })
        if menu.action:
            menu.action.write(action_data)
            action_id = menu.action.id
            Log.success('Action updated #%s name: %s' % (action_id, name))
        else:
            action_id = Action.create(action_data)
            menu.action = "%s,%s" % (Action._name, action_id)
            Log.success('Action created #%s name: %s' % (action_id, name))
        context['action_to_delete_ids'] = context.get('action_to_delete_ids', []) + [action_id]

    return context


def __process_import(ctx, odoo, record, context):
    def create_vals_from_line_and_map(line, mapping):
        vals = {}
        for dest, src in mapping.items():
            if src not in line.keys():
                Log.error('The key %s is not found in the CSV lines' % src)
            vals[dest] = line.get(src)
        return vals

    datas = record.get('import', [])
    model_name = datas.get('model')
    model = odoo.env[model_name]
    number = datas.get('number', False)
    mapping = datas.get('map', False)
    keys = datas.get('keys', False)
    path = datas.get('path', False)
    import_random = datas.get('random', False)
    view_ref = datas.get('view_ref', False)
    pick = datas.get('pick', [])
    if not os.path.isfile(path):
        Log.error('File %s not found' % path)
    lines = []
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lines.append(row)
    if not lines:
        Log.error('No line found in the file %s' % path)
    fields = model.fields_get()
    view_info = None
    if view_ref:
        object_from_xmlid = ctx.obj['object_from_xml_id'](view_ref)
        if not object_from_xmlid:
            Log.error('Can not found the view with the XML-ID %s' % view_ref)
        else:
            view_info = model.fields_view_get(view_id=object_from_xmlid.id)
    number = number if number > 0 else len(lines)
    diff = number - len(lines)
    if diff > 0:
        coeff = number / len(lines) + 1
        lines *= coeff
    if import_random:
        pkg_random.shuffle(lines)
    lines = lines[:number]
    for __tmp_i, __tmp_val in enumerate(pick):
        pick[__tmp_i] = (__tmp_val.keys()[0], __tmp_val.values()[0])
    for i, line in enumerate(lines):
        values = create_vals_from_line_and_map(line, mapping)
        ref = False
        if keys:
            if set(keys) & set(values.keys()) != set(keys):
                Log.error('Some keys on import not found in the mapping')
            ref = [['%s' % _key, '=', values.get(_key)] for _key in keys]
        records = __get_ref_records(ctx, odoo, model, ref, False, 1, context)
        values = [(k, v) for k, v in values.items() if v != '']
        values = __merge_values_and_pick(values, pick)
        if not records:
            ids = [model.create(
                __process_values(ctx, odoo, model, 'create', values, fields, {}, {}, view_info, context))]
            Log.success('Creating a record <%s> with id=%s is successful' % (model._name, ids[0],))
            # records = model.browse(ids)
        else:
            ids = [x.id for x in records]
            records.write(
                __process_values(ctx, odoo, model, 'write', values, fields, {}, {}, view_info,
                                 context))
            Log.success('Updating %s records of <%s> is successful' % (len(ids), model._name))
    return context


def __try_pick(field_value):
    if isinstance(field_value, basestring):
        return pkg_random.choice(glob.glob(field_value))
    else:
        return pkg_random.choice(field_value) if field_value else False


def __merge_values_and_pick(values, pick):
    vals = []
    blacklist = []
    if values:
        for field_name, field_value in values:
            blacklist.append(field_name)
            vals.append((field_name, field_value))
    if pick:
        for field_name, field_value in pick:
            if field_name in blacklist:
                continue
            vals.append((field_name, __try_pick(field_value)))
    return vals


def __process_record(ctx, odoo, record, context):
    data = record.get('record', {})
    ref = data.get('ref', data.get('refs', False))
    model_name = data.get('model')
    model = odoo.env[model_name]
    order = data.get('order', False)
    limit = data.get('limit', False)
    typology = data.get('typology', 'multi')

    records = __get_ref_records(ctx, odoo, model, ref, order, limit, context)
    if typology == 'one' and len(records) > 0:
        for item in records:
            context.update(__process_record_item(ctx, odoo, record, item, context))
        return context
    else:
        return __process_record_item(ctx, odoo, record, records, context)


def __process_record_item(ctx, odoo, record, records, context):
    data = record.get('record', {})
    model_name = data.get('model')
    model = odoo.env[model_name]
    # SET VARS
    ALLOWED_TYPOLOGIES = ['model', 'one', 'multi', 'last', 'first']
    # GET DEFAULT PARAMS
    typology = data.get('typology', 'multi')
    record_context = data.get('context', {})
    for r_ctx_key, r_ctx_value in record_context.items():
        record_context.update({r_ctx_key: yaml_eval(r_ctx_value, context)})
    if record_context:
        odoo.env.context.update(record_context)
    context.update(record_context)
    condition = data.get('condition', True)
    if not isinstance(condition, basestring):
        condition = unicode(condition)
    condition_before = yaml_eval(condition, context, before_eval=True)
    condition = yaml_eval(condition, context)
    if not condition:
        Log.warn('Condition not satisfied [%s], continue' % condition_before)
        return context
    unlink = data.get('unlink', False)
    values = data.get('values', [])
    pick = data.get('pick', [])
    create = data.get('create', True)
    update = data.get('update', data.get('write', True))
    order = data.get('order', False)
    limit = data.get('limit', False)
    exports = data.get('export', [])
    many2many = data.get('many2many', [])
    many2one = data.get('many2one', [])
    model_key = data.get('key', '')
    model_key = model_key.strip().lower() + '_' if model_key else ''
    functions = data.get('functions', [])
    workflows = data.get('workflows', [])
    view_ref = data.get('view_ref', False)
    ref = data.get('ref', data.get('refs', False))
    # ASSERTION
    assert model_name, 'No model name given'
    assert typology in ALLOWED_TYPOLOGIES, 'The typology %s should be in %s' % (typology, ALLOWED_TYPOLOGIES)
    assert isinstance(many2many, (list, tuple)), 'The many2many should be a list (-)'
    assert isinstance(values, (list, tuple)), 'The values should be a list (-)'
    tmp_many2many = {}
    for tm2m_item in many2many:
        for tm2m_data in tm2m_item.items():
            tm2m_data = list(tm2m_data)
            assert len(tm2m_data) == 2, 'Error on many2many format'
            assert tm2m_data[1] in ['add', 'keep', 'remove', 'erase',
                                    'replace'], 'In many2many the accepted values are: add, remove and replace'
            if tm2m_data[1] in ['add', 'keep']:
                tm2m_data[1] = 'add'
            elif tm2m_data[1] in ['remove', 'erase']:
                tm2m_data[1] = 'remove'
            elif tm2m_data[1] in ['replace']:
                tm2m_data[1] = 'replace'
            tmp_many2many[tm2m_data[0]] = tm2m_data[1]
    many2many = tmp_many2many
    assert isinstance(many2many, dict), 'The many2many should be a dictionnary'
    tmp_many2one = {}
    for tm2o_item in many2one:
        for tm2o_field in tm2o_item.keys():
            tmp_many2one[tm2o_field] = {}
            for tm2on_value in tm2o_item[tm2o_field]:
                tmp_many2one[tm2o_field].update(tm2on_value)
    many2one = tmp_many2one
    assert isinstance(many2one, dict), 'The many2one should be a dictionnary'
    view_info = None
    if view_ref:
        object_from_xmlid = ctx.obj['object_from_xml_id'](view_ref)
        if not object_from_xmlid:
            Log.error('Can not found the view with the XML-ID %s' % view_ref)
        else:
            view_info = model.fields_view_get(view_id=object_from_xmlid.id)
    # PROCESSING VALUES
    for __tmp_i, __tmp_val in enumerate(values):
        if isinstance(__tmp_val, tuple):
            __tmp_val = {__tmp_val[0]: __tmp_val[1]}
        values[__tmp_i] = (__tmp_val.keys()[0], __tmp_val.values()[0])
    for __tmp_i, __tmp_val in enumerate(pick):
        pick[__tmp_i] = (__tmp_val.keys()[0], __tmp_val.values()[0])
    values = __merge_values_and_pick(values, pick)
    # records = __get_ref_records(ctx, odoo, model, ref, order, limit, context)
    if data.get('show', []):
        show_fields = data.get('show') if isinstance(data.get('show'), (list, tuple)) else ['id', 'display_name']
        px = PrettyTable()
        px.field_names = [x.title() for x in show_fields]
        for f in px.field_names:
            px.align[f] = "l"
        for px_record in records:
            px.add_row([getattr(px_record, f, '-') for f in show_fields])
        Log.info(px)
    # PROCESSING UNLINK
    if unlink:
        try:
            records.unlink()
            Log.success('Unlink is successful')
        except:
            Log.error('Unlink is fail')
        records = model
    # PROCESSING CREATE AND WRITE
    if values:
        fields = model.fields_get()
        if not records:
            if create:
                ids = [model.create(
                    __process_values(ctx, odoo, model, 'create', values, fields, many2many, many2one, view_info,
                                     context))]
                Log.success('Creating a record <%s> with id=%s is successful' % (model._name, ids[0],))
                records = model.browse(ids)
            else:
                Log.warn('Skip creating a record <%s>' % (model._name,))
        else:
            if update:
                ids = [x.id for x in records]
                records.write(
                    __process_values(ctx, odoo, model, 'write', values, fields, many2many, many2one, view_info,
                                     context))
                Log.success('Updating %s records of <%s> is successful' % (len(ids), model._name))
            else:
                Log.warn('Skip updating records of <%s>' % (model._name,))
    # PROCESSING TYPOLOGIES
    if typology == 'one':
        if records:
            records = records[0]
        else:
            Log.error('Can not force the typology=%s, records=%s' % (typology, len(records)))
    elif typology == 'last':
        if records:
            records = records[-1]
        else:
            Log.error('Can not force the typology=%s, records=%s' % (typology, len(records)))
    elif typology == 'first':
        if records:
            records = records[0]
        else:
            Log.error('Can not force the typology=%s, records=%s' % (typology, len(records)))
    elif typology == 'model':
        if records:
            records = records[0:0]
        else:
            Log.error('Can not force the typology=%s, records=%s' % (typology, len(records)))
    if isinstance(records, odoorpc.models.Model):
        ids = [x.id for x in records]
    else:
        ids = []
    # PROCESSING FUNCTIONS
    for func_line in functions:
        func_name = func_line.get('name')
        func_args = func_line.get('args', {})
        func_api = func_line.get('api', 'multi')
        func_kwargs = func_line.get('kwargs', True)
        args = {}
        func_res = False
        for arg_key, arg_value in func_args.items():
            args[arg_key] = yaml_eval(arg_value, context)
        if func_api == 'multi':
            rec = records
            Log.code('Execute the function %s on %s with params %s' % (func_name, rec, args))
            if func_kwargs:
                func_res = getattr(rec, func_name)(**args)
            else:
                func_res = getattr(rec, func_name)(*args.values())
        elif func_api == 'one':
            for rec in records:
                Log.code('Execute the function %s on %s with params %s' % (func_name, rec, args))
                if func_kwargs:
                    func_res = getattr(rec, func_name)(**args)
                else:
                    func_res = getattr(rec, func_name)(*args.values())
        elif func_api == 'model':
            rec = model
            Log.code('Execute the function %s on %s with params %s' % (func_name, rec, args))
            if func_kwargs:
                func_res = getattr(rec, func_name)(**args)
            else:
                func_res = getattr(rec, func_name)(*args.values())
        context.update({"%s_%s%s" % (model._name.replace('.', '_'), model_key, func_name): func_res})
    for wkf in workflows:
        Log.code('Execute the signal %s on the records' % (wkf, records))
        model.signal_workflow([x.id for x in records], wkf)
    for export_line in exports:
        for export_key, export_expr in export_line.items():
            context[export_key] = eval(export_expr, {
                'record': records[0] if len(records) > 0 else False,
                'records': records,
                'ids': ids,
                'model': model,
                'odoo': odoo,
                'env': odoo.env,
            })
    export_model_record_key = "%s_%srecord" % (model._name.replace('.', '_'), model_key)
    export_model_records_key = "%s_%srecords" % (model._name.replace('.', '_'), model_key)
    if isinstance(records, odoorpc.models.Model):
        context.update({
            '%s' % export_model_record_key: records[0] if len(records) > 0 else False,
            '%s_id' % export_model_record_key: records[0].id if len(records) > 0 else False,
            '%s' % export_model_records_key: records,
        })
    return context


@cli.command()
@click.argument('datas', type=click.STRING, required=True, nargs=-1)
@click.option('--repeat', '-r', type=click.INT, default=1)
@click.pass_context
def yaml_load(ctx, datas, repeat):
    """Process yaml files"""
    datas = process_yamls(ctx, datas, repeat)
    blocks = []
    datas = [data for data in datas if data]
    for data in datas:
        validate(data, SCHEMA_GLOBAL)
    for data in datas:
        if not data:
            continue
        if not isinstance(data, dict):
            Log.warn('A block is ignored, continue')
        block = data.copy()
        blocks.append(block)

    __yaml_load(ctx, blocks)


def __yaml_load(ctx, blocks):
    odoo = ctx.obj['action_login']()
    elapsed_time_start = time.time()

    def __count(model, domain):
        return odoo.env[model].search_count(domain)

    def __browse(model, domain):
        return odoo.env[model].browse(odoo.env[model].search(domain))

    def __get_elapsed_time():
        total = time.time() - elapsed_time_start
        mins = int(total / 60)
        secs = int(total % 60)
        return "%s mins %s secs" % (mins, secs)

    context = dict(
        odoo.env.context,
        today=datetime.now().strftime(DATE_FORMAT),
        now=datetime.now().strftime(DATETIME_FORMAT),
        odoo=odoo,
        env=odoo.env,
        self=odoo,
        fake=fake,
        f=fake,
        Decimal=Decimal,
        count=__count,
        browse=__browse,
        elapsed_time=__get_elapsed_time,
    )
    odoo_context = odoo.env.context.copy()
    __process_blocks(ctx, odoo, blocks, context, odoo_context)


def __process_blocks(ctx, odoo, blocks, context, odoo_context):
    for block in blocks:
        for k, v in odoo.env.context.items():
            del odoo.env.context[k]
        odoo.env.context.update(odoo_context)
        if 'load' in block:
            context.update(__process_load(ctx, odoo, block, context))
        if 'record' in block:
            context.update(__process_record(ctx, odoo, block, context))
        if 'vars' in block:
            context.update(__process_vars(ctx, odoo, block, context))
        if 'sleep' in block:
            context.update(__process_sleep(ctx, odoo, block, context))
        if 'message' in block:
            context.update(__process_message(ctx, odoo, block, context))
        if 'show' in block:
            context.update(__process_show(ctx, odoo, block, context))
        if 'import' in block:
            context.update(__process_import(ctx, odoo, block, context))
        if 'menu' in block:
            odoo.env.context.update({'ir.ui.menu.full_list': True, })
            context.update(__process_menu(ctx, odoo, block, context))
            odoo.env.context.update({'ir.ui.menu.full_list': False, })
        if 'menu_delete' in block:
            odoo.env.context.update({'ir.ui.menu.full_list': True, })
            context.update(__process_delete_menu(ctx, odoo, block, context))
            odoo.env.context.update({'ir.ui.menu.full_list': False, })


@cli.command()
@click.argument('name', type=click.STRING, required=False)
@click.option('--keys', is_flag=True, default=False)
@click.pass_context
def fake_template(ctx, name, keys):
    """Show a fake examples"""
    for attr in dir(fake):
        if not attr.startswith('_'):
            if name and (name not in attr and attr not in name):
                continue
            try:
                Log.code('{:.<30}{}'.format(attr, getattr(fake, attr)() if not keys else '*'))
            except:
                pass


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True, readable=True,
                                        resolve_path=True), required=True, default=os.getcwd())
@click.option('--dirs/--no-dirs', is_flag=True, default=True)
@click.option('--files/--no-files', is_flag=True, default=True)
@click.option('--parent/--no-parent', is_flag=True, default=True)
@click.option('--unique', is_flag=True, default=False)
@click.option('--sep', '-s', type=click.STRING, default=',')
@click.option('--quotes', '-q', type=click.STRING, default='')
@click.option('--contains', '-c', type=click.STRING, multiple=True, default=('__openerp__.py', '__manifest__.py'))
@click.option('--exclude', '-x', type=click.STRING, multiple=True, default=('.git',))
@click.pass_context
def files(ctx, path, dirs, files, parent, unique, sep, quotes, contains, exclude):
    """Show files and directories"""
    data = []
    data_with_parent = []
    for root, dirnames, filenames in os.walk(path):
        for x in exclude:
            if x in root:
                break
        else:
            if dirs:
                if not contains or (contains and set(filenames) & set(contains)):
                    dirname = os.path.basename(root)
                    if not exclude or (exclude and dirname not in exclude):
                        data.append(root)
                        data_with_parent.append(dirname)
            if files:
                for filename in filenames:
                    data.append(os.path.join(root, filename))
                    data_with_parent.append(filename)
    if unique:
        data = list(set(data))
        data_with_parent = list(set(data_with_parent))
    if parent:
        Log.info(sep.join([u"%s%s%s" % (quotes, os.path.relpath(x, path), quotes) for x in data]))
    else:
        Log.info(sep.join([u"%s%s%s" % (quotes, x, quotes) for x in data_with_parent]))


@cli.command()
@click.pass_context
def yaml_template(ctx):
    """Show an example"""
    example = """
---
repeat: 1 # default is one
database : Name of the database
host : host
mode : test|prod|dev
port : 8069
load : Name of the section
condition : $env['re.partner'].search_count() < 20$ #condition
sleep: 20 (in seconds)
---
vars:
    - var1: ici la valeur de var1
    - var2: pick_PRODUCT            #Pick from the dictionnary
    - var3: rand_ICIALLCHARS_4      #Pick randomely 4 chars
---
message:
    title: Title $repeat_index$ / $repeat_total$
    body: |
        Here the body
        It can contain $var1$ and ${var2}
        Elapsed time : $elapsed_time$
---
record:
    model: res.partner
    refs: Accepts domain [[...]], xml-id, __ALL, name and ID  # else a new record will created if values
    order: id asc             # used by refs
    limit: 1                  # used by refs
    view_ref: xmlid of the view to force playing the onchanges
    condition: $sale_order_count$ <= 20 
    pick:                     # Like default values
        customer: [True, False]
        ref: ['a','b','c']
        reference: sequence
        image: /ll/*/images/man-*.*  #blob
    values:                   # many2many and one2many accepts domains, ID, filter by name
        - field1: value1
        - field2: value2
        - field3: $fake.first_name()$
        - field3: $f.last_name$
    create: True              # create a record with values if not found
    update: True              # update records with values
    unlink: True              # unlinks records
    typology: one|multi|multi|last|first   # slice records, Used for functions and workflows
                                           # default multi
    functions:
        - 
            name: func1
            args:
                arg1: val1
                arg2: val2
            api: model|multi|one
            kwargs: False
        - 
            name: func2
            args:
                arg1: val2
                arg2: val
        # auto export model_name_func_nameg
    workflows:
        - signal1
        - signal2
    export:
        - record_id: record.id
        - test_name: record.name
    show:
        - field1
        - field2
    many2many:
        - fieldm2m: add(default)|remove|replace    
    many2one:
        - fieldm2o: 
            - limit: 1
            - order: name desc
    context:                               # add keys/values to the context of variables
        key1: val1
        key2: val2
        field_parent: order_id             # pass the field_parent for the onchange
        sale_order_count: env['sale.order'].search_count([])
---
import:
  model: res.partner
  path: path/partners.csv
  view_ref: XML-ID
  pick:                     # Like default values
      customer: [True, False]
      ref: ['a','b','c']
      reference: sequence
      image: /ll/*/images/man-*.*  #blob
  map:
      name: nom
      street: adresse
      country_id: pays
      lang: langue
      customer: client
      supplier: fournisseur
  keys:
    - name
  number: 2
  random: True
---
load:
  model: sale.order
  repeat: 10
  values:
    -
      - partner_id: C1
      - order_line/product_id: P1
    -
      - order_line/product_id: P2
    -
      - order_line/product_id: P3
---
menu:
  name: My_DEBUG
  code: MD
---
menu:
  name: Sales
  parent_code: MD
  code: SALES

---
menu:
  name: Partenaires
  parent_code: SALES
  code: PARTNERS
  sequence: 1
  action:
    model: res.partner

---
menu:
  name: Clients
  parent_code: SALES
  code: CLIENTS
  sequence: 2
  action:
    model: res.partner
    context: {default_customer: True}
    domain: [['customer', '=', True]]
    view_mode: tree,form
---
menu:
  name: Toutes les commandes
  parent_code: SALES
  code: DEVIS
  sequence: 2
  action:
    model: sale.order
    context: {}
    domain: []
    views:
      -
        type: tree
        attributes:
          string: Les commandes
          default_order: create_date desc
        sequence: 1
        fields:
          - id
          - name :
              widget: hello
              test: yoo
          - state
      -
        type: form
        ref: sale.view_quotation_tree
        sequence: 3
---
menu_delete: True
    """
    Log.info(example)


if __name__ == '__main__':
    cli(obj={})


def main():
    return cli(obj={})
