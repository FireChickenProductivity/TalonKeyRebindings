# Installation
Download the code, unzip, and place in the talon user directory. After talon runs, it should generate the needed folders.

# Keybindings
Keybindings can be defined by creating .csv files in the Key Bindings folder. The name of the file determines the name of the context in which the keybindings are active. Only the key bindings defined in main.csv are active by default. Each binding goes on a separate line.

Example lines:

a,b

c,ctrl-s

d,on editing

f,off editing

The first line rebinds a to b. The second binds c to control s. The third binds d to activating the keybindings in the "editing.csv" file. The fourth binds f to deactivating the keybindings in the "editing.csv" file. Keys are specified the way you specify them to talon normally (see this wiki page for details: https://talon.wiki/key_action/). 

In general, keybindings are of the form: (keystroke),(keystroke or context change)
