# mandrill_odoo
Mandrill Odoo Integration 
=========================

This is in a very early stage. The problem that this solves, is when you use Mandrill as a transactional email system from Odoo to send mass mail, the rejected and bounces emails, stays in the Odoo database, not allowing you to enhance your Mandrill reputation. So this reduce your bounce rate for future sends, declaring the rejected emails as opt-outs.

In this stage this works as an autonomous system (no inside Odoo), so it uses webservices. It also use Mandrill API to read rejections.

Hope in the near future to convert it to an Odoo module

Install Instructions
from Linux:
1) sudo pip install mandrill # it installs mandrill's python libraries.
2) rename config.ini.sample to config.ini and put there your parameters (odoo user and password, url, and database) and your Mandrill API.
3) then run it:
python mandrill_api.py




