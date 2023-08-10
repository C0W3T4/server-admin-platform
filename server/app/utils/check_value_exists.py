def check_if_in_list_of_dict(sample_dict, value):
    return [True for elem in sample_dict
            if value == elem.id]


def check_if_users_ids_in_list_of_response(sample_dict, value):
    return [True for elem in sample_dict
            if value == elem.user.id]


def check_if_teams_ids_in_list_of_response(sample_dict, value):
    return [True for elem in sample_dict
            if value == elem.team.id]


def check_if_hosts_ids_in_list_of_response(sample_dict, value):
    return [True for elem in sample_dict
            if value == elem.host.id]


def check_if_groups_ids_in_list_of_response(sample_dict, value):
    return [True for elem in sample_dict
            if value == elem.group.id]


def check_if_schedules_ids_in_list_of_response(sample_dict, value):
    return [True for elem in sample_dict
            if value == elem.schedule.id]
