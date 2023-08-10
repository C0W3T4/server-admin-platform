from paramiko import SSHClient, AutoAddPolicy
from app.utils.remove_whitespaces import remove_whitespaces_add_dashes
from app.schemas import inventory_schema


def create_inventory_file(organization_name, inventory_file, company_name, hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        company = remove_whitespaces_add_dashes(company_name)
        organization = remove_whitespaces_add_dashes(organization_name)
        file_name = remove_whitespaces_add_dashes(inventory_file)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            f"touch {company}/{organization}/inventories/{file_name}")

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


def update_inventory_file(organization_name, inventory_organization_name, inventory_file, new_inventory_file, company_name, hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        company = remove_whitespaces_add_dashes(company_name)

        old_organization = remove_whitespaces_add_dashes(
            inventory_organization_name)
        organization = remove_whitespaces_add_dashes(organization_name)
        file_name = remove_whitespaces_add_dashes(inventory_file)
        new_file_name = remove_whitespaces_add_dashes(new_inventory_file)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            f"mv {company}/{old_organization}/inventories/{file_name} {company}/{organization}/inventories/{new_file_name}"
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


def delete_inventory_file(inventories, company_name, hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()
    success: bool = True

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        company = remove_whitespaces_add_dashes(company_name)

        for inventory in inventories:
            (stdin, stdout, stderr) = ssh_client.exec_command(
                f"rm {company}/{remove_whitespaces_add_dashes(inventory.organization.name)}/inventories/{remove_whitespaces_add_dashes(inventory.inventory_file)}"
            )
            cmd_output = stdout.read().decode("utf8")
            cmd_output_error = stderr.read().decode("utf8")

            if not cmd_output and (not cmd_output_error or "File exists" in cmd_output_error):
                pass
            else:
                success = False

        return success
    except Exception as error:
        return False
    finally:
        ssh_client.close()


def write_inventory_file(organization_name, inventory_file, file_content: str, company_name, hostname, port, username, password, timeout: int) -> inventory_schema.InventoryStatus:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        company = remove_whitespaces_add_dashes(company_name)
        organization = remove_whitespaces_add_dashes(organization_name)
        file_name = remove_whitespaces_add_dashes(inventory_file)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            f"tee {company}/{organization}/inventories/{file_name} <<-EOF {file_content}"
        )

        cmd_output = stdout.read().decode("utf8")
        cmd_output_error = stderr.read().decode("utf8")

        if file_content.strip() in cmd_output and (not cmd_output_error or "File exists" in cmd_output_error or 'desejado "EOF"' in cmd_output_error or "wanted `EOF'" in cmd_output_error):
            return inventory_schema.InventoryStatus.successful
        else:
            return inventory_schema.InventoryStatus.error
    except Exception as error:
        return False
    finally:
        ssh_client.close()
