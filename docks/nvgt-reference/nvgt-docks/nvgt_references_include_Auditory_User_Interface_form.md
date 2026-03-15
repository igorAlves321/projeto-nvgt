# Auditory User Interface (form.nvgt)
## Classes
### audio_form
This class facilitates the easy creation of user interfaces that convey their usage entirely through audio.

#### Notes:
* many of the methods in this class only work on certain types of controls, and will return false and set an error value if used on invalid types of controls. This will generally be indicated in the documentation for each function.
* Exceptions are not used here. Instead, we indicate errors through `audio_form::get_last_error()`.
* An audio form object can have up to 50 controls.


#### Methods
##### activate_progress_timer
Activate progress updates on a progress bar control.

`bool audio_form::activate_progress_timer(int control_index);`

###### Arguments:
* int control_index: the index of the progress bar.

###### Returns:
bool: true if the progress bar was successfully activated, false otherwise.


##### add_list_item
Add a string item to a list control.

1. `bool audio_form::add_list_item(int control_index, string option, int position = -1, bool selected = false, bool focus_if_first = true);`
2. `bool audio_form::add_list_item(int control_index, string option, string id, int position = -1, bool selected = false, bool focus_if_first = true);`

###### Arguments (1):
* int control_index: the control index of the list to add to.
* string option: the item to add to the list.
* int position = -1: the position to insert the new item at (-1 = end of list).
* bool selected = false: should this item be selected by default?
* bool focus_if_first = true: if this item is the first in the list and no other item gets explicitly focused, this item will be focused.

###### Arguments (2):
* int control_index: the control index of the list to add to.
* string option: the item to add to the list.
* string id: the ID of the item in the list.
* int position = -1: the position to insert the new item at (-1 = end of list).
* bool selected = false: should this item be selected by default?
* bool focus_if_first = true: if this item is the first in the list and no other item gets explicitly focused, this item will be focused.

###### Returns:
bool: true if the item was successfully added, false otherwise.

###### Remarks:
This function only works on list controls.


##### clear_list
Clear a list control of all its items.

`bool audio_form::clear_list(int control_index);`

###### Arguments:
* int control_index: the index of the list to clear.

###### Returns:
bool: true if the list was successfully cleared, false otherwise.


##### create_button
Creates a new button and adds it to the audio form.

`int audio_form::create_button(string caption, bool primary = false, bool cancel = false, bool overwrite = true);`

###### Arguments:
* string caption: the label to associate with the button.
* bool primary = false: should this button be activated by pressing enter anywhere in the form?
* bool cancel = false: should this button be activated by pressing escape anywhere in the form?
* bool overwrite = true: overwrite any existing primary/cancel settings.

###### Returns:
int: the control index of the new button, or -1 if there was an error. To get error information, look at `audio_form::get_last_error();`.


##### create_checkbox
Creates a new checkbox and adds it to the audio form.

`int audio_form::create_checkbox(string caption, bool initial_value = false, bool read_only = false);`

###### Arguments:
* string caption: the text to be read when tabbing over this checkbox.
*( bool initial_value = false: the initial value of the checkbox (true = checked, false = unchecked).
* bool read_only = false: can the user check/uncheck this checkbox?

###### Returns:
int: the control index of the new checkbox, or -1 if there was an error. To get error information, see `audio_form::get_last_error();`.


##### create_input_box
Creates an input box control on the audio form.

`int audio_form::create_input_box(string caption, string default_text = "", string password_mask = "", int maximum_length = 0, bool read_only = false, bool multiline = false, bool multiline_enter = true);`

###### Arguments:
* string caption: the label of the input box (e.g. what will be read when you tab over it?).
* string default_text = "": the text to populate the input box with by default (if any).
* string password_mask = "": a string to mask typed characters with, (e.g. "star"). Mainly useful if you want your field to be password protected. Leave blank for no password protection.
* int maximum_length = 0: the maximum number of characters that can be typed in this field, 0 for unlimited.
* bool read_only = false: should this text field be read-only?
* bool multiline = false: should this text field have multiple lines?
* bool multiline_enter = true: should pressing enter in this field insert a new line (if it's multiline)?

###### Returns:
int: the control index of the new input box, or -1 if there was an error. To get error information, look at `audio_form::get_last_error();`.


##### create_keyboard_area
Creates a new keyboard area and adds it to the audio form.

`int audio_form::create_keyboard_area(string caption);`

###### Arguments:
* string caption: the text to be read when tabbing onto the keyboard area.

###### Returns:
int: the control index of the new keyboard area, or -1 if there was an error. To get error information, see `audio_form::get_last_error();`.


##### create_link
Creates a new link and adds it to the audio form.

`int audio_form::create_link(string caption, string url);`

###### Arguments:
* string caption: the label of the link.
* string url: The link to open.

###### Returns:
int: the control index of the new link, or -1 if there was an error. To get error information, see `audio_form::get_last_error();`.

###### Remarks:
The link control is similar to buttons, but this opens the given link when pressed. This also speaks the error message if the link cannot be opened or the link isn't an actual URL. If you want the maximum possible customization, use `audio_form::create_button` method instead.


##### create_list
Creates a new list control and adds it to the audio form.

`int audio_form::create_list(string caption, int maximum_items = 0, bool multiselect = false, bool repeat_boundary_items = false);`

###### Arguments:
* string caption: the label to attach to this list.
* int maximum_items = 0: the maximum number of allowed items, 0 for unlimited.
* bool multiselect = false: can the user select multiple items in this list?
* bool repeat_boundary_items = false: do items repeat if you press the arrow keys at the edge of the list?

###### Returns:
int: the control index of the new list, or -1 if there was an error. To get error information, look at `audio_form::get_last_error();`.


##### create_progress_bar
Creates a new progress bar control and adds it to the audio form.

`int audio_form::create_progress_bar(string caption, int speak_interval = 5, bool speak_global = true);`

###### Arguments:
* string caption: the label to associate with the progress bar.
* int speak_interval = 5: how often to speak percentage changes.
* bool speak_global = true: should progress updates be spoken even when this control doesn't have keyboard focus?

###### Returns:
int: the control index of the new progress bar, or -1 if there was an error. To get error information, look at `audio_form::get_last_error();`.


##### create_slider
Creates a new slider control and adds it to the audio form.

`int audio_form::create_slider(string caption, double default_value = 50, double minimum_value = 0, double maximum_value = 100, string text = "", double step_size = 1);`

###### Arguments:
* string caption: the text to be spoken when this slider is tabbed over.
* double default_value = 50: the default value to set the slider to.
* double minimum_value = 0: the minimum value of the slider.
* double maximum_value = 100: the maximum value of the slider.
* string text = "": extra text to be associated with the slider.
* double step_size = 1: the value that will increment/decrement the slider value.

###### Returns:
int: the control index of the new slider, or -1 if there was an error. To get error information, see `audio_form::get_last_error();`.


##### create_status_bar
Creates a new status bar and adds it to the audio form.

`int audio_form::create_status_bar(string caption, string text);`

###### Arguments:
* string caption: the label of the status bar.
* string text: the text to display on the status bar.

###### Returns:
int: the control index of the new status bar, or -1 if there was an error. To get error information, see `audio_form::get_last_error();`.


##### create_subform

Creates a new sub form and adds it to the audio form.

int audio_form::create_subform(string caption, audio_form@ f);

###### Arguments:

* string caption: the label to associate with the sub form.

* audio_form@ f: an object pointing to an already created form.

###### Returns:

int: the control index of the new sub form control, or -1 if there was an error. To get error information, look at `audio_form::get_last_error();`.

###### Example:

```NVGT
#include "form.nvgt"
// some imaginary global application variables.
bool logostart = true, menuwrap = false, firespace = false, radar = true;
// First, lets make a class which stores a category name and the form that the category is linked to.
class settings_category {
	string name;
	audio_form@ f;
	settings_category(string n, audio_form@ f) {
		this.name = n;
		@this.f = @f;
	}
}
void settings_dialog() {
	// Define some categories and settings on each category like this:
	audio_form fc_general;
	fc_general.create_window();
	int f_logostart = fc_general.create_checkbox("Play &logo on startup", logostart);
	int f_menuwrap = fc_general.create_checkbox("Wrap &menus", menuwrap);
	audio_form fc_gameplay;
	fc_gameplay.create_window();
	int f_firespace = fc_gameplay.create_checkbox("Use space instead of control to &fire", firespace);
	int f_radar = fc_gameplay.create_checkbox("Enable the &radar", firespace);
	// Add as many categories as you want this way.
	audio_form f; // The overarching main form.
	f.create_window("Settings", false, true);
	int f_category_list = f.create_tab_panel("&Category"); // The user will select categories from here. Note: you can also use create_list.
	int f_category_display = f.create_subform("General settings", @fc_general); // Now by default, the main form embeds the general category form right there.
	int f_ok = f.create_button("&Save settings", true);
	int f_cancel = f.create_button("Cancel", false, true);
	// Now lets create a structured list of categories that can be browsed based on the class above.
	settings_category@[] categories = {
		settings_category("General", @fc_general),
		settings_category("Gameplay", @fc_gameplay)
	};
	// And then add the list of categories to the form's list.
	for (uint i = 0; i < categories.length(); i++) {
		f.add_list_item(f_category_list, categories[i].name);
	}
	// Focus the form's list position on the general category, then set the form's initial focused control to the category list.
	f.set_list_position(f_category_list, 0);
	f.focus(0);
	settings_category@ last_category = @categories[0]; // A handle to the currently selected category so we can detect changes to the selection.
	// Finally this is the loop that does the rest of the magic.
	while (!f.is_pressed(f_cancel)) {
		wait(5);
		f.monitor();
		int pos = f.get_list_position(f_category_list);
		settings_category@ selected_category = null;
		if (pos > -1 and pos < categories.length())
			@selected_category = @categories[pos];
		if (@last_category != @selected_category) {
			last_category.f.subform_control_index = -1; // Later improvements to audio form will make this line be handled internally.
			last_category.f.focus_silently(0); // Make sure that if the category is reselected, it is focused on the first control.
			@last_category = @selected_category;
			f.set_subform(f_category_display, @selected_category.f);
			f.set_caption(f_category_display, selected_category.name + " settings");
		}
		// The following is a special feature I came up with in stw which makes it so that if you are in the category list, keyboard shortcuts from the entire form will work regardless of category.
		if (f.get_current_focus() == f_category_list and key_down(KEY_LALT) or key_down(KEY_RALT)) {
			for (uint i = 0; i < categories.length(); i++) {
				if (categories[i].f.check_shortcuts(true)) {
					f.set_list_position(f_category_list, i);
					@last_category = @categories[i];
					f.set_subform(f_category_display, @last_category.f);
					f.set_caption(f_category_display, last_category.name + " settings");
					f.focus(f_category_display);
					break;
				}
			}
		}
		// Now we can finally check for the save button.
		if (f.is_pressed(f_ok)) {
			logostart = fc_general.is_checked(f_logostart);
			menuwrap = fc_general.is_checked(f_menuwrap);
			firespace = fc_gameplay.is_checked(f_firespace);
			radar = fc_gameplay.is_checked(f_radar);
			return;
		}
	}
}
// Lets make this thing run so we can see it work.
void main() {
	show_window("test");
	settings_dialog();
}
```



##### create_window

Creates a window to show audio form controls.

1. void audio_form::create_window();

2. void audio_form::create_window(string window_title, bool change_screen_title = true, bool say_dialog = true, bool silent = false);

###### Arguments (2):

* string window_title: the title of the window.

* bool change_screen_title = true: whether or not the main window's title should be set as well.

* bool say_dialog = true: whether or not the window should be reported as a dialog (in the context of the audio form).

* bool silent = false: should this window be shown silently?

###### Example:

```NVGT
#include "form.nvgt"
#include "speech.nvgt"
void main() {
	audio_form f;
	f.create_window("Test");
	wait(50); // Give screen readers time to speak the window title.
	int f_exit = f.create_button("exit");
	f.focus(f_exit);
	while (true) {
		wait(5);
		f.monitor();
		if (f.is_pressed(f_exit))
			exit();
	}
}
```



##### delete_control
Removes a control with a particular index from the audio form.

`bool audio_form::delete_control(int control_index);`

###### Arguments:
* int control_index: the index of the control to delete.

###### Returns:
bool: true if the control was successfully deleted, false otherwise.


##### delete_list_item
Remove an item from a list control.

`bool audio_form::delete_list_item(int control_index, int list_index, bool reset_cursor = true, bool speak_deletion_status = true);`

###### Arguments:
* int control_index: the index of the list to remove the item from.
* int list_index: the index of the item to remove.
* bool reset_cursor = true: should the user's cursor position be reset to the top of the list upon success?
* bool speak_deletion_status = true: should the user be informed of the deletion via speech feedback?

###### Returns:
bool: true if the item was successfully deleted, false otherwise.


##### delete_list_selections
Unselect any currently selected items in a list control.

`bool audio_form::delete_list_selections(int control_index, bool reset_cursor = true, bool speak_deletion_status = true);`

###### Arguments:
* int control_index: the index of the list to unselect items in.
* bool reset_cursor = true: should the user's cursor position be reset to the top of the list upon success?
* bool speak_deletion_status = true: should the user be informed of the unselection via speech feedback?

###### Returns:
bool: true if the selection was successfully cleared, false otherwise.


##### edit_list_item
Edits the value of a list item.

`bool audio_form::edit_list_item(int control_index, string new_option, int position);`

###### Arguments:
* int control_index: the index of the list containing the item.
* string new_option: the new text of the item.
* int position: the item's index in the list.

###### Returns:
bool: true if the item's value was successfully updated, false otherwise.


##### edit_list_item_id
Modifies the ID of a list item.

`bool audio_form::edit_list_item_id(int control_index, string new_id, int position);`

###### Arguments:
* int control_index: the index of the list containing the item.
* string new_id: the new ID of the list item.
* int position: the item's index in the list.

###### Returns:
bool: true if the item's ID was successfully updated, false otherwise.


##### focus
Set a particular control to have the keyboard focus, and notify the user.

`bool audio_form::focus(int control_index);`

###### Arguments:
* int control_index: the index of the control to focus.

###### Returns:
bool: true if the control was successfully focused, false otherwise.


##### focus_interrupt
Set a particular control to have the keyboard focus, and notify the user (cutting off any previous speech).

`bool audio_form::focus_interrupt(int control_index);`

###### Arguments:
* int control_index: the index of the control to focus.

###### Returns:
bool: true if the control was successfully focused, false otherwise.


##### focus_silently
Set a particular control to have the keyboard focus, without notifying the user.

`bool audio_form::focus_silently(int control_index);`

###### Arguments:
* int control_index: the index of the control to focus.

###### Returns:
bool: true if the control was successfully focused, false otherwise.


##### get_cancel_button
Get the control index of the cancel button (e.g. the button activated when pressing escape anywhere on an audio form).

`int audio_form::get_cancel_button();`

###### Returns:
int: the control index of the cancel button.


##### get_caption
Get the caption of a control.

`string audio_form::get_caption(int control_index);`

###### Arguments:
* int control_index: the index of the control to query.

###### Returns:
string: the caption of the control.


##### get_checked_list_items
Get a list of all currently checked items in a list control.

`int[]@ audio_form::get_checked_list_items(int control_index);`

###### Arguments:
* int control_index: the index of the list to query.

###### Returns:
int[]@: handle to an array containing the index of every checked item in the list.

###### Remarks:
This function only works on multiselect lists. If you want something that also works on single-select lists, see `get_list_selections()`.


##### get_control_count
Returns the number of controls currently present on the form.

`int audio_form::get_control_count();`

###### Returns:
int: the number of controls currently on the form.


##### get_control_type
Returns the type of a control.

`int audio_form::get_control_type(int control_index);`

###### Arguments:
* int control_index: the index of the control to get the type of.

###### Returns:
int: the type of the control (see control_types for more information).


##### get_current_focus
Get the control index of the control with the keyboard focus.

`int audio_form::get_current_focus();`

###### Returns:
int: the control index that currently has the keyboard focus.


##### get_custom_type
Get the custom type of the control, if available.

`string audio_form::get_custom_type(int control_index);`

###### Arguments:
* int control_index: the control you want to check.

###### Returns:
string: the custom type set on this control if available, an empty string otherwise.


##### get_default_button
Get the control index of the default button (e.g. the button activated when pressing enter anywhere on an audio form).

`int audio_form::get_default_button();`

###### Returns:
int: the control index of the default button.


##### get_last_error
Get the last error that was raised from this form.

`int audio_form::get_last_error();`

###### Returns:
int: the last error code raised by this audio_form ( see audioform_errorcodes for more information).

###### Remarks:
As noted in the introduction to this class, exceptions are not used here. Instead, we indicate errors through this function.


##### get_line_column
Get the current line column of an input box. 

`int audio_form::get_line_column(int control_index);`

###### Arguments:
* int control_index: the index of the input box to retrieve the line column from.

###### Returns:
int: The line column of the input box, or -1 if there was an error.

###### Remarks:
This method only works on input boxes.


##### get_line_number
Get the current line number of an input box. 

`int audio_form::get_line_number(int control_index);`

###### Arguments:
* int control_index: the index of the input box to retrieve the line number from.

###### Returns:
int: The line number of the input box, or -1 if there was an error.

###### Remarks:
This method only works on input boxes.


##### get_link_url
Retrieves the URL of the link control.

`string audio_form::get_link_url(int control_index);`

###### Arguments:
* int control_index: the index of the control.

###### Returns:
string: the URL.

###### Remarks:
This method only works on link control.


##### get_list_count
Get the number of items contained in a list control.

`int audio_form::get_list_count(int control_index);`

###### Arguments:
* int control_index: index of the list control to query.

###### Returns:
int: the number of items in the list.


##### get_list_index_by_id
Get the index of a list item by its ID.

`int audio_form::get_list_index_by_id(int control_index, string id);`

###### Arguments:
* int control_index: the index of the list.
* string id: the ID of the item to query.

###### Returns:
int: the index of the item, -1 on error.


##### get_list_item
Get the text of a particular list item.

`string audio_form::get_list_item(int control_index, int list_index);`

###### Arguments:
* int control_index: the index of the list.
* int list_index: the index of the item to get.

###### Returns:
string: the text of the item.


##### get_list_item_id
Get the ID of a particular list item.

`string audio_form::get_list_item_id(int control_index, int list_index);`

###### Arguments:
* int control_index: the index of the list.
* int list_index: the index of the item to get.

###### Returns:
string: the ID of the item.


##### get_list_position
Get the user's currently focused item in a list control.

`int audio_form::get_list_position(int control_index);`

###### Arguments:
* int control_index: the index of the list.

###### Returns:
int: the user's current cursor position in the list.


##### get_list_selections
Get a list of all items currently selected in a list control.

`int[]@ audio_form::get_list_selections(int control_index);`

###### Arguments:
* int control_index: the index of the list to query.

###### Returns:
int[]@: handle to an array containing the index of every selected item in the list (see remarks).

###### Remarks:
In the context of this function, a selected item is any item that  is checked (if the list supports multiselection), as well as the currently selected item. If you want to only get the state of checked list items, see the `get_checked_list_items()` function.


##### get_progress
Get the value of a progress bar.

`int audio_form::get_progress(int control_index);`

###### Arguments:
* int control_index: the index of the progress bar to query.

###### Returns:
int: the current value of the progress bar.

###### Remarks:
This method only works on progress bar controls.


##### get_slider
Get the value of a slider.

`double audio_form::get_slider(int control_index);`

###### Arguments:
* int control_index: the index of the slider to query.

###### Returns:
double: the current value of the slider. In case of error, this may return -1. To get error information, see `audio_form::get_last_error();`.

###### Remarks:
This method only works on slider control.


##### get_slider_maximum_value
Get the maximum value of a slider.

`double audio_form::get_slider_maximum_value(int control_index);`

###### Arguments:
* int control_index: the index of the slider to query.

###### Returns:
double: the maximum allowable value the slider may be set to. In case of error, this may return -1. To get error information, see `audio_form::get_last_error();`.

###### Remarks:
This method only works on slider control.


##### get_slider_minimum_value
Get the minimum value of a slider.

`double audio_form::get_slider_minimum_value(int control_index);`

###### Arguments:
* int control_index: the index of the slider to query.

###### Returns:
double: the minimum allowable value the slider may be set to. In case of error, this may return -1. To get error information, see `audio_form::get_last_error();`.

###### Remarks:
This method only works on slider control.


##### get_text
Get the text from an input box or status bar.

`string audio_form::get_text(int control_index);`

###### Arguments:
* int control_index: the index of the control to retrieve the text from.

###### Returns:
string: The text from the control, or an empty string if there was an error.

###### Remarks:
This method only works on input boxes and status bars.


##### has_custom_type
Determines whether the control has its custom type set.

`bool audio_form::has_custom_type(int control_index);`

###### Arguments:
* int control_index: the control you want to check.

###### Returns:
bool: true if the control has its custom type set, false otherwise.

###### Remarks:
Please note that this method is equivalent to `audio_form::get_custom_type(control_index).empty()`


##### is_checked
Get the state of a checkbox.

`bool audio_form::is_checked(int control_index);`

###### Arguments:
* int control_index: the index of the control to query.

###### Returns:
bool: true if the checkbox is checked, false otherwise.

###### Remarks:
This function only works on checkbox controls.


##### is_disallowed_char
Determines whether the text of a given control contains characters that are not allowed, set by the `audio_form::set_disallowed_chars` method.

`bool audio_form::is_disallowed_char(int control_index, string char, bool search_all = true);`

###### Arguments:
* int control_index: the index of the control.
* string char: one or more characters to query
* bool search_all = true: toggles whether to search character by character or to match the entire string.

###### Returns:
bool: true if the text of the control contains disallowed characters, false otherwise.

###### Remarks:
The `search_all` parameter will match the characters depending upon its state. If set to false, the entire string will be searched. If set to true, it will loop through each character and see if one of them contains disallowed character. Thus, you will usually set this to true. One example you might set to false is when the form only has 1 character length, but it is not required, it is looping each character already. However, it is also a good idea to turn this off for the maximum possible performance if you're sure that the input only requires 1 length of characters.


##### is_enabled
Determine if a particular control is enabled or not.

`bool audio_form::is_enabled(int control_index);`

###### Arguments:
* int control_index: the index of the control to query.

###### Returns:
bool: true if the control is enabled, false if it's disabled.


##### is_list_item_checked
Determine if the list item at a particular index is checked or not.

`bool audio_form::is_list_item_checked(int control_index, int item_index);`

###### Arguments:
* int control_index: the index of the list containing the item to be checked.
* int item_index: the index of the item to check.

###### Returns:
bool: true if the item exists and is checked, false otherwise.


##### is_multiline
Determine if a particular control is multiline or not.

`bool audio_form::is_multiline(int control_index);`

###### Arguments:
* int control_index: the index of the control to query.

###### Returns:
bool: true if the control is multiline, false otherwise.

###### Remarks:
This function only works on input boxes.


##### is_pressed
Determine if a particular button was just pressed.

`bool audio_form::is_pressed(int control_index);`

###### Arguments:
* int control_index: the index of the control to query.

###### Returns:
bool: true if the button was just pressed, false otherwise.

###### Remarks:
This function only works on button controls.


##### is_read_only
Determine if a particular control is read-only or not.

`bool audio_form::is_read_only(int control_index);`

###### Arguments:
* int control_index: the index of the control to query.

###### Returns:
bool: true if the control is read-only, false if it's not.

###### Remarks:
This function only works on input boxes and checkboxes.


##### is_visible
Determine if a particular control is visible or not.

`bool audio_form::is_visible(int control_index);`

###### Arguments:
* int control_index: the index of the control to query.

###### Returns:
bool: true if the control is visible, false if it's invisible.


##### monitor
Processes all keyboard input, and dispatches all events to the form. Should be called in your main loop.

`int audio_form::monitor();`

###### Returns:
int: this value can be ignored for users of this class; it's used internally for subforms.


##### pause_progress_timer
Pause updating of a progress bar control.

`bool audio_form::pause_progress_timer(int control_index);`

###### Arguments:
* int control_index: the index of the progress bar.

###### Returns:
bool: true if the progress bar was paused, false otherwise.


##### set_button_attributes
Set the primary and cancel flags of a button.

`bool audio_form::set_button_attributes(int control_index, bool primary, bool cancel, bool overwrite = true);

###### Arguments:
* int control_index: the index of the button to update.
* bool primary: should this button be made primary (e.g. pressing enter from anywhere on the form activates it)?
* bool cancel: should this button be made the cancel button (e.g. should pressing escape from anywhere on the form always activate it?).
* bool overwrite = true: should the previous primary and cancel buttons (if any) be overwritten?

###### Returns:
bool: true if the attributes were successfully set, false otherwise.


##### set_caption
Sets the caption of a control.

`bool audio_form::set_caption(int control_index, string caption);`

###### Arguments:
* int control_index: the index of the control.
* string caption: the caption to set on the control (see remarks for more infromation).

###### Returns:
bool: true if the caption was successfully set, false otherwise.

###### Remarks:
The caption is read every time a user focuses this particular control.

It is possible to associate hotkeys with controls by putting an "&" symbol in the caption. For example, setting the caption of a button to "E&xit" would assign the hotkey alt+x to focus it.


##### set_checkbox_mark
Set the state of a checkbox (either checked or unchecked).

`bool audio_form::set_checkbox_mark(int control_index, bool checked);`

###### Arguments:
* int control_index: the control index of the checkbox.
* bool checked: whether the checkbox should be set to checked or not.

###### Returns:
bool: true if the operation was successful, false otherwise. To get error information, look at `audio_form::get_last_error();`.


##### set_custom_type
Sets a custom type for a control.

`bool audio_form::set_custom_type(int control_index, string custom_type);`

###### Arguments:
* int control_index: the index of the control.
* string custom_type: a custom text type to set on the control.

###### Returns:
bool: true if the custom text type was successfully set, false otherwise.


##### set_default_controls
Sets default and cancel buttons for this form.

`bool set_default_controls(int primary, int cancel);`

###### Arguments:
* int primary: the control index of the button to make primary.
* int cancel: the control index of the cancel button.

###### Returns:
bool: true if the controls were successfully set, false otherwise.


##### set_default_keyboard_echo
Sets the default keyboard echo of controls on your form.

`bool audio_form::set_default_keyboard_echo(int keyboard_echo, bool update_controls = true);`

###### Arguments:
* int keyboard_echo: the keyboard echo mode to use (see text_entry_speech_flags for more information).
* bool update_controls = true: whether or not this echo should be applied to any controls that already exist on your form.

###### Returns:
bool: true if the echo was successfully set, false otherwise.


##### set_disallowed_chars
Sets the whitelist/blacklist characters of a control.

`bool audio_form::set_disallowed_chars(int control_index, string chars, bool use_only_disallowed_chars = false, string char_disallowed_description = "");`

###### Arguments:
* int control_index: the index of the control.
* string chars: the characters to set.
* bool use_only_disallowed_chars = false: sets whether the control should only use the characters in this list. true means use only characters that are in the list, and false means allow only characters that are not in the list.
* string char_disallowed_description = "": the text to speak when an invalid character is inputted.

###### Returns:
bool: true if the characters were successfully set, false otherwise.

###### Remarks:
Setting the `use_only_disallowed_chars` parameter to true will restrict all characters that are not in the list. This is useful to prevent other characters in number inputs.

Setting the chars parameter to empty will clear the characters and will switch back to default.

Please note that these character sets will also restrict the text from being pasted if the clipboard contains disallowed characters.


##### set_enable_go_to_index
Toggles whether the control can use go to line functionality.

`bool audio_form::set_enable_go_to_index(int control_index, bool enabled);`

###### Arguments:
* int control_index: the index of the control.
* bool enabled: enables the go to line functionality.

###### Returns:
bool: true if the state was successfully set, false otherwise.


##### set_enable_search
Toggles whether the control can use search functionality.

`bool audio_form::set_enable_search(int control_index, bool enabled);`

###### Arguments:
* int control_index: the index of the control.
* bool enabled: enables the search functionality.

###### Returns:
bool: true if the state was successfully set, false otherwise.


##### set_keyboard_echo
Set the keyboard echo for a particular control.

`bool audio_form::set_keyboard_echo(int control_index, int keyboard_echo);`

###### Arguments:
* int control_index: the index of the control to modify.
* int keyboard_echo: the keyboard echo mode to use (see text_entry_speech_flags for more information).

###### Returns:
bool: true if the keyboard echo was successfully set, false otherwise.


##### set_link_url
Sets the URL of the link control.

`bool audio_form::set_link_url(int control_index, string new_url);`

###### Arguments:
* int control_index: the index of the control.
* string new_url: the URL to set.

###### Returns:
bool: true on success, false on failure.

###### Remarks:
This method only works on link control.


##### set_list_multinavigation
Configures how the multi-letter navigation works in a list control.

`bool audio_form::set_list_multinavigation(int control_index, bool letters, bool numbers, bool nav_translate = true);`

###### Arguments:
* int control_index: the index of the list control.
* bool letters: can the user navigate with letters?
* bool numbers: can the user navigate with the numbers.
* bool nav_translate = true: should the letters work with the translated alphabet in use?

###### Returns:
bool: true if the settings were successfully set, false otherwise.


##### set_list_position
Set the user's cursor in a list control.

`bool audio_form::set_list_position(int control_index, int position = -1, bool speak_new_item = false);`

###### Arguments:
* int control_index: the index of the list.
* int position = -1: the new cursor position (-1 for no selection).
* bool speak_new_item = false: should the user be notified of the selection change via speech?

###### Returns:
bool: true if the cursor position was successfully set, false otherwise.


##### set_list_properties
Sets the properties of a list control.

`bool audio_form::set_list_propertyes(int control_index, bool multiselect=false, bool repeat_boundary_items=false);`

###### Arguments:
* int control_index: the index of the list.
* bool multiselect = false: can the user select multiple items in this list?
* bool repeat_boundary_items = false: do items repeat if you press the arrow keys at the edge of the list?

###### Returns:
bool: true on success, false on failure.


##### set_progress
Sets the progress percentage on the progress control.

`bool audio_form::set_progress(int control_index, int value);`

###### Arguments:
* int control_index: the index of the control.
* int value: the percentage to set.

###### Returns:
bool: true on success, false on failure.

###### Remarks:
This method only works on progress control.


##### set_slider
Sets the value of the slider control.

`bool audio_form::set_slider(int control_index, double value, double min = -1, double max = -1);`

###### Arguments:
* int control_index: the index of the control.
* double value: the value to set.
* double min = -1: the minimum value to set. This can be omitted.
* double max = -1: the maximum value to set. This can be omitted.

###### Returns:
bool: true on success, false on failure.

###### Remarks:
This method only works on slider control.


##### set_state
Set the enabled/visible state of a control.

`bool audio_form::set_state(int control_index, bool enabled, bool visible);`

###### Arguments:
* int control_index: the index of the control.
* bool enabled: is the control enabled (e.g. if it's a button, being disabled would make the button unpressable).
* bool visible: can the user access the control with the navigation commands?

###### Returns:
bool: true if the state was successfully set, false otherwise.


##### set_subform

Sets a sub form to use on the current form.

bool audio_form::set_subform(int control_index, audio_form@ f);

###### Arguments:

* int control_index: the control index of the sub form created with `audio_form::create_subform` method.

* audio_form@ f: an object pointing to an already created form.

###### Returns:

bool: true if the operation was successful, false otherwise. To get error information, look at `audio_form::get_last_error();`.

###### Example:

```NVGT
#include "form.nvgt"
// some imaginary global application variables.
bool logostart = true, menuwrap = false, firespace = false, radar = true;
// First, lets make a class which stores a category name and the form that the category is linked to.
class settings_category {
	string name;
	audio_form@ f;
	settings_category(string n, audio_form@ f) {
		this.name = n;
		@this.f = @f;
	}
}
void settings_dialog() {
	// Define some categories and settings on each category like this:
	audio_form fc_general;
	fc_general.create_window();
	int f_logostart = fc_general.create_checkbox("Play &logo on startup", logostart);
	int f_menuwrap = fc_general.create_checkbox("Wrap &menus", menuwrap);
	audio_form fc_gameplay;
	fc_gameplay.create_window();
	int f_firespace = fc_gameplay.create_checkbox("Use space instead of control to &fire", firespace);
	int f_radar = fc_gameplay.create_checkbox("Enable the &radar", firespace);
	// Add as many categories as you want this way.
	audio_form f; // The overarching main form.
	f.create_window("Settings", false, true);
	int f_category_list = f.create_tab_panel("&Category"); // The user will select categories from here. Note: you can also use create_list.
	int f_category_display = f.create_subform("General settings", @fc_general); // Now by default, the main form embeds the general category form right there.
	int f_ok = f.create_button("&Save settings", true);
	int f_cancel = f.create_button("Cancel", false, true);
	// Now lets create a structured list of categories that can be browsed based on the class above.
	settings_category@[] categories = {
		settings_category("General", @fc_general),
		settings_category("Gameplay", @fc_gameplay)
	};
	// And then add the list of categories to the form's list.
	for (uint i = 0; i < categories.length(); i++) {
		f.add_list_item(f_category_list, categories[i].name);
	}
	// Focus the form's list position on the general category, then set the form's initial focused control to the category list.
	f.set_list_position(f_category_list, 0);
	f.focus(0);
	settings_category@ last_category = @categories[0]; // A handle to the currently selected category so we can detect changes to the selection.
	// Finally this is the loop that does the rest of the magic.
	while (!f.is_pressed(f_cancel)) {
		wait(5);
		f.monitor();
		int pos = f.get_list_position(f_category_list);
		settings_category@ selected_category = null;
		if (pos > -1 and pos < categories.length())
			@selected_category = @categories[pos];
		if (@last_category != @selected_category) {
			last_category.f.subform_control_index = -1; // Later improvements to audio form will make this line be handled internally.
			last_category.f.focus_silently(0); // Make sure that if the category is reselected, it is focused on the first control.
			@last_category = @selected_category;
			f.set_subform(f_category_display, @selected_category.f);
			f.set_caption(f_category_display, selected_category.name + " settings");
		}
		// The following is a special feature I came up with in stw which makes it so that if you are in the category list, keyboard shortcuts from the entire form will work regardless of category.
		if (f.get_current_focus() == f_category_list and key_down(KEY_LALT) or key_down(KEY_RALT)) {
			for (uint i = 0; i < categories.length(); i++) {
				if (categories[i].f.check_shortcuts(true)) {
					f.set_list_position(f_category_list, i);
					@last_category = @categories[i];
					f.set_subform(f_category_display, @last_category.f);
					f.set_caption(f_category_display, last_category.name + " settings");
					f.focus(f_category_display);
					break;
				}
			}
		}
		// Now we can finally check for the save button.
		if (f.is_pressed(f_ok)) {
			logostart = fc_general.is_checked(f_logostart);
			menuwrap = fc_general.is_checked(f_menuwrap);
			firespace = fc_gameplay.is_checked(f_firespace);
			radar = fc_gameplay.is_checked(f_radar);
			return;
		}
	}
}
// Lets make this thing run so we can see it work.
void main() {
	show_window("test");
	settings_dialog();
}
```



##### set_text
Sets the text of the control.

`bool audio_form::set_text(int control_index, string new_text);`

###### Arguments:
* int control_index: the index of the control.
* string new_text: the text to set.

###### Returns:
bool: true on success, false on failure.

###### Remarks:
This method only works on input field, slider, and status bar.



#### Properties
##### active
Determine if the form is currently active.

`bool audio_form::active;`





## Enums
### audioform_errorcodes
This enum contains any error values that can be returned by the `audio_form::get_last_error();` function.

* form_error_none: No error.
* form_error_invalid_index: you provided a control index that doesn't exist.
* form_error_invalid_control: you are attempting to do something on an invalid control.
* form_error_invalid_value: You provided an invalid value.
* form_error_invalid_operation: you tried to perform an invalid operation.
* form_error_no_window: you haven't created an audio_form window yet.
* form_error_window_full: the window is at its maximum number of controls
* form_error_text_too_long: the text provided is too long.
* form_error_list_empty: indicates that a list control is empty.
* form_error_list_full: indicates that a list control is full.
* form_error_invalid_list_index: the list has no item at that index.
* form_error_control_invisible: the specified control is invisible.
* form_error_no_controls_visible: no controls are currently visible.


### control_event_type
Lists all possible event types that can be raised.

* event_none: no event.
* event_focus: a control gained keyboard focus.
* event_list_cursor: the cursor changed in a list control.
* event_text_cursor: the cursor changed in an input box.
* event_button: a button was pressed.
* event_checkbox: a checkbox's state has changed.
* event_slider: a slider's value has been changed.


### control_types
This is a complete list of all control types available in the audio form, as well as a brief description of what they do.

* ct_button: a normal, pressable button.
* ct_input: any form of text box.
* ct_checkbox: a checkable/uncheckable control.
* ct_progress: a progress bar that can both beep and speak.
* ct_status_bar: a small informational area for your users to get information quickly.
* ct_list: a list of items.
* ct_slider: a slider, adjustable to a given percent with the arrow keys.
* ct_form: a child form.
* ct_keyboard_area: an area that captures all keys from the user (minus a few critical ones like tab and shift+tab) and lets you handle them, useful for embedding your game controls within your UI.


### text_edit_mode_constants
This is a list of constants that specify text editing modes, used mainly with `audio_form::edit_text();`.

* edit_mode_replace: replace text.
* edit_mode_trim_to_length: trim the final text to a given length.
* edit_mode_append_to_end: append text to the end.

See the `audio_form::edit_text();` documentation for more information.


### text_entry_speech_flags
This enum provides constants to be used with the character echo functionality in input boxes.

* textflag_none: no echo.
* textflag_characters: echo characters only.
* textflag_words: echo words only.
* textflag_characters_words: echo both characters and words.



## Global Properties
### audioform_input_disable_ralt
Set whether or not the right Alt key should be disabled in input boxes, mostly useful for users with non-english keyboards.

`bool audioform_input_disable_ralt;`


### audioform_keyboard_echo
Set the default echo mode for all the forms. Default is `textflag_characters`

`int audioform_keyboard_echo;`


### audioform_word_separators
A list of characters that should be considered word boundaries for navigation in an input box.

`string audioform_word_separators;`




