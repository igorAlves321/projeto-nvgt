# Environment
In this reference, the environment section specifically refers to the script/system environment that your program is being run on. Examples could include the current line number in the nvgt script being compiled, the operating system being run on or fetching the value of a shell environment variable.


## Enums
### system_power_state
This is a list of possible values returned from the `system_power_info()` function.

* POWER_STATE_ERROR: an error was encountered.
* POWER_STATE_UNKNOWN: the power state is unknown.
* POWER_STATE_ON_BATTERY: the system is running on  battery power.
* POWER_STATE_NO_BATTERY: the system has no battery installed.
* POWER_STATE_CHARGING: the battery is currently recharging.
* POWER_STATE_CHARGED: the battery is fully charged, but still actively plugged in.



## Functions
### chdir

Change the current working directory.

bool chdir(const string&in new_directory);

#### Arguments:

* const string&in new_directory: The directory you'd like to change into. Note that this directory must already exist.

#### Returns:

bool: true if NVGT could set the current working directory to the specified directory; false otherwise.

#### Example:

```NVGT
void main() {
	string directory = input_box("Chdir Test", "Enter a valid path to a directory: ");
	// Could we switch to it?
	if (chdir (directory))
		alert("Success", "That directory is valid and could be switch to.");
	else 
		alert("Failure", "The directory could not be switched to. Check that you have typed the name correctly and that the directory exists.");
}
```



### cwdir

Check the current working directory.

string cwdir();

#### Returns:

string: a string containing the current working directory.

#### Example:

```NVGT
void main() {
	alert("Current Working Directory is", cwdir());
}
```



### environment_variable_exists

Check if the given environment variable exists.

bool environment_variable_exists(const string&in name);

#### Arguments:

* const string&in name: the name of the environment variable to check.

#### Returns:

bool: true if the specified environment variable exists, false otherwise.

#### Example:

```NVGT
void main() {
	bool exists = environment_variable_exists("PATH");
	if (exists)
		alert("Info", "The PATH variable exists.");
	else
		alert("Info", "The PATH variable does not exist.");
}
```



### expand_environment_variables

Expand environment variables.

string expand_environment_variables(const string&in variables);

#### Arguments:

* const string&in variables: A string containing the variable(s) you wish to expand.

#### Returns:

string: the expanded environment variable(s) if successful or an empty string if not.

#### Example:

```NVGT
void main() {
	// The end goal here is to obtain the user's home directory on the running system if possible. This logic happens in a below function; here we just display the result.
	alert("Result", get_home_directory());
}
string get_home_directory() {
	if (system_is_windows) return expand_environment_variables("%USERPROFILE%");
	else if (system_is_unix) return expand_environment_variables("$HOME");
	else return "Unknown";
}
```



### get_preferred_locales

Get a list of the user's preferred locales.

string[]@ get_preferred_locales();

#### Returns:

string[]@: a handle to an array containing the locale names (as strings).

#### Example:

```NVGT
void main() {
	string[]@ locales = get_preferred_locales();
	string result; // To be shown to the user.
	for (uint i = 0; i < locales.length(); i++)
		result += locales[i] + ",\n";
	// Strip off the trailing comma and new line.
	result.trim_whitespace_right_this();
	result.erase(result.length() - 1);
	alert("Info", "The locales on your system are: " + result);
}
```



### system_power_info

Determine the state of the system's battery.

system_power_state system_power_info(int&out seconds = void, int&out percent = void);

#### Arguments:

* int&out seconds = void: Where to store the number of remaining charge time in seconds.

* int&out percent = void: Where to store the percentage of battery charge remaining.

#### Returns:

system_power_state: One of the system_power_state constants.

#### Remarks:

This could be useful for various reasons, such as backing up game data on low battery or showing extra mercy to online game players who run out of battery power who you might otherwise punish/tag for unlawful disconnection.

If the battery percentage or time remaining cannot be determined, that value will be set to -1.

Whether a time or percentage is available is up to the underlying operating system.

#### Example:

```NVGT
// Utility function to convert a system_power_state to a string.
string describe_power_state(system_power_state st) {
	switch (st) {
		case POWER_STATE_ERROR: return "error";
		case POWER_STATE_ON_BATTERY: return "on battery";
		case POWER_STATE_NO_BATTERY: return "no battery";
		case POWER_STATE_CHARGING: return "charging";
		case POWER_STATE_CHARGED: return "charged";
		default: return "unknown";
	}
}
void main() {
	system_power_state old_state = system_power_info();
	show_window(describe_power_state(old_state));
	while (!key_pressed(KEY_ESCAPE) and !key_pressed(KEY_AC_BACK)) {
		wait(5);
		int seconds, percent;
		system_power_state st = system_power_info(seconds, percent);
		if (st != old_state) show_window(describe_power_state(st));
		old_state = st;
		if (key_pressed(KEY_SPACE)) {
			string time_str = seconds > -1? " (" + timespan(seconds, 0).format() + ")" : "";
			screen_reader_speak(percent > -1? percent + "%" + time_str : "unable to determine battery percent");
		}
	}
}
```



### write_environment_variable

Write to an environment variable.

void write_environment_variable(const string&in variable, const string&in value);

#### Arguments:

* const string&in variable: The environment variable you wish to write to.

* const string&in value: The value you wish to write to this variable.

#### Example:

```NVGT
void main() {
	write_environment_variable("NVGT_Test_for_docs", "Testing");
	alert("Result", read_environment_variable("NVGT_Test_for_docs"));
}
```




## Global Properties
### COMMAND_LINE

COMMAND_LINE returns anything that is passed as command line arguments. Note that it returns anything after the application name, and keep in mind that you will have to parse the output yourself (basic example below).

const string COMMAND_LINE;

#### Example:

```NVGT
void main() {
	const string[]@ arguments = COMMAND_LINE.split(" ");
	// Did we get any arguments?
	if (arguments[0] == "")
		alert("Command Line", "No arguments provided.");
	else
		alert("Command Line", "The first argument is " + arguments[0]);
}
```



### PLATFORM

This property returns a string containing the current platform, such as "Windows NT".

const string PLATFORM;

#### Example:

```NVGT
void main() {
	alert("Your current Platform  is", PLATFORM);
}
```



### PLATFORM_ARCHITECTURE

This property returns a string containing the current platform architecture, such as "AMD64".

const string PLATFORM_ARCHITECTURE;

#### Example:

```NVGT
void main() {
	alert("Your current Platform architecture is", PLATFORM_ARCHITECTURE);
}
```



### PLATFORM_DISPLAY_NAME

This property returns a string containing the current platform display name, such as "Windows 8".

const string PLATFORM_DISPLAY_NAME;

#### Remarks:

Due to a backwards compatibility problem in windows, this function by default will cap out at Windows 8 even if the user is running a newer version of Windows. If determining the most modern windows version on the user's system is important to you, you can create a gamename.exe.manifest file to target your app for modern windows. Here is some [microsoft documentation](https://learn.microsoft.com/en-us/windows/win32/sysinfo/targeting-your-application-at-windows-8-1) that explains how, you can probably just use the example manifest provided there.

#### Example:

```NVGT
void main() {
	alert("Your current Platform display name is", PLATFORM_DISPLAY_NAME);
}
```



### PLATFORM_VERSION

This property returns a string containing the current platform version, such as "6.2 (Build 9200)".

const string PLATFORM_VERSION;

#### Example:

```NVGT
void main() {
	alert("Your current Platform version is", PLATFORM_VERSION);
}
```



### PROCESSOR_COUNT

This property returns the number of processors on your system. Note that this returns the number of threads, not physical cores.

const uint PROCESSOR_COUNT;

#### Example:

```NVGT
void main() {
	alert("Processor Threads Count", PROCESSOR_COUNT);
}
```



### system_is_chromebook

This property is true if the application is running on a Google Chromebook.

const bool system_is_chromebook;

#### Example:

```NVGT
void main() {
	if(system_is_chromebook)
		alert("example", "This application is running on a chromebook!");
	else
		alert("example", "This application is not running on a chromebook.");
}
```



### system_is_DeX_mode

This property is true if the application is running in Samsung DeX mode, which is a desktop-like environment available on certain Samsung devices. It allows a mobile device to provide a desktop experience when connected to an external display.

const bool system_is_DeX_mode;

#### Example:

```NVGT
void main() {
	if(system_is_DeX_mode)
		alert("example", "This application is running in Samsung DeX mode!");
	else
		alert("example", "This application is not running in Samsung DeX mode.");
}
```



### system_is_mobile

This property is true if the application is running on any mobile device, for example a cell phone.

const bool system_is_mobile;

#### Example:

```NVGT
void main() {
	if(system_is_mobile)
		alert("example", "This application is running on a mobile device!");
	else
		alert("example", "This application is not running on a mobile device.");
}
```



### system_is_tablet

This property is true if the application is running on any device that identifies itself as a tablet.

const bool system_is_tablet;

#### Example:

```NVGT
void main() {
	if(system_is_tablet)
		alert("example", "This application is running on a tablet!");
	else
		alert("example", "This application is not running on a tablet.");
}
```



### system_is_unix

This property is true if the application is running on a unix operating system, which in regards to NVGT's platforms is almost everything other than windows.

const bool system_is_unix;

#### Example:

```NVGT
void main() {
	if(system_is_unix)
		alert("example", "This application is running on a unix operating system!");
	else
		alert("example", "This application is probably running on windows, or in any case not a unix operating system");
}
```



### system_is_windows

This property is true if the application is running on a windows operating system.

const bool system_is_windows;

#### Example:

```NVGT
void main() {
	if(system_is_windows)
		alert("example", "This application is running on windows!");
	else
		alert("example", "This application is not running on windows.");
}
```



### system_node_id

This property returns the node ID, or another words, primary MAC address, of your system.

const string system_node_id;

#### Example:

```NVGT
void main() {
	alert("Your system node/host ID is", system_node_id);
}
```



### system_node_name

This property returns the node name, or another word, host name, of your system.

const string system_node_name;

#### Example:

```NVGT
void main() {
	alert("Your system node/host name is", system_node_name);
}
```





