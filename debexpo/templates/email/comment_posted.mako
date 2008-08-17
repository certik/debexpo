# -*- coding: utf-8 -*-
<%inherit file="/base.mako"/>To: ${ c.to }
Subject: ${ _('Comment posted on %s' % c.package) }

${ _('''A comment has been posted on a package that you are subscribed to.

%s made the following comment about the %s package:''' % (c.user.name, c.package)) }

${ c.comment }

${ _('You can view information on the package by visiting:') }

${ c.config['debexpo.server'] }${ h.rails.url_for('package', packagename=c.package) }

${ _('You can change your subscription by visiting your user account settings.') }

${ _('Thanks,') }
