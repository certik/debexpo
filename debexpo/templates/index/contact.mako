# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>

<h1>${ _('Contact') }</h1>

<p><strong>${ _('Site email') }</strong>: <a href="mailto: ${ c.config['debexpo.email'] }">${ c.config['debexpo.email'] }</a></p>
