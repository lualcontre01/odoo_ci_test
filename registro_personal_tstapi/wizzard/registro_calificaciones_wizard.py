# -*- coding: utf-8 -*-
from openerp import models, fields, api


class AsignarCalificacion(models.TransientModel):
    _name = 'asignar_calificacion'
    _description = 'Asistente para asignacion de calificaciones'

    primer_nombre = fields.Char('Primer Nombre')
    calificacion = fields.Selection(string="Calificacion",
                                    selection=[('a', 'A'), ('b', 'B')],
                                    required=False)
    alumnos_ids = fields.One2many('calificacion_alumnos','calificacion_id',
                                  'Alumnos')


class CalificacionAlumnos(models.TransientModel):
    _name = 'calificacion_alumnos'

    calificacion_id = fields.Many2one('asignar_calificacion')
    name = fields.Char('Nombre Completo')