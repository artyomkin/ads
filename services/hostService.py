from DAO.HostDao import HostDao
import logging

logger = logging.getLogger(__name__)


def save(host):
    if HostDao.exists():
        existing_host = HostDao.objects.find(filter="id = '{}'".format(host.id))
        if existing_host is not None and len(existing_host) > 0:
            logger.info("Host with id {} already exists.".format(host.id))
            return False

    HostDao({
        "hostname": host.hostname,
        "ip": host.ip,
        "ssh_user": host.ssh_user,
        "owner_username": host.owner_username
    }).save()
    logger.info("Host with id {} was successfully saved.".format(host.id))
    return True


def delete(id):
    existing_host = HostDao.objects.find(filter="id = '{}'".format(id))
    if existing_host is None or len(existing_host) == 0:
        logger.info("Host with id {} does not exist.".format(id))
        return False
    HostDao({"id": id}).delete()
    logger.info("Host with id {} was successfully deleted.".format(id))
    return True
