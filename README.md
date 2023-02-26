# Note
This is a work in progress. There may be unidentified issues.

# Installation
Download the code, unzip, and place in the talon user directory. After talon runs, it should generate the needed folders.

# Keybindings
Keybindings can be defined by creating .txt files in the Key Bindings folder. The name of the file determines the name of the context in which the keybindings are active. Only the key bindings defined in main.txt are active by default. Only letters and the underscore character (_) are allowed in the names of these files. Each binding goes on a separate line.

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

# Known Issues
The keybindings may not load at all if any of the files are formatted incorrectly.

Having a keybinding work with modifier keys requires making a separate version of the binding for each modifier key combination.

Having a comma appear on the right hand side of a binding comma requires putting everything after the binding comma in double quotes.
