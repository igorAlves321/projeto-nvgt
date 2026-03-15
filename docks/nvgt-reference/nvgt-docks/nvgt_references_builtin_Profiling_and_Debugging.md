# Profiling and Debugging
## Functions
### assert

Evaluates an expression and terminates the script execution if the result is false.

void assert(bool expression, string message = "");

#### Arguments

* expression: The expression to evaluate.

* message: The message to display if false.

#### Remarks

This is useful for testing and debugging scenarios, allowing you to report a problem.

In the event that the evaluated expression returns false, an exception is thrown, using the message parameter in the event that the exception is unhandled.

Please note that, unlike BGT, asserts can actually trigger in release builds.

#### Example:

```NVGT
void main() {
	assert(false, "I am an assertion violation. I love causing chaos!");
}
```



### c_debug_message

Print a message to the C debugger.

void c_debug_message(const string&in message);

#### Arguments:

* const string&in message: The message to print to the C debugger's console.

#### Example:

```NVGT
void main() {
	c_debug_message("I am a debug message");
	c_debug_break();
}
```



### garbage_collect

Manually triggers the garbage collector.

void garbage_collect(bool full = true);

### Arguments

full: True for a full cycle, false for a small increment.

### Remarks

If full is set to false, the garbage collector only runs a small increment. If you have set the garbage collect mode to manual, you will need to regularly call this function yourself throughout the game. Otherwise this will be done automatically every 5-25 milliseconds, either in a dedicated thread, or during a wait() operation.

If full is set to true, this will do a full cleanout. This could take considerably longer, especially in larger games, so the automatic system never does this. It is up to you to perform a full cycle at a time that is appropriate for your game.

#### Example:

```NVGT
void main() {
	garbage_collect();
}
```



### generate_profile

Returns any data stored in the profiler.

string generate_profile(bool reset = true);

###Arguments

* reset: If true, resets profile data.

#### Example:

```NVGT
void main() {
	start_profiling();
	wait(1000);
	alert("Profile", generate_profile());
}
```



### get_call_stack

Get the call stack (list of functions called) at the current point in time in your script.

string get_call_stack();

#### Returns:

string: a formatted list of the call stack.

#### Remarks:

In the context of a catch block, it's better to use the `last_exception_call_stack` property. If you use `get_call_stack()`, you'll get the callstack where you are in the try statement, as opposed to the call stack that actually caused the exception being caught.

#### Example:

```NVGT
// Define some example functions.
void test1() {test2();}
void test2() {test3();}
void test3() {
	alert("Call stack", get_call_stack());
}
void main() {
	test1();
}
```



### get_call_stack_size

Get the size of the call stack.

int get_call_stack_size();

#### Returns:

int: the size of the call stack (i.e. how many functions deep are you currently?)

#### Remarks:

This function doesn't work in the context of exceptions. If you call it in a catch block, you'll most likely get the call stack in the try block, not what actually threw the exception.

#### Example:

```NVGT
void test1() {test2();}
void test2() {test3();}
void test3() {test4();}
void test4() {
	alert("Call stack size is", get_call_stack_size());
}
void main() {
	test1();
}
```



### get_exception_file

Get the name/path of the source file where the exception occurred.

string get_exception_file();

#### Returns:

string: the name/path of the file where the exception was thrown.

#### Example:

```NVGT
void main() {
	try {
		// Throw an index-out-of-bounds error.
		string[] arr = {"a", "test"};
		string item = arr[2];
	}
	catch {
		alert("Exception file path", get_exception_file());
	}
}
```



### get_exception_function

Get the Angelscript function signature of the function that threw the exception.

string get_exception_function();

#### Returns:

string: the Angelscript function signature of the throwing function.

#### Example:

```NVGT
void main() {
	try {
		// Throw an index-out-of-bounds error.
		string[] arr = {"a", "test"};
		string item = arr[2];
	}
	catch {
		alert("Exception function signature", get_exception_function());
	}
}
```



### get_exception_info

Get informative information about an exception, for example "index-out-of-bounds".

string get_exception_info();

#### Returns:

string: information about the exception currently being caught.

#### Example:

```NVGT
void main() {
	try {
		// Throw an index-out-of-bounds error.
		string[] arr = {"a", "test"};
		string item = arr[2];
	}
	catch {
		alert("Exception info", get_exception_info());
	}
}
```



### get_exception_line

Get the line an exception occurred on.

int get_exception_line();

#### Returns:

int: the line number the exception occurred on.

#### Example:

```NVGT
void main() {
	try {
		// Throw an index-out-of-bounds error.
		string[] arr = {"a", "test"};
		string item = arr[2];
	}
	catch {
		alert("Exception line", get_exception_line());
	}
}
```



### get_last_error

Get the last error flagged by the engine.

int get_last_error();

#### Returns:

int: the error code that was flagged.

#### Remarks

This will usually be flagged for recoverable errors in functions that can't return error information directly, such as input and conversion functions, or when more information is available, such as in file or threading operations. More serious errors will usually throw exceptions.

Please note: At this time there are very few functions that make use of this flag.

#### Example:

```NVGT
void main() {
	input_box("Test", "Cancel to cause an error"); // Error is set if you cancel.
	alert("Error", get_last_error());
}
```



### is_debugger_present

Determines if your app is being ran through a debugger.

bool is_debugger_present();

#### Returns:

bool: true if a debugger is present, false otherwise.

#### Example:

```NVGT
void main() {
	bool present = is_debugger_present();
	if (present)
		alert("Info", "A debugger is present.");
	else
		alert("Info", "A debugger is not present.");
}
```



### reset_profiler

Resets the profiler.

void reset_profiler();

#### Example:

```NVGT
void main() {
	start_profiling();
	wait(1000);
	reset_profiler(); // Profiler is still running.
	wait(1000);
	alert("Profile", generate_profile());
}
```



### start_profiling

Starts the profiler.

void start_profiling();

#### Example:

```NVGT
void main() {
	start_profiling();
	wait(1000);
	alert("Profile", generate_profile());
}
```



### stop_profiling

Stops and resets the profiler.

void stop_profiling();

#### Example:

```NVGT
void main() {
	start_profiling();
	wait(1000);
	stop_profiling();
	wait(1000);
	start_profiling();
	wait(1000);
	alert("Profile", generate_profile());
}
```



### throw

Throws an exception with a particular message.

void throw(const string&in msg);

#### Arguments:

* const string&in msg: the message to include in your exception.

#### Remarks:

This is presently slightly limited, the only value of the exception you can set is the message. There are plans to expand this in the future.

#### Example:

```NVGT
void main() {
	throw("Something went horribly wrong");
}
```




## Global Properties
### garbage_collect_auto_frequency

Controls how often extra garbage collection is performed in automatic modes. Default is 300000 milliseconds (5 minutes). Valid values are from 2000 (2 seconds) to 86400000 (24 hours).

int garbage_collect_auto_frequency;

### Remarks

When this interval has passed, the system will lightly perform extra garbage cleanup.

#### Example:

```NVGT
void main() {
	alert("GC frequency", garbage_collect_auto_frequency);
}
```



### garbage_collect_mode

Set or retrieve the mode for the garbage collector. Default is 2 (see remarks below).

int garbage_collect_mode;

### Remarks

This has a range of 1 to 3, where:

1 is manual (you are responsible for calling the garbage_collect function when convenient).

2 is automatic (called every wait() cycle on the main thread before sleeping).

3 is asynchronous (same as 2, but called on a dedicated thread).

#### Example:

```NVGT
void main() {
	alert("GC mode", garbage_collect_mode);
}
```



### last_exception_call_stack

Returns the call stack of the currently thrown exception.

string last_exception_call_stack;

#### Remarks:

In the context of a catch block, it's better to use this property over `get_call_stack()`. In a catch block, `get_call_stack()` will return the callstack where you are in the try statement, as opposed to the call stack that actually caused the exception being caught.

#### Example:

```NVGT
void test1() {test2();}
void test2() {throw("I am an exception");}
void main() {
	try {
		test1();
	}
	catch {
		alert("Call stack", last_exception_call_stack);
	}
}
```



### SCRIPT_COMPILED

Determine if the script is compiled or not. I.e., are you running from source?

bool SCRIPT_COMPILED;

#### Example:

```NVGT
void main() {
	alert("Example", SCRIPT_COMPILED ? "The script is currently compiled" : "The script is not currently compiled");
}
```



### SCRIPT_CURRENT_FILE

Returns the current file your script is running form.

string SCRIPT_CURRENT_FILE;

#### Example:

```NVGT
void main() {
	alert("Your script is contained in", SCRIPT_CURRENT_FILE);
}
```



### SCRIPT_CURRENT_FUNCTION

Returns the signature of the current function in your script.

string SCRIPT_CURRENT_FUNCTION;

#### Example:

```NVGT
void main() {
	alert("The current function is", SCRIPT_CURRENT_FUNCTION);
	random_func("", 0, 0, 0);
}
// Function with random unused parameters to showcase the function signatures.
bool random_func(const string& in a, int b, uint64 c, uint8 = 1) {
	alert("The current function is", SCRIPT_CURRENT_FUNCTION);
	return true;
}
```



### SCRIPT_CURRENT_LINE

Returns the current line in your script as it's executing.

string SCRIPT_CURRENT_LINE;

#### Example:

```NVGT
void main() {
	alert("The current line is", SCRIPT_CURRENT_LINE);
}
```



### SCRIPT_EXECUTABLE

Returns the path of the executable running your script.

string SCRIPT_EXECUTABLE;

#### Remarks:

If you're running from source, this will return the path to your NVGT binary.

#### Example:

```NVGT
void main() {
	alert("The executable path of the script is", SCRIPT_EXECUTABLE);
}
```





