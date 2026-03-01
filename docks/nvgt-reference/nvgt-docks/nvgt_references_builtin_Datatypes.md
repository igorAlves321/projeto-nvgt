# Datatypes
In this documentation, we consider a datatype to be any class or primitive that typically stores one value. While such a datatype could contain a pointer/handle to a more complex type that may store many values (in which case the handle itself is the single value the datatype contains), the types documented here do not directly contain more than one piece of data be that a string of text, a dynamically typed handle or just a simple number.

Beware that a few of these datatypes may get quite advanced, and you are not expected to understand what all of them do (particularly the dynamically typed ones) during the course of normal game development. Instead, we recommend learning about basic datatypes here, and then coming back and looking at any that seemed confusing at first glance when you are trying to solve a particular problem usually relating to a variable you have that needs to be able to store more than one kind of value.


## any

A class that can hold one object of any type, most similar to a dictionary in terms of usage but with only one value and thus no keys.

1. any();

2. any(?&in value);

### Arguments (2):

* ?&in value: The default value stored in this object.

### Remarks:

Though NVGT uses Angelscript which is a statically typed scripting language, there are sometimes occasions when one may not know the type of value that could be stored in a variable, or may want to create a function that can accept an argument of any type. While this isn't the only way to do so, the any object provides a safe way to accomplish this task, possibly the safest / least restrictive of all available such options. There should be no type that this object can't store.

The biggest downside to this class is simply that storing and retrieving values from it is just as bulky as the usual way of doing so from dictionary objects. That is, when retrieving a value one must first create a variable then call the any::retrieve() method passing a reference to that variable.

something to note is that the constructor of this class is not marked explicit, meaning that if you create a function that takes an any object as it's argument, the user would then be able to directly pass any type to that argument of your function without any extra work.

Again just like with dictionaries, there is no way to determine the type of a stored value. Instead if one wants to print the value contained within one of these variables, they must carefully attempt the retrieval with different types until it succeeds where the value can then be printed.

### Example:

```NVGT
// Lets create a version of the join function that accepts an array of any objects and supports numbers, strings, and vectors.
string anyjoin(any@[]@ args, const string&in delimiter) {
	if (@args == null) return ""; // Nobody should ever be passing the null keyword to this function, but if they do this line prevents an exception.
	string[] args_as_strings;
	for (uint i = 0; i < args.length() && args[i] != null; i++) {
		// We must attempt retrieving each type we wish to support.
		int64 arg_int;
		double arg_double;
		string arg_string;
		vector arg_vector;
		if (args[i].retrieve(arg_string)) args_as_strings.insert_last(arg_string);
		else if (args[i].retrieve(arg_vector)) args_as_strings.insert_last("(%0, %1, %2)".format(arg_vector.x, arg_vector.y, arg_vector.z));
		else if (args[i].retrieve(arg_double)) args_as_strings.insert_last(arg_double);
		else if (args[i].retrieve(arg_int)) args_as_strings.insert_last(arg_int);
		else args_as_strings.insert_last("<unknown type>");
	}
	return join(args_as_strings, delimiter);
}
void main() {
	string result = anyjoin({"the player has", 5, "lives, has", 32.97, "percent health, and is at", vector(10, 15, 0)}, " ");
	alert("example", result);
}
```



### Methods
#### retrieve
Fetch the value from an any object and store it in a variable.

`bool retrieve(?&out result);`

##### Arguments:
* ?&out result: A variable that the value should be copied into.

##### Returns:
bool: true if successful, false if the variable supplied is of the wrong type.

##### Example:
See the main any chapter where this function is used several times.


#### store

Store a new value in an any object, replacing an existing one.

void store(?&in value);

##### Arguments:

* ?&in value: The value that should be stored (can be any type).

##### Example:

```NVGT
void main() {
	int number;
	string text;
	any example;
	example.store("hello");
	example.retrieve(text); // Check the return value of the retrieve function for success if you are not certain of what type is stored.
	example.store(42); // The previous text value has now been deleted.
	example.retrieve(number);
	alert(text, number);
}
```





## ref

A class that can hold an extra reference to a handle of any type.

1. ref();

2. ref(const ?&in handle);

### Arguments (2):

* const ?&in handle: The handle that this ref object should store at construction.

### Remarks:

In Angelscript, a handle is the simplest method of pointing multiple variables at a single object, or passing an object to a function without copying it in memory. If you know any c++, it is sort of like a c++ shared pointer. You can only create a handle to a complex object, and a few built-in NVGT objects do not support them such as the random number generators because they are registered as value types. Describing handles much further is beyond the scope of this reference chapter, but you can [learn more about handles from the Angelscript documentation](https://www.angelcode.com/angelscript/sdk/docs/manual/doc_script_handle.html) including why a few complex objects in NVGT don't support them.

Usually handles must be typed to the object they are pointing at, for example I could create a variable called `dictionary@ d;~ to create an empty handle to a dictionary object.

The type restriction on handles is almost always perfectly ok, however in a few super rare cases it can become bothersome or could make a coding task more tedious. The ref object is a workaround for that. Where ever typed handles can be used to point to an object, a ref object could point to it as well.

Unlike normal typed handles, one must cast a ref object back to the type it is storing in order to actually call methods or access properties of the stored type.

The = (assignment) operator is supported which causes the ref object to point to the value supplied, and the == (equality) operator is supported to compare whether a ref object and either another ref object or typed handle are pointing to the same actual object.

### Example:

```NVGT
// Lets create a function that can set the volume of either a mixer or a sound object.
void set_volume(ref@ obj, int volume) {
	mixer@ m = cast<mixer@>(obj);
	if (@m != null) {
		m.set_volume(volume);
		return;
	}
	sound@ s = cast<sound@>(obj);
	if (@s != null) s.set_volume(volume);
}
void main() {
	sound my_sound;
	my_sound.load("c:\\windows\\media\\ding.wav");
	mixer mix;
	my_sound.set_mixer(mix);
	set_volume(mix, -5);
	alert("mixer volume", mix.volume);
	set_volume(my_sound, -10);
	alert("sound volume", my_sound.volume);
	my_sound.close();
}
```




## string
### Methods
#### count

Count the number of times a substring appears in another string.

uint64 string::count(const string&in search, uint64 start = 0);

##### Arguments:

* const string&in search: the substring to search for.

* uint64 start = 0: the zero-based position to start searching at.

##### Returns:

uint64: the number of occurances of the given substring found.

##### Example:

```NVGT
void main() {
	alert("test", "testtest".count("test"));
}
```



#### empty

Check to see if a string is empty.

1. bool string::empty();

2. bool string::is_empty();

##### Returns:

bool: True if the string is empty; false otherwise.

##### Example:

```NVGT
void main() {
	string test = input_box("String is Empty Tester", "Enter a string.");
	if (test.empty())
		alert("String is Empty Tester", "The string appears to be empty.");
	else
		alert("String is Empty Tester", "The string isn't empty.");
}
```



#### ends_with

Determines if a string ends with another string.

bool string::ends_with(const string&in str);

##### Arguments:

* const string&in str: the string to look for.

##### Returns:

bool: true if the string ends with the specified search, false if not.

##### Example:

```NVGT
void main() {
	string suffix = "test";
	string text = input_box("Test", "Enter a string");
	if (text.is_empty()) {
		alert("Info", "Nothing was entered.");
		exit();
	}
	if (text.ends_with(suffix))
		alert("Info", "The entered string ends with " + suffix);
	else
		alert("Info", "The entered string does not end with " + suffix);
}
```



#### erase

Remove a portion of a string, starting at a given index.

void string::erase(uint pos, int count = -1);

##### Arguments:

* uint pos: the position to start erasing from.

* int count = -1: the number of characters to erase after the specified index. If -1, erases all characters starting at the given pos until the end of the string.

##### Remarks

Please note this modifies the calling string. To keep the original you will need to make a copy.

In the event of boundary errors (start + count >= length), an exception is thrown.

##### Example:

```NVGT
void main() {
	string text = input_box("String", "enter at least a 3-character string.");
	if (text.length() < 3) {
		alert("Info", "Your string must be at least three characters.");
		exit(1);
	}
	alert("Before removal, the string is", text);
	text.erase(2);
	alert("After removal, the string is", text);
}
```



#### escape

Modify a string with suitable escape sequencing.

string string::escape(bool strict_JSON = false);

##### Arguments:

* strict_JSON: Use JSON escaping. Defaults to false if not specified.

##### Returns:

string: A new string with the escaped data.

##### Remarks

The strict_JSON parameter is only necessary under special circumstances, namely the escape behaviour for characters \x7 and \xb. If you know you won't be touching these characters, you can merely call escape without a parameter and it will still escape safely.

##### Example:

```NVGT
void main() {
	string test="test\xbtest";
	alert("Escaped", test.escape(false));
	alert("Escaped", test.escape(true));
}
```



#### find
Find the position of a substring from within a string.

`int string::find(const string &in search, uint start = 0);`

##### Arguments:
* search: The string to search for.
* start: The index to start searching from. Default is 0 (beginning).

##### Returns
The position where the substring starts if found, or -1 otherwise.

##### Remarks
If the start is less than 0, -1 is returned.


#### find_first
Find the position of a substring from within a string.

`int string::find_first(const string &in search, uint start = 0);`

##### Arguments:
* search: The string to search for.
* start: The index to start searching from. Default is 0 (beginning).

##### Returns
The position where the substring starts if found, or -1 otherwise.

##### Remarks
If the start is less than 0, -1 is returned.

This appears to be an alias for string::find.


#### find_first_not_of
Find the first occurrence of any character that is not present in the search string.

`int string::find_first_not_of(const string &in search, uint start = 0);`

##### Arguments:
* search: The characters to exclude in a match.
* start: The index to start searching from. Default is 0 (beginning).

##### Returns
The position where a match was found, or -1 otherwise.

##### Remarks
This can be useful in several scenarios, such as splitting strings or quickly finding out if your string has invalid characters. A scenario where this could be useful is if you are finding parts of a URL or path, you might want to `find_first_not_of(":\\/.")`.


#### find_first_of
Find the first occurrence of any character in the search string.

`int string::find_first_of(const string &in search, uint start = 0);`

##### Arguments:
* search: A string of characters to search for.
* start: The index to start searching from. Default is 0 (beginning).

##### Returns
The position where a match was found, or -1 otherwise.

##### Remarks
Where find and find_first will find an occurrence of an entire substring, this will match any character. This is useful, for instance, if you need to search for delimiters before splitting.


#### find_last
Find the position of a substring from within a string, searching right to left.

`int string::find_last(const string &in search, uint start = -1);`

##### Arguments:
* search: The string to search for.
* start: The index to start searching from. Default is -1 (end).

##### Returns
The position where the substring starts if found, or -1 otherwise.

##### Remarks
This is useful if what you need to find is closer to the end of a string than the start.

This appears to be an alias for string::rfind.


#### find_last_not_of
Find the first occurrence of any character that is not present in the search string, searching from right to left.

`int string::find_last_not_of(const string &in search, uint start = 0);`

##### Arguments:
* search: The characters to exclude in a match.
* start: The index to start searching from. Default is -1 (end).

##### Returns
The position where a match was found, or -1 otherwise.

##### Remarks
This can be useful in several scenarios, such as splitting strings or quickly finding out if your string has invalid characters. A scenario where this could be useful is if you are finding parts of a URL or path, you might want to `find_last_not_of(":\\/.")`.


#### find_last_of
Find the first occurrence of any character in the search string, searching right to left.

`int string::find_last_of(const string &in search, uint start = 0);`

##### Arguments:
* search: a string of characters to search for.
* start: The index to start searching from. Default is -1 (end).

##### Returns
The position where a match was found, or -1 otherwise.

##### Remarks
Where find and find_last will find an occurrence of an entire substring, this will match any character. This is useful, for instance, if you need to search for delimiters before splitting.


#### format

Formats a string with placeholders.

string string::format(const ?&in = null...);

##### Arguments:

* const ?&in = null: Any stringable value. You can pass up to 16 parameters.

##### Returns:

Returns the formatted string.

##### Remarks:

This method is useful in situations when:

1. You want to have multiple formats for messages, such as short and long messages.

2. You don't want to use concatenation.

3. You want to use a placeholder more than once in a string.

##### Example:

```NVGT
void main() {
	string[] greetings = {"Hello %0! How are you?", "Hola %0! ¿Cómo estás?"};
	string[] messages = {"You have %0 health", "%0 health"};
	alert("Greeting:", greetings[random(0, 1)].format("Literary"));
	alert("Message:", messages[random(0, 1)].format(1000));
}
```



#### insert
Insert a string into another string at a given position.

`void string::insert(uint pos, const string&in other);`

##### Arguments:
* uint pos: the index to insert the other string at.
* const string&in other: the string to insert.

##### Remarks
Please note this modifies the calling string. To keep the original you will need to make a copy.

If pos is out of bounds, an exception is thrown.


#### is_alphabetic

Checks whether a string contains only alphabetical characters and nothing else.

bool string::is_alphabetic(string encoding = "UTF8");

##### Arguments:

* string encoding = "UTF8": The encoding to check against, with the UTF8 encoding being cached for speed.

##### Returns:

bool: true if the input string contains only alphabetic characters, false otherwise.

##### Remarks:

This function only returns true if the string contains only alphabetical characters in the given encoding. If a single other non-alphabetical character is encountered, this function will return false.

If this function is called on a string that contains data that is not in the specified encoding, the results are undefined.

##### Example:

```NVGT
void main() {
	alert("example", "aabdslf".is_alphabetic()); // Should show true.
	string input = input_box("example", "enter a string");
	if(input.empty()) {
		alert("Info", "You must type a string.");
		exit(1);
	}
	if(input.is_alphabetic())
		alert("example", "you typed a string that contains only alphabetical characters");
	else
		alert("example", "this string contains more than just alphabetical characters");
}
```



#### is_alphanumeric

Checks whether a string contains only alphabetical or numeric characters and nothing else.

bool string::is_alphanumeric(string encoding = "UTF8");

##### Arguments:

* string encoding = "UTF8": The encoding to check against, with the UTF8 encoding being cached for speed.

##### Returns:

bool: true if the input string contains only alphabetic or numeric characters, false otherwise.

##### Remarks:

This function only returns true if the string contains only alphabetical or numeric characters in the given encoding. If a single other non-alphanumeric character is encountered, this function will return false.

If this function is called on a string that contains data that is not in the specified encoding, the results are undefined.

##### Example:

```NVGT
void main() {
	alert("example", "aabdslf".is_alphanumeric()); // Should show true.
	string input = input_box("example", "enter a string");
	if(input.empty()) {
		alert("Info", "You must type a string.");
		exit(1);
	}
	if(input.is_alphanumeric())
		alert("example", "you typed a string that contains only alphanumeric characters");
	else
		alert("example", "this string contains more than just alphanumeric characters");
}
```



#### is_digits

Checks if a string is only digits (numbers).

##### Arguments:

* string encoding = "UTF8": The encoding to check against, with the UTF8 encoding being cached for speed.

##### Returns:

bool: true if the input string is only digits; false otherwise.

##### Remarks:

This function only returns true if the string contains digits in the given encoding. If a single non-numaric character is encountered, this function will return false.

If this function is called on a string that contains data that is not in the specified encoding, the results are undefined.

##### Example:

```NVGT
void main() {
	alert("Example", "123".is_digits()); // Should return true.
	string input = input_box("Example", "Enter a string");
	if (input.is_digits()) alert("Example", "This string is only digits.");
	else alert("Example", "This input contains non-numaric characters.");
}
```



#### is_lower

Checks whether a string is completely lowercase.

bool string::is_lower(string encoding = "UTF8");

##### Arguments:

* string encoding = "UTF8": The encoding to check against, with the UTF8 encoding being cached for speed.

##### Returns:

bool: true if the input string is lowercase.

##### Remarks:

This function only returns true if the string contains only lowercase characters in the given encoding. If a single uppercase or punctuation character is encountered, this function will return false.

If this function is called on a string that contains data that is not in the specified encoding, the results are undefined.

##### Example:

```NVGT
void main() {
	alert("example", "HELLO".is_lower()); // Should show false.
	string input = input_box("example", "enter a string");
	if(input.is_empty())
		exit();
	if(input.is_lower())
		alert("example", "you typed a lowercase string");
	else
		alert("example", "you did not type a lowercase string");
}
```



#### is_punctuation

Checks whether a string contains only punctuation characters and nothing else.

bool string::is_punctuation(string encoding = "UTF8");

##### Arguments:

* string encoding = "UTF8": The encoding to check against, with the UTF8 encoding being cached for speed.

##### Returns:

bool: true if the input string contains only punctuation characters.

##### Remarks:

This function only returns true if the string contains only punctuation characters in the given encoding. If a single alphanumeric or other non-punctuation character is encountered, this function will return false.

If this function is called on a string that contains data that is not in the specified encoding, the results are undefined.

##### Example:

```NVGT
void main() {
	alert("example", ".?!".is_punctuation()); // Should show true.
	string input = input_box("example", "enter a string");
	if(input.is_empty())
		exit();
	if(input.is_punctuation())
		alert("example", "you typed a string that contains only punctuation characters");
	else
		alert("example", "this string contains more than just punctuation");
}
```



#### is_upper

Checks whether a string is completely uppercase.

bool string::is_upper(string encoding = "UTF8");

##### Arguments:

* string encoding = "UTF8": The encoding to check against, with the UTF8 encoding being cached for speed.

##### Returns:

bool: true if the input string is uppercase.

##### Remarks:

This function only returns true if the string contains only uppercase characters in the given encoding. If a single lowercase or punctuation character is encountered, this function will return false.

If this function is called on a string that contains data that is not in the specified encoding, the results are undefined.

##### Example:

```NVGT
void main() {
	alert("example", "HELLO".is_upper()); // Should show true.
	string input = input_box("example", "enter a string");
	if(input.is_empty())
		exit();
	if(input.is_upper())
		alert("example", "you typed an uppercase string");
	else
		alert("example", "you did not type an uppercase string");
}
```



#### length

Returns the length (how large a string is).

1. uint string::length();

2. uint string::size();

##### returns:

uint: The length of a string.

##### Remarks:

Note: This returns the length in bytes, rather than characters of any given text encoding.

##### Example:

```NVGT
void main() {
	string test = input_box("String Length Tester", "Enter a string to see its length.");
	if (test.length() <= 0)
		alert("String Length Tester", "You appear to have provided an empty string!");
	else if (test.length() == 1)
		alert("String Length Tester", "You appear to have only provided a single character!");
	else
		alert("String Length Tester", "The provided string is " + test.length()+" characters!");
}
```



#### lower

Converts a string to lowercase, returning a new string.

string string::lower();

##### Returns:

string: the specified string in lowercase.

##### Example:

```NVGT
void main() {
	string text = input_box("Text", "Enter the text to convert to lowercase.");
	if (text.empty()) {
		alert("Info", "You typed a blank string.");
		exit(1);
	}
	alert("Your string lowercased is", text.lower());
}
```



#### lower_this

Converts a string to lowercase, modifying the calling string object.

string& string::lower();

##### Returns:

string&: a reference to the specified string in lowercase.

##### Example:

```NVGT
void main() {
	string text = input_box("Text", "Enter the text to convert to lowercase.");
	if (text.empty()) {
		alert("Info", "You typed a blank string.");
		exit(1);
	}
	text = text.lower_this();
	alert("Your string lowercased is", text);
}
```



#### remove_UTF8_BOM

Remove the UTF-8 BOM from a string.

string string::remove_UTF8_BOM();

##### Arguments:

None.

##### Returns:

None.

##### Remarks

A BOM (Byte Order Mark) is a special marker used at the beginning of a text file to indicate the byte order of multi-byte character encodings, such as UTF-16 or UTF-32. Byte order refers to how multi-byte values are stored in memory, for example, little-endian (least significant byte first) or big-endian (most significant byte first).

While UTF-8 does not require a BOM due to its self-synchronizing, byte-based encoding, some older applications rely on it to detect that a file is encoded in UTF-8.

In UTF-8, the BOM is represented as the byte sequence \xEF\xBB\xBF. If present, it appears at the very beginning of the string or file.

Note: This modifies the calling string. If you need to preserve the BOM for later, you will need to make a copy of the string before processing or else reconstruct it manually.

##### Example:

```NVGT
void main() {
	string test="\xEF\xBB\xBFtest";
	test.remove_UTF8_BOM();
	alert("No BOM", test);
}
```



#### replace
Try to find any occurrences of a particular string, and replace them with a substitution in a given string object, returning a new string.

`string string::replace(const string&in search, const string&in replacement, bool replace_all = true);`

##### Arguments:
* const string&in search: the string to search for.
* const string&in replacement: the string to replace the search text with (if found).
* bool replace_all = true: whether or not all occurrences should be replaced, or only the first one.

##### Returns:
string: the specified string with the replacement applied.


#### replace_characters
Replace a group of characters with another group of characters, returning a new string.

`string string::replace_characters(const string&in character_list, const string&in replace_with);`

##### Arguments:
* character_list: The list of characters to replace.
* replace_with: The characters to replace them with.

##### Returns:
string: A new string with the replacements applied.

##### Remarks
Characters are replaced in sequence: The first character in the list is replaced with the first character in the replace string, the second with the second and so on. Thus, `"ladies".replace_characters("ld", "bb")` will return "babies".

The comparison is case-sensitive. `"ladies".replace_characters("LD", "bb")` will still return "ladies".

If the replacement string is shorter than the character list, the remaining characters in the list will be erased.

If the replacement string is longer than the character list, excess characters are ignored.


#### replace_characters_this
Replace a group of characters with another group of characters, modifying the calling string.

`string& string::replace_characters(const string&in character_list, const string&in replace_with);`

##### Arguments:
* character_list: The list of characters to replace.
* replace_with: The characters to replace them with.

##### Returns:
string: A reference to the calling string with the replacements applied.

##### Remarks
Characters are replaced in sequence: The first character in the list is replaced with the first character in the replace string, the second with the second and so on. Thus, `"ladies".replace_characters("ld", "bb")` will return "babies".

The comparison is case-sensitive. `"ladies".replace_characters("LD", "bb")` will still return "ladies".

If the replacement string is shorter than the character list, the remaining characters in the list will be erased.

If the replacement string is longer than the character list, excess characters are ignored.


#### replace_range
Replace a specified number of characters at the provided index with a new string.

`string string::replace_range(uint start, int count, const string&in replacement);`

##### Arguments:
* uint start: The position to insert the new string.
* int count: The number of characters to replace.
* const string&in replacement: the string to insert.

##### Returns:
string: the specified string with the replacement applied.

##### Remarks
Note the word "replace" here implies the deletion of an old string and adding a new string in its place. A better, though still slightly ambiguous word might be "overwrite". It is similar, though by no means identical, to the following:
```
string.erase(start, count);
string.insert(start, replacement);
```

In the event of boundary errors (start + count >= length), an exception is thrown.

If count <= 0, no processing takes place.


#### replace_this
Try to find any occurrences of a particular string, and replace them with a substitution in a given string object, modifying the calling string.

`string& string::replace_this(const string&in search, const string&in replacement, bool replace_all = true);`

##### Arguments:
* const string&in search: the string to search for.
* const string&in replacement: the string to replace the search text with (if found).
* bool replace_all = true: whether or not all occurrences should be replaced, or only the first one.

##### Returns:
string&: a two-way reference to the specified string with the replacement applied.


#### resize

Resize a string to a particular size (in bytes).

void string::resize(uint new_size);

##### Arguments:

* uint new_size: the new size of the string (in bytes).

##### Example:

```NVGT
void main() {
	string test = "abcdef";
	alert("The string is", test.length() + " characters");
	test.resize(3);
	alert("The string is", test.length() + " characters");
}
```



#### reverse

Reverse a string.

string string::reverse(string encoding = "UTF8");

##### Arguments:

* string encoding = "UTF8": The string's encoding, with UTF8 cached for speed.

##### Returns:

string: The specified string in reverse.

##### Remarks:

This function reverses the characters of a string based on a given encoding. To reverse the raw bytes of a string, for example if you are operating on binary data, see the reverse_bytes function instead.

##### Example:

```NVGT
void main() {
	string text = input_box("Text", "Enter some text to reverse.");
	if (text.is_empty()) {
		alert("Info", "nothing was entered.");
		exit();
	}
	string result = text.reverse();
	alert("Reversed string", result);
}
```



#### reverse_bytes

Reverses the raw bytes contained within a string.

string string::reverse_bytes();

##### Returns:

string: A copy of the string with it's bytes reversed.

##### Remarks:

If you want to reverse the characters within a string given an encoding such as UTF8, use the reverse method instead.

##### Example:

```NVGT
void main() {
	string raw = hex_to_string("1a2b3c4d");
	raw = raw.reverse_bytes();
	alert("reverse_bytes", string_to_hex(raw)); // Should show 4D3C2B1A.
	// Lets make it clear how this function differs from string::reverse. We'll make a string of emojis and show the results of both methods.
	string emojis = "🦟🦗🐜🐝🐞🦂🕷";
	alert("emojis reversed properly", emojis.reverse()); // string::reverse takes the UTF8 encoding into account.
	alert("broken emojis", emojis.reverse_bytes()); // This string no longer contains valid character sequences, and so the emoticons will most certainly not show correctly. Aww you can see if you run this example that it seems even string::reverse_bytes() can't quite get rid of mosquitos though... 😀
}
```



#### rfind
Find the position of a substring from within a string, searching right to left.

`int string::rfind(const string &in search, uint start = -1);`

##### Arguments:
* search: The string to search for.
* start: The index to start searching from. Default is -1 (end).

##### Returns
The position where the substring starts if found, or -1 otherwise.

##### Remarks
This is useful if what you need to find is closer to the end of a string than the start.


#### slice

Extracts a substring starting at the given index and ending just before the index end (exclusive).

string string::slice(int start = 0, int end = 0);

##### Arguments:

* int start = 0: The index where the substring begins (inclusive).

* int end = 0: The index where the substring ends (exclusive).

##### Returns:

string: A new string with the characters modified.

##### Remarks

This can be a tripping point due to two factors: Strings are zero-based indexing, and slicing is end-exclusive. Therefore, to retrieve characters 4 to 6, your parameters would be 3, 6.

Negative indexes count backwards from the end of a string. Thus, "hello".slice(-4, 4) is the same as "hello".slice(1, 4): Both would return "ell".

If start is greater than the string's length, or negative beyond the start of the string, the result is an empty string.

If end is 0 or otherwise beyond the string's bounds, it is treated as string.length().

Any situation where start >= end after resolving indexes returns an empty string. An example of this would be "hello".slice(-3, 1), which would be equivalent to "hello".slice(2, 1).

This method is useful for extracting a string between two points (for instance when parsing HTML or XML, as in slice(tag_start, tag_end)). For length-based extraction, prefer substr.

##### Example:

```NVGT
void main() {
	string text = "Hello, world!";
	string substring = text.slice(0, 5);
	alert("Info", substring);
	text = "Welcome to NVGT";
	substring = text.slice(11, 16);
	alert("Info", substring);
}
```



#### split

Splits a string into an array at a given delimiter.

string[]@ string::split(const string&in delimiter, bool full = true, bool allow_blanks = false);

##### Arguments:

* const string&in delimiter: the delimiter to split at.

* bool full: Use all or any of the delimiter characters.

* bool allow_blanks: Specifies whether to allow empty fields.

##### Returns:

string[]@: a handle to an array containing each part of the split string.

##### Remarks:

* The full parameter decides how to treat delimiter strings with multiple characters (such as "\r\n"). If enabled, the entire string is treated as a single delimiter ("\r\n"). If disabled, any character in the string counts as a delimiter ("\r" or "\n"). If the delimiter string is a single character this parameter is effectively meaningless.

* The allow_blanks parameter decides how to treat consecutive delimiters. See the example for how this works in practice.

* If the input string is empty, the output depends on the allow_blanks parameter. If true, an array with the blank string as the only element is returned. If false, an empty array is returned.

##### Example:

```NVGT
void main() {
	// basic split/join example
	string test = "welcome to the example";
	string[]@ parts = test.split(" ");
	alert("Parts", join(parts, ", "));
	// Blank fields test
	string test2="Humphrey,Eccleston,,50";
	alert("New string", test2);
	parts=test2.split(",", true, false);
	alert("Fields with data", parts.length()); // Should output 3.
	parts=test2.split(",", true, true);
	alert("Total fields", parts.length()); // Should output 4.
}
```



#### starts_with

Determines if a string starts with another string.

bool string::starts_with(const string&in str);

##### Arguments:

* const string&in str: the string to look for.

##### Returns:

bool: true if the string starts with the specified search, false if not.

##### Example:

```NVGT
void main() {
	string prefix = "abc";
	string text = input_box("Test", "Enter a string");
	if (text.is_empty()) {
		alert("Info", "Nothing was entered.");
		exit();
	}
	if (text.starts_with(prefix))
		alert("Info", "The entered string starts with " + prefix);
	else
		alert("Info", "The entered string does not start with " + prefix);
}
```



#### substr

Extracts a substring starting at the given index and containing a specific number of characters.

string string::substr(uint start = 0, int count = -1);

##### Arguments:

* uint start = 0: The index where the substring begins (inclusive).

* int count = -1: The number of characters to include in the substring (see remarks).

##### Returns:

string: A new string with the characters modified.

##### Remarks

If the count is out of bounds, the string is returned from the start index to the end.

If the start index is out of bounds, an empty string is returned.

This is useful for working with fixed length data (for instance, give me 4 characters at position 4). If you want to split a string between start and end points, prefer slice.

##### Example:

```NVGT
void main() {
	string text = "Hello, world!";
	string substring = text.substr(7, 5); // Extracts "world"
	alert("Info", substring);
}
```



#### trim_whitespace

Trims any and all whitespace from the beginning and end of a string, returning a new string.

string string::trim_whitespace();

##### Returns:

string: the specified string, with any trailing/leading whitespace removed.

##### Remarks:

Any and all whitespace, including the tab character and new lines, will be removed.

##### Example:

```NVGT
void main() {
	string text = input_box("String", "Enter a string");
	if (text.is_empty()) {
		alert("Info", "You didn't enter a string.");
		exit();
	}
	string result = text.trim_whitespace();
	alert("Trimmed string", result);
}
```



#### trim_whitespace_left

Trims any and all whitespace from the left side of a string, returning a new string.

string string::trim_whitespace_left();

##### Returns:

string: the specified string, with the whitespace removed from the left side.

##### Remarks:

Any and all whitespace, including the tab character and new lines, will be removed.

##### Example:

```NVGT
void main() {
	string text = input_box("String", "Enter a string");
	if (text.is_empty()) {
		alert("Info", "You didn't enter a string.");
		exit();
	}
	string result = text.trim_whitespace_left();
	alert("Trimmed string", result);
}
```



#### trim_whitespace_left_this

Trims any and all whitespace from the left side of a string, modifying the calling string.

string& string::trim_whitespace_left();

##### Returns:

string&: a two-way reference to the specified string, with the whitespace removed from the left side.

##### Remarks:

Any and all whitespace, including the tab character and new lines, will be removed.

##### Example:

```NVGT
void main() {
	string text = input_box("String", "Enter a string");
	if (text.empty()) {
		alert("Info", "You didn't enter a string.");
		exit();
	}
	text = text.trim_whitespace_left();
	alert("Trimmed string", text);
}
```



#### trim_whitespace_right

Trims any and all whitespace from the right side of a string, returning a new string.

string string::trim_whitespace_right();

##### Returns:

string: the specified string, with the whitespace removed from the right side.

##### Remarks:

Any and all whitespace, including the tab character and new lines, will be removed.

##### Example:

```NVGT
void main() {
	string text = input_box("String", "Enter a string");
	if (text.is_empty()) {
		alert("Info", "You didn't enter a string.");
		exit();
	}
	string result = text.trim_whitespace_right();
	alert("Trimmed string", result);
}
```



#### trim_whitespace_right_this

Trims any and all whitespace from the right side of a string, modifying the calling string.

string& string::trim_whitespace_right();

##### Returns:

string&: a two-way reference to the specified string, with the whitespace removed from the right side.

##### Remarks:

Any and all whitespace, including the tab character and new lines, will be removed.

##### Example:

```NVGT
void main() {
	string text = input_box("String", "Enter a string");
	if (text.empty()) {
		alert("Info", "You didn't enter a string.");
		exit();
	}
	text = text.trim_whitespace_right();
	alert("Trimmed string", text);
}
```



#### trim_whitespace_this

Trims any and all whitespace from the beginning and end of a string, modifying the calling string.

string& string::trim_whitespace_this();

##### Returns:

string&: a reference to the specified string, with any trailing/leading whitespace removed.

##### Remarks:

Any and all whitespace, including the tab character and new lines, will be removed.

##### Example:

```NVGT
void main() {
	string text = input_box("String", "Enter a string");
	if (text.empty()) {
		alert("Info", "You didn't enter a string.");
		exit();
	}
	text = text.trim_whitespace_this();
	alert("Trimmed string", text);
}
```



#### unpacket
Copies individual raw bytes from the string (starting at the given offset) into the provided output variables.

`int string::unpacket(int offset, ?&out var1, ...);`

##### Arguments:
* offset: Position in the string to start extracting from.
* var1: The first variable slot to fill.

##### Returns
A new offset in the string where you should continue the extraction process.

##### Remarks
The "..." above denotes that this function can take a variable number of arguments. In fact, it can take up to 16 output variables.

The following snippet will save the string "hello" into five variables named a, b, c, d, and e. These variables can be of any type.
`"hello".unpacket(0, a, b, c, d, e);`

This method does not unpack multi-byte types like 4-byte integers or floats.


#### upper

Converts a string to uppercase, returning a new string.

string string::upper();

##### Returns:

string: the specified string in uppercase.

##### Example:

```NVGT
void main() {
	string text = input_box("Text", "Enter the text to convert to uppercase.");
	if (text.empty()) {
		alert("Info", "You typed a blank string.");
		exit(1);
	}
	alert("Your string uppercased is", text.upper());
}
```



#### upper_this

Converts a string to uppercase, modifying the calling string.

string& string::upper();

##### Returns:

string&: a reference to the specified string in uppercase.

##### Example:

```NVGT
void main() {
	string text = input_box("Text", "Enter the text to convert to uppercase.");
	if (text.empty()) {
		alert("Info", "You typed a blank string.");
		exit(1);
	}
	text = text.upper_this();
	alert("Your string uppercased is", text);
}
```






