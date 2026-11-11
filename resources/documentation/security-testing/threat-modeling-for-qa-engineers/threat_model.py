"""Threat model for a checkout service, built with PyTM 1.3.

Generates a STRIDE-based threat report and a data flow diagram (DFD)
from a code-level description of the system.

Usage:
    pip install -r requirements.txt
    python threat_model.py --report report.md   # threat report
    python threat_model.py --dfd | dot -Tpng -o dfd.png   # requires Graphviz
"""

from pytm import TM, Boundary, Dataflow, Datastore, ExternalEntity, Process

tm = TM("Checkout service threat model")
tm.description = "Threat model for the checkout API and its data stores"
tm.isOrdered = True

# Trust boundaries: each one is a place where data crosses a privilege level.
internet = Boundary("Internet")
dmz = Boundary("DMZ")
internal = Boundary("Internal Network")

user = ExternalEntity("Customer")
user.inBoundary = internet

web = Process("Checkout Web App")
web.inBoundary = dmz

api = Process("Checkout API")
api.inBoundary = internal

db = Datastore("Orders DB")
db.inBoundary = internal
db.storesPII = True

Dataflow(user, web, "HTTPS checkout request")
Dataflow(web, api, "Signed API call")
Dataflow(api, db, "SQL over TLS")

tm.process()
