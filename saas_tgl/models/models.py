# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DBPlan(models.Model):
    _name = 'db.plan'

    name = fields.Char()
    username = fields.Char()
    password = fields.Char()


class DBClient(models.Model):
    _name = 'db.client'
    _inherits = {'res.partner':'partner_id'}

    plan_id = fields.Many2one('db.plan')
    client_name = fields.Char()
    
    




