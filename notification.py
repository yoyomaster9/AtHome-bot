# Will contian all code making the bot run misc commands on a day

# Notiications will be on trigger basis - weekday, time
# Trigger will be - if now.today in weekday and now.time in time:

# Discord input will be @notification add [...days...], [...times...], 'Content'

def firstTimeStartup():
    # Need code to create folder /notifications
    # allows for expandability, call Notification.save() to save
    # will also load up existing notifications
    startup()

    pass

def startup():
    # Maybe?
    pass

def load(notification):
    # Will need method to load notification from storage into memory
    pass

class Notification:
    def __init__(self, date, time, content):
        # date and time might be lists
        # content will be the string that is retured if trigger is true
        self.date = date
        self.time = time
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
