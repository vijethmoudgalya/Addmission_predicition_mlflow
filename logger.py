from datetime import datetime


class App_Logger:
    def __init__(self):
        pass

    def log(self, file_object, log_message):
        try:
            self.now = datetime.now()
            self.date = self.now.date()
            self.current_time = self.now.strftime("%H:%M:%S")
            file_object.write(
                str(self.date) + "/" + str(self.current_time) + "\t\t" + log_message +"\n")
        except Exception as e:
            print(e)