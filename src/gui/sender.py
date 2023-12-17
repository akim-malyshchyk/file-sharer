import os.path
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib  # pylint:disable=wrong-import-position

from src.logic.sender import Sender
from src.settings import PORT, SERVER_IP, SEP1


class FileChooserWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.filename = None
        self.progress = 0
        self.ip = SERVER_IP

        self.set_default_size(350, 350)
        self.set_title('File transfer')

        box = Gtk.Box.new(Gtk.Orientation.VERTICAL, 0)
        box.set_margin_start(5)
        box.set_margin_end(5)
        box.set_margin_top(5)
        self.set_child(box)

        label = Gtk.Label(label="Receiver IP address:")
        box.set_margin_top(20)

        box.append(label)

        self.entry = Gtk.Entry()
        self.entry.set_text(self.ip)
        self.entry.set_margin_start(5)
        self.entry.set_margin_end(5)
        self.entry.set_margin_top(5)
        self.entry.set_margin_bottom(35)
        box.append(self.entry)

        self.open_file_dialog = Gtk.FileChooserNative.new(title="Choose a file",
                                                          parent=self,
                                                          action=Gtk.FileChooserAction.OPEN)
        self.open_file_dialog.connect("response", self.open_file_response)

        buttons = [
            ("Choose File", self.on_file_clicked),
            ("Send", self.on_send_clicked),
        ]

        for label, action in buttons:
            button = Gtk.Button(label=label)
            button.set_valign(Gtk.Align.START)
            button.set_margin_start(5)
            button.set_margin_end(5)
            button.set_margin_bottom(5)
            button.connect("clicked", action)
            box.append(button)

        self.progressbar = Gtk.ProgressBar()
        self.progressbar.set_margin_top(10)
        self.progressbar.set_show_text(True)
        self.progressbar.set_text('No file chosen')
        box.append(self.progressbar)
        self.timeout_id = GLib.timeout_add(50, self.on_timeout, None)

    def on_timeout(self, user_data):
        new_value = user_data or 0

        if new_value is not None and new_value > 1:
            new_value = 0

        self.progressbar.set_fraction(new_value)
        return True

    def on_file_clicked(self, widget):  # pylint:disable=unused-argument
        self.open_file_dialog.show()

    def open_file_response(self, dialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_file()
            filename = file.get_path()
            self.filename = filename
            self.progressbar.set_text(os.path.basename(filename))

    def on_send_clicked(self, widget):  # pylint:disable=unused-argument
        s = Sender(host=self.entry.get_text(), port=PORT)
        s.connect((s.host, s.port))
        filesize = os.path.getsize(self.filename)

        s.send(f'{self.filename}{SEP1}{filesize}'.encode())
        for progress in s.send_file(self.filename, filesize):
            self.on_timeout(user_data=progress)

        s.close()

        self.progressbar.set_text('Done')


def on_activate(app):
    win = FileChooserWindow(app)
    win.present()


def main():
    app = Gtk.Application(application_id='com.akim.FileTransfer')
    app.connect('activate', on_activate)
    app.run(None)


if __name__ == '__main__':
    main()
