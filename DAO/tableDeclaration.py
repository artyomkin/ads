from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
Column, ForeignKey, event, ForeignKeyConstraint, UniqueConstraint
from pathlib import Path
import yaml

with open("{}/.config/ads/config.yaml".format(Path.home()), "r") as configFile:
    config = yaml.safe_load(configFile)
    dbPath = config['db']['path']

metadata = MetaData()
engine = create_engine("sqlite:///{}".format(dbPath))

def _enable_fk_pragma(connection, conn_record):
    connection.execute('pragma foreign_keys = ON')

event.listen(engine, 'connect', _enable_fk_pragma)

users = Table('users', metadata,
              Column('username', String(255), nullable=False, primary_key=True),
              Column('password', String(255), nullable=False)
)

hosts = Table('hosts', metadata,
              Column('hostname', String(255), primary_key=True),
              Column('owner_username', ForeignKey('users.username', ondelete="CASCADE"), primary_key=True),
              Column('ip', String(255), nullable=False),
              Column('ssh_user', String(255), nullable=False)
)

configurations = Table('configurations', metadata,
              Column('name', String(255), primary_key=True),
              Column('owner_username', ForeignKey('users.username', ondelete="CASCADE"), primary_key=True)
)

confGroups = Table('confGroups', metadata,
                   Column('id', Integer(), primary_key=True),
                   Column('name', String(255)),
                   Column('owner_username', ForeignKey('users.username', ondelete="CASCADE")),
                   UniqueConstraint('name', 'owner_username')
                   )

confToConfGroups = Table('confToConfGroups', metadata,
                         Column('conf_name', primary_key=True),
                         Column('conf_owner_username', primary_key=True),
                         Column('conf_group_id', ForeignKey('confGroups.id', ondelete="CASCADE"), primary_key=True),
                         ForeignKeyConstraint(
                            ['conf_name', 'conf_owner_username'],
                            ['configurations.name', 'configurations.owner_username'],
                            ondelete='CASCADE'
                            )
                         )

confGroupToConfGroups = Table('confGroupsToConfGroups', metadata,
                              Column('conf_group_child_id', ForeignKey('confGroups.id', ondelete='CASCADE')),
                              Column('conf_group_parent_id', ForeignKey('confGroups.id', ondelete='CASCADE')),
                              )

hostGroups = Table('hostGroups', metadata,
             Column('id', Integer(), primary_key=True),
             Column('name', String(255)),
             Column('owner_username', ForeignKey('users.username', ondelete="CASCADE")),
             UniqueConstraint('name','owner_username')

)

hostToHostGroups = Table('hostToHostGroups', metadata,
              Column('hostname', primary_key=True),
              Column('host_owner_username', primary_key=True),
              Column('host_group_id', ForeignKey('hostGroups.id', ondelete="CASCADE"), primary_key=True),
              ForeignKeyConstraint(
                  ['hostname', 'host_owner_username'],
                  ['hosts.hostname', 'hosts.owner_username'],
                  ondelete='CASCADE'
              )
)

hostGroupToHostGroups = Table('hostGroupsToHostGroups', metadata,
                   Column('host_group_child_id', ForeignKey('hostGroups.id', ondelete="CASCADE")),
                   Column('host_group_parent_id', ForeignKey('hostGroups.id', ondelete="CASCADE"))
)

hostGroupToConfGroups = Table('hostGroupToConfGroup', metadata,
                             Column('host_group_id', ForeignKey('hostGroups.id', ondelete="CASCADE")),
                             Column('conf_group_id', ForeignKey('confGroups.id', ondelete="CASCADE"))
                             )

metadata.create_all(engine)

conn = engine.connect()
