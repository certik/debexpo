# -*- coding: utf-8 -*-
<%inherit file="../base.mako"/>

<%def name="list()">

<table width="100%">
  <tr>
    <th>${ _('Package') }</th>
    <th>${ _('Description') }</th>
    <th>${ _('Version') }</th>
    <th>${ _('Uploader') }</th>
    <th>${ _('Needs a sponsor') }</th>
  </tr>

% if len(c.packages) > 0:

    % for package in c.packages:
      <tr>
	<td class="lines"><a href="${ h.rails.url_for('package', packagename=package['name']) }">${ package['name'] }</a></td>
	<td class="lines">${ package['description'] }</td>
	<td class="lines">${ package['version'] }</td>
	<td class="lines">${ package['uploader'] }</td>
	<td class="lines">${ package['needs_sponsor'] }</td>
      </tr>
    % endfor

% else:

    <tr>
      <td class="lines" colspan="5" align="center">${ _('No packages') }</td>
    </tr>

% endif

</table>

</%def>
