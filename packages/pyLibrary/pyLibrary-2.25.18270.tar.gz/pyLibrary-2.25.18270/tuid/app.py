# encoding: utf-8
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Author: Kyle Lahnakoski (kyle@lahnakoski.com)
#
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import os

import flask
from flask import Flask, Response

from mo_dots import listwrap, coalesce, unwraplist
from mo_json import value2json, json2value
from mo_logs import Log, constants, startup, Except
from mo_logs.strings import utf82unicode, unicode2utf8
from mo_times import Timer, Date
from pyLibrary.env.flask_wrappers import cors_wrapper
from tuid.service import TUIDService
from tuid.util import map_to_array

OVERVIEW = None
QUERY_SIZE_LIMIT = 10 * 1000 * 1000
EXPECTING_QUERY = b"expecting query\r\n"
TOO_BUSY = 10

class TUIDApp(Flask):

    def run(self, *args, **kwargs):
        # ENSURE THE LOGGING IS CLEANED UP
        try:
            Flask.run(self, *args, **kwargs)
        except BaseException as e:  # MUST CATCH BaseException BECAUSE argparse LIKES TO EXIT THAT WAY, AND gunicorn WILL NOT REPORT
            Log.warning("TUID service shutdown!", cause=e)
        finally:
            Log.stop()


flask_app = None
config = None
service = None


@cors_wrapper
def tuid_endpoint(path):
    try:

        if flask.request.headers.get("content-length", "") in ["", "0"]:
            # ASSUME A BROWSER HIT THIS POINT, SEND text/html RESPONSE BACK
            return Response(
                EXPECTING_QUERY,
                status=400,
                headers={
                    "Content-Type": "text/html"
                }
            )
        elif int(flask.request.headers["content-length"]) > QUERY_SIZE_LIMIT:
            return Response(
                unicode2utf8("request too large"),
                status=400,
                headers={
                    "Content-Type": "text/html"
                }
            )
        request_body = flask.request.get_data().strip()
        query = json2value(utf82unicode(request_body))

        # ENSURE THE QUERY HAS THE CORRECT FORM
        if query['from'] != 'files':
            Log.error("Can only handle queries on the `files` table")

        ands = listwrap(query.where['and'])
        if len(ands) != 3:
            Log.error(
                'expecting a simple where clause with following structure\n{{example|json}}',
                example={"and": [
                    {"eq": {"branch": "<BRANCH>"}},
                    {"eq": {"revision": "<REVISION>"}},
                    {"in": {"path": ["<path1>", "<path2>", "...", "<pathN>"]}}
                ]}
            )

        rev = None
        paths = None
        branch_name = None
        for a in ands:
            rev = coalesce(rev, a.eq.revision)
            paths = unwraplist(coalesce(paths, a['in'].path, a.eq.path))
            branch_name = coalesce(branch_name, a.eq.branch)
        paths = listwrap(paths)

        if len(paths) == 0:
            response, completed = [], True
        elif service.conn.pending_transactions > TOO_BUSY:  # CHECK IF service IS VERY BUSY
            # TODO:  BE SURE TO UPDATE STATS TOO
            Log.note("Too many open transactions")
            response, completed = [], False
        else:
            # RETURN TUIDS
            with Timer("tuid internal response time for {{num}} files", {"num": len(paths)}):
                response, completed = service.get_tuids_from_files(
                    revision=rev, files=paths, going_forward=True, repo=branch_name
                )

            if not completed:
                Log.note(
                    "Request for {{num}} files is incomplete for revision {{rev}}.",
                    num=len(paths), rev=rev
                )

        if query.meta.format == 'list':
            formatter = _stream_list
        else:
            formatter = _stream_table

        return Response(
            formatter(response),
            status=200 if completed else 202,
            headers={
                "Content-Type": "application/json"
            }
        )
    except Exception as e:
        e = Except.wrap(e)
        Log.warning("could not handle request", cause=e)
        return Response(
            unicode2utf8(value2json(e, pretty=True)),
            status=400,
            headers={
                "Content-Type": "text/html"
            }
        )


def _stream_table(files):
    yield b'{"format":"table", "header":["path", "tuids"], "data":['
    for f, pairs in files:
        yield value2json([f, map_to_array(pairs)]).encode('utf8')
    yield b']}'


def _stream_list(files):
    if not files:
        yield b'{"format":"list", "data":[]}'
        return

    sep = b'{"format":"list", "data":['
    for f, pairs in files:
        yield sep
        yield value2json({"path": f, "tuids": map_to_array(pairs)}).encode('utf8')
        sep = b","
    yield b']}'


@cors_wrapper
def _head(path):
    return Response(b'', status=200)


@cors_wrapper
def _default(path):
    return Response(
        OVERVIEW,
        status=200,
        headers={
            "Content-Type": "text/html"
        }
    )


if __name__ in ("__main__",):
    Log.note("Starting TUID Service App...")
    flask_app = TUIDApp(__name__)
    flask_app.add_url_rule(str('/'), None, tuid_endpoint, defaults={'path': ''}, methods=[str('GET'), str('POST')])
    flask_app.add_url_rule(str('/<path:path>'), None, tuid_endpoint, methods=[str('GET'), str('POST')])

    try:
        config = startup.read_settings(
            filename=os.environ.get('TUID_CONFIG')
        )
        constants.set(config.constants)
        Log.start(config.debug)

        service = TUIDService(config.tuid)
        Log.note("Started TUID Service")
    except BaseException as e:  # MUST CATCH BaseException BECAUSE argparse LIKES TO EXIT THAT WAY, AND gunicorn WILL NOT REPORT
        try:
            Log.error("Serious problem with TUID service construction!  Shutdown!", cause=e)
        finally:
            Log.stop()

    if config.flask:
        if config.flask.port and config.args.process_num:
            config.flask.port += config.args.process_num
        Log.note("Running Flask...")
        flask_app.run(**config.flask)


