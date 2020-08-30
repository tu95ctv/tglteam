# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api
from odoo.exceptions import UserError
import os
from os import listdir
from os.path import isfile, join


class DocumentTemplateType(models.Model):
    _name = 'document.template.type'
    
    name = fields.Char('Name')
    sequence = fields.Integer('Sequence')


class DocumentTemplate(models.Model):
    _name = 'document.template'

    name = fields.Char('Name')
    file_name = fields.Char('File Name')
    data = fields.Binary('Data')
    type_id = fields.Many2one('document.template.type')

    # def _read_63_file_and_assign_to_db(self):
    #     here_path = os.path.abspath(__file__)
    #     BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(here_path)))
    #     bieu_mau_path = os.path.join(BASE_DIR, 'static/CAC BIEU MAU HANH CHINH')
    #     onlyfiles = [f for f in listdir(bieu_mau_path) if isfile(join(bieu_mau_path, f))]
        # for fname in onlyfiles:
        #     name = os.path.splitext(fname)[0].replace('-',' ').replace('_',' ').capitalize()
        #     document_template_obj = self.search([('name', '=', name)])
        #     if not document_template_obj:
        #         file = open(os.path.join(bieu_mau_path, fname), "rb")
        #         out = file.read()
        #         file.close()
        #         gentextfile = base64.b64encode(out)
        #         self.create({'name': name, 'data':gentextfile, 'file_name':fname })

#         odoo_template = '''
# <record id="%s" model="document.template">
#     <field name="name">%s</field>
#     <field name="file_name">%s</field>
#     <field name="data" type="base64" file="hr_document_template/static/CAC BIEU MAU HANH CHINH/%s"/>
# </record>
# '''
#         rs =''
#         for fname in onlyfiles:
#             name = os.path.splitext(fname)[0].replace('-',' ').replace('_',' ').capitalize()
#             template_id = unidecode(name.replace(' ','_'))
#             tmpl = odoo_template%(template_id, name,  fname, fname )
#             rs +=tmpl
#         f = open(os.path.join(BASE_DIR,'gentemplate.xml') , "w", encoding="utf-8")
#         f.write(rs)
#         f.close()










    

