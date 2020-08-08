from typing import Any
from typing import List
from typing import Dict

from errbot.backends.base import Message as ErrbotMessage
from errbot import BotPlugin
from errbot import ValidationException
from errbot import arg_botcmd
from errbot import botcmd
from decouple import config as get_config


def get_config_item(
    key: str, config: Dict, overwrite: bool = False, **decouple_kwargs
) -> Any:
    """
    Checks config to see if key was passed in, if not gets it from the environment/config file

    If key is already in config and overwrite is not true, nothing is done. Otherwise, config var is added to config
    at key
    """
    if key not in config and not overwrite:
        config[key] = get_config(key, **decouple_kwargs)


class Report(BotPlugin):
    """Report a message anonymously to the group's admins for violating our community guidelines"""

    def configure(self, configuration: Dict) -> None:
        """
        Configures the plugin
        """
        self.log.debug("Starting Config")
        if configuration is None:
            configuration = dict()

        # name of the channel to post in
        get_config_item("REPORT_CHANNEL", configuration)
        get_config_item("REPORT_DM", configuration, cast=bool, default=True)
        super().configure(configuration)

    def check_configuration(self, configuration: Dict) -> None:
        """
        Validates our config
        Raises:
            errbot.ValidationException when the configuration is invalid
        """
        if configuration["REPORT_CHANNEL"][0] != "#":
            raise ValidationException(
                "REPORT_CHANNEL should be in the format #channel-name"
            )
        return

    @botcmd
    @arg_botcmd(
        "report_link",
        nargs="*",
        type=str,
        help="Link the the slack message you are reporting",
    )
    @arg_botcmd(
        "--reason",
        type=str,
        dest="reason",
        default="",
        help="Add any additional details to your report",
    )
    def report(self, msg: ErrbotMessage, report_link: List[str], reason: str) -> str:
        """
        Send a 100% anonymous report to the admins about a message that violates our community guidelines.
        """
        # topic is a nargs representation of whatever was passed in, lets make it a sentence
        report_link = " ".join(report_link)
        if reason != "":
            reason = f"Reason: {reason}"
        report = f"Received anonymous report. {report_link}. {reason}"
        if self.config["REPORT_DM"]:
            self.warn_admins(report)
        self.send(self.build_identifier(self.config["REPORT_CHANNEL"]), report)
        return "Report sent to the admins"
