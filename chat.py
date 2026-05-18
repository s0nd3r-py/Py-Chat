import threading
from socket import AF_INET, SOCK_STREAM, socket

from customtkinter import *

set_default_color_theme("theme.json")


class MainWindow(CTk):
    def __init__(self):
        super().__init__()

        self.geometry("400x500")
        self.title("Chat")

        self.username = "sdksdsdwsd"

        self.top_frame = CTkFrame(self)
        self.top_frame.pack(fill="x")

        self.name_button = CTkButton(
            self.top_frame, text="Нік", command=self.open_name_window
        )
        self.name_button.pack(side="left", padx=5, pady=5)

        self.chat_field = CTkScrollableFrame(self)
        self.chat_field.pack(fill="both", expand=True, padx=5, pady=5)

        self.bottom_frame = CTkFrame(self)
        self.bottom_frame.pack(fill="x")

        self.message_entry = CTkEntry(
            self.bottom_frame, placeholder_text="Введіть повідомлення..."
        )
        self.message_entry.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.message_entry.bind("<Return>", self.send_message_event)

        self.send_button = CTkButton(
            self.bottom_frame, text="Відправити", command=self.send_message
        )
        self.send_button.pack(side="right", padx=5, pady=5)

        self.switch_theme = CTkSwitch(
            self.top_frame, text="Темна тема", command=self.toggle_theme
        )
        self.switch_theme.pack(side="right", padx=5, pady=5)

        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(("6.tcp.eu.ngrok.io", 17142))

            start_message = self.username + " приєднався до чату"
            self.sock.send(start_message.encode("utf-8"))

            threading.Thread(target=self.receive_messages, daemon=True).start()
        except:
            self.add_message("Помилка підключення до сервера")

    def open_name_window(self):
        dialog = CTkInputDialog(text="Введіть ваш нік", title="Нік")
        name = dialog.get_input()
        if name is not None and name != "":
            self.username = name
            self.add_message(f"Ваш нік змінено на: {self.username}")

    def add_message(self, message, is_owner=False):
        if is_owner:
            align = "e"
            bg_color = "#000000"
            text_color = "white"
        else:
            align = "w"
            bg_color = "#4B4B4B"
            if get_appearance_mode() == "white":
                text_color = "white"
                bg_color = "#666666"
            else:
                text_color = "white"
                bg_color = "#777777"
        frame = CTkFrame(self.chat_field, fg_color=bg_color, corner_radius=10)
        frame.pack(anchor=align, pady=5, padx=10)
        label = CTkLabel(
            frame, text=message, text_color=text_color, wraplength=250, justify="left"
        )
        label.pack(padx=5, pady=10)
        self.chat_field.update_idletasks()
        self.chat_field._parent_canvas.yview_moveto(1.0)

    def send_message(self):
        text = self.message_entry.get()
        if not text:
            return
        msg = f"{self.username}: {text}"
        try:
            self.sock.send(msg.encode("utf-8"))
            self.add_message(msg, is_owner=True)
        except:
            self.add_message("Помилка відправки повідомлення")
        self.message_entry.delete(0, "end")

    def receive_messages(self):
        while True:
            try:
                data = self.sock.recv(1024).decode("utf-8")
                if data:
                    msg = data
                    self.add_message(msg)
            except:
                self.add_message("Помилка отримання повідомлення")
                break

    def toggle_theme(self):
        if self.switch_theme.get() == 1:
            set_appearance_mode("dark")
        else:
            set_appearance_mode("light")

    def send_message_event(self, event):
        self.send_message()


win = MainWindow()
win.mainloop()
