from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, CheckConstraint
from pathlib import Path
import yaml

with open("{}/.config/ads/config.yaml".format(Path.home()), "r") as configFile:
    config = yaml.safe_load(configFile)
    dbPath = config['db']['path']

metadata = MetaData()
engine = create_engine("sqlite:///{}".format(dbPath))

users = Table('users', metadata,
              Column('username', String(255), nullable=False, primary_key=True),
              Column('password', String(255), nullable=False)
)

hosts = Table('hosts', metadata,
              Column('hostname', String(255), primary_key=True),
              Column('owner_username', ForeignKey('users.username'), primary_key=True),
              Column('ip', String(255), nullable=False),
              Column('ssh_user', String(255), nullable=False)
)

configurations = Table('configurations', metadata,
              Column('name', String(255), primary_key=True),
              Column('owner_username', ForeignKey('users.username'), primary_key=True)
)

confGroups = Table('confGroups', metadata,
                   Column('id', Integer(), primary_key=True),
                   Column('name', String(255)),
                   Column('owner_username', ForeignKey('users.username'))
                   )

confToConfGroups = Table('confToConfGroups', metadata,
                         Column('conf_name', ForeignKey('configurations.name'), primary_key=True),
                         Column('conf_owner_username', ForeignKey('configurations.owner_username'), primary_key=True),
                         Column('conf_group_id', ForeignKey('confGroups.id'), primary_key=True)
                         )

confGroupToConfGroups = Table('confGroupsToConfGroups', metadata,
                              Column('conf_group_child_id', ForeignKey('confGroups.id')),
                              Column('conf_group_parent_id', ForeignKey('confGroups.id'))
                              )

hostGroups = Table('hostGroups', metadata,
             Column('id', Integer(), primary_key=True),
              Column('name', String(255)),
              Column('owner_username', ForeignKey('users.username'))
)

hostToHostGroups = Table('hostToHostGroups', metadata,
              Column('hostname', ForeignKey('hosts.hostname'), primary_key=True),
              Column('host_owner_username', ForeignKey('hosts.owner_username'), primary_key=True),
              Column('host_group_id', ForeignKey('hostGroups.id'), primary_key=True)
)

hostGroupToHostGroups = Table('hostGroupsToHostGroups', metadata,
                   Column('host_group_child_id', ForeignKey('hostGroups.id')),
                   Column('host_group_parent_id', ForeignKey('hostGroups.id'))
)

hostGroupToConfGroups = Table('hostGroupToConfGroup', metadata,
                             Column('host_group_id', ForeignKey('hostGroups.id')),
                             Column('conf_group_id', ForeignKey('confGroups.id'))
                             )

metadata.create_all(engine)

conn = engine.connect()
