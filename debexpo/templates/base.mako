# -*- coding: utf-8 -*-
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>

  <head>
    <link rel="stylesheet" type="text/css" href="/style.css" />
    <title>${ c.config['debexpo.sitename'] }</title>

% if c.feed_url:

    <link rel="alternate" href="${ c.feed_url }" title="RSS Feed" type="application/rss+xml" />

% endif

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

    <table><tr><td class="navigation-td">
    <!--Left column containing navigation-->
    <div id="menu">
        <div class="start">
            <h2>Welcome</h2>
            <ul>
                <li>${ h.tags.link_to(
                        _('Start page'),
                        h.url_for('index')) }
                </li>
<!--                <li>${ h.tags.link_to(
                        _('News'),
                        h.url_for('news')) }
                </li>-->
            </ul>
        </div>

        <div class="maintainers">
            <h2>Maintainers</h2>
            <ul>
                <li>${ h.tags.link_to(
                        _('Introduction'),
                        h.url_for('intro', anchor='maintainers')) }
                </li>
                <li>${ h.tags.link_to(
                        _('Sign me up'),
                        h.url_for(controller='register', action='maintainer')) }
                </li>
                <li>${ h.tags.link_to(
                        _('My account'),
                        h.url_for('my')) }
                </li>
                <li>${ h.tags.link_to(
                        _('My packages'),
                        h.url_for(controller='packages', action='my')) }
                </li>
            </ul>
        </div>

        <div class="sponsors">
            <h2>Sponsors</h2>
            <ul>
                <li>${ h.tags.link_to(
                        _('Introduction'),
                        h.url_for('intro', anchor='sponsors')) }
                </li>
                <li>${ h.tags.link_to(
                        _('Sign me up'),
                        h.url_for(controller='register', action='sponsor')) }
                </li>
                <li>${ h.tags.link_to(
                        _('My account'),
                        h.url_for('my')) }
                </li>
            </ul>
        </div>

        <div class="support">
            <h2>Support</h2>
            <ul>
<!--                <li>${ h.tags.link_to(
                        _('Q & A'),
                        h.url_for('qa')) }
                </li>-->
                <li>${ h.tags.link_to(
                        _('Contact'),
                        h.url_for('contact')) }
                </li>
            </ul>
        </div>
    </div>

    </td>
    <td>

    <!--Right column containing main content-->
    <div id="maincontent">
      ${next.body()}
    </div>

    </td></tr></table>

    <div id="footer">
        debexpo
        -
        Copyright © 2008 Jonny Lamb
        -
        <a href="mailto:${ c.config['debexpo.email'] }">Support contact</a>
    </div>
  </body>
</html>
