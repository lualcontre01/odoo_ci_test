# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Enterprise Management Solution
#    GRP Estado Uruguay
#    Copyright (C) 2017 Quanam (ATEL SA., Uruguay)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning


class RegistroPersonal(models.Model):
    _name = 'registro_personal'
    _rec_name = 'name'
    _description = 'Registro de personas'

    name = fields.Char('Nombre Completo', readonly=True,
                       compute='get_nombre_completo')
    primer_nombre = fields.Char(string="Primer Nombre")
    segundo_nombre = fields.Char(string="Segundo Nombre")
    primer_apellido = fields.Char(string="Primer Apellido")
    segundo_apellido = fields.Char(string="Segundo Apellido")
    edad = fields.Integer(string="Edad")
    credito = fields.Integer(string=u"Creditos",
                             readonly=True,
                             compute="calc_credito")
    materia_ids = fields.One2many(comodel_name="registro_materia",
                                  inverse_name="registro_id",
                                  string="Materias")
    materia_pesada_ids = fields.One2many('registro_materia_pesada',
                                         'registro_id',
                                         'Materias Pesadas')
    calificacion = fields.Selection(string="Calificacion",
                                    selection=[('a', 'A'), ('b', 'B')],
                                    required=False)

    @api.one
    def get_nombre_completo(self):
        for record in self:
            record.name = record.primer_nombre + ' ' + record.primer_apellido

    @api.one
    def calc_credito(self):
        for record in self.materia_ids:
            self.credito += record.credito

    @api.multi
    def calc_materia_pesada(self):
        domain = [('credito', '>=', 20)]
        materia_brws = self.env['registro_materia'].search(domain)
        for record in materia_brws:
            if record not in self.materia_pesada_ids:
                self.materia_pesada_ids.create({
                    'registro_id': self.id,
                    'name': record.name,
                    'valor_credito': record.credito
                })
            else:
                raise Warning('Registros Actualizados')


class RegistroMaterias(models.Model):
    _name = 'registro_materia'
    _rec_name = 'name'
    _description = u'Materias y Descripción'

    registro_id = fields.Many2one(comodel_name="registro_personal",
                                  string="Personal")
    name = fields.Char('Nombre de Materia')
    credito = fields.Integer('Credito de la materia')


class MateriasPesadas(models.Model):
    _name = 'registro_materia_pesada'
    _rec_name = 'name'
    _description = 'Lista Materias Importantes'

    registro_id = fields.Many2one('registro_personal')
    name = fields.Char('Nombre')
    valor_credito = fields.Integer('Peso de materia')
