import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import *
import threading
from tkinter import messagebox
from tkinter import filedialog
import time


class EmailSenderApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Email Sender")

        self.is_recurring = BooleanVar()
        self.is_recurring.set(False)

        self.frame = Frame()
        self.frame.grid(column=0, row=0, padx=10, pady=10)

        Label(self.frame, text="Sender's Email:").grid(column=0, row=0, sticky="w")
        self.sender_email_entry = Entry(self.frame)
        self.sender_email_entry.grid(column=1, row=0, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Sender's Password:").grid(column=0, row=1, sticky="w")
        self.sender_password_entry = Entry(self.frame, show="*")
        self.sender_password_entry.grid(column=1, row=1, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Recipient's Email:").grid(column=0, row=2, sticky="w")
        self.recipient_email_entry = Entry(self.frame)
        self.recipient_email_entry.grid(column=1, row=2, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Subject:").grid(column=0, row=3, sticky="w")
        self.subject_entry = Entry(self.frame)
        self.subject_entry.grid(column=1, row=3, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Message:").grid(column=0, row=4, sticky="w")
        self.message_body_text = Text(self.frame, width=40, height=10)
        self.message_body_text.grid(column=1, row=4, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Send After (seconds):").grid(column=0, row=5, sticky="w")
        self.send_after_entry = Entry(self.frame)
        self.send_after_entry.grid(column=1, row=5, padx=10, pady=5, columnspan=2)

        Label(self.frame, text="Recurring Email:").grid(column=0, row=6, sticky="w")
        self.recurring_email_checkbox = Checkbutton(self.frame, variable=self.is_recurring)
        self.recurring_email_checkbox.grid(column=1, row=6, padx=10, pady=5, columnspan=2)

        self.attach_button = Button(self.frame, text="Attach File", command=self.attach_file)
        self.attach_button.grid(column=0, row=7, padx=10, pady=5)

        self.attached_files_label = Label(self.frame, text="Attached Files:")
        self.attached_files_label.grid(column=0, row=8, sticky="w", padx=10, pady=5)

        self.send_button = Button(self.frame, text="Send Email", command=self.send_email)
        self.send_button.grid(column=1, row=9, padx=10, pady=10, columnspan=2)

        self.attached_files = []

    def attach_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.attached_files.append(file_path)
            self.update_attached_files_label()

    def update_attached_files_label(self):
        attached_files_text = "\n".join([file.split("/")[-1] for file in self.attached_files])
        self.attached_files_label.config(text=f"Attached Files:\n{attached_files_text}")

    
    def send_email(self):
        is_recurring = self.is_recurring.get()
        if is_recurring:
            send_after_seconds = float(self.send_after_entry.get())
            threading.Thread(target=self.schedule_recurring_email, args=(send_after_seconds,)).start()
        else:
            threading.Thread(target=self.send_single_email).start()

    def send_single_email(self):
        sender_email = self.sender_email_entry.get()
        sender_password = self.sender_password_entry.get()
        recipient_email = self.recipient_email_entry.get()
        subject = self.subject_entry.get()
        message_body = self.message_body_text.get("1.0", "end")
        
        try:
            smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
            smtp_server.starttls()
            smtp_server.login(sender_email, sender_password)

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(message_body, "plain"))
      
            smtp_server.sendmail(sender_email, recipient_email, message.as_string())
            smtp_server.quit()
            messagebox.showinfo("Email Sent", "Email sent successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # After sending 3 recurring email break the loop
    def schedule_recurring_email(self, send_after_seconds):
        # Declare variable count and assign value 0
        count = 0
        while True:
            if(count < 3):
                count+=1
                self.send_single_email()
                time.sleep(send_after_seconds)
            else:
                break

def main():
    app = EmailSenderApp()
    app.mainloop()

if __name__ == "__main__":
    main()
