from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, CheckConstraint

metadata = MetaData()
engine = create_engine("sqlite:///test.db")

users = Table('users', metadata,
              Column('username', String(255), nullable=False, primary_key=True),
              Column('password', String(255), nullable=False)
)

hosts = Table('hosts', metadata,
              Column('id', Integer(), primary_key=True),
              Column('hostname', String(255), nullable=False),
              Column('ip', String(255), nullable=False),
              Column('ssh_user', String(255), nullable=False),
              Column('owner_username', ForeignKey('users.username'))
)

configurations = Table('configurations', metadata,
              Column('id', Integer(), primary_key=True),
              Column('name', String(255), nullable=False),
              Column('path', String(255), nullable=False),
              Column('owner_username', ForeignKey('users.username'))
)

hostGroups = Table('hostGroups', metadata,
                   Column('id', Integer(), primary_key=True),
                   Column('name', String(255), nullable=False),
                   Column('owner_username', ForeignKey('users.username'))
)

hostToGroup = Table('hostToGroups', metadata,
                   Column('host_id', ForeignKey('hosts.id')),
                   Column('host_group_id', ForeignKey('hostGroups.id'))
)

hostGroupToHostGroup = Table('hostGroupsToHostGroups', metadata,
                   Column('host_group_child_id', ForeignKey('hostGroups.id')),
                   Column('host_group_parent_id', ForeignKey('hostGroups.id'))
)

metadata.create_all(engine)
