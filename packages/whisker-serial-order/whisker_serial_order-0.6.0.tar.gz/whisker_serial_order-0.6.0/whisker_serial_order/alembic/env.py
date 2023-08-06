#!/usr/bin/env python
# whisker_serial_order/alembic/env.py

"""
===============================================================================

    Copyright © 2016-2018 Rudolf Cardinal (rudolf@pobox.com).

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

===============================================================================
"""

import logging
from cardinal_pythonlib.logs import configure_logger_for_colour
from alembic import context
from sqlalchemy import engine_from_config, pool

from whisker_serial_order.models import Base
from whisker_serial_order.settings import dbsettings

log = logging.getLogger(__name__)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # http://alembic.readthedocs.org/en/latest/cookbook.html
    # noinspection PyUnusedLocal
    def process_revision_directives(context_, revision, directives):
        if config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []

    url = config.get_main_option("sqlalchemy.url")
    # RNC
    context.configure(
        url=url,
        target_metadata=target_metadata,
        render_as_batch=True,  # for SQLite mode; http://stackoverflow.com/questions/30378233  # noqa
        literal_binds=True,
        compare_type=True,
        process_revision_directives=process_revision_directives,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)

    # http://alembic.readthedocs.org/en/latest/cookbook.html
    # noinspection PyUnusedLocal
    def process_revision_directives(context_, revision, directives):
        if config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []

    with connectable.connect() as connection:
        # RNC
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # for SQLite mode; http://stackoverflow.com/questions/30378233  # noqa
            compare_type=True,
            process_revision_directives=process_revision_directives,
        )
        with context.begin_transaction():
            context.run_migrations()


rootlogger = logging.getLogger()
rootlogger.setLevel(logging.DEBUG)
configure_logger_for_colour(rootlogger)

log.debug(dbsettings)
if not dbsettings.get('url'):
    raise ValueError("Database URL not specified")

config = context.config
target_metadata = Base.metadata
config.set_main_option('sqlalchemy.url', dbsettings['url'])

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
