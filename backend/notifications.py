import twilio

class Notification:
    def __init__(self, phone_number):
        self.own_number = "+44 7360 495347"
        self.user_number = phone_number

    
    def send(self):
        print(f"Sending message to {self.user}: {self.message}")

    def send_sms_noti(self, message)
        client = Client()
        message = client.messages.create(
            to=self.user_number,
            from_=self.own_number,
            body=message
        )
        print(f"Sent SMS notification to {self.user_number}: {message.sid}")