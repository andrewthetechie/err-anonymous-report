# err-anonymous-report
An errbot plugin to allow anonymous reporting of messages to a group's admins

# Config options
* REPORT_CHANNEL: The channel to send reports to
* REPORT_DM: Bool, Default True, will send a report to bot_admins as well via self.warn_admins

# Commands
./report [report_link] [--reason [optional]]

i.e.

./report http://linktomessage.com --reason 'Violates Rule #2'
