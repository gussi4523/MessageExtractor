import urwid

# Dynamic list of widgets
body = urwid.SimpleFocusListWalker([])

# We'll keep references to edit and output so handle_input can use them
edit = None
output = None

# Handle enter key - only works if edit/output exist
def handle_input(key):
    global edit, output
    if key == 'enter' and edit and output:
        text = edit.edit_text
        output.set_text(f"You entered: {text}")
        edit.edit_text = ""  # clear input

# Button actions
def add_element(button):
    body.append(urwid.Text("✨ New Element"))

def add_webhook(button):
    global edit, output
    # Create new Edit and Text widgets
    edit = urwid.Edit("(Click on it to type) URL: ")
    output = urwid.Text("")
    # Append them to the body so they show up in UI
    body.append(edit)
    body.append(output)

def delete_webhook(button):
    body.append(urwid.Text("❌ Webhook deleted"))

# Create buttons
button = urwid.Button("Add webhook", on_press=add_webhook)
button1 = urwid.Button("Delete webhook", on_press=delete_webhook)
add_button = urwid.Button("➕ Add Element", on_press=add_element)

# Insert buttons as first row
button_row = urwid.Columns([button, button1, add_button])
body.insert(0, button_row)  # put buttons at top

# Create ListBox from body
listbox = urwid.ListBox(body)

# Run main loop with unhandled_input
loop = urwid.MainLoop(listbox, unhandled_input=handle_input)
loop.run()
