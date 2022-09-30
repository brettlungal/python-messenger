from persistence.mailbox_actions import MailboxActions

class Mailbox:

    def __init__(self, messages):
        self.messages = messages

    def launch_mailbox_interface(self):
        choice = None
        while choice != "q":
            choice = input("Please select something or enter q to return to previous menu")

    