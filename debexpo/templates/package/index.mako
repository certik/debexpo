# -*- coding: utf-8 -*-
<%inherit file="../base.mako"/>

<%def name="main()">

<h1>${ _('Details about package %s') % c.package.name }</h1>

<table>
  <tr>
    <th>${ _('Name') }:</th>
    <td>${ c.package.name }</td>
  </tr>

  <tr>
    <th>${ _('Uploader') }:</th>
    <td><a href="${ h.url_for(controller='packages', action='uploader', id=c.package.user.email, packagename=None) }">${ c.package.user.name }</a> &lt;<a href="mailto: ${ c.package.user.email }">${ c.package.user.email }</a>&gt;

% if c.config['debexpo.debian_specific'] == 'true':

    (<a href="http://qa.debian.org/developer.php?login=${ c.package.user.email }">Debian QA page</a>)

% endif

    </td>
  </tr>

  <tr>
    <th>${ _('Description') }:</th>
    <td>${ c.package.description }</td>
  </tr>

</table>

<h1>${ _('Package versions') }</h1>

% for package_version in c.package.package_versions:

<fieldset>
  <legend>${ package_version.version }</legend>

  <table>
    <tr>
      <th>${ _('Version') }:</th>
      <td>${ package_version.version }</td>
    </tr>

    <tr>
      <th>${ _('Uploaded') }:</th>
      <td>${ package_version.uploaded }</td>
    </tr>

    <tr>
      <th>${ _('Debian Source Control file URL') }:</th>
      <td>

    % for pkgfile in package_version.source_packages[0].package_files:

        % if pkgfile.filename.endswith('.dsc'):

            <a href="${ c.config['debexpo.server'] }/debian/${ pkgfile.filename }">${ c.config['debexpo.server'] }/debian/${ pkgfile.filename }</a>

	% endif

    % endfor
      
      </td>
    </tr>

    <tr>
      <th>${ _('Section') }:</th>
      <td>${ package_version.section }</td>
    </tr>

    <tr>
      <th>${ _('Priority') }:</th>
      <td>${ package_version.priority }</td>
    </tr>

% if c.config['debexpo.debian_specific'] == 'true':

    % if package_version.closes is not None:

        % for bug in package_version.closes.split(','):

    <tr>
      <th>${ _('Closes bugs') }:</th>
      <td><a href="http://bugs.debian.org/${ bug }">${ bug }</a></td>
    </tr>

        % endfor

    % endif

% endif

  </table>

</fieldset>

% endfor

</%def>
