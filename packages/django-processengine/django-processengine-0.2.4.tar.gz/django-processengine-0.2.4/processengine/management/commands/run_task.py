import json
from contextlib import suppress

from django.conf import settings
from django.core.management.base import BaseCommand
from processengine.models import Process

from processengine.helpers import slack_notification

SPACER_LINE = """
===============================================================================
"""


class Command(BaseCommand):
    help = 'Runs a specified task through the process engine.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('task', nargs='+')

    def handle(self, *args, **options):
        """
        Run the specified task through the process engine.
        """
        task_name = options['task'][0]

        if hasattr(settings, 'SLACK_WEBHOOK'):
            slack_channel = settings.SLACK_PROCESS_CHANNEL
            slack_username = settings.SLACK_PROCESS_USERNAME
            slack_emoji = settings.SLACK_PROCESS_EMOJI
            service_name = settings.SERVICE_NAME
            if hasattr(settings, 'ENV'):
                service_name += " " + settings.ENV

        params = {}
        if task_name in settings.PROCESS_MAP:
            param_string = None
            with suppress(IndexError):
                param_string = options['task'][1]
            if param_string:
                try:
                    params = json.loads(param_string)
                except Exception as e:
                    if all([ not settings.DEBUG,
                           hasattr(settings,'SLACK_WEBHOOK') ]):
                        param_string = str(param_string)
                        title = service_name + ": Process Creation Failed"
                        message = (
                            "Arguments for task {} don't appear to be valid"
                            " JSON.\nArguments were {}")
                        message = message.format(task_name, param_string)
                        slack_notification(message=message,
                                           channel=slack_channel,
                                           username=slack_username,
                                           emoji=slack_emoji,
                                           title=title)
                    else:
                        message = ("Arguments for task {} do not appear to be "
                                   "valid JSON.".format(task_name))
                        message = (SPACER_LINE + "\n" + message + "\n"
                                   + SPACER_LINE)
                        self.stderr.write(message)
                    return
                if not type(params) == dict:
                    if all([ not settings.DEBUG,
                             hasattr(settings, 'SLACK_WEBHOOK') ]):
                        title = service_name + ": Process Creation Failed"
                        message = ("Arguments for task {} are not a valid dict"
                                   ".\nArguments were {}")
                        message = message.format(task_name, param_string)
                        slack_notification(
                            message=message,
                            channel=settings.SLACK_PROCESS_CHANNEL,
                            username=settings.SLACK_PROCESS_USERNAME,
                            emoji=settings.SLACK_PROCESS_EMOJI,
                            title=title)
                    else:
                        message = ("Arguments for task {} do not appear to be "
                              "a JSON dict.".format(task_name))
                        message = (SPACER_LINE + "\n" + message + "\n" +
                                   SPACER_LINE)
                        self.stderr.write(message)
                    return
            process = Process.objects.create(name=task_name, context=params)
            message = "Running task '{}' with the following task ids:\n{}"
            message = message.format(task_name, process.task_ids)
            if settings.DEBUG:
                message = SPACER_LINE + "\n" + message + "\n" + SPACER_LINE
                self.stdout.write(self.style.SUCCESS(message))
            elif hasattr(settings,'SLACK_WEBHOOK'):
                title = service_name + ": Process Creation Succeeded"
                slack_notification(message=message,
                                   channel=settings.SLACK_PROCESS_CHANNEL,
                                   username=settings.SLACK_PROCESS_USERNAME,
                                   emoji=settings.SLACK_PROCESS_EMOJI,
                                   title=title)
        else:
            if not settings.DEBUG and settings.SLACK_WEBHOOK:
                title = settings.SERVICE_NAME + ": Process Creation Failed"
                message = (
                    "We attempted to create a process running task *'{}'*, "
                    "but this task is unknown.")
                message = message.format(task_name)
                slack_notification(message=message,
                                   channel=settings.SLACK_PROCESS_CHANNEL,
                                   username=settings.SLACK_PROCESS_USERNAME,
                                   emoji=settings.SLACK_PROCESS_EMOJI,
                                   title=title)
            else:
                message = "Couldn't find task '{}'".format(task_name)
                message = SPACER_LINE + "\n" + message + "\n" + SPACER_LINE
                self.stderr.write(message)
