from typing import Any, List


def get_hosts_by_group(sample_list: List[Any]) -> list[dict[str, Any]]:
    groups_hosts: List[dict[str, Any]] = []
    s = set()
    for element in sample_list:
        s.add(element.group)
    for e in s:
        groups_hosts.append(dict(
            group=e,
            hosts=[]
        ))
    for group_host in groups_hosts:
        for element in sample_list:
            if group_host["group"].id == element.group.id:
                group_host["hosts"].append(element.host)

    return groups_hosts


def get_ids_list(sample_list: List[Any]) -> List[int]:
    ids_list: List[int] = []

    for element in sample_list:
        ids_list.append(element.id)

    return ids_list


def get_users_ids_list_from_response(sample_list: List[Any]) -> List[int]:
    ids_list: List[int] = []

    for element in sample_list:
        ids_list.append(element.user.id)

    return ids_list


def get_teams_ids_list_from_response(sample_list: List[Any]) -> List[int]:
    ids_list: List[int] = []

    for element in sample_list:
        ids_list.append(element.team.id)

    return ids_list


def get_hosts_ids_list_from_response(sample_list: List[Any]) -> List[int]:
    ids_list: List[int] = []

    for element in sample_list:
        ids_list.append(element.host.id)

    return ids_list


def get_groups_ids_list_from_response(sample_list: List[Any]) -> List[int]:
    ids_list: List[int] = []

    for element in sample_list:
        ids_list.append(element.group.id)

    return ids_list


def get_templates_ids_list_from_response(sample_list: List[Any]) -> List[int]:
    ids_list: List[int] = []

    for element in sample_list:
        ids_list.append(element.template.id)

    return ids_list


def get_schedules_ids_list_from_response(sample_list: List[Any]) -> List[int]:
    ids_list: List[int] = []

    for element in sample_list:
        ids_list.append(element.schedule.id)

    return ids_list
