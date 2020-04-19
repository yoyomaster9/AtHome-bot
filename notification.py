# Will contian all code making the bot run misc commands on a day

def firstTimeStartup():
    # Need code to create folder /notifications
    # allows for expandability, call Notification.save() to save
    pass

class Notification:
    def __init__(self, trigger, content):
        # trigger will be datetime formatted
        # content will be the string that is retured if trigger is true
        self.trigger = trigger
        self.content = content

        # Might also need self.id

    def checkTrigger(self, now): # rename this
        # Will determine if now (datetime) passes the check
        # returns true or false
        pass

    def formatContent(self, ctx):
        # might need to take self.content and format based on discord ctx
        # Will return discord-friendly string
        # Emoji/Roles that couldn't be found will not be formatted
        pass

    def save(self):
        # Will need to save notifications to outside folder for storage
        # Allows for expandability
        pass

    def getID(self):
        # Might need this for future
        pass
