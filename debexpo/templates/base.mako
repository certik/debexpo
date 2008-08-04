# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>

  <head>
    <link rel="stylesheet" type="text/css" href="/style.css" />
    <title>${ c.config['debexpo.sitename'] }</title>
  </head>

  <body>
    <div id="header">
      <div id="logo">
        ${ h.tags.image(
            c.config['debexpo.logo'],
            c.config['debexpo.sitename'])}
      </div>

      <div id="headertitle">${ c.config['debexpo.sitename'] }</div>
        <div id="headersubtitle">${ c.config['debexpo.tagline'] }</div>
      </div>
    </div>

    <div id="floatmenu">
        <div class="start">
            <h2>Welcome</h2>
            <ul>
                <li>News</li>
            </ul>
        </div>
    </div>

<%"""
      <div class="menuitem">${ _('Welcome') }</div>
      <div class="menusubitem"><a href="${ h.rails.url_for('index') }">${ _('Start page') }</a></div>
      <div class="menusubitem"><a href="${ h.rails.url_for('news') }">${ _('News') }</a></div>

      <div class="menuitem">${ _('For maintainers') }</div>
      <div class="menusubitem"><a href="${ h.rails.url_for('intro') }#maintainers">${ _('Introduction') }</a></div>
      <div class="menusubitem"><a href="${ h.rails.url_for('register') }">${ _('Sign me up') }</a></div>
      <div class="menusubitem"><a href="${ h.rails.url_for('my') }">${ _('My account') }</a></div>
      <div class="menusubitem"><a href="${ h.rails.url_for(controller='packages', action='my', id=None) }">${ _('My packages') }</a></div>

      <div class="menuitem">For sponsors</div>
      <div class="menusubitem"><a href="${ h.rails.url_for('intro') }#sponsors">${ _('Introduction') }</a></div>
      <div class="menusubitem"><a href="${ h.rails.url_for('register') }">${ _('Sign me up') }</a></div>
      <div class="menusubitem"><a href="${ h.rails.url_for('my') }">${ _('My account') }</a></div>
      <div class="menusubitem"><a href="${ h.rails.url_for(controller='packages', action=None, id=None) }">${ _('Package list') }</a></div>

      <div class="menuitem">${ _('Support') }</div>
      <div class="menusubitem"><a href="${ h.rails.url_for('qa') }">${ _('Q &amp; A') }</a></div>
      <div class="menusubitem"><a href="${ h.rails.url_for('contact') }">${ _('Contact') }</a></div>
"""%>

    <div id="maincontent">
      ${next.body()}
    </div>

    <div id="footer">
        debexpo
        -
        Copyright © 2008 Jonny Lamb
        -
        <a href="mailto:${ c.config['debexpo.email'] }">Support contact</a>
    </div>
  </body>
</html>
