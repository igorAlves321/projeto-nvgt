# User Interface
This section contains all functions that involve directly interacting with the user, be that by showing a window, checking the state of a key, or placing data onto the users clipboard. These handle generic input such as from the keyboard, and also generic output such as an alert box.

## Window management notes:
* You can only have one NVGT window showing at a time.
* without an nvgt window, there is no way to capture keyboard and mouse input from the user.
* It is strongly advised to always put `wait(5);` in your main loops. This prevents your game from hogging the CPU, and also prevents weird bugs with the game window sometimes freezing etc.


## Enums
### key_code
This is a complete list of possible keycodes in NVGT, as well as a short description of what they are. These are registered in the key_code enum, meaning you can use this type to pass any value listed here around though it is also safe to use unsigned integers.

#### Letter keys
* KEY_UNKNOWN: unknown.
* KEY_A: the A key.
* KEY_B: the B key.
* KEY_C: the C key.
* KEY_D: the D key.
* KEY_E: the E key.
* KEY_F: the F key.
* KEY_G: the G key.
* KEY_H: the H key.
* KEY_I: the I key.
* KEY_J: the J key.
* KEY_K: the K key.
* KEY_L: the L key.
* KEY_M: the M key.
* KEY_N: the N key.
* KEY_O: the O key.
* KEY_P: the P key.
* KEY_Q: the Q key.
* KEY_R: the R key.
* KEY_S: the S key.
* KEY_T: the T key.
* KEY_U: the U key.
* KEY_V: the V key.
* KEY_W: the W key.
* KEY_X: the X key.
* KEY_Y: the Y key.
* KEY_Z: the Z key.

#### Number keys
* KEY_1: the 1 key.
* KEY_2: the 2 key.
* KEY_3: the 3 key.
* KEY_4: the 4 key.
* KEY_5: the 5 key.
* KEY_6: the 6 key.
* KEY_7: the 7 key.
* KEY_8: the 8 key.
* KEY_9: the 9 key.
* KEY_0: the 0 key.

#### Special keys
* KEY_RETURN: the Return (or enter) key.
* KEY_ESCAPE: the Escape key.
* KEY_BACK: the Backspace key.
* KEY_TAB: the Tab key.
* KEY_SPACE: the Space key.
* KEY_MINUS: the Minus (dash) key.
* KEY_EQUALS: the Equals key.
* KEY_LEFTBRACKET: the Left Bracket key.
* KEY_RIGHTBRACKET: the Right Bracket key.
* KEY_BACKSLASH: the Backslash key.
* KEY_NONUSHASH: the Non-US Hash key.
* KEY_SEMICOLON: the Semicolon key.
* KEY_APOSTROPHE: the Apostrophe key.
* KEY_GRAVE: the Grave key.
* KEY_COMMA: the Comma key.
* KEY_PERIOD: the Period key.
* KEY_SLASH: the Slash key.
* KEY_CAPSLOCK: the Caps Lock key.

#### Function keys
* KEY_F1: the F1 key.
* KEY_F2: the F2 key.
* KEY_F3: the F3 key.
* KEY_F4: the F4 key.
* KEY_F5: the F5 key.
* KEY_F6: the F6 key.
* KEY_F7: the F7 key.
* KEY_F8: the F8 key.
* KEY_F9: the F9 key.
* KEY_F10: the F10 key.
* KEY_F11: the F11 key.
* KEY_F12: the F12 key.
* KEY_F13: the F13 key.
* KEY_F14: the F14 key.
* KEY_F15: the F15 key.
* KEY_F16: the F16 key.
* KEY_F17: the F17 key.
* KEY_F18: the F18 key.
* KEY_F19: the F19 key.
* KEY_F20: the F20 key.
* KEY_F21: the F21 key.
* KEY_F22: the F22 key.
* KEY_F23: the F23 key.
* KEY_F24: the F24 key.

#### Arrow keys
* KEY_RIGHT: the Right Arrow key.
* KEY_LEFT: the Left Arrow key.
* KEY_DOWN: the Down Arrow key.
* KEY_UP: the Up Arrow key.

#### Numpad keys
* KEY_NUMLOCKCLEAR: the Num Lock key.
* KEY_NUMPAD_DIVIDE: the numpad divide key.
* KEY_NUMPAD_MULTIPLY: the numpad multiply key.
* KEY_NUMPAD_MINUS: the numpad minus key.
* KEY_NUMPAD_PLUS: the numpad plus key.
* KEY_NUMPAD_ENTER: the numpad enter key.
* KEY_NUMPAD_1: the Numpad 1 key.
* KEY_NUMPAD_2: the Numpad 2 key.
* KEY_NUMPAD_3: the Numpad 3 key.
* KEY_NUMPAD_4: the Numpad 4 key.
* KEY_NUMPAD_5: the Numpad 5 key.
* KEY_NUMPAD_6: the Numpad 6 key.
* KEY_NUMPAD_7: the Numpad 7 key.
* KEY_NUMPAD_8: the Numpad 8 key.
* KEY_NUMPAD_9: the Numpad 9 key.
* KEY_NUMPAD_0: the Numpad 0 key.
* KEY_NUMPAD_PERIOD: the Numpad Period key.

#### Modifier keys
* KEY_LCTRL: the Left Control key.
* KEY_LSHIFT: the Left Shift key.
* KEY_LALT: the Left Alt key.
* KEY_LGUI: the left windows/command/super key (depending on platform).
* KEY_RCTRL: the Right Control key.
* KEY_RSHIFT: the Right Shift key.
* KEY_RALT: the Right Alt key.
* KEY_RGUI: the right windows/command/super key (depending on platform).

#### Miscellaneous keys
* KEY_MODE: the Mode key.
* KEY_APPLICATION: the Application key.
* KEY_POWER: the Power key.
* KEY_PRINTSCREEN: the Print Screen key.
* KEY_SCROLLLOCK: the Scroll Lock key.
* KEY_PAUSE: the Pause key.
* KEY_INSERT: the Insert key.
* KEY_HOME: the Home key.
* KEY_PAGEUP: the Page Up key.
* KEY_DELETE: the Delete key.
* KEY_END: the End key.
* KEY_PAGEDOWN: the Page Down key.

#### Media keys
* KEY_MUTE: the Mute key.
* KEY_VOLUMEUP: the Volume Up key.
* KEY_VOLUMEDOWN: the Volume Down key.
* KEY_MEDIA_NEXT_TRACK: the next track key.
* KEY_MEDIA_PREVIOUS_TRACK: the previous track key.
* KEY_MEDIA_STOP: the stop media key.
* KEY_MEDIA_PLAY: the play media key.
* KEY_MUTE: the mute key.
* KEY_MEDIA_SELECT: the media select key.

#### Browser and Application keys
* KEY_AC_SEARCH: the AC Search key.
* KEY_AC_HOME: the AC Home key.
* KEY_AC_BACK: the AC Back key.
* KEY_AC_FORWARD: the AC Forward key.
* KEY_AC_STOP: the AC Stop key.
* KEY_AC_REFRESH: the AC Refresh key.
* KEY_AC_BOOKMARKS: the AC Bookmarks key.

#### Additional keys
* KEY_MEDIA_EJECT: the eject key.
* KEY_SLEEP: the sleep key.
* KEY_MEDIA_REWIND: the media rewind key.
* KEY_MEDIA_FAST_FORWARD: the media fast forward key.
* KEY_SOFTLEFT: the Soft Left key.
* KEY_SOFTRIGHT: the Soft Right key.
* KEY_CALL: the Call key.
* KEY_ENDCALL: the End Call key.
* KEY_AC_SEARCH: the AC Search key.
* KEY_AC_HOME: the AC Home key.
* KEY_AC_BACK: the AC Back key.
* KEY_AC_FORWARD: the AC Forward key.
* KEY_AC_STOP: the AC Stop key.
* KEY_AC_REFRESH: the AC Refresh key.
* KEY_AC_BOOKMARKS: the AC Bookmarks key.


### key_modifier

This is a complete list of supported key modifiers and their descriptions. These are registered in the key_modifier enum, so you can use that type to pass any value listed here around.

* KEYMOD_NONE: no modifier.

* KEYMOD_LSHIFT: left shift key.

* KEYMOD_RSHIFT: right shift key.

* KEYMOD_LCTRL: left control key.

* KEYMOD_RCTRL: right control key.

* KEYMOD_LALT: left alt key.

* KEYMOD_RALT: right alt key.

* KEYMOD_LGUI: left windows/command/super key (depending on platform).

* KEYMOD_RGUI: right windows/command/super key (depends on platform).

* KEYMOD_NUM: numlock key.

* KEYMOD_CAPS: capslock key.

* KEYMOD_MODE: input switch mode (only on certain keyboards).

* KEYMOD_SCROLL: scroll lock key.

* KEYMOD_CTRL: either control key.

* KEYMOD_SHIFT: either shift key.

* KEYMOD_ALT: either alt key.

* KEYMOD_GUI: either windows/command/super key.

#### Example:

```NVGT
void main() {
	show_window("Example");
	wait(50); // Give the screen readers enough time to speak the window title before speaking.
	screen_reader_output("Press alt+f4 to close this window.", true);
	while (true) {
		wait(5);
		if (keyboard_modifiers & KEYMOD_ALT > 0 && key_pressed(KEY_F4))
			exit();
	}
}
```



### message_box_flags
This is an enumeration of possible flags to be passed to the message_box(), alert(), question(), and similar functions.

* MESSAGE_BOX_ERROR: the message box should act like an error dialog.
* MESSAGE_BOX_WARNING: the message box should act like a warning dialog.
* MESSAGE_BOX_INFORMATION: the message box should act like an informative dialog.
* MESSAGE_BOX_BUTTONS_LEFT_TO_RIGHT: arrange the buttons in the dialog from left to right.
* MESSAGE_BOX_BUTTONS_RIGHT_TO_LEFT: arrange the buttons from right-to-left in the message box.


### touch_device_type
These are the possible types of touch input devices.

* TOUCH_DEVICE_INVALID = -1: Returned if an invalid ID is passed to get_touch_device_type.
* TOUCH_DEVICE_DIRECT: A touch screen with window-relative coordinates.
* TOUCH_DEVICE_INDIRECT_ABSOLUTE: A trackpad with absolute device coordinates.
* TOUCH_DEVICE_INDIRECT_RELATIVE: A trackpad with screen cursor-relative coordinates.



## Functions
### alert

Display a message box with an OK button to the user.

int alert(const string&in title, const string&in text, bool can_cancel = false, uint flags = 0);

#### Arguments:

* const string&in title: the title of the dialog.

* const string&in text: the text of the dialog.

* bool can_cancel = false: determines if a cancel button is present.

* uint flags = 0: a combination of flags (see message_box_flags for more information).

#### Returns:

int: the number of the button that was pressed, either OK or cancel.

#### Example:

```NVGT
void main() {
	alert("Hello", "I am a standard alert");
	alert("Hi", "And I'm a cancelable one", true);
}
```



### android_request_permission
Request a permission from the Android operating system either synchronously or asynchronously.

`bool android_request_permission(string permission, android_permission_request_callback@ callback = null, string callback_data = "");`

#### Arguments:
* string permission: A permission identifier such as android.permission.RECORD_AUDIO.
* android_permission_request_callback@ callback = null: An optional function that should be called when the user responds to the permission request (see remarks).
* string callback_data = "": An arbitrary string that is passed to the given callback function.

#### Returns:
bool: true if the request succeeded (see remarks), false otherwise or if this function was not called on Android.

#### Remarks:
The callback signature this function expects is registered as :
`funcdef void android_permission_request_callback(string permission, bool granted, string user_data);`

This function behaves very differently depending on whether you've provided a callback or not. If you do not, this function blocks the thread that called it until the user responds to the permission request, in which case it returns true or false depending on whether the user has actually granted the permission. On the other hand if you do provide a callback, the instant return value of this function only indicates whether the request has been made rather than whether the permission has been granted, as that information will be provided later in the given callback.

Beware that the callback you provide might get invoked on any thread, thus the provision of a more simple, blocking alternative. If you do provide a callback, you are responsible for handling any data races that may result.


### android_show_toast
Shows an Android toast notification, small popups that are unique to that operating system.

`bool android_show_toast(const string&in message, int duration, int gravity = -1, int x_offset = 0, int y_offset = 0);`

#### Arguments:
* const string&in message: The message to display.
* int duration: 0 for short or 1 for long, all other values are undefined.
* int gravity = -1: One of [the values on this page](https://developer.android.com/reference/android/view/Gravity) or -1 for no preference.
* int x_offset = 0, int y_offset = 0: Only used if gravity is set, see Android developer documentation.

#### Returns:
bool: true if the toast was shown, false otherwise or if called on a platform other than Android.

#### Remarks:
[Learn more about android toasts notifications here.](https://developer.android.com/guide/topics/ui/notifiers/toasts)


### clipboard_get_text

Returns the text currently on the user's clipboard.

string clipboard_get_text();

#### Returns:

string: The text on the user's clipboard, as UTF_8.

#### Example:

```NVGT
void main() {
	string text = clipboard_get_text();
	if (text == "")
		alert("Info", "Your clipboard is empty");
	else
		if (text.length() > 1024)
			alert("Info", "Your clipboard contains a long string. It is " + text.length() + " characters");
		else
			alert("Info", "Your clipboard contains " + text);
}
```



### clipboard_set_raw_text

Sets the text on the user's clipboard, using the system encoding.

bool clipboard_set_raw_text(const string&in text);

#### Arguments:

* const string&in text: the text to copy, assumed to be in the system's encoding.

#### Returns:

Bool: true on success, false on failure.

#### Remarks:

To copy UTF-8 text, see clipboard_set_text().

#### Example:

```NVGT
void main() {
	string text = input_box("Text", "Enter the text to copy.");
	clipboard_set_raw_text(text);
	if (text == "")
		alert("Info", "Your clipboard has been cleared.");
	else
		alert("Info", "Text copied");
}
```



### clipboard_set_text

Sets the text on the user's clipboard.

bool clipboard_set_text(const string&in text);

#### Arguments:

* const string&in text: the text to copy, assumed to be UTF_8.

#### Returns:

Bool: true on success, false on failure.

#### Remarks:

To copy text in the system encoding, see clipboard_set_raw_text().

#### Example:

```NVGT
void main() {
	string text = input_box("Text", "Enter the text to copy.");
	clipboard_set_text(text);
	if (text == "")
		alert("Info", "Your clipboard has been cleared.");
	else
		alert("Info", "Text copied");
}
```



### destroy_window

Destroys the currently shown window, if it exists.

bool destroy_window();

#### Returns:

bool: true if the window was successfully destroyed, false otherwise.

#### Example:

```NVGT
void main() {
	alert("Info", "Pressing SPACE will destroy the window");
	show_window("Example");
	while (true) {
		wait(5); // Don't hog all the CPU time.
		if (key_pressed(KEY_SPACE)) {
			destroy_window();
			wait(2000); // Simulate doing things while the window isn't active.
			exit();
		}
	}
}
```



### exit

Completely shut down your application, returning a particular exit code to your operating system in the process.

void exit(int exit_code = 0);

#### Arguments:

* int exit_code = 0: the exit code to return to your operating system.

#### Example:

```NVGT
void main() {
	show_window("Example");
	screen_reader_output("Press escape to exit.", true);
	while (true) {
		wait(5);
		if (key_pressed(KEY_ESCAPE)) {
			screen_reader_output("Goodbye.", true);
			wait(500);
			exit();
		}
	}
}
```



### focus_window

Attempt to bring your NVGT window to the foreground.

bool focus_window();

#### Returns:

bool: true if the window was successfully focused, false otherwise.

#### Example:

```NVGT
void main() {
	timer focuser;
	show_window("Focus every 5 seconds example");
	while (true) {
		wait(5);
		if (key_pressed(KEY_ESCAPE)) exit();
		if (focuser.has_elapsed(5000)) {
			focuser.restart();
			focus_window();
		}
	}
}
```



### get_characters

Determine any printable characters typed into the games window since this function's lass call.

string get_characters();

#### Returns:

string: Any characters typed since this function was last called, or an empty string if none are available.

#### Remarks:

This is the function one would use if they wished to integrate a virtual text field of any sort into their games or applications.

Unlike functions such as key_down or keys_pressed, this function focuses specifically on textual content which has been input to the application. A character returned from this function, for example, could be anything from the space bar to an emoticon inserted using the windows emoji picker.

A typical use case would involve calling this function once per iteration of your game loop and storing any new characters that are typed into a buffer that composes a chat message or a username or anything else requiring virtual text input.

#### Example:

```NVGT
void main() {
	string buffer;
	show_window("get_characters example");
	while (!key_pressed(KEY_ESCAPE)) {
		wait(5);
		string char = get_characters();
		if (!char.empty()) {
			buffer += char;
			screen_reader_speak(char, true); // You need to process this further for screen readers, such as replacing . with period and other punctuation.
		}
		if (key_pressed(KEY_RETURN)) {
			screen_reader_speak("You typed " + (!buffer.empty()? buffer : "nothing"), true);
			buffer = "";
		}
	}
}
```



### get_touch_device_name
Determine the name of a touch device given it's ID.

`string get_touch_device_name(uint64 device_id);`

#### Returns:
string : The name of the given device, or an empty string on failure.


### get_touch_device_type
Determine the type of a touch device given it's ID.

`touch_device_type get_touch_device_name(uint64 device_id);`

#### Returns:
touch_device_type: The type of the given device, or TOUCH_DEVICE_TYPE_INVALID if a bad ID is given.


### get_touch_devices

Enumerate all available touch input devices on the system.

uint64[]@ get_touch_devices();

#### Returns:

uint64[]@: An array of touch device IDs, may be empty of no touch devices are available.

#### Remarks:

You can pass any of the IDs returned from this function to the get_touch_device_type, get_touch_device_name, or query_touch_device functions.

Note that on some platforms, certain touch devices might not become available until they first receive input. For example this is true with the Android touch screen.

#### Example:

```NVGT
void main() {
	uint64[]@ devices = get_touch_devices();
	if (devices.length() < 1) {
		alert("no devices", "There are no detectable touch devices on your system.");
		exit();
	}
	for (uint i = 0; i < devices.length(); i++)
		alert("device " + devices[i], get_touch_device_name(devices[i]));
}
```



### get_window_os_handle

Returns the native handle used by the operating system to manage NVGT's window.

uint64 get_window_os_handle();

#### Returns:

uint64: An HWND / NSWindow\* / similar handle that the operating system uses to manage the window.

#### Remarks:

This function is only useful for someone trying to do something advanced, usually involving passing the identifier for the game window to a system API function or something similar. If you don't understand what this function does, you should probably avoid it for the present.

#### Example:

```NVGT
void main() {
	// Lets set the window title using the windows API, typically you'd use show_window a second time for this.
	show_window("hello");
	uint64 handle = get_window_os_handle();
	library lib;
	lib.load("user32");
	lib.call("int SetWindowTextA(uint64, ptr)", handle, "example window");
	wait(500); // Let the user observe the change before exiting.
}
```



### get_window_text

Returns the title of your window.

string get_window_text();

#### Returns:

string: the title of your window.

#### Example:

```NVGT
void main() {
	string[] possible_titles = {"Hello world", "NVGT test", "My game", "Example", "Window title example"};
	show_window(possible_titles[random(0, possible_titles.length() - 1)]);
	while (true) {
		wait(5);
		if (key_pressed(KEY_ESCAPE)) exit();
		if (key_pressed(KEY_SPACE)) {
			screen_reader_output("The window title currently is: " + get_window_text(), true);
			show_window(possible_titles[random(0, possible_titles.length() - 1)]); // Randomize the title again.
		}
	}
}
```



### idle_ticks

Obtain the time passed in milliseconds since a user has pressed a key or used the mouse.

uint64 idle_ticks();

#### returns

uint64: the number of milliseconds since a user has last interacted with the machine.

#### remarks

This function can serve as a useful utility to verify whether a user has been away from the keyboard.

It is currently integrated for windows and MacOS. On linux, it will always return 0 until further notice.

#### Example:

```NVGT
void main() {
	int64 t;
	show_window("Idle test");
	wait(50);
	screen_reader_speak("Press space to check the idle time and escape to exit.", true);
	while (!key_pressed(KEY_ESCAPE)) {
		wait(5);
		if (key_pressed(KEY_SPACE))
			screen_reader_speak("You have been idle for %0 milliseconds".format(t), true);
		t = idle_ticks();
	}
}
```



### info_box

Displays a dialog to the user consisting of a read-only text field and a close button.

bool info_box(const string&in title, const string&in label, const string&in text, uint64 flags = 0);

#### Arguments:

* const string&in title: the title of the dialog.

* const string&in label: the text to display above the text field.

* const string&in text: the text to display in the text field.

* uint64 flags = 0: a combination of flags, see message_box_flags for more information.

#### Returns:

bool: true if the user pressed the close button, false otherwise.

#### Example:

```NVGT
void main() {
	info_box("Test", "Information", "this is a\r\nlong string\r\nthat can be split\r\nacross lines");
}
```



### input_box

Displays a dialog to the user consisting of an input field, an OK button and a cancel button.

string input_box(const string&in title, const string&in text, const string&in default_text = "", uint64 flags = 0);

#### Arguments:

* const string&in title: the title of the input box.

* const string&in text: the text to display above the text field.

* const string&in default_text = "": the contents to populate the text box with by default.

* uint64 flags = 0: a combination of flags, see message_box_flags for more information.

#### Returns:

string: the text that the user typed.

#### Example:

```NVGT
void main() {
	string name = input_box("Name", "What is your name?", "John Doe");
	if (name.is_empty()) {
		alert("Error", "You didn't type a name, unidentified person!");
		exit();
	}
	alert("Hi", name + "!");
}
```



### install_keyhook

Attempts to install NVGT's JAWS keyhook.

bool install_keyhook(bool allow_reinstall = true);

#### Arguments:

* bool allow_reinstall = true: whether or not this function will reinstall the hook on subsequent calls.

#### Returns:

bool: true if the keyhook was successfully installed, false otherwise.

#### Remarks:

This keyhook allows NVGT games to properly capture keyboard input while the JAWS for Windows screen reader is running.

Note that installing it when JAWS is not running may yield unintended consequences, such as functionality of other screen readers being slightly limited while in your game window.

#### Example:

```NVGT
void main() {
	bool success = install_keyhook();
	if (success) {
		alert("Info", "The keyhook was successfully installed!");
		uninstall_keyhook();
	}
	else
		alert("Info", "The keyhook was not successfully installed.");
}
```



### is_console_available

Determine if your application has access to a console window or not.

bool is_console_available();

#### Returns:

bool: true if your application has access to a console window, false otherwise.

#### Remarks:

If this function returns false, it is very likely that any output passed to the print or println functions or the cout/cerr datastreams will be silently dropped.

#### Example:

```NVGT
void main() {
	if (is_console_available()) println("hello from the console!");
	else alert("console unavailable", "hello from the user interface!");
}
```



### is_window_active

Determines if your game's window is active (i.e. has the keyboard focus).

bool is_window_active();

#### Returns:

bool: true if your game window has the keyboard focus, false if not.

#### Example:

```NVGT
void main() {
	show_window("Test");
	wait(1000); // Give the user time to alt+tab away if they so choose.
	bool active = is_window_active();
	if (active)
		alert("Info", "Your game window is active.");
	else
		alert("Info", "Your game window is not active.");
}
```



### is_window_hidden

Determines if your game's window is hidden or not.

bool is_window_hidden();

#### Returns:

bool: true if your game window is hidden, false if it's shown.

#### Example:

```NVGT
void main() {
	show_window("Test");
	bool hide = random_bool();
	if (hide) hide_window();
	alert("The window is", is_window_hidden() ? "hidden" : "shown");
}
```



### key_down

Determine if a particular key is held down.

bool key_down(uint key);

#### Arguments:

* uint key: the key to check.

#### Returns:

bool: true if the key is down at all, false otherwise.

#### Remarks:

For a complete list of keys that can be passed to this function, see input constants.

#### Example:

```NVGT
void main() {
	show_window("Example");
	while (true) {
		wait(5);
		if (key_down(KEY_SPACE))
			screen_reader_output("space", true);
		if (key_pressed(KEY_ESCAPE))
			exit();
	}
}
```



### key_pressed

Determine if a particular key is pressed.

bool key_pressed(uint key);

#### Arguments:

* uint key: the key to check.

#### Returns:

bool: true if the key was just pressed, false otherwise.

#### Remarks:

For a complete list of keys that can be passed to this function, see input constants.

#### Example:

```NVGT
void main() {
	show_window("Example");
	while (true) {
		wait(5);
		if (key_pressed(KEY_SPACE))
			screen_reader_output("You just pressed space!", true);
		if (key_pressed(KEY_ESCAPE))
			exit();
	}
}
```



### key_released

Determine if a particular key was just released.

bool key_released(uint key);

#### Arguments:

* uint key: the key to check.

#### Returns:

bool: true if the key was just released, false otherwise.

#### Remarks:

For a complete list of keys that can be passed to this function, see input constants.

#### Example:

```NVGT
void main() {
	show_window("Example");
	while (true) {
		wait(5);
		if (key_released(KEY_SPACE))
			screen_reader_output("you just released the space key", true);
		if (key_pressed(KEY_ESCAPE))
			exit();
	}
}
```



### key_repeating

Determine if a particular key is repeating (i.e. it's being held, but wasn't just pressed).

bool key_repeating(uint key);

#### Arguments:

* uint key: the key to check.

#### Returns:

bool: true if the key is repeating, false otherwise.

#### Remarks:

For a complete list of keys that can be passed to this function, see input constants.

#### Example:

```NVGT
void main() {
	show_window("Example");
	while (true) {
		wait(5);
		if (key_repeating(KEY_SPACE))
			screen_reader_output("space", true);
		if (key_pressed(KEY_ESCAPE))
			exit();
	}
}
```



### key_up

Determine if a particular key is up.

bool key_up(uint key);

#### Arguments:

* uint key: the key to check.

#### Returns:

bool: true if the key is up, false otherwise.

#### Remarks:

For a complete list of keys that can be passed to this function, see input constants.

#### Example:

```NVGT
void main() {
	int last_spoken = ticks(); // Speak periodically to avoid overwhelming the user (or their screen reader).
	show_window("Example");
	while (true) {
		wait(5);
		if (key_up(KEY_SPACE) && (ticks() - last_spoken) >= 500) {
			last_spoken = ticks();
			screen_reader_output("space is up", true);
		}
		if (key_pressed(KEY_ESCAPE))
			exit();
	}
}
```



### keys_down
Returns a handle to an array of keys that are held down.

`uint[]@ keys_down();`

#### Returns:
uint[]@: a handle to an array containing keys that are held down.

#### Remarks:
For a complete list of keys that can be returned by this function, see input constants.


### keys_pressed
Returns a handle to an array of keys that were just pressed.

`uint[]@ keys_pressed();`

#### Returns:
uint[]@: a handle to an array containing keycodes that were just pressed.

#### Remarks:
For a complete list of keys that can be returned by this function, see input constants.


### keys_released
Returns a handle to an array of keys that were just released.

`uint[]@ keys_released();`

#### Returns:
uint[]@: a handle to an array containing keycodes that were just released.

#### Remarks:
For a complete list of keys that can be returned by this function, see input constants.


### message_box

Displays a customizable message box.

int message_box(const string&in title, const string&in text, string[]@ buttons, uint flags = 0);

#### Arguments:

* const string&in title: the title of the message box.

* const string&in text: the text of the message box.

* string[]@ buttons: a string array of button names, see remarks for more info.

* uint flags = 0: a combination of flags (see message_box_flags for more information).

#### Returns:

int: the number of the button that was pressed, according to its position in the buttons array.

#### Remarks:

Notes on button syntax:

* A grave character (`) prepending button text is default enter key.

* A tilde character (~) before text means default cancel.

#### Example:

```NVGT
void main() {
	message_box("Hello there", "I am a message box with two buttons", {"`OK", "~Cancel"});
}
```



### open_file_dialog

Displays a dialog from which a user may select a file to open.

string open_file_dialog(string filters = "", string default_location = "")

#### Arguments:

* string filters = "": A list of file extension filters (see remarks).

* string default_location = "": The absolute initial directory to select files from (empty for OS default).

#### Returns:

string: The path to a file or an empty string on failure/cancelation.

#### Remarks:

The file extension filters are specified in the format description:extension|description:extension|description:extension1;extension2;extension3... You can also use the filter \* as an all files filter. for example: audio files:mp3;wav;ogg|text files:txt;rtf;md|all files:* would produce 3 items in the file type combo box, those being audio files, text files and all files.

On some platforms it might be possible for the user to select a file that does not yet exist, so you should check for that condition yourself after the user selects a file just to be safe if that is important to you.

This function is blocking, though we plan to add a version of the API in the future that uses a callback function or an event you can wait on if you wish to use this dialog asynchronously.

You should only call this function on your application's main thread, which is what happens by default unless you use any of NVGT's threading facilities.

#### Example:

```NVGT
void main() {
	string location = open_file_dialog("NVGT scripts:nvgt", cwdir());
	if (location.empty()) return;
	alert("example", "you selected " + location);
}
```



### query_touch_device

Check what fingers are in contact with a touch device and where they are on the screen, if any.

touch_finger[]@ query_touch_device(uint64 device_id = 0);

#### Arguments:

* uint64 device_id = 0: The device to query, 0 for the last device that received input.

#### Returns:

touch_finger[]@: An array of structures containing touch coordinates and pressure (see remarks).

#### Remarks:

Each structure in the returned array represents a finger, thus the length of the array indicates how many fingers are touching the device.

Touch_finger objects contain only 4 properties. Int64 id is a unique identifier of the finger that will remain the same as long as the finger touches the devices, float x and float y contain the coordinates of the finger on the device, and the float pressure property indicates how much force or pressure the finger is being applied to the device with.

Usage of this structure other than to receive touch input is not endorsed by the NVGT developers and may lead to unexpected results, most notably creating a touch_finger instance manually will likely set it's properties to random uninitialized memory on the stack. You have been warned.

#### Example:

```NVGT
void main() {
	// Report the number of fingers touching the device.
	show_window("touch example");
	tts_voice tts;
	int prev_finger_count = 0;
	tts.speak("ready", true);
	while (!key_pressed(KEY_ESCAPE) and !key_pressed(KEY_AC_BACK)) {
		wait(5);
		touch_finger[]@ fingers = query_touch_device(); // This will query the last device that was touched.
		if (fingers.length() != prev_finger_count) {
			tts.speak(fingers.length() + (fingers.length() != 1? " fingers" : " finger"), true);
			prev_finger_count = fingers.length();
		}
	}
}
```



### question

Display a yes/no dialog box to the user.

int question(const string&in title, const string&in text, bool can_cancel = false, uint flags = 0);

#### Arguments:

* const string&in title: the title of the dialog.

* const string&in text: the text of the dialog.

* bool can_cancel = false: determines if a cancel button is present alongside the other buttons.

* uint flags = 0: a combination of flags (see message_box_flags for more information).

#### Returns:

int: the number of the button that was pressed (1 for yes, 2 for no).

#### Example:

```NVGT
void main() {
	int res = question("Hello there", "Do you like pizza?");
	alert("Info", "You clicked " + (res == 1 ? "yes" : "no"));
}
```



### refresh_window
Updates the game window, pulling it for any new events and responding to messages from the operating system.

`void refresh_window();`

#### Remarks:
You do not need to call this function yourself so long as you use the recommended wait() function in your game's loops, as wait() implicitly calls this function. We provide refresh_window() standalone unless you want to use your own / a different sleeping mechanism such as nanosleep, in which case you do need to manually pull the window using this function.

For UI windows to function on the vast mejority of operating systems, they must maintain a constant stream of communication between the operating system and the program that created them. If a window stops receiving and handling such communications for even a few seconds, it will first become laggy before the operating system decides that the window has gone dead and begins reporting that the application is in a not responding or busy state.

To solve this problem in NVGT applications, refresh_window() is provided to do all of this message handling for you in one repeated function call. This function will pull the operating system for any new messages or events and process them, updating the states of functions like key_pressed, get_characters etc. If it is not repeatedly called in some way, your entire application will be disfunctional.


### save_file_dialog

Displays a dialog from which a user may select a location to save a file.

string save_file_dialog(string filters = "", string default_location = "")

#### Arguments:

* string filters = "": A list of file extension filters (see remarks).

* string default_location = "": The absolute initial directory to select from (empty for OS default).

#### Returns:

string: The path to save to or an empty string on failure/cancelation.

#### Remarks:

The file extension filters are specified in the format description:extension|description:extension|description:extension1;extension2;extension3... You can also use the filter \* as an all files filter. for example: audio files:mp3;wav;ogg|text files:txt;rtf;md|all files:* would produce 3 items in the file type combo box, those being audio files, text files and all files.

Keep in mind that the user may select a file that already exists if they wish to overwrite it.

This function is blocking, though we plan to add a version of the API in the future that uses a callback function or an event you can wait on if you wish to use this dialog asynchronously.

You should only call this function on your application's main thread, which is what happens by default unless you use any of NVGT's threading facilities.

#### Example:

```NVGT
void main() {
	string location = save_file_dialog("text files (*.txt):txt|all files:*");
	if (location.empty()) return;
	alert("example", "you selected " + location);
}
```



### select_folder_dialog

Displays a dialog from which a user may select a folder.

string select_folder_dialog(string default_location = "")

#### Arguments:

* string default_location = "": The absolute initial directory to select from (empty for OS default).

#### Returns:

string: The path to a folder or an empty string on failure/cancelation.

#### Remarks:

Be aware that on some platforms, the user might be able to select a directory that does not yet exist.

This function is blocking, though we plan to add a version of the API in the future that uses a callback function or an event you can wait on if you wish to use this dialog asynchronously.

You should only call this function on your application's main thread, which is what happens by default unless you use any of NVGT's threading facilities.

#### Example:

```NVGT
void main() {
	string location = select_folder_dialog();
	if (location.empty()) return;
	alert("example", "you selected " + location);
}
```



### set_application_name
This function lets you set the name of your application. This is a name that's sent to your operating system in certain instances, for example in volume mixer dialogs or when an app goes not responding. It does not effect the window title or anything similar.

`bool set_application_name(const string&in application_name);`

#### Arguments:
* const string&in application_name: the name to set for your application.

#### Returns:
bool: true if the name was successfully set, false otherwise.


### show_window

Shows a window with the specified title.

bool show_window(const string&in title);

#### Arguments:

* const string&in title: the title of the window.

#### Returns:

bool: true if window creation was successful, false otherwise.

#### Remarks:

This window doesn't do any event processing by default. As such, you have to create a loop in order to keep it alive.

#### Example:

```NVGT
void main() {
	alert("Info", "Press escape to close the window.");
	show_window("Example");
	while (true) {
		wait(5); // Don't hog all the CPU.
		if (key_pressed(KEY_ESCAPE))
			exit();
	}
}
```



### total_keys_down

Returns the total number of keys that are currently held down.

int total_keys_down();

#### Returns:

int: the number of keys currently held down.

#### Example:

```NVGT
void main() {
	int check_time = 1000, orig_ticks = ticks();
	show_window("Example");
	while (true) {
		wait(5);
		if ((ticks() - orig_ticks) >= check_time) {
			orig_ticks = ticks();
			int key_count  = total_keys_down();
			screen_reader_output(key_count + " " + (key_count == 1 ? "key is" : "keys are") + " currently held down.", true);
		}
		if (key_pressed(KEY_ESCAPE))
			exit();
	}
}
```



### uninstall_keyhook

Uninstall's NVGT's JAWS keyhook.

void uninstall_keyhook();

#### Remarks:

This keyhook allows NVGT games to properly capture keyboard input while the JAWS for Windows screen reader is running.

#### Example:

```NVGT
void main() {
	install_keyhook();
	alert("Info", "Keyhook installed. Uninstalling...");
	uninstall_keyhook();
	alert("Done", "Keyhook uninstalled.");
}
```



### urlopen

Opens the specified URL in the appropriate application, for example an https:// link in your web browser, or a tt://link in TeamTalk.

bool urlopen(const string&in url);

#### Arguments:

* const string&in url: The URL to open.

#### Returns:

bool: true if the URl was successfully opened, false otherwise.

#### Remarks:

What application this function opens depends on what the user has set on their system; there's no way for you to control it.

#### Example:

```NVGT
void main() {
	urlopen("https://nvgt.dev");
}
```



### wait

Waits for a specified number of milliseconds.

void wait(int milliseconds);

#### Arguments:

* int milliseconds: the number of milliseconds to wait for.

#### Remarks:

This function blocks the calling thread, meaning no other work can happen on that thread until the wait period is over.

On the main thread, it performs other essential tasks, such as incremental garbage collection, internal event processing, and refreshing the window.

It is strongly advised to always put `wait(5);` in your main loops. This prevents your game from hogging the CPU, and also makes sure that the window remains responsive and has been updated with the latest input events from the user.

Please note that, due to low-level operating system scheduling behaviors, the millisecond parameter is not an exact value, but rather a guaranteed minimum. This is even more important to remember when calling from the main thread given the additional tasks performed. It should therefore never be used as a time marker where accuracy is required.

#### Example:

```NVGT
void main() {
	alert("Info", "Once you press OK, I will wait for 2000 milliseconds (2 seconds).");
	wait(2000);
	alert("Info", "2000 milliseconds passed!");
}
```





