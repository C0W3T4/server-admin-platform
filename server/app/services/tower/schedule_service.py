from crontab import CronTab
from croniter import croniter
from json import dumps
from datetime import datetime
from typing import Any, List
from app.schemas import schedule_schema


def add_job_schedule(command: str, comment: str, schedule_datetime: datetime, repeat_frequency: schedule_schema.ScheduleRepeatFrequency, schedule_every: int, schedule_weekdays: List[int]) -> bool:
    try:
        cron = CronTab(user=True)
        cron.env['SHELL'] = '/bin/bash'

        job = cron.new(
            command=command,
            comment=comment
        )

        if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.run_once.name:
            job.minute.on(schedule_datetime.minute)
            job.hour.on(schedule_datetime.hour)
            job.day.on(schedule_datetime.day)
            job.month.on(schedule_datetime.month)

        if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.minute.name:
            if schedule_every:
                job.minute.every(schedule_every)

        if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.hour.name:
            job.minute.on(schedule_datetime.minute)
            if schedule_every:
                job.hour.every(schedule_every)

        if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.day.name:
            job.minute.on(schedule_datetime.minute)
            job.hour.on(schedule_datetime.hour)
            if schedule_every:
                job.day.every(schedule_every)

        if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.week.name:
            job.minute.on(schedule_datetime.minute)
            job.hour.on(schedule_datetime.hour)
            if schedule_weekdays:
                for index, week_day in enumerate(schedule_weekdays):
                    if index == 0:
                        job.dow.on(week_day)
                    else:
                        job.dow.also.on(week_day)

        if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.month.name:
            job.minute.on(schedule_datetime.minute)
            job.hour.on(schedule_datetime.hour)
            job.day.on(schedule_datetime.day)
            if schedule_every:
                job.month.every(schedule_every)

        if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.year.name:
            job.minute.on(schedule_datetime.minute)
            job.hour.on(schedule_datetime.hour)
            job.day.on(schedule_datetime.day)
            job.month.on(schedule_datetime.month)

        cron.write_to_user(user=True)
        return True
    except Exception as error:
        return False


def update_job_schedule(comment: str, schedule_datetime: datetime, repeat_frequency: schedule_schema.ScheduleRepeatFrequency, schedule_every: int, schedule_weekdays: List[int]) -> bool:
    try:
        cron = CronTab(user=True)
        cron.env['SHELL'] = '/bin/bash'

        for job in cron:
            if job.comment == comment:
                job.clear()

                if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.run_once.name:
                    job.minute.on(schedule_datetime.minute)
                    job.hour.on(schedule_datetime.hour)
                    job.day.on(schedule_datetime.day)
                    job.month.on(schedule_datetime.month)

                if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.minute.name:
                    if schedule_every:
                        job.minute.every(schedule_every)

                if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.hour.name:
                    job.minute.on(schedule_datetime.minute)
                    if schedule_every:
                        job.hour.every(schedule_every)

                if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.day.name:
                    job.minute.on(schedule_datetime.minute)
                    job.hour.on(schedule_datetime.hour)
                    if schedule_every:
                        job.day.every(schedule_every)

                if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.week.name:
                    job.minute.on(schedule_datetime.minute)
                    job.hour.on(schedule_datetime.hour)
                    if schedule_weekdays:
                        for index, week_day in enumerate(schedule_weekdays):
                            if index == 0:
                                job.dow.on(week_day)
                            else:
                                job.dow.also.on(week_day)

                if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.month.name:
                    job.minute.on(schedule_datetime.minute)
                    job.hour.on(schedule_datetime.hour)
                    job.day.on(schedule_datetime.day)
                    if schedule_every:
                        job.month.every(schedule_every)

                if repeat_frequency == schedule_schema.ScheduleRepeatFrequency.year.name:
                    job.minute.on(schedule_datetime.minute)
                    job.hour.on(schedule_datetime.hour)
                    job.day.on(schedule_datetime.day)
                    job.month.on(schedule_datetime.month)

                cron.write_to_user(user=True)
        return True
    except Exception as error:
        return False


def remove_job_schedules(resource_schedules: Any | list | None) -> bool:
    try:
        cron = CronTab(user=True)
        cron.env['SHELL'] = '/bin/bash'

        for job in cron:
            for resource_schedule in resource_schedules:
                if job.comment == resource_schedule.cron_job_id:
                    job.delete()

        cron.write_to_user(user=True)
        return True
    except Exception as error:
        return False


def get_job_schedule_info(resource_schedules: Any | list | None) -> list[dict[str, Any]] | None:
    try:
        cron = CronTab(user=True)
        cron.env['SHELL'] = '/bin/bash'

        schedule_info_response: list[dict[str, Any]] = []

        for job in cron:
            for resource_schedule in resource_schedules:
                if job.comment == resource_schedule.cron_job_id:
                    sch: croniter = job.schedule(date_from=datetime.now())

                    schedule_info: dict[str, Any] = dict(
                        cron_job_id=resource_schedule.cron_job_id,
                        frequency=job.frequency(),
                        frequency_per_hour=job.frequency_per_hour(),
                        frequency_per_day=job.frequency_per_day(),
                        frequency_per_year=job.frequency_per_year(),
                        prev_date=sch.get_prev(),
                        next_date=sch.get_next()
                    )
                    schedule_info_response.append(schedule_info)
        return schedule_info_response
    except Exception as error:
        return None


def check_job_id(comment: str) -> bool:
    try:
        cron = CronTab(user=True)
        cron.env['SHELL'] = '/bin/bash'

        for job in cron:
            if job.comment == comment:
                return True
        return False
    except Exception as error:
        return False


def add_crontab_schedule_template(token: str, schedule_datetime: datetime, repeat_frequency: schedule_schema.ScheduleRepeatFrequency, schedule_every: int, schedule_weekdays: List[int], comment: str, template_id, organization_id) -> bool:
    try:
        payload = dumps({"template_id": template_id,
                        "organization_id": organization_id})

        cmd = f"curl -X POST -H 'Content-Type: application/json' -H 'Authorization: Bearer {token}' -d '{payload}' 127.0.0.1:8000/api/jobs/launch"

        schedule_added = add_job_schedule(
            cmd,
            comment,
            schedule_datetime,
            repeat_frequency,
            schedule_every if schedule_every else None,
            schedule_weekdays if schedule_weekdays else None
        )

        if schedule_added:
            return True
        else:
            return False
    except Exception as error:
        return False


def add_crontab_schedule_project(token: str, schedule_datetime: datetime, repeat_frequency: schedule_schema.ScheduleRepeatFrequency, schedule_every: int, schedule_weekdays: List[int], comment: str, project_id) -> bool:
    try:
        cmd = f"curl -X PUT -H 'Content-Type: application/json' -H 'Authorization: Bearer {token}' 127.0.0.1:8000/api/projects/{project_id}/repo"

        schedule_added = add_job_schedule(
            cmd,
            comment,
            schedule_datetime,
            repeat_frequency,
            schedule_every if schedule_every else None,
            schedule_weekdays if schedule_weekdays else None
        )

        if schedule_added:
            return True
        else:
            return False
    except Exception as error:
        return False


def add_crontab_schedule_inventory(token: str, schedule_datetime: datetime, repeat_frequency: schedule_schema.ScheduleRepeatFrequency, schedule_every: int, schedule_weekdays: List[int], comment: str, inventory_id) -> bool:
    try:
        cmd = f"curl -X PUT -H 'Content-Type: application/json' -H 'Authorization: Bearer {token}' 127.0.0.1:8000/api/inventories/{inventory_id}/sync"

        schedule_added = add_job_schedule(
            cmd,
            comment,
            schedule_datetime,
            repeat_frequency,
            schedule_every if schedule_every else None,
            schedule_weekdays if schedule_weekdays else None
        )

        if schedule_added:
            return True
        else:
            return False
    except Exception as error:
        return False
