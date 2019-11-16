from guizero import App, Box, PushButton
app = App()

buttons_box = Box(app, width="fill", align="top")
cancel = PushButton(buttons_box, text="Cancel", align="right")
ok = PushButton(buttons_box, text="OK", align="right")

app.display()
