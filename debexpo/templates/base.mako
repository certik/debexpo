# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>

  <head>
    <link rel="stylesheet" type="text/css" href="/style.css" />
    <title>${ c.config['debexpo.sitename'] }</title>
  </head>

  <body>
    <div id="header">
      <div id="debianlogo">
        <img src="${ c.config['debexpo.logo'] }" alt="${ c.config['debexpo.sitename'] } logo" />
      </div>

      <div id="headertitle">${ c.config['debexpo.sitename'] }</div>
        <div id="headersubtitle">${ c.config['debexpo.tagline'] }</div>
      </div>
    </div>

    <div id="floatmenu">
      <div class="menuitem">${ _('Welcome') }</div>
      <div class="menusubitem"><a href="${ h.url_for('index') }">${ _('Start page') }</a></div>
      <div class="menusubitem"><a href="${ h.url_for('news') }">${ _('News') }</a></div>

      <div class="menuitem">${ _('For maintainers') }</div>
      <div class="menusubitem"><a href="${ h.url_for('intro') }#maintainers">${ _('Introduction') }</a></div>
      <div class="menusubitem"><a href="${ h.url_for('register') }">${ _('Sign me up') }</a></div>
      <div class="menusubitem"><a href="${ h.url_for('my') }">${ _('My account') }</a></div>
      <div class="menusubitem"><a href="${ h.url_for(controller='packages', action='my', id=None) }">${ _('My packages') }</a></div>

      <div class="menuitem">For sponsors</div>
      <div class="menusubitem"><a href="${ h.url_for('intro') }#sponsors">${ _('Introduction') }</a></div>
      <div class="menusubitem"><a href="${ h.url_for('register') }">${ _('Sign me up') }</a></div>
      <div class="menusubitem"><a href="${ h.url_for('my') }">${ _('My account') }</a></div>
      <div class="menusubitem"><a href="${ h.url_for(controller='packages', action=None, id=None) }">${ _('Package list') }</a></div>

      <div class="menuitem">${ _('Support') }</div>
      <div class="menusubitem"><a href="${ h.url_for('qa') }">${ _('Q &amp; A') }</a></div>
      <div class="menusubitem"><a href="${ h.url_for('contact') }">${ _('Contact') }</a></div>
    </div>

    <div id="maincontent">
      ${self.main()}
    </div>

    <div id="footer"><a href="mailto:${ c.config['debexpo.email'] }">${ c.config['debexpo.email'] }</a></div>
  </body>
</html>
