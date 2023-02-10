#!/usr/bin/env python

# SPDX-FileCopyrightText: 2013 SAP SE Srdjan Boskovic <srdjan.boskovic@sap.com>
#
# SPDX-License-Identifier: Apache-2.0

# -*- coding: utf-8 -*-

import os
import pytest
from pyrfc import Server, set_ini_file_directory, ABAPApplicationError


def my_stfc_connection(request_context=None, REQUTEXT=""):
    print("stfc invoked")
    print("request_context", request_context)
    print(f"REQUTEXT: {REQUTEXT}")

    return {"ECHOTEXT": REQUTEXT, "RESPTEXT": "Python server here"}


dir_path = os.path.dirname(os.path.realpath(__file__))
set_ini_file_directory(dir_path)

server = Server({"dest": "gateway"}, {"dest": "MME"})


class TestServer:
    def teardown_method(self):
        pass

    def test_add_wrong_function(self):
        with pytest.raises(ABAPApplicationError) as ex:
            server.add_function("STFC_CONNECTION1", my_stfc_connection)
        error = ex.value
        assert error.code == 5
        assert error.key == "FU_NOT_FOUND"
        assert error.message == "ID:FL Type:E Number:046 STFC_CONNECTION1"

    def test_add_function_twice(self):
        with pytest.raises(TypeError) as ex:
            server.add_function("STFC_CONNECTION", my_stfc_connection)
            server.add_function("STFC_CONNECTION", my_stfc_connection)
        error = ex.value
        assert error.args[0] == "Server function 'STFC_CONNECTION' already installed."

    @pytest.mark.skip(reason="manual test only")
    def test_stfc_connection(self):
        print("\nPress CTRL-C to skip server test...")
        server.serve()
