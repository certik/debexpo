# -*- coding: utf-8 -*-

<%inherit file="../base.mako"/>

<%def name="main()">

<h1>${ _('Sign up for your own account at %s') % c.config['debexpo.sitename'] }</h1>

<fieldset>
  <legend>${ _('Account type') }</legend>

  <p>
    First you must select what type of account you are applying for.
  </p>

  <h2>${ _('Maintainer') }</h2>

  <p>blurb here</p>

  <p><a href="${ h.rails.url_for(action='maintainer') }">${ _('Click here to proceed') }</a>.</p>

  <h2>${ _('Sponsor') }</h2>

  <p>blurb here</p>

  <p><a href="${ h.rails.url_for(action='sponsor') }">${ _('Click here to proceed') }</a>.</p>

</fieldset>

</%def>
