from sqlalchemy import *
from migrate import *

meta = MetaData()

application = Table(
    "app", meta,
    Column("app_id", String, primary_key=True),
    Column("app_token", String(256)),
    Column("name", String(256)),
    Column("creation_ts", DateTime),
    Column("last_update_ts", DateTime)
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata

    meta.bind = migrate_engine
    application.create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pass
