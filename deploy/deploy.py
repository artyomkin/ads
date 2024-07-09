import subprocess
import ansible_runner

def runDeploy(hostNameList, roleNameList):
    hostNames = ','.join(hostNameList)
    roleNames = ','.join(roleNameList)
    ansible_runner.run(
        playbook='/home/welllet/PycharmProjects/diploma/ansible/main.yaml',
        limit=hostNames,
        inventory='/home/welllet/PycharmProjects/diploma/ansible/hosts.ini',
        extravars={
            "_roles": roleNames
        }
    )

