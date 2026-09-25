# -*- coding: utf-8 -*-


def post_init_hook(env):
    env['ir.model']._logs_partout_activate_defaults()
