# Menu Interface (menu.nvgt)
## Classes
### menu
This class gives you an easy way to create a typical menu based on the audio_form list control item, including some nice aditional options such as navigation sounds, wrapping, and more.

#### Methods
##### add_item
Add an item to the menu.

`bool menu::add_item(string text, string id = "", int position = -1);`

###### Arguments:
* string text: the text of the item to add to the menu.
* string id = "": the ID of the item.
* int position = -1: the position to insert the new item at (-1 = end of menu).

###### Returns:
int: the  position of the new item in the menu.


##### intro
Produces the intro sequence for the menu. It is not  required to call this function if you don't want to.

`void menu::intro();`


##### monitor
Monitors the menu; handles keyboard input, the callback, sounds and more. Should be called in a loop as long as the menu is active.

`bool menu::monitor();`

###### Returns:
bool: true if the menu should keep running, or false if it has been exited or if an option has been selected.


##### reset
Resets the menu to it's default state.

`void menu::reset(bool reset_settings = false);`

###### Arguments:
* bool reset_settings = false: If this is enabled, the sounds and other such properties are cleared.



#### Properties
##### automatic_intro
If this is true, the intro function will be automatically called the first time the monitor method is invoqued, then the variable will be set to false. It can be set to true again at any time to cause the intro sequence to repeat, or the intro function can be called manually.

bool menu::automatic_intro;`


##### click_sound
The sound played when the user changes positions in the menu.

`string menu::click_sound;`


##### close_sound
The sound played when the user escapes out of the menu.

`string menu::close_sound;`


##### edge_sound
The sound which plays when the user attempts moving beyond the border of a menu while wrapping is disabled.

`string menu::edge_sound;`


##### focus_first_item
If this is false, the user will be required to press an arrow key to focus either the first or last item of the menu after the intro function has been called. Otherwise they will be focused on the first item.
This is disabled by default.

`bool menu::focus_first_item;`


##### intro_text
The text spoken when the void intro() function is called.

`string menu::intro_text;`


##### open_sound
The sound played when the void intro() function is called.

`string menu::open_sound;`


##### pack_file
Optionally set this to a pack containing sounds.

`pack menu::pack_file;`


##### select_sound
The sound played when the user chooses an option in the menu.

`string menu::select_sound;`


##### wrap
If the user moves beyond an edge of the menu, set this to true to jump them to the other edge, or false to play an edge sound and repeat the last item.
By default this is set to false.

`bool menu::wrap;`


##### wrap_delay
How much time (in ms) should the menu block when wrapping. Defaults to 10ms.

`uint menu::wrap_delay;`


##### wrap_sound
The sound played when the menu wraps (only happens when bool wrap = true).

`string menu::wrap_sound;`






