from main import db
from datetime import datetime


class Misc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    os = db.Column(db.String(32), nullable=False)
    os_version = db.Column(db.String(32), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False)
    last_contacted = db.Column(db.DateTime,  nullable=True)
    employee = db.Column(db.String(10),  db.ForeignKey('users.id'), nullable=True)
    linked_to = db.Column(db.String(10), db.ForeignKey('computers.id'), nullable=False)

    def __init__(self, os, os_version, last_updated, last_contacted, employee, linked_to=None):
        self.os = os
        self.os_version = os_version
        self.last_updated = last_updated
        self.last_contacted = last_contacted
        self.employee = employee
        self.linked_to = linked_to
