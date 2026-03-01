# Filesystem
This section contains documentation of functions and properties that allow you to check the existance of / delete a file, create / enumerate directories, and in other ways interact with and/or manipulate the filesystem.

If you wish to specifically read and write files, you should look at the file datastream class.


## Functions
### directory_create

Creates a directory if it doesn't already exist.

bool directory_create(const string&in directory);

#### Arguments:

* const string&in directory: path to the directory to create (can be nested, relative or absolute).

#### Returns:

bool: true if the directory was successfully created or already exists, false otherwise.

#### Example:

```NVGT
void main() {
	if (directory_exists("test")) {
		alert("Info", "The test directory already exists; nothing to do");
		exit();
	}
	if (directory_create("test")) {
		alert("Info", "Directory created. Deleting...");
		alert("Info", directory_delete("test") ? "Success": "Fail");
	}
	else
		alert("Error", "Couldn't create the directory.");
}
```



### directory_delete
Deletes a directory.

`bool directory_delete(string directory);`

#### Arguments:
* string directory: the directory to delete.

#### Returns:
bool: true if the directory was successfully deleted, false otherwise.


### directory_exists

Query whether or not a directory exists.

bool directory_exists(const string&in directory);

#### Arguments:

* const string&in directory: the directory whose existence will be checked (can be a relative or absolute path).

#### Returns:

bool: true if the directory exists, false otherwise.

#### Example:

```NVGT
void main() {
	alert("Directory exists", directory_exists("test") ? "There is a test folder in the current directory" : "There is not a test folder in the current directory");
}
```



### file_copy
Coppies a file from one location to another.

`bool file_copy(const string&in source_filename, const string&in destination_filename);`

#### Arguments:
* const string&in source_filename: the path/name of the file to be coppied.
* const string&in destination_filename: the path (including filename) to copy the file to.

#### Returns:
bool: true if the file was successfully coppied, false otherwise.


### file_delete
Deletes a file.

`bool file_delete(const string&in filename);`

#### Arguments:
* const string&in filename: the name of the file to delete.

#### Returns:
bool: true if the file was successfully deleted, false otherwise.


### file_exists
Check for the existence of a particular file.

`bool file_exists(const string&in file_path);`

#### Arguments:
* const string&in file_path: the path to the file to query.

#### Returns:
bool: true if the file exists, false otherwise.


### file_get_contents

Reads the entire content of a file and returns it as a string.

string file_get_contents(string filename)

#### Arguments:

* string filename: the name of the file to read.

#### Returns:

The contents of the file on success, an empty string on failure.

#### Remarks:

This is a convenience function, though it is currently the only way to read an Android asset. If you wish to access a file with more control, see the file datastream class.

Be careful to avoid reading files that are too large with this function, as the entire file will be in memory in order to return it as a continguous string.

#### Example:

```NVGT
void main() {
	string filename = input_box("Filename", "Enter the name of a file to read.", "");
	string contents = file_get_contents(filename);
	if (contents == "")
		alert("Example", "Either the file was not found, or it contained no text.");
	else {
		clipboard_set_text(contents);
		alert("Example", "The contents of the file is now on your clipboard.");
	}
}
```



### file_get_date_created

Get a datetime object representing the creation date of a particular file.

datetime file_get_date_created(const string&in filename);

#### Arguments:

* const string&in filename; the name of the file to check.

#### Returns:

datetime: an initialized datetime object, with all its fields set to the creation date of the file.

#### Remarks:

The date returned is in UTC, not your local timezone.

#### Example:

```NVGT
void main() {
	datetime dt = file_get_date_created("file_get_date_created.nvgt");
	alert("file_get_date_created.nvgt was created on", dt.year + "-" + dt.month + "-" + dt.day + ", " + dt.hour +":" + dt.minute + ":" + dt.second);
}
```



### file_get_date_modified

Get a datetime object representing the modification date of a particular file.

datetime file_get_date_modified(const string&in filename);

#### Arguments:

* const string&in filename: the name of the file to check.

#### Returns:

datetime: an initialized datetime object, with all its fields set to the modification date of the file.

#### Remarks:

The date returned is in UTC, not your local timezone.

#### Example:

```NVGT
void main() {
	datetime dt = file_get_date_modified("file_get_date_modified.nvgt");
	alert("file_get_date_modified.nvgt was modified on", dt.year + "-" + dt.month + "-" + dt.day + ", " + dt.hour +":" + dt.minute + ":" + dt.second);
}
```



### file_get_size

Get the size of a file (in bytes).

int64 file_get_size(const string&in filename);

#### Arguments:

* const string&in filename: the name/path of the file to get the size of.

#### Returns:

int64: the size of the file (in bytes).

#### Example:

```NVGT
void main() {
	alert("file_get.size.nvgt is", file_get_size("file_get_size.nvgt") + " bytes");
}
```



### file_put_contents

Writes a string to a file.

bool file_put_contents(string filename, string content, bool append = false)

#### Arguments:

* string filename: the name of the file to write to.

* string content: the content to write.

* bool append = false: specifies whether the current contents of the file should be overwritten when writing.

#### Returns:

bool: true on success, false on failure.

#### Example:

```NVGT
void main() {
	if (!file_put_contents("example.txt", "This is an example"))
		alert("Example", "Failed to write the file.");
	else
		alert("Example", "Successfully wrote the example file.");
}
```



### get_preferences_path

Determines the best location to store user data for your game, creating the directory for you if necessary.

string get_preferences_path(string company_name, string product_name);

#### Arguments:

* string company_name: The name of your organization, can be blank.

* string product_name: The name of your game or application.

#### Remarks:

This is the recommended way to determine where your game should store application data. While other properties exist such as DIRECTORY_APPDATA which can be used to compose your own path if you desire, this function is generally more robust and platform agnostic than trying to prepare your own storage path using directory constants. This also frees you from needing to check for the existance of the directory before writing to it.

The company name and product name should never change for an application once you start using them, lest players lose access to their previous save data due to the directory changing names. The company name can be blank if you wish to only create one level of new directories in the users appdata, though this is generally not recommended to avoid clutter.

Both the company and product name are expected to contain only spaces and alphanumeric characters if you wish to be as platform agnostic as possible.

You should not assume that DIRECTORY_APPDATA + "/" + company_name + "/" + product_name will be the same as the directory returned by this function, or even that both the company and product names will be used all the time. On android, for example, this function always just returns the app's internal storage path.

This function is also registered as the alias DIRECTORY_PREFERENCES, for those who prefer the old style of directory constants naming.

#### Example:

```NVGT
void main() {
	string path = get_preferences_path("", "documentation example");
	alert("test", "data will be stored at " + path);
	directory_delete(path); // In this example we don't actually want this directory to save.
}
```



### glob

Return a list of files and directories on the filesystem given a path glob.

string[]@ glob(const string&in path_pattern, glob_options options = GLOB_DEFAULT);

#### Arguments:

* const string&in path_pattern: The pattern to match files and directories with (Unix shell like, see remarks).

* glob_options options: A bitwise of glob_options enum constants that influence the behavior of this function (see remarks).

#### Returns:

string[]@: A list of all matching files and directories that match the given path pattern, an empty array on no matches or failure.

#### Remarks:

This function provides for one of the easiest ways to enumerate the filesystem in NVGT, particularly because the path patterns provided can actually cause semi-recursive directory searches. The search starts at the current working directory unless an absolute path is given.

The glob patterns have simple rules:

* path separators must be matched exactly, \* will not cause a recursive lookup

* \* matches any sequence of characters

* ? matches any single character

* [set] matches any characters between the brackets

* [!set] matches any characters that are not listed between the brackets

* `\*, \[, \] etc` exactly match a special character usually used as part of the glob expression

There is no guarantee that the items returned will appear in any particular order in the array.

The following glob_options constance are defined:

* GLOB_DEFAULT: the default options

* GLOB_IGNORE_HIDDEN: do not match when directory entries begin with a .

* GLOB_FOLLOW_SYMLINKS: traverse even across symbolic links if the given pattern demands it

* GLOB_CASELESS: match case insensitively

#### Example:

```NVGT
void main() {
	// List all .nvgt files within the filesystem documentation directory.
	string[]@ items = glob("../*/*.nvgt");
	alert("files found", string(items));
}
```




## Global Properties
### DIRECTORY_APPDATA

Property that returns the user's roaming application directory, which is usually where game data can be written to.

const string DIRECTORY_APPDATA;

#### remarks:

A slash character is already appended to the directory returned by this property.

This function may return different values depending on the operating system the application is being run on.

* On Windows, usually C:\Users\%username%\appdata\roaming/.

* on macOS, usually ~/Library/Preferences/.

* on Linux, usually ~/.config/.

* on Android, the app's internal storage path.

In any case, the directory returned should be writable.

#### Example:

```NVGT
void main() {
	alert("example", "data for the game could be stored at " + DIRECTORY_APPDATA + "my_game/");
}
```



### DIRECTORY_TEMP

Property that returns the system's temporary directory, a place where short-term data can be stored.

const string DIRECTORY_TEMP;

#### remarks:

A slash character is already appended to the directory returned by this property.

This function may return different values depending on the operating system the application is being run on.

* On Windows, usually C:\Users\%username%\appdata\local\temp/.

* on macOS and Linux systems, usually /tmp/.

* on Android, the app's cache path.

In any case the directory returned should be writable, though you should expect things you store there to be deleted by external factors at any time.

#### Example:

```NVGT
void main() {
	alert("example", "a temporary file for the game could be stored at " + DIRECTORY_TEMP + "filename.txt");
}
```





