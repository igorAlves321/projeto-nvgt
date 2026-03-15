# Dictionary Retrieval (dget.nvgt)
## Dictionary retrieval functions
The way you get values out of AngelScript dictionaries by default is fairly annoying, mainly due to its usage of out values instead of returning them. Hence this include, which attempts to simplify things.


## functions
### dgetb
Get a boolean value out of a dictionary.

`bool dgetn(dictionary@ the_dictionary, string key, bool def = false);`

#### Arguments:
* dictionary@ the_dictionary: a handle to the dictionary to get the value from.
* string key: the key of the value to look up.
* bool def = false: the value to return if the key wasn't found.

#### Returns:
bool: the value for the particular key in the dictionary, or the default value if not found.


### dgetn
Get a numeric value out of a dictionary.

`double dgetn(dictionary@ the_dictionary, string key, double def = 0.0);`

#### Arguments:
* dictionary@ the_dictionary: a handle to the dictionary to get the value from.
* string key: the key of the value to look up.
* double def = 0.0: the value to return if the key wasn't found.

#### Returns:
double: the value for the particular key in the dictionary, or the default value if not found.


### dgets
Get a string value out of a dictionary.

`string dgets(dictionary@ the_dictionary, string key, string def = 0.0);`

#### Arguments:
* dictionary@ the_dictionary: a handle to the dictionary to get the value from.
* string key: the key of the value to look up.
* string def = "": the value to return if the key wasn't found.

#### Returns:
string: the value for the particular key in the dictionary, or the default value if not found.


### dgetsl
Get a string array out of a dictionary.

`string[] dgetsl(dictionary@ the_dictionary, string key, string[] def = []);`

#### Arguments:
* dictionary@ the_dictionary: a handle to the dictionary to get the value from.
* string key: the key of the value to look up.
* string[] def = []: the value to return if the key wasn't found.

#### Returns:
string[]: the value for the particular key in the dictionary, or the default value if not found.

#### Remarks:
The default value for this function is a completely empty (but initialized) string array.




