from paramiko import SSHClient, AutoAddPolicy
from app.utils.get_project_name_url import get_project_name_from_git_url
from app.utils.remove_whitespaces import remove_whitespaces_add_dashes
from app.schemas import project_schema


def clone_repo(source_control_url, organization_name, credential_password, credential_username, company_name, hostname, port, username, password, timeout: int) -> project_schema.ProjectStatus:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        company = remove_whitespaces_add_dashes(company_name)
        organization = remove_whitespaces_add_dashes(organization_name)
        project = get_project_name_from_git_url(source_control_url)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            f"git clone https://{credential_password}@github.com/{credential_username}/{project}.git {company}/{organization}/projects/{project}"
        )

        cmd_output = stdout.read().decode("utf8")
        cmd_output_error = stderr.read().decode("utf8")

        if "fatal: Too many arguments" in cmd_output_error or "Repository not found" in cmd_output_error or "No such device or address" in cmd_output_error or "could not read Password" in cmd_output_error:
            return project_schema.ProjectStatus.failed
        if "already exists and is not an empty directory" in cmd_output_error:
            (update_stdin, update_stdout, update_stderr) = ssh_client.exec_command(
                f"cd {company}/{organization}/projects/{project};git pull"
            )

            update_cmd_output = update_stdout.read().decode("utf8")
            update_cmd_output_error = update_stderr.read().decode("utf8")

            if "Already up to date" in update_cmd_output and not update_cmd_output_error:
                return project_schema.ProjectStatus.successful
            if "Updating" in update_cmd_output and "From" in update_cmd_output_error:
                return project_schema.ProjectStatus.successful
            if update_cmd_output_error:
                return project_schema.ProjectStatus.failed
        if not cmd_output and "Cloning into" in cmd_output_error:
            return project_schema.ProjectStatus.successful
        if cmd_output_error:
            return project_schema.ProjectStatus.failed
    except Exception as error:
        return False
    finally:
        ssh_client.close()


def update_repo(source_control_url, organization_name, credential_password, credential_username, company_name, hostname, port, username, password, timeout: int) -> project_schema.ProjectStatus:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        company = remove_whitespaces_add_dashes(company_name)
        organization = remove_whitespaces_add_dashes(organization_name)
        project = get_project_name_from_git_url(source_control_url)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            f"cd {company}/{organization}/projects/{project};git pull"
        )

        cmd_output = stdout.read().decode("utf8")
        cmd_output_error = stderr.read().decode("utf8")

        if "No such file or directory" in cmd_output_error:
            (cloned_stdin, cloned_stdout, cloned_stderr) = ssh_client.exec_command(
                f"git clone https://{credential_password}@github.com/{credential_username}/{project}.git {company}/{organization}/projects/{project}"
            )

            cloned_cmd_output = cloned_stdout.read().decode("utf8")
            cloned_cmd_output_error = cloned_stderr.read().decode("utf8")

            if "fatal: Too many arguments" in cloned_cmd_output_error or "Repository not found" in cloned_cmd_output_error or "No such device or address" in cloned_cmd_output_error or "could not read Password" in cloned_cmd_output_error:
                return project_schema.ProjectStatus.failed
            if not cloned_cmd_output and "Cloning into" in cloned_cmd_output_error:
                return project_schema.ProjectStatus.successful
            if cloned_cmd_output_error:
                return project_schema.ProjectStatus.failed
        if "Already up to date" in cmd_output and not cmd_output_error:
            return project_schema.ProjectStatus.successful
        if "Updating" in cmd_output and "From" in cmd_output_error:
            return project_schema.ProjectStatus.successful
        if cmd_output_error:
            return project_schema.ProjectStatus.failed
    except Exception as error:
        return False
    finally:
        ssh_client.close()


def delete_projects(projects, company_name, hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()
    success: bool = True

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        company = remove_whitespaces_add_dashes(company_name)

        for project in projects:
            (stdin, stdout, stderr) = ssh_client.exec_command(
                f"rm -rf {company}/{remove_whitespaces_add_dashes(project.organization.name)}/projects/{get_project_name_from_git_url(project.source_control_url)}"
            )
            cmd_output = stdout.read().decode("utf8")
            cmd_output_error = stderr.read().decode("utf8")

            if not cmd_output and not cmd_output_error:
                pass
            else:
                success = False

        return success
    except Exception as error:
        return False
    finally:
        ssh_client.close()


def update_project_name(organization_name, project_organization_name, project_source_control_url, updated_project_source_control_url, company_name, hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        company = remove_whitespaces_add_dashes(company_name)

        old_organization_name = remove_whitespaces_add_dashes(
            project_organization_name)
        new_organization_name = remove_whitespaces_add_dashes(
            organization_name)
        old_project_name = get_project_name_from_git_url(
            project_source_control_url)
        new_project_name = get_project_name_from_git_url(
            updated_project_source_control_url)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            f"mv {company}/{old_organization_name}/projects/{old_project_name} {company}/{new_organization_name}/projects/{new_project_name}"
        )

        cmd_output = stdout.read().decode("utf8")
        cmd_output_error = stderr.read().decode("utf8")

        if not cmd_output and (not cmd_output_error or "No such file or directory" in cmd_output_error or "File exists" in cmd_output_error):
            return True
        else:
            return False
    except Exception as error:
        return False
    finally:
        ssh_client.close()
