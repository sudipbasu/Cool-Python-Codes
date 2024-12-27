import wx
import random
import string
import pyperclip

def generate_password(length=12, use_uppercase=True, use_digits=True, use_symbols=True):
    """Generate a random password."""
    char_set = string.ascii_lowercase
    if use_uppercase:
        char_set += string.ascii_uppercase
    if use_digits:
        char_set += string.digits
    if use_symbols:
        char_set += string.punctuation

    return ''.join(random.choice(char_set) for _ in range(length))

class PasswordGeneratorFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Random Password Generator", size=(400, 300))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Password Length
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.StaticText(panel, label="Password Length:"), flag=wx.RIGHT, border=10)
        self.length_input = wx.TextCtrl(panel)
        self.length_input.SetValue("12")
        hbox1.Add(self.length_input, flag=wx.EXPAND)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.ALL, border=10)

        # Options
        self.uppercase_checkbox = wx.CheckBox(panel, label="Include Uppercase")
        self.uppercase_checkbox.SetValue(True)
        vbox.Add(self.uppercase_checkbox, flag=wx.LEFT, border=10)

        self.digits_checkbox = wx.CheckBox(panel, label="Include Digits")
        self.digits_checkbox.SetValue(True)
        vbox.Add(self.digits_checkbox, flag=wx.LEFT, border=10)

        self.symbols_checkbox = wx.CheckBox(panel, label="Include Symbols")
        self.symbols_checkbox.SetValue(True)
        vbox.Add(self.symbols_checkbox, flag=wx.LEFT, border=10)

        # Buttons
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        generate_button = wx.Button(panel, label="Generate Password")
        generate_button.Bind(wx.EVT_BUTTON, self.on_generate_password)
        hbox2.Add(generate_button, flag=wx.RIGHT, border=10)

        copy_button = wx.Button(panel, label="Copy to Clipboard")
        copy_button.Bind(wx.EVT_BUTTON, self.on_copy_to_clipboard)
        hbox2.Add(copy_button)

        vbox.Add(hbox2, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Password Display
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(wx.StaticText(panel, label="Generated Password:"), flag=wx.RIGHT, border=10)
        self.password_display = wx.TextCtrl(panel, style=wx.TE_READONLY)
        hbox3.Add(self.password_display, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox3, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

    def on_generate_password(self, event):
        try:
            length = int(self.length_input.GetValue())
            use_uppercase = self.uppercase_checkbox.GetValue()
            use_digits = self.digits_checkbox.GetValue()
            use_symbols = self.symbols_checkbox.GetValue()

            password = generate_password(length, use_uppercase, use_digits, use_symbols)
            self.password_display.SetValue(password)
        except ValueError:
            wx.MessageBox("Please enter a valid number for the password length.", "Error", wx.OK | wx.ICON_ERROR)

    def on_copy_to_clipboard(self, event):
        password = self.password_display.GetValue()
        if password:
            pyperclip.copy(password)
            wx.MessageBox("Password copied to clipboard!", "Success", wx.OK | wx.ICON_INFORMATION)
        else:
            wx.MessageBox("No password to copy. Generate a password first.", "Error", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App(False)
    frame = PasswordGeneratorFrame()
    frame.Show()
    app.MainLoop()
