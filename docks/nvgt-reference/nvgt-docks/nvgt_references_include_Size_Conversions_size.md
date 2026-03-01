# Size Conversions (size.nvgt)
## Size Conversions Include
This include provides a simple function to convert an unsigned int to a human readable size. It also provides a few very useful size constants.


## Functions
### size_to_string

Converts an unsigned int into a human-readable size.

string size_to_string(uint64 size, uint8 round_place = 2);

#### Arguments:

* uint64 size: the size to convert.

* uint8 round_place = 2: how many decimal places to round the sizes to.

#### Returns:

The given size as a human-readable string.

#### Example:

```NVGT
#include "size.nvgt"
void main() {
	uint64[] sizes = {193, 3072, 1048576, 3221225472, 1099511627776, 35184372088832};
	string results;
	for (uint i = 0; i < sizes.length(); i++)
		results += sizes[i] + " bytes = " + size_to_string(sizes[i]) + ",\n";
	// Strip off the trailing comma and new line.
	results.trim_whitespace_right_this();
	results.erase(results.length() - 1);
	alert("Results", results);
}
```




## Global Properties
### GIGABYTES

The number of bytes in a gigabyte.

const uint GIGABYTES;

#### Example:

```NVGT
#include "size.nvgt"
void main() {	
	alert("Info", "A gigabyte is " + GIGABYTES + " bytes");
}
```



### KILOBYTES

The number of bytes in a kilobyte.

const uint KILOBYTES;

#### Example:

```NVGT
#include "size.nvgt"
void main() {
	alert("Info", "10 kilobytes is " + 10 * KILOBYTES + " bytes");
}
```



### MEGABYTES

The number of bytes in a megabyte.

const uint MEGABYTES;

#### Example:

```NVGT
#include "size.nvgt"
void main() {
	alert("Info", "19 megabytes is " + 19 * MEGABYTES + " bytes");
}
```



### SIZE_TO_STRING_UNITS

String array of all the supported units for size_to_string().

const array<string> SIZE_TO_STRING_UNITS;

#### Example:

```NVGT
#include "size.nvgt"
void main() {
	string possible_units;
	for (uint i = 0; i < SIZE_TO_STRING_UNITS.length(); i++)
		possible_units += SIZE_TO_STRING_UNITS[i] + ",\n";
	// Strip off the trailing comma and new line.
	possible_units.trim_whitespace_right_this();
	possible_units.erase(possible_units.length() - 1);
	alert("Info", "The possible units are: " + possible_units + ".");
}
```



### TERABYTES

The number of bytes in a terabyte.

const uint TERABYTES;

#### Example:

```NVGT
#include "size.nvgt"
void main() {	
	alert("Info", "A terabyte is " + TERABYTES + " bytes");
}
```





