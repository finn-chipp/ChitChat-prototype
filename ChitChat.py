import kivy, socket, threading
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window

Window.size = (1150, 800)

Builder.load_string("""<main>
    BoxLayout:
        size: root.width, root.height
        orientation: "vertical"
        TextInput:
            id: chat_box
            size_hint_y: 0.8
            background_normal: ""
            background_active: ""
            background_color: 23/255, 38/255, 48/255, 1
            foreground_color: 1, 1, 1, 0.75
            cursor_color: 23/255, 38/255, 48/255, 1
            selection_color: 113/255, 128/255, 138/255, 0.5
            readonly: True
            font_size: 24
        BoxLayout:
            size_hint_y: 0.2
            padding: 2
            spacing: 2
            BoxLayout:
                size_hint_x: 0.3
                spacing: 2
                orientation: "vertical"
                TextInput:
                    id: ip_box
                    background_normal: ""
                    background_active: ""
                    background_color: 73/255, 88/255, 98/255, 1
                    foreground_color: 1, 1, 1, 0.75
                    cursor_color: 113/255, 128/255, 138/255, 1
                    selection_color: 113/255, 128/255, 138/255, 0.5
                    multiline: False
                    font_size: 24
                    text: "server ip"
                    on_text_validate: root.ids.port_box.focus = True
                TextInput:
                    id: port_box
                    background_normal: ""
                    background_active: ""
                    background_color: 73/255, 88/255, 98/255, 1
                    foreground_color: 1, 1, 1, 0.75
                    cursor_color: 113/255, 128/255, 138/255, 1
                    selection_color: 113/255, 128/255, 138/255, 0.5
                    multiline: False
                    font_size: 24
                    text: "port"
                    on_text_validate: root.ids.username_box.focus = True
                TextInput:
                    id: username_box
                    background_normal: ""
                    background_active: ""
                    background_color: 73/255, 88/255, 98/255, 1
                    foreground_color: 1, 1, 1, 0.75
                    cursor_color: 113/255, 128/255, 138/255, 1
                    selection_color: 113/255, 128/255, 138/255, 0.5
                    multiline: False
                    font_size: 24
                    text: "username"
                    on_text_validate: root.ids.ip_box.focus = True
                Button:
                    background_normal: ""
                    background_color: 60/255, 60/255, 60/255, 1
                    font_size: 24
                    text: "Connect"
                    on_release: root.connect()
            BoxLayout:
                spacing: 2
                TextInput:
                    id: message_box
                    background_normal: ""
                    background_active: ""
                    background_color: 53/255, 68/255, 78/255, 1
                    foreground_color: 1, 1, 1, 0.75
                    cursor_color: 113/255, 128/255, 138/255, 1
                    selection_color: 113/255, 128/255, 138/255, 0.5
                    size_hint_x: 0.67
                    font_size: 24
                Button:
                    size_hint_x: 0.03
                    background_normal: ""
                    background_color: 60/255, 60/255, 60/255, 1
                    font_size: 24
                    text: ">"
                    on_release: root.send()
""")

def stop():
    global server
    try:
        server.send(bytes(f"{4:<64}stop", "ascii"))
    except:
        pass

def error(self):
    self.ids.chat_box.text += "-----An error was encountered in your app. No one else will see this message.\n       This can be caused if you have attempted to send a message containing\n       non-ASCII characters, if the server is currently unoperational, or if the\n       connection information you have entered is invalid.-----\n"

def update_feed(self):
    global server
    while True:
        try:
            self.ids.chat_box.text += server.recv(int(server.recv(64).decode("ascii"))).decode("ascii")
        except:
            break

class main(Widget):
    def connect(self):
        try:
            global server, username
            stop()
            self.ids.chat_box.text = ""
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect((self.ids.ip_box.text, int(self.ids.port_box.text)))
            username = self.ids.username_box.text
            up_f = threading.Thread(target = update_feed, args = [self])
            up_f.start()
            server.send(bytes(f"{len(username):<64}{username}", "ascii"))
        except:
            error(self)
    def send(self):
        try:
            global server, username
            message = f"[{username}]\n{self.ids.message_box.text}\n"
            server.send(bytes(f"{len(message):<64}{message}", "ascii"))
            self.ids.message_box.text = ""
            self.ids.message_box.focus = True
        except:
            error(self)

class ChitChat(App):
    def build(self):
        self.icon = "icon.png"
        return main()
    def on_stop(self):
        stop()

if __name__ == "__main__":
    ChitChat().run()
