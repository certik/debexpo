# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>To: ${ c.to }
Subject: ${ _('Please activate your account') }

${ _('''Hello,

Please activate your account by visiting the following address
in your web-browser:''') }

${ c.activate_url }

${ _('Thanks,') }
