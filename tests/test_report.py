from errbot import ValidationException
import pytest

pytest_plugins = ["errbot.backends.test"]

extra_plugin_dir = "."


# Tests for botcmds
def test_report_to_channel_and_dm(testbot):
    """
    Tests require_2fa
    """
    testbot.push_message(
        "!report http://test.com --reason 'test report, please ignore'"
    )
    msgs = []
    # in this mode, we send 3 messages. One to the report channel, one via self.warn_admins, and one back to the user
    for i in range(0, 3):
        msgs.append(testbot.pop_message())
    # first message goes to the admin report channel. In test mode, this is just one single chatroom but in use,
    # this should be a private channel
    assert (
        "Received anonymous report. http://test.com. Reason: test report, please ignore"
        in msgs
    )
    # this message gets sent back to the user reporting the issue
    assert "Report sent to the admins" in msgs


def test_report_to_only_channel(testbot):
    plugin = testbot.bot.plugin_manager.get_plugin_obj_by_name("AnonymousReports")
    plugin.config["REPORT_DM"] = False

    testbot.push_message(
        "!report http://test.com --reason 'test report, please ignore'"
    )
    msgs = []
    # in this mode, we send23 messages. One to the report channel and one back to the user
    for i in range(0, 2):
        msgs.append(testbot.pop_message())
    # first message goes to the admin report channel. In test mode, this is just one single chatroom but in use,
    # this should be a private channel
    assert (
        "Received anonymous report. http://test.com. Reason: test report, please ignore"
        in msgs
    )
    # this message gets sent back to the user reporting the issue
    assert "Report sent to the admins" in msgs
