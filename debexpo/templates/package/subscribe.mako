# -*- coding: utf-8 -*-
<%inherit file="../base.mako"/>

<h1>${ _('Subscribe to package %s') % c.package.name }</h1>

${ h.rails.form(h.url_for()) }
<p>${ h.rails.select('level', h.rails.options_for_select(c.subscriptions, c.current_subscription)) }
<br/>
${ h.rails.submit(_('Submit')) }</p>
${ h.rails.end_form() }

<p><a href="${ h.url_for('package', packagename=c.package.name) }">${ _('Back to package details') }</a>
