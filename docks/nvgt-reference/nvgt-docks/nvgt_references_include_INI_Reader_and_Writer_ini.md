# INI Reader and Writer (ini.nvgt)
## INI Reader and Writer
This is a class designed to read and write INI configuration files.

I can't promise that the specification will end up being followed to the letter, but I'll try. At this time, though the order of keys and sections will remain the same, the whitespace, comment, and line structure of an externally created ini file may not remain in tact if that file is updated and rewritten using this include.


## classes
### ini
This constructor just takes an optional filename so you can load an INI file directly on object creation if you want. Note though that doing it this way makes it more difficult to instantly tell if there was a problem do to the lack of a return value, so you must then evaluate ini::get_error_line() == 0 to verify a successful load.

`ini(string filename = "");`

#### Arguments:
* string filename = "": an optional filename to load on object creation.


#### methods
##### clear_section
Deletes all keys from the given section without deleting the section itself.

`bool ini::clear_section(string section);`

###### Arguments:
* string section: the name of the section to clear.

###### Returns:
bool: true if the section was successfully cleared, false if it doesn't exist.


##### create_section
Creates a new INI section with the given name.

`bool ini::create_section(string section_name);`

###### Arguments:
* string section_name: the name of the section to create.

###### Returns:
bool: true if the section was successfully created, false otherwise.


##### delete_key
Delete a key from a given section.

`bool ini::delete_key(string section, string key);`

###### Arguments:
* string section: the name of the section the key is stored in (if any).
* string key: the name of the key to delete.

###### Returns:
bool: true if the key was successfully deleted, false and sets an error if the key you want to delete doesn't exist or if the key name is invalid.


##### delete_section
Delete the given section.

`bool ini::delete_section(string section);`

###### Arguments:
* string section: the name of the section to delete (set this argument to a blank string to delete all sectionless keys).

###### Returns:
bool: true if the section was successfully deleted, false otherwise.


##### dump
Dump all loaded data into a string, such as what's used by the save function, or so that you can encrypt it, pack it or such things.

`string ini::dump(bool indent = false);`

###### Arguments:
* bool indent = false:  If this is set to true, all keys in every named section will be proceeded with a tab character in the final output.

###### Returns:
string: the entire INI data as a string.


##### get_bool
Fetch a boolean value from the INI data given a section and key.

`bool ini::get_bool(string section, string key, bool default_value = false);`

###### Arguments:
* string section: the section to get the value from (if any).
* string key: the key of the value.
* bool default_value = false: the default value to return if the key isn't found.

###### Returns:
bool: the value at the particular key if found, the default value if not.

###### Remarks:
All getters will use this format, and if one returns a default value (blank string, an int that equals 0, a boolean that equals false etc), and if you want to know whether the key actually existed, use the error checking system.


##### get_double
Fetch a double from the INI data given a section and key.

`double ini::get_double(string section, string key, double default_value = 0.0);`

###### Arguments:
* string section: the section to get the value from (if any).
* string key: the key of the value.
* double default_value = 0.0: the default value to return if the key isn't found.

###### Returns:
double: the value at the particular key if found, the default value if not.

###### Remarks:
All getters will use this format, and if one returns a default value (blank string, an int that equals 0, a boolean that equals false etc), and if you want to know whether the key actually existed, use the error checking system.


##### get_error_line
Return the line the last error took place on if applicable. This does not clear the error information, since one may wish to get the line number and the text which are in 2 different functions. So make sure to call this function before `ini::get_error_text()` if the line number is something you're interested in retrieving.

`int ini::get_error_line();`

###### Returns:
int: the line number of the last error, if any. A return value of -1 means that this error is not associated with a line number, and 0 means there is no error in the first place.


##### get_error_text
Returns the last error message, almost always used if an INI file fails to load and you want to know why. This function also clears the error, so to figure out the line, call `ini::get_error_line()` before calling this.

`string ini::get_error_text();`

###### Returns:
string: the last error message, if any.


##### get_string
Fetch a string from the INI data given a section and key.

`string ini::get_string(string section, string key, string default_value = "");`

###### Arguments:
* string section: the section to get the value from (if any).
* string key: the key of the value.
* string default_value = "": the default value to return if the key isn't found.

###### Returns:
string: the value at the particular key if found, the default value if not.

###### Remarks:
All getters will use this format, and if one returns a default value (blank string, an int that equals 0, a boolean that equals false etc), and if you want to know whether the key actually existed, use the error checking system.


##### is_empty
Determine if the INI object has no data in it.

`bool ini::is_empty();`

###### Returns:
bool: true if there is no data loaded into this ini object, false otherwise.


##### key_exists
Determine if a particular key exists in the INI data.

`bool ini::key_exists(string section, string key);`

###### Arguments:
* string section: the name of the section to look for the key in.
* string key: the name of the key.

###### Returns:
bool: true if the specified key exists, false otherwise.

###### Remarks:
An error will be accessible from the error system if the given section doesn't exist.


##### list_keys
List all key names in a given section.

`string[]@ ini::list_keys(string section);`

###### Arguments:
* string section: the section to list keys from(pass a blank string for all sectionless keys as usual).

###### Returns:
string[]@: a handle to an array containing all the keys.  An empty array means that the section is either blank or doesn't exist, the latter being able to be checked with the error system.


##### list_sections
List all section names that exist.

`string[]@ list_sections(bool include_blank_section = false);`

###### Arguments:
* bool include_blank_section = false: Set this argument to true if you wish to include the empty element at the beginning of the list for the keys that aren't in sections, for example for automatic data collection so you don't have to insert yourself when looping through.

###### Returns:
string[]@: a handle to an array containing all the key names.


##### list_wildcard_sections
Returns all section names containing a wildcard identifier. This way if searching through a file containing many normal sections and a few wildcard sections, it is possible to query only the wildcards for faster lookup.

`string[]@ ini::list_wildcard_sections();`

###### Returns:
string[]@: a handle to an array containing all the wildcard sections.


##### load
Load an INI file.

`bool ini::load(string filename, bool robust = true);`

###### Arguments:
* string filename: the name of the ini file to load.
* bool robust = true: if true, a temporary backup copy of the ini data will be created before saving, and it'll be restored on error. This is slower and should only be used when necessary, but insures 0 data loss.

###### Returns:
bool: true if the ini data was successfully loaded, false otherwise.


##### load_string
This function loads INI data stored as a string, doing it this way insures that ini data can come from any source, such as an encrypted string if need be.

`bool ini::load_string(string data, string filename = "*");`

###### Arguments:
* string data: the INI data to load (as a string).
* string filename = "*": the new filename to set on the INI object, if any.

###### Returns:
bool: true if the data was successfully loaded, false otherwise.

###### Remarks:
Input data is expected to have CRLF line endings.


##### reset
Resets all variables to default. You can call this yourself and it is also called by loading functions to clear data from partially successful loads upon error.

`void ini::reset(bool make_blank_section = true);

###### Arguments:
* bool make_blank_section = true: this argument is internal, and exists because the `ini::load_string()` function creates that section itself.


##### save
Save everything currently loaded to a file.

`bool ini::save(string filename, bool indent = false);`

###### Arguments:
* string filename: the name of the file to write to.
* bool indent = false:  If this is set to true, all keys in every named section will be proceeded with a tab character in the final output.

###### Returns:
bool: true if the data was successfully saved, false otherwise.


##### save_robust
This function is similar to `ini::save()`, but it first performs a temporary backup of any existing data, then restores that backup if the saving fails. This is slower and should only be used when necessary, but should insure 0 data loss.

`bool ini::save_robust(string filename, bool indent = false);`

###### Arguments:
* string filename: the name of the file to write to.
* bool indent = false:  If this is set to true, all keys in every named section will be proceeded with a tab character in the final output.

###### Returns:
bool: true if the data was successfully saved, false otherwise.


##### section_exists
Determine if a particular section exists in the INI data.

bool ini::section_exists(string section);`

###### Arguments:
* string section: the name of the section to check for.

###### Returns:
bool: true if the section exists, false if not.


##### set_bool
Set a boolean value in the INI data given a section name, a key and a value.

`bool ini::set_bool(string section, string key, bool value);`

###### Arguments:
* string section: the section to put this key/value pair in (leave blank to add at the top of the file without a section).
* string key: the name of the key.
* bool value: the value to set.

###### Returns:
bool: true if the value was successfully written, false otherwise.

###### Remarks:
All of the other setters use this format. If the key exists already, the value, of course, will be updated.


##### set_double
Set a double in the INI data given a section name, a key and a value.

`bool ini::set_double(string section, string key, double value);`

###### Arguments:
* string section: the section to put this key/value pair in (leave blank to add at the top of the file without a section).
* string key: the name of the key.
* double value: the value to set.

###### Returns:
bool: true if the double was successfully written, false otherwise.

###### Remarks:
All of the other setters use this format. If the key exists already, the value, of course, will be updated.


##### set_string
Set a string in the INI data given a section name, a key and a value.

`bool ini::set_string(string section, string key, string value);`

###### Arguments:
* string section: the section to put this key/value pair in (leave blank to add at the top of the file without a section).
* string key: the name of the key.
* string value: the value to set.

###### Returns:
bool: true if the string was successfully written, false otherwise.

###### Remarks:
All of the other setters use this format. If the key exists already, the value, of course, will be updated.



#### properties
##### loaded_filename
Contains the filename of the currently loaded INI data.

`string loaded_filename;`






