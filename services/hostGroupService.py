from DAO.HostGroupDao import HostToGroupDao, HostGroupDao
from DAO.HostDao import HostDao
from entities.HostGroup import HostGroup
import services.hostService
import logging

logger = logging.getLogger(__name__)


def save(hostGroup):
    if HostGroupDao.exists():
        existingHostGroupDao = HostGroupDao.objects.find(filter="name = '{}'".format(hostGroup.name))
        if existingHostGroupDao is not None and len(existingHostGroupDao) > 0:
            logger.info("Host group {} already exists".format(hostGroup.name))
            return False

    for host in hostGroup.hosts:
        services.hostService.save(host)

def saveHostToGroup(hostname, hostGroupName):
