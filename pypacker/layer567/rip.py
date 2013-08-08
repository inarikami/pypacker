"""Routing Information Protocol."""

from .. import pypacker
from .. import triggerlist

import logging

logger = logging.getLogger("pypacker")

# RIP v2 - RFC 2453
# http://tools.ietf.org/html/rfc2453

REQUEST		= 1
RESPONSE	= 2

class RIP(pypacker.Packet):
	__hdr__ = (
		("cmd", "B", REQUEST),
		("v", "B", 2),
		("rsvd", "H", 0),
		("rte_auth", None, triggerlist.TriggerList)
		)

	def _dissect(self, buf):
		l = []
		off = 4
		
		while off+20 <= len(buf):
			if buf[off : off+2] == b"\xff\xff":
				auth_rte = Auth(buf[off : off+20])
			else:
				auth_rte = RTE(buf[off : off+20])
			#logger.debug("RIP: adding auth/rte: %s" % auth_rte)
			l.append(auth_rte)
			off += 20
		self.rte_auth.extend(l)


# TODO: add RIPTriggerList to disambugiate between RTE/Auth -> ref to class via (CLZ, val1, val2, ...) -> zip(["family", ...], t[1:])
class RTE(pypacker.Packet):
	__hdr__ = (
		("family", "H", 2),
		("route_tag", "H", 0),
		("addr", "I", 0),
		("subnet", "I", 0),
		("next_hop", "I", 0),
		("metric", "I", 1)
		)

class Auth(pypacker.Packet):
	__hdr__ = (
		("rsvd", "H", 0xFFFF),
		("type", "H", 2),
		("auth", "16s", 0)
		)
