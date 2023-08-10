from paramiko import SSHClient, AutoAddPolicy
from app.utils.remove_whitespaces import remove_whitespaces_add_dashes


def create_organization_directories(company_name, organization_name, hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()
        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        company = remove_whitespaces_add_dashes(company_name)
        organization = remove_whitespaces_add_dashes(organization_name)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            f"mkdir {company}/{organization};mkdir {company}/{organization}/inventories;mkdir {company}/{organization}/projects"
        )

        cmd_output = stdout.read().decode("utf8")
        cmd_output_error = stderr.read().decode("utf8")

        if not cmd_output and (not cmd_output_error or "File exists" in cmd_output_error):
            return True
        else:
            return False
    except Exception as error:
        return False
    finally:
        ssh_client.close()


def update_organization_name(old_organization_name, organization_name, company_name, hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        company = remove_whitespaces_add_dashes(company_name)

        old_organization = remove_whitespaces_add_dashes(old_organization_name)
        organization = remove_whitespaces_add_dashes(organization_name)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            f"mv {company}/{old_organization} {company}/{organization}"
        )

        cmd_output = stdout.read().decode("utf8")
        cmd_output_error = stderr.read().decode("utf8")

        if not cmd_output and (not cmd_output_error or "File exists" in cmd_output_error):
            return True
        else:
            return False
    except Exception as error:
        return False
    finally:
        ssh_client.close()


def delete_organization_remote(organization_name, company_name, hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        company = remove_whitespaces_add_dashes(company_name)

        organization = remove_whitespaces_add_dashes(organization_name)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            f"rm -rf {company}/{organization}"
        )

        cmd_output = stdout.read().decode("utf8")
        cmd_output_error = stderr.read().decode("utf8")

        if not cmd_output and not cmd_output_error:
            return True
        else:
            return False
    except Exception as error:
        return False
    finally:
        ssh_client.close()
