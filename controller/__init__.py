#!/usr/bin/env python
# -*- coding: utf-8 -*-

from controller import com, data, user, tripitaka
from controller.com import invalid

views = com.views + data.views + user.views + tripitaka.views
handlers = com.handlers + data.handlers + user.handlers + [
    invalid.ApiTable, invalid.ApiSourceHandler]
modules = com.modules
InvalidPageHandler = invalid.InvalidPageHandler
