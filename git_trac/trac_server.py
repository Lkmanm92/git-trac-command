"""
Interface to the Sage Trac server

Uses XML-RPC to talk to the trac server.

EXAMPLES::

"""
##############################################################################
#  The "git trac ..." command extension for git
#  Copyright (C) 2013  Volker Braun <vbraun.name@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################


from datetime import datetime

from .trac_ticket import TracTicket
from .digest_transport import DigestTransport


class TracServer(object):

    def __init__(self, server, anonymous_location, authenticated_location):
        self.server = server
        self.anonymous_proxy = self._create_anonymous_server_proxy(
            server, anonymous_location)
        self.authenticated_proxy = None
        self._current_ticket_number = None

    def __repr__(self):
        return "Trac server at " + self.server

    def _create_anonymous_server_proxy(self, url_server, url_location):
        import urllib.parse
        url = urllib.parse.urljoin(url_server, url_location)
        transport = DigestTransport()
        from xmlrpc.client import ServerProxy
        return ServerProxy(url, transport=transport)

    def load(self, ticket_number):
        ticket_number = int(ticket_number)
        ticket = TracTicket(ticket_number, self.anonymous_proxy)
        return ticket

