# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
import base64
import re 
from io import BytesIO
import json

class ResCompany(models.Model):
    _inherit = "res.company"

    arabic_name = fields.Char('Arabic Name')
    other_name1 = fields.Char('Invoice First Line')
    other_name = fields.Char('Invoice Second Line')
    report_footer_text_english1 = fields.Text(string=' English Line 1')
    report_footer_text_arabic1 = fields.Text(string='Invoice Footer')
    terms_conditons_invoise = fields.Boolean(string='Terms & conditions in customer invoice')
    terms_conditons = fields.Text('Text')

class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', size=24, change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", 'State')
    country_id = fields.Many2one('res.country', 'Country')
    swift_code = fields.Char('Swift Code')
    ifsc = fields.Char('IFSC')
    branch_name = fields.Char('Branch Name')
    iban_number = fields.Char('IBAN Number')

class account_invoice(models.Model):
    _inherit = "account.move"


    qr_code_base64 = fields.Char("QR Code", store=True) 
    confirmation_datetime = fields.Datetime(string='Confirmation Date', readonly=True, copy=False, store=True)
    date_config = fields.Date('Payment date')

    bank_account_id = fields.Many2one('res.partner.bank', 'Bank Account')

    def action_post(self):
        res = super(account_invoice, self).action_post()
        self.write({'confirmation_datetime': fields.Datetime.now()})
        return  res


    def get_tax_totals_json(self, str):
        return json.loads(str)


    def generate_qr_code(self):

        
        def get_qr_encoding(tag, field):
            print("XXXXXXXXXXXXXx", field)
            company_name_byte_array = field.encode('UTF-8')
            company_name_tag_encoding = tag.to_bytes(length=1, byteorder='big')
            company_name_length_encoding = len(company_name_byte_array).to_bytes(length=1, byteorder='big')
            return company_name_tag_encoding + company_name_length_encoding + company_name_byte_array


        for record in self:
            qr_code_str = ''

            if not record.confirmation_datetime:
                record.confirmation_datetime = record.invoice_date
            seller_name_enc = get_qr_encoding(1, record.company_id.display_name)
            company_vat_enc = get_qr_encoding(2, record.company_id.vat)
            time_sa = fields.Datetime.context_timestamp(self.with_context(tz='Asia/Riyadh'), record.confirmation_datetime).strftime("%Y-%m-%d %H:%M:%S")
            timestamp_enc = get_qr_encoding(3, str(time_sa))
            invoice_total_enc = get_qr_encoding(4, str(record.amount_total))
            total_vat_enc = get_qr_encoding(5, str(record.currency_id.round(record.amount_total - record.amount_untaxed)))

            str_to_encode = seller_name_enc + company_vat_enc + timestamp_enc + invoice_total_enc + total_vat_enc
            qr_code_str = base64.b64encode(str_to_encode).decode('UTF-8')
            record.qr_code_base64 = qr_code_str

    def tax_invoice_print_v2(self):
        return self.env.ref('khalid_v2_invoice_templates.action_tax_invoice_report_v2').report_action(self)

    def get_name(self,name):
        newname = re.sub("[\[\[].*?[\]\]]", "",name)
        return newname