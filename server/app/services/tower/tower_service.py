from paramiko import SSHClient, AutoAddPolicy
from app.utils.get_project_name_url import get_project_name_from_git_url
from app.utils.remove_whitespaces import remove_whitespaces_add_dashes
from app.schemas import job_schema, template_schema, host_schema


def check_host_connection(hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        return True
    except Exception as error:
        return False
    finally:
        ssh_client.close()


def install_tower_services(hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()
        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            "sudo -S dnf install -y python3 ansible git-all")

        stdin.write(password + '\n')
        stdin.flush()

        cmd_output = stdout.read().decode("utf8")
        cmd_output_error = stderr.read().decode("utf8")

        if not cmd_output_error or "[sudo]" in cmd_output_error:
            return True
        else:
            return False
    except Exception as error:
        return False
    finally:
        ssh_client.close()


def prepare_utils_directory(add_schedule_file: str, hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            f"mkdir utils;mkdir utils/logs;python3 -m venv utils/venv;source utils/venv/bin/activate;pip install python-crontab"
        )

        cmd_output = stdout.read().decode("utf8")
        cmd_output_error = stderr.read().decode("utf8")

        if (not cmd_output or "Successfully installed" in cmd_output or "Requirement already satisfied" in cmd_output) and (not cmd_output_error or "File exists" in cmd_output_error or "WARNING" in cmd_output_error):
            (added_file_stdin, added_file_stdout, added_file_stderr) = ssh_client.exec_command(
                f"tee ~/utils/add_schedule.py <<-EOF {add_schedule_file}"
            )

            added_file_cmd_output = added_file_stdout.read().decode("utf8")
            added_file_cmd_output_error = added_file_stderr.read().decode("utf8")

            if add_schedule_file.strip() in added_file_cmd_output and (not added_file_cmd_output_error or "File exists" in added_file_cmd_output_error or 'desejado "EOF"' in added_file_cmd_output_error or "wanted `EOF'" in added_file_cmd_output_error):
                return True
            else:
                return False
        else:
            return False
    except Exception as error:
        return False
    finally:
        ssh_client.close()


def create_tower_directory(company_name, hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        company = remove_whitespaces_add_dashes(company_name)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            f"mkdir {company}"
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


def update_company_name(old_company_name, company_name, hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        old_company = remove_whitespaces_add_dashes(old_company_name)
        company = remove_whitespaces_add_dashes(company_name)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            f"mv {old_company} {company}"
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


def add_host_fingerprint(host_ipv4, hostname, port, username, password, timeout: int) -> host_schema.HostStatus:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        (get_key_stdin, get_key_stdout, get_key_stderr) = ssh_client.exec_command(
            f"ssh-keyscan -H {host_ipv4}"
        )

        get_key_cmd_output = get_key_stdout.read().decode("utf8")
        get_key_cmd_output_error = get_key_stderr.read().decode("utf8")

        if not get_key_cmd_output and (not get_key_cmd_output_error or 'No route to host' in get_key_cmd_output_error):
            return host_schema.HostStatus.unreachable

        if get_key_cmd_output:
            (check_key_stdin, check_key_stdout, check_key_stderr) = ssh_client.exec_command(
                f"grep '{get_key_cmd_output}' ~/.ssh/known_hosts"
            )

            check_key_cmd_output = check_key_stdout.read().decode("utf8")
            check_key_cmd_output_error = check_key_stderr.read().decode("utf8")

            if not check_key_cmd_output:
                (write_key_stdin, write_key_stdout, write_key_stderr) = ssh_client.exec_command(
                    f"echo '{get_key_cmd_output.strip()}' >> ~/.ssh/known_hosts"
                )

                write_key_cmd_output = write_key_stdout.read().decode("utf8")
                write_key_cmd_output_error = write_key_stderr.read().decode("utf8")

                if not write_key_cmd_output and not write_key_cmd_output_error:
                    return host_schema.HostStatus.successful
                else:
                    return host_schema.HostStatus.failed
            else:
                return host_schema.HostStatus.successful
        else:
            return host_schema.HostStatus.failed
    except Exception as error:
        return False
    finally:
        ssh_client.close()


def delete_host_fingerprint(host_ipv4, hostname, port, username, password, timeout: int) -> bool:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()

        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        (stdin, stdout, stderr) = ssh_client.exec_command(
            f"ssh-keygen -R {host_ipv4}"
        )

        cmd_output = stdout.read().decode("utf8")
        cmd_output_error = stderr.read().decode("utf8")

        if "known_hosts updated" in cmd_output and (not cmd_output_error or "not found in" in cmd_output_error or "No such file or directory" in cmd_output_error):
            return True
        elif not cmd_output and "not found in" in cmd_output_error:
            return True
        else:
            return False
    except Exception as error:
        return False
    finally:
        ssh_client.close()


def launch_jobs(template_organization_name, template_project_source_control_url, template_playbook_name, template_inventory_file, template_privilege_escalation, template_forks, template_verbosity, template_launch_type, template_extra_vars, template_credential_username, template_credential_password, company_name, hostname, port, username, password, timeout: int) -> str:
    ssh_client = SSHClient()

    try:
        ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        ssh_client.load_system_host_keys()
        ssh_client.connect(hostname=hostname, port=port,
                           username=username, password=password, timeout=timeout)

        company = remove_whitespaces_add_dashes(company_name)
        organization = remove_whitespaces_add_dashes(
            template_organization_name)
        project = get_project_name_from_git_url(
            template_project_source_control_url)
        inventory_file_name = remove_whitespaces_add_dashes(
            template_inventory_file)

        cmd = f"ansible-playbook {company}/{organization}/projects/{project}/{template_playbook_name} -i {company}/{organization}/inventories/{inventory_file_name} -u {template_credential_username} -K"

        if template_privilege_escalation:
            cmd += f" -b"
        if template_forks:
            cmd += f" -f {template_forks}"
        if template_verbosity and template_verbosity != template_schema.Verbosity.zero:
            cmd += f" -{template_verbosity}"
        if template_launch_type == template_schema.LaunchType.check:
            cmd += f" -C"
        if template_extra_vars:
            cmd += f" -e 'ansible_password={template_credential_password} {template_extra_vars}'"
        else:
            cmd += f" -e 'ansible_password={template_credential_password}'"

        (stdin, stdout, stderr) = ssh_client.exec_command(cmd)

        stdin.write(template_credential_password + '\n')
        stdin.flush()

        cmd_output = stdout.read().decode("utf8")
        cmd_output_error = stderr.read().decode("utf8")

        if cmd_output and (not cmd_output_error or "Can not control echo on the terminal" in cmd_output_error or "DEPRECATION WARNING" in cmd_output_error):
            return cmd_output
        else:
            return job_schema.JobStatus.failed
    except Exception as error:
        return False
    finally:
        ssh_client.close()
