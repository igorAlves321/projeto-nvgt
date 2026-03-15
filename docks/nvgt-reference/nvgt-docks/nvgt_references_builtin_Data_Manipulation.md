# Data Manipulation
## Classes
### json_array
#### Methods
##### add

Add a value to the end of a JSON array.

void json_array::add(var@ value);

###### Arguments:

* var@ value: a handle to the value to be set.

###### Example:

```NVGT
void main() {
	json_array@ arr = parse_json("[]");
	for (uint i = 0; i < 5; i++)
		arr.add(random(1, 100));
	alert("Filled array", arr.stringify());
}
```



##### clear

Clears the JSON array completely.

void json_array::clear();

###### Example:

```NVGT
void main() {
	string data = "[1, 2, 3, 4, 5]";
	json_array@ arr = parse_json(data);
	alert("Before being cleared", arr.stringify());
	arr.clear();
	alert("After being cleared", arr.stringify());
}
```



##### is_array

Determine if the value at the given index is a JSON array or not.

bool json_array::is_array(uint index);

###### Arguments:

* uint index: the position of the item.

###### Returns:

bool: true if the value at the specified index is a JSON array, false otherwise.

###### Example:

```NVGT
void main() {
	json_array@ arr = parse_json("[[1, 2], [3, 4]]");
	alert("Info", arr.is_array(1) ? "It is an array": "It is not an array");
}
```



##### is_null

Determine if the value at the given index is null.

bool json_array::is_null(uint index);

###### Arguments:

* uint index: the position of the item.

###### Returns:

bool: true if the value at the specified index is null, false otherwise.

###### Example:

```NVGT
void main() {
	json_array@ arr = parse_json("[1, 2, null, 4]");
	alert("Info", "Index 1 " + (arr.is_null(1) ? " is null": " is not null"));
	alert("Info", "Index 2 " + (arr.is_null(2) ? " is null": " is not null"));
}
```



##### is_object

Determine if the value at the given index is a JSON object.

bool json_array::is_object(uint index);

###### Arguments:

* uint index: the position of the item.

###### Returns:

bool: true if the value at the specified index is a JSON object, false otherwise.

###### Example:

```NVGT
void main() {
	json_array@ arr = parse_json("""[{}, {}, "test", {}]""");
	alert("Info", "Position 0 " + (arr.is_object(0) ? "is an object" : "is not an object"));
	alert("Info", "Position 2 " + (arr.is_object(2) ? "is an object": "is not an object"));
}
```



##### remove

Remove a value from the JSON array given an index.

void json_array::remove(uint index);

###### Arguments:

* uint index: the index of the value to remove.

###### Example:

```NVGT
void main() {
	string data = """[47, 4, 584, 43, 8483]""";
	json_array@ arr = parse_json(data);
	alert("Initial", arr.stringify());
	arr.remove(2);
	alert("After removal", arr.stringify());
}
```



##### size

Return the size of the JSON array.

uint json_array::size();

###### Example:

```NVGT
void main() {
	string data = "[";
	for (int i = 0; i < random(10, 20); i++)
		data += i + ", ";
	// Strip off the trailing comma and space character, as they'll make the JSON throw a syntax error.
	data.erase(data.length() - 1);
	data.erase(data.length() - 1);
	data += "]";
	clipboard_set_text(data);
	json_array@ arr = parse_json(data);
	alert("Info", "The JSON array contains " + arr.size() + " items");
}
```



##### stringify

Return the JSON array as a string.

string json_array::stringify(int indent = 0, int step = -1);

###### Arguments:

* int indent = 0: specifies how many spaces to use to indent the JSON. If 0, no indentation or formatting is performed.

* int step = -1: the outwards indentation step, for example setting it to two would cause your outdents to only be two spaces. -1 (the default) keeps it how it is, normally you don't need to use this parameter.

###### Returns:

string: the JSON array as a string.

###### Example:

```NVGT
void main() {
	string data = """["Apple", "Banana", "Orange", "Lemon"]""";
	json_array@ arr = parse_json(data);
	alert("JSON array", arr.stringify(4));
}
```




#### Operators
##### get_opIndex

Get a value out of the JSON array with literal syntax, for example `arr[2]`.

var@ json_array::get_opIndex(uint index) property;

###### Arguments:

* uint index: the index of the value to get.

###### Returns:

var@: a handle to the object, or null if not found.

###### Example:

```NVGT
void main() {
	json_array@ cats = parse_json("""["Athena", "Willow", "Punk", "Franky", "Yoda", "Waffles"]""");
	alert("The third cat is", cats[2]);
	for (uint i = 0; i < cats.size(); i++)
		alert("Awww", "Hi " + cats[i]);
}
```



##### opCall

Get a value out of a JSON array using a query.

var@ json_array::opCall(string query);

###### Arguments:

* string query: the JSON query (see the remarks section for details).

###### Returns:

var@: a handle to the object, or null if it couldn't be found.

###### Remarks:

Queries are formatted like so, using key names and indexes separated with ".":

> world.player.0

It can be as nested as you like.

###### Example:

```NVGT
void main() {
	string data = """[[["Colorado", "Kansas", "Minnesota"]]]""";
	json_array@ arr = parse_json(data);
	string location = arr("0.0.0");
	alert("My favorite state is", location);
}
```



##### set_opIndex

Set a value in the JSON array at a particular position.

void json_array::set_opIndex(uint index, var@ value) property;

###### Arguments:

* uint index: the index to insert the item at.

* var@ value: the value to set.

###### Example:

```NVGT
void main() {
	json_array@ arr = parse_json("[]");
	arr[0] = "meow";
	alert("Info", "Cats say " + arr[0]);
}
```




#### Properties
##### empty

Determine if the JSON array is empty.

const bool json_array::empty;

###### Example:

```NVGT
void main() {
	json_array@ arr = parse_json("[]");
	json_array@ arr2 = parse_json("[1, 2, 3]");
	alert("First is empty", arr.empty ? "true" : "false");
	alert("Second is empty", arr2.empty ? "true" : "false");
}
```



##### escape_unicode
Determines the amount of escaping that occurs in JSON parsing.

`bool json_array::escape_unicode;`

###### Remarks:
If this property is true, escaping will behave like normal. If it's false, only the characters absolutely vital to JSON parsing are escaped.




### json_object
#### Methods
##### clear

Clears the JSON object completely.

void json_object::clear();

###### Example:

```NVGT
void main() {
	string data = """{"numbers": [1, 2, 3, 4, 5]}""";
	json_object@ o = parse_json(data);
	alert("Before being cleared", o.stringify());
	o.clear();
	alert("After being cleared", o.stringify());
}
```



##### exists

Determine if a key exists in the JSON object.

bool json_object::exists(const string?&in key);

###### Arguments:

* const string&in key: the key to search for.

###### Returns:

bool: true if the key exists, false if not.

###### Example:

```NVGT
void main() {
	string data = """{"engine": "NVGT"}""";
	json_object@ o = parse_json(data);
	alert("Info", (o.exists("engine") ? "The key exists" : "The key does not exist"));
}
```



##### get_keys

Get a list of all the keys in the JSON object.

string[]@ json_object::get_keys();

###### Returns:

string[]@: a handle to an array of strings containing all the keys of the JSON object.

###### Remarks:

Note that this function isn't recursive, you only get the keys for the object you're running this function on, not any child objects.

###### Example:

```NVGT
void main() {
	string data = """{"thing": 1, "other_thing": "test", "another": true}""";
	json_object@ o = parse_json(data);
	string[]@ keys = o.get_keys();
	alert("The keys are", join(keys, ", "));
}
```



##### is_array

Determine if the value with the given key is a JSON array or not.

bool json_object::is_array(string key);

###### Arguments:

* string key: the key to query.

###### Returns:

bool: true if the value with the specified key is a JSON array, false otherwise.

###### Example:

```NVGT
void main() {
	string data = """{"classes": ["json_object", "json_array"]}""";
	json_object@ o = parse_json(data);
	alert("Info", o.is_array("classes") ? "array": "nonarray");
}
```



##### is_null

Determine if the value with the given key is null.

bool json_object::is_null(string key);

###### Arguments:

* string key: the key to query.

###### Returns:

bool: true if the value with the specified key is null.

###### Example:

```NVGT
void main() {
	string data = """{"brain": null}""";
	json_object@ o = parse_json(data);
	alert("Info", o.is_null("brain") ? "null" : "not null");
}
```



##### is_object

Determine if the value with the given key is a JSON object or not.

bool json_object::is_object(string key);

###### Arguments:

* string key: the key to query.

###### Returns:

bool: true if the value with the specified key is a JSON object, false otherwise.

###### Example:

```NVGT
void main() {
	string data = """{"json_object": {}}""";
	json_object@ o = parse_json(data);
	alert("Info", o.is_object("json_object") ? "Object" : "Non-object");
}
```



##### remove

Remove a value from the JSON object given a key.

void json_object::remove(const string&in key);

###### Arguments:

* const string&in key: the key of the value to remove.

###### Example:

```NVGT
void main() {
	string data = """{"name": "Quin"}""";
	json_object@ o = parse_json(data);
	alert("Initial", o.stringify());
	o.remove("name");
	alert("After removal", o.stringify());
}
```



##### set

Set a value in a JSON object.

void json_object::set(const string&in key, var@ value);

###### Arguments:

* const string&in key: the key to give the value.

* var@ value: a handle to the value to be set.

###### Example:

```NVGT
void main() {
	json_object@ o = parse_json("{}");;
	o.set("nvgt_user", true);
	alert("Info", (bool(o["nvgt_user"]) ? "You are an NVGT user" : "You are not a regular NVGT user"));
}
```



##### size

Return the size of the JSON object.

uint json_object::size();

###### Remarks:

Note that this function returns the number of top-level keys; it's not recursive.

###### Example:

```NVGT
void main() {
	string data = """{"numbers": [1, 2, 3, 4, 5]}""";
	json_object@ o = parse_json(data);
	alert("Info", "The json object's size is " + o.size());
}
```



##### stringify

Return the JSON object as a string.

string json_object::stringify(int indent = 0, int step = -1);

###### Arguments:

* int indent = 0: specifies how many spaces to use to indent the JSON. If 0, no indentation or formatting is performed.

* int step = -1: the outwards indentation step, for example setting it to two would cause your outdents to only be two spaces. -1 (the default) keeps it how it is, normally you don't need to use this parameter.

###### Returns:

string: the JSON object as a string.

###### Example:

```NVGT
void main() {
	string data = """{"name": "Quin", "age": 18}""";
	json_object@ o = parse_json(data);
	alert("JSON object", o.stringify(4));
}
```




#### Operators
##### get_opIndex

Get a value out of the JSON object with literal syntax, for example `json["key"]`.

var@ json_object::get_opIndex(const string&in key) property;

###### Arguments:

* const string&in key: the key of the object to get.

###### Returns:

var@: a handle to the object, or null if not found.

###### Example:

```NVGT
void main() {
	string data = """{"name": "Quin", "age": 18}""";
	json_object@ o = parse_json(data);
	alert("Info", o["name"] + " is " + o["age"]);
}
```



##### opCall

Get a value out of a JSON object using a query.

var@ json_object::opCall(const string&in query);

###### Arguments:

* const string&in query: the JSON query (see the remarks section for details).

###### Returns:

var@: a handle to the object, null if not found.

###### Remarks:

Queries are formatted like so:

> first_field.subfield.subfield

It can be as nested as you like.

This method also works on json_array's, and you access array indexes just with their raw numbers, like so:

> world.players.0

###### Example:

```NVGT
void main() {
	string data = """{"countries":{"us":["Colorado", "Kansas", "Minnesota"]}}""";
	json_object@ o = parse_json(data);
	string locations = o("countries.us");
	alert("My favorite states are", locations);
}
```



##### set_opIndex

Set a value in the JSON object with a particular key.

void json_object::set_opIndex(const string&in key, var@ value) property;

###### Arguments:

* const string&in key: the key of the object.

* var@ value: the value to set.

###### Example:

```NVGT
void main() {
	json_object@ o = parse_json("{}");
	o["name"] = "Quin";
	alert("Hi", "I am " + o["name"]);
}
```




#### Properties
##### escape_unicode
Determines the amount of escaping that occurs in JSON parsing.

`bool json_object::escape_unicode;`

###### Remarks:
If this property is true, escaping will behave like normal. If it's false, only the characters absolutely vital to JSON parsing are escaped.




### pack
#### methods
##### add_file
Add a file on disk to a pack.

`bool pack::add_file(const string&in disk_filename, const string&in pack_filename, bool allow_replace = false);`

###### Arguments:
* const string&in disk_filename: the filename of the file to add to the pack.
* const string&in pack_filename: the name the file should have in your pack.
* bool allow_replace = false: if a file already exists in the pack with that name, should it be overwritten?

###### Returns:
bool: true if the file was successfully added, false otherwise.


##### add_memory
Add content stored in memory to a pack.

`bool pack::add_memory(const string&in pack_filename, const string&in data, bool replace = false);`

###### Arguments:
* const string&in pack_filename: the name the file should have in your pack.
* const string&in data: a string containing the data to be added.
* bool allow_replace = false: if a file already exists in the pack with that name, should it be overwritten?

###### Returns:
bool: true if the data was successfully added, false otherwise.


##### close
Closes a pack, freeing all its resources.

`bool pack::close();`

###### Returns:
bool: true if the pack was successfully closed, false otherwise.


##### delete_file
Attempt to remove a file from a pack.

`bool pack::delete_file(const string&in filename);`

###### Arguments:
* const string&in filename: the name of the file to be deleted.

###### Returns:
bool: true if the file was successfully deleted, false otherwise.


##### file_exists
Query whether or not a file exists in your pack.

`bool pack::file_exists(const string&in filename);`

###### Arguments:
* const string&in filename: the name of the file to query.

###### Returns:
bool: true if the file exists in the pack, false if not.


##### get_file_name
Get the name of a file with a particular index.

`string pack::get_file_name(int index);`

###### Arguments:
* int index: the index of the file to retrieve (see remarks).

###### Returns:
string: the name of the file if found, or an empty string if not.

###### Remarks:
The index you pass to this function is the same index you'd use to access an element in the return value from `pack::list_files()`.


##### get_file_offset
Get the offset of a file in your pack.

`uint pack::get_file_offset(const string&in filename);`

###### Arguments:
* const string&in filename: the name of the file to get the offset of.

###### Returns:
uint: the offset of the file (in bytes).

###### Remarks:
Do not confuse this with the offset parameter in the pack::read_file method. This function is provided encase you wish to re-open the pack file with your own file object and seek to a file's data within that external object. The offset_in_file parameter in the read_file method is relative to the file being read.


##### get_file_size
Returns the size of a particula file in the pack.

`uint pack::get_file_size(const string&in filename);`

###### Arguments:
* const string&in filename: the name of the file to query the size of.

###### Returns:
uint: the size of the file (in bytes), or 0 if no file with that name was found.


##### list_files
Get a list of all the files in the pack.

`string[]@ pack::list_files();`

###### Returns:
string[]@: a handle to an array of strings containing the names of every file in the pack.


##### open
Open a pack to perform operations on it.

`bool pack::open(const string&in filename, uint mode, bool memload = false);`

###### Arguments:
* const string&in filename: the name of the pack file to open.
* uint mode: the mode to open the pack in (see `pack_open_modes` for more information).
* bool memload = false: whether or not the pack should be loaded into memory as opposed to on disk.

###### Returns:
bool: true if the pack was successfully opened with the given mode, false otherwise.

###### Remarks:
To open an embedded pack, prefix it with `*`, like this:

`pack.open("*embedded.dat");`

For BGT compatibility, you can use a single `*` to open the first available embedded pack.

`pack.open("*");`


##### read_file
Get the contents of a file contained in a pack.

`string pack::read_file(const string&in pack_filename, uint offset_in_file, uint size);`

###### Arguments:
* const string&in pack_filename: the name of the file to be read.
* uint offset_in_file: the offset within the file to begin reading data from (do not confuse this with pack::get_file_offset)
* uint size: the number of bytes to read (see `pack::get_file_size` to read the entire file).

###### Returns:
string: the contents of the file.

###### Remarks:
This function allows you to read chunks of data from a file, as well as an entire file in one call. To facilitate this, the offset and size parameters are provided. offset is relative to the file being read E. 0 for the beginning of it. So to read a file in one chunk, you could execute:
```
string file_contents = my_pack.read_file("filename", 0, my_pack.get_file_size("filename"));
```


##### set_pack_identifier
Set the identifier of this pack object (e.g. the first 8-bytes that determine if you have a valid pack or not).

`bool pack::set_pack_identifier(const string&in ident);`

###### Arguments:
* const string&in ident: the new identifier (see remarks).

###### Returns:
bool: true if the pack's identifier was properly set, false otherwise.

###### Remarks:
* The default pack identifier is "NVPK" followed by 4 NULL bytes.
* Your pack identifier should be 8 characters or less. If it's less than 8 characters, 0s will be added as padding on the end. If it's larger than 8, the first 8 characters will be used.




### regexp

The regexp object allows for the easy usage of regular expressions in NVGT.

regexp(const string&in pattern, int options = RE_UTF8);

#### Arguments:

* const string&in pattern: the regular expression's pattern (see remarks).

* int options = RE_UTF8: a combination of any of the values from the `regexp_options` enum.

#### Remarks:

Regular expressions are a language used for matching, substituting, and otherwise manipulating text. To learn about the regular expression syntax that nVGT uses (called PCRE), see this link: https://en.wikipedia.org/wiki/Perl_Compatible_Regular_Expressions

#### Example:

```NVGT
void main() {
	regexp re("^[a-z]{2,4}$"); // Will match any lowercase alphabetical string between 2 and 4 characters in length.
	string compare = input_box("Text", "Enter the text to check against the regular expression.");
	if (compare.empty()) {
		alert("Regular expression tester", "You didn't type a string to test.");
		exit(1);
	}
	bool matches = re.match(compare);
	alert("The regular expression", matches ? "matches" : "does not match");
}
```



#### methods
##### match
Determine if the regular expression matches against a particular string or not.

1. `bool regexp::match(const string&in subject, uint64 offset = 0);`
2. `bool regexp::match(const string&in subject, uint64 offset, int options);`

###### Arguments (1):
* const string&in subject: the string to compare against.
* uint64 offset = 0: the offset to start the comparison at.

###### Arguments (2):
* const string&in subject: the string to compare against.
* uint64 offset: the offset to start the comparison at.
* int options: any combination of the values found in the `regexp_options` enum.

###### Returns:
bool: true if the regular expression matches the given string, false if not.





## Enums
### pack_open_modes
This is a list of all the possible open modes to be passed to the `pack::open()` function.

* PACK_OPEN_MODE_NONE.
* PACK_OPEN_MODE_APPEND: open the pack and append data to it.
* PACK_OPEN_MODE_CREATE: create a new pack.
* PACK_OPEN_MODE_READ: open the pack for reading.


### regexp_options
This enum holds various constants that can be passed to the regular expression classes in order to change their behavior.

#### Notes:
Portions of this regexp_options documentation were Copied from POCO header files.
* Options marked [ctor] can be passed to the constructor of regexp objects.
* Options marked [match] can be passed to match, extract, split and subst.
* Options marked [subst] can be passed to subst.

See the PCRE documentation for more information.

#### Constants:
* RE_CASELESS: case insensitive matching (/i) [ctor]
* RE_MULTILINE: enable multi-line mode; affects ^ and $ (/m) [ctor]
* RE_DOTALL: dot matches all characters, including newline (/s) [ctor]
* RE_EXTENDED: totally ignore whitespace (/x) [ctor]
* RE_ANCHORED: treat pattern as if it starts with a ^ [ctor, match]
* RE_DOLLAR_END_ONLY: dollar matches end-of-string only, not last newline in string [ctor]
* RE_EXTRA: enable optional PCRE functionality [ctor]
* RE_NOT_BOL: circumflex does not match beginning of string [match]
* RE_NOT_EOL: $ does not match end of string [match]
* RE_UNGREEDY: make quantifiers ungreedy [ctor]
* RE_NOT_EMPTY: empty string never matches [match]
* RE_UTF8: assume pattern and subject is UTF-8 encoded [ctor]
* RE_NO_AUTO_CAPTURE: disable numbered capturing parentheses [ctor, match]
* RE_NO_UTF8_CHECK: do not check validity of UTF-8 code sequences [match]
* RE_FIRSTLINE: an unanchored pattern is required to match before or at the first newline in the subject string, though the matched text may continue over the newline [ctor]
* RE_DUPNAMES: names used to identify capturing subpatterns need not be unique [ctor]
* RE_NEWLINE_CR: assume newline is CR ('\r'), the default [ctor]
* RE_NEWLINE_LF: assume newline is LF ('\n') [ctor]
* RE_NEWLINE_CRLF: assume newline is CRLF ("\r\n") [ctor]
* RE_NEWLINE_ANY: assume newline is any valid Unicode newline character [ctor]
* RE_NEWLINE_ANY_CRLF: assume newline is any of CR, LF, CRLF [ctor]
* RE_GLOBAL: replace all occurrences (/g) [subst]
* RE_NO_VARS: treat dollar in replacement string as ordinary character [subst]



## Functions
### ascii_to_character

Return the character that corresponds to the given ascii value.

string ascii_to_character(uint8 ascii);

#### Arguments:

* uint8 ascii: the ascii value to convert.

#### Returns:

string: the character for the given ascii value.

#### Example:

```NVGT
void main() {
	uint8 ascii = parse_int(input_box("ASCII value", "Enter the ascii value to convert."));
	alert("Info", ascii + " has a value of " + ascii_to_character(ascii));
}
```



### character_to_ascii

Return the ascii value for the given character.

uint8 character_to_ascii(const string&in character);

#### Arguments:

* const string&in character: the character to convert.

#### Returns:

uint8: the ascii value for the given character.

#### Remarks:

If a string containing more than one character is passed as input to this function, only the left-most character is checked.

If an empty string is passed, the function returns 0.

#### Example:

```NVGT
void main() {
	string character = input_box("Character", "Enter a character to convert");
	if (character.is_empty()) {
		alert("Error", "You did not type anything.");
		exit();
	}
	if (character.length() != 1) { // The user typed more than one character.
		alert("Error", "You must only type a single character.");
		exit();
	}
	alert("Info", character + " has an ascii value of " + character_to_ascii(character));
}
```



### join

turn an array into a string, with each element being separated by the given delimiter.

string join(const string[]@ elements, const string&in delimiter);

#### Arguments:

* const string[]@ elements: a handle to the array to join.

* const string&in delimiter: the delimiter used to separate each element in the array (can be empty).

#### Returns:

string: the given array as a string.

#### Remarks:

If an empty array is passed, a blank string is returned.

The delimiter is not appended to the end of the last item in the returned string. For example if an array contains [1, 2, 3] and you join it with a delimiter of . (period), the result would be "1.2.3" without an extra delimiter appended.

#### Example:

```NVGT
void main() {
	string[] names = {"Sam", "Quin", "Patrick"};
	string people = join(names, ", ");
	alert("Info", people);
}
```



### number_to_words

Convert a number into its string equivalent, for example, one thousand four hundred and fifty six.

string number_to_words(int64 the_number, bool include_and = true);

#### Arguments:

* int64 the_number: the number to convert.

* bool include_and = true: whether or not to include the word "and" in the output.

#### Returns:

string: the specified number, converted to a readable string.

#### Remarks:

At this time, this function only produces English results.

#### Example:

```NVGT
void main() {
	int64 num = random(1000, 100000);
	string result = number_to_words(num);
	alert("Info", num + " as a string is " + result);
}
```



### pack_set_global_identifier
Set the global identifier of all your packs (e.g. the first 8-bytes that determine if you have a valid pack or not).

`bool pack_set_global_identifier(const string&in ident);`

#### Arguments:
* const string&in ident: the new identifier (see remarks).

#### Returns:
bool: true if the identifier was properly set, false otherwise.

#### Remarks:
* The default pack identifier is "NVPK" followed by 4 NULL bytes.
* Your pack identifier should be 8 characters or less. If it's less than 8 characters, 0s will be added as padding on the end. If it's larger than 8, the first 8 characters will be used.
* NVGT will refuse to open any pack files that do not match this identifier.


### regexp_match

Test if the text matches the specified regular expression.

bool regexp_match(const string&in text, const string&in pattern);

#### Arguments:

* const string&in text: the text to compare against the regular expression.

* const string&in pattern: the regular expression to match.

#### Returns:

bool: true if the text matches the given regular expression, false otherwise.

#### Remarks:

If you would like a lower level interface to regular_expressions in NVGT, check out the regexp class which this function more or less wraps.

To learn more about regular expressions, visit: https://en.wikipedia.org/wiki/Regular_expression

#### Example:

```NVGT
void main() {
	bool match = regexp_match("Test", "^[a-zA-Z]+$");
	alert("the regular expression", match ? "matches" : "does not match");
}
```



### string_base32_decode

Decodes a string from base32.

string string_base32_decode(const string&in the_data);

#### Arguments:

* const string&in the_data: The data that is to be decoded.

#### Returns:

String: The decoded string on success or an empty string on failure.

#### Remarks:

You can learn more about the base32 format [here](https://en.wikipedia.org/wiki/Base32).

#### Example:

```NVGT
void main() {
	string text = input_box("Text", "Enter the text to decode.");
	if (text.is_empty()) {
		alert("Error", "You did not type any text.");
		exit();
	}
	alert("Info", string_base32_decode(text));
}
```



### string_base32_encode

Encodes a string as base32.

string string_base32_encode(const string&in the_data);

#### Arguments:

* const string&in the_data: The data that is to be encoded.

#### Returns:

String: The encoded string on success or an empty string on failure.

#### Remarks:

You can learn more about the base32 format [here](https://en.wikipedia.org/wiki/Base32).

#### Example:

```NVGT
void main() {
	string text = input_box("Text", "Enter the text to encode.");
	if (text.is_empty()) {
		alert("Error", "You did not type any text.");
		exit();
	}
	alert("Info", string_base32_encode(text));
}
```



### string_base32_normalize

Normalize a string to conform to the base32 spec.

string string_base32_normalize(const string&in the_data);

#### Arguments:

* const string&in the_data: the string to normalize.

#### Returns:

string: the normalized string.

#### Remarks:

The primary thing this function does is to skip separators, convert all letters to uppercase, and make sure the length is a multiple of 8.

To learn more about base32, click [here](https://en.wikipedia.org/wiki/Base32).

#### Example:

```NVGT
void main() {
	string text = input_box("Text", "Enter the text to normalize.");
	if (text.is_empty()) {
		alert("Error", "You didn't type anything.");
		exit();
	}
	alert("Info", string_base32_normalize(text));
}
```



### string_base64_decode

Decodes a string which has previously been encoded in base64.

string string_base64_decode(const string&in the_data, string_base64_options options = STRING_BASE64_PADLESS);

#### Arguments:

* const string&in the_data: The data that is to be decoded.

* string_base64_options options = STRING_BASE64_PADLESS: A bitwise of options that control the behavior of the decoding (see remarks).

#### Returns:

String: The decoded string on success or an empty string on failure.

#### Remarks:

The following options may be passed to the options argument of this function:

* STRING_BASE64_DEFAULT: The defaults passed to the string_base64_encode function.

* STRING_BASE64_URL: Use base64 URL encoding as opposed to the / and = characters.

* STRING_BASE64_PADLESS: Allows decoding even if the string does not end with = padding characters.

You can learn more about base64 [here.](https://en.wikipedia.org/wiki/Base64)

#### Example:

```NVGT
void main() {
	alert("example", string_base64_decode("aGVsbG8=")); // Should print "hello".
}
```



### string_base64_encode

Encodes a string as base64.

string string_base64_encode(const string&in the_data, string_base64_options options = STRING_BASE64_DEFAULT);

#### Arguments:

* const string&in the_data: The data that is to be encoded.

* string_base64_options options = STRING_BASE64_DEFAULT: A bitwise of options that control the behavior of the encoding (see remarks).

#### Returns:

String: The encoded string on success or an empty string on failure.

#### Remarks:

The following options may be passed to the options argument of this function:

* STRING_BASE64_DEFAULT: The default options (i.e. insert padding and do not use URL encoding).

* STRING_BASE64_URL: Use base64 URL encoding as opposed to the / and = characters.

* STRING_BASE64_PADLESS: Allows decoding even if the string does not end with = padding characters.

You can learn more about base64 [here.](https://en.wikipedia.org/wiki/Base64)

#### Example:

```NVGT
void main() {
	alert("example", string_base64_encode("Hello")); // Should print SGVsbG8=
}
```




## Global Properties
### pack_global_identifier
Represents the identifier currently being used for all your packs.

`const string pack_global_identifier;`




