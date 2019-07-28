#!/usr/bin/env python
# -*- coding: utf-8 -*-

from controller import com, cbeta, user, admin
from controller.com import invalid

views = com.views + cbeta.views + user.views + admin.views
handlers = com.handlers + cbeta.handlers + user.handlers + [
    invalid.ApiTable, invalid.ApiSourceHandler]
modules = com.modules
InvalidPageHandler = invalid.InvalidPageHandler
