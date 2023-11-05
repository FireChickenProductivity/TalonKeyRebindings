# Note
This is a work in progress. There may be unidentified issues.

# Installation
Download the code, unzip, and place in the talon user directory. After talon runs, it should generate the needed folders.

# Keybindings
Keybindings can be defined by creating .txt files in the "Fire Chicken Key Bindings Input" folder that this code will generate in the talon user directory. The name of the file determines the name of the context in which the keybindings are active. Only the key bindings defined in main.txt are active by default. Only letters and the underscore character (_) are allowed in the names of these files. Each binding goes on a separate line.

Example lines:

a,b

c,ctrl-s

d,on editing

f,off editing

z,mouse 0

The first line rebinds a to b. The second binds c to control s. The third binds d to activating the keybindings in the "editing.txt" file. The fourth binds f to deactivating the keybindings in the "editing.txt" file. Keys are specified the way you specify them to talon normally (see this wiki page for details: https://talon.wiki/key_action/). The fifth line binds z to the left mouse button.

In general, keybindings are of the form: (keystroke),(keystroke or context change)

# Additional Actions

In addition to keystrokes, there are other actions that can be put on the right of the comma.

(positive integer) tap (keystroke here)

will perform the keystroke every positive integer milliseconds.

(positive integer) (positive integer) tap (keystroke here)

after the key is pressed and released, this performs the keystroke the second positive integer number of times with the first positive integer milliseconds delay inbetween. 

type (put text here)

types the text with talon keybinds temporarily disabled until the typing finishes. 

# Programmer Interface
The following talon actions can be used to modify the key binds:

keybinder_add_key_bind(text, context_name = 'main')

text is text to insert into the keybinding file. context_name is the name of the keybinding file to insert into (you do not need to add the file extension).

keybinder_remove_key_bind(binding_keystroke, context_name = 'main')

binding_keystroke is the text for the keystroke that has been bound to (omit double quotes when used to surround the keystroke in the file). This is just the keystroke and not the entire keybinding line. context_name is the name of the keybinding file to remove from (you do not need to add the file extension).

keybinder_remove_context(context_name)

Removes the keybindings associated with the specified context. context_name is the name of the keybinding file to remove (you do not need to add the file extension).

keybinder_activate_context(context_name)

Activates the specified context. 

keybinder_deactivate_context(context_name)

Deactivates the specified context. 

# Known Issues
The keybindings may not load at all if any of the files are formatted incorrectly.

Having a keybinding work with modifier keys requires making a separate version of the binding for each modifier key combination.

Having a comma appear on the right hand side of a binding comma requires putting everything after the binding comma in double quotes.
