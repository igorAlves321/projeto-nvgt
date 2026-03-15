# Streams
## datastreams
Streams, also known as datastreams, are one of the primary ways of moving around and manipulating data in nvgt. With their convenient function calls, low memory footprint when dealing with large datasets and with their ability to connect to one another to create a chain of mutations on any data, datastreams are probably the most convenient method for data manipulation in NVGT that exist.

A datastream could be a file on disk, a file downloading from/uploading to the internet, a simple incapsulated string, or some sort of a manipulator such as an encoder, decryptor or compression stream.

Datastreams can roughly be split into 3 categories, or if you want to be really specific 2.5.
* sources: These streams are things like file objects, internet downloads, or really anything that either inputs new data into the application or outputs data from it. Thus, they can read, write or both depending on the properties of the stream.
* readers: These streams only support read/input operations, an example may be a decoder. Usually these attach to another stream, read data from the connected stream, and mutate that data as the stream is read from.
* writers: The polar opposite of readers, these streams usually connect to another stream E. a file object opened in writing mode where data gets mutated (usually encoded) before being written to the connected stream.

Occasionally, you may see a reader referred to as a decoder, and a writer referred to as an encoder.

Particularly when considering reader and writer streams that manipulate data, you can typically chain any number of streams of the same type together to cause a sequence of data mutations to be performed in one function call. For example you could connect an inflating_reader to a hex_decoder that is in turn connected to a file object in read mode. From that point, calling any of the read functions associated with the inflating stream would automatically first read from the file, hex decode it, and decompress/inflate it as needed. Inversely, you could connect a deflating_writer to a hex encoder which is connected to a file object in write mode, causing any data written to the inflating stream to be compressed, hex encoded, and finally written to the file.

There are a few readers and writers that, instead of manipulating data in any way as they pass through, give you details about that data. You can see counting_reader and counting_writer as examples of this, these streams count the number of lines and characters that are read or written through them.

Lets put this together with a little demonstration. Say you have a compressed and hex encoded file with many lines in it, and you'd like to read the file while determining the line count as the file is read. You could execute the following, for example:
```
counting_reader f(inflating_reader(hex_decoder(file("test.txt", "rb"))));
string result;
while(f.good()) {
	result += f.read(100);
	alert("test", "currently on line " + f.lines + " on character position " + f.pos);
}
f.close();
alert("test", "The file contains a total of " + f.lines + " and after decoding, contains the following text: \n" + result);
```

More datastreams could be added to the engine at any time.

The available datastreams are listed below in this subsection of the documentation.

All streams are derived from the datastream class, so you will want to have a look at the documentation for that class first before seeing what extras are provided by the datastream you want to work with.


## datastream

The base class for all datastreams, this stream can read and write to an internal string buffer maintained by the class if constructed directly. Any other datastream can also be cast to the "datastream" type to facilitate passing datastreams of any type throughout the application, and thus any child datastreams such as encoders, file sources or any others will contain the functions listed here as they are derived from the datastream class.

1. datastream();

2. datastream(string initial_data = "", string encoding = "", datastream_byte_order byteorder = STREAM_BYTE_ORDER_NATIVE);

### Arguments (2):

* string initial_data = "": The initial contents of this stream derived from a string.

* string encoding = "": The text encoding used to read or write strings to this stream (see remarks), this argument appears in all non-empty child datastream constructors.

* datastream_byte_order byteorder = STREAM_BYTE_ORDER_NATIVE: The byte order to read or write binary data to this stream using (see remarks), this argument appears in all non-empty child datastream constructors.

### Remarks:

If this class is directly instantiated, the effect is basically that the string class gets wrapped with streaming functions. The default datastream class will create an internal string object, and any data passed into the initial_data parameter will be copied to that internal string. Then, the read/write functions on the stream will do their work on the internal string object held by the datastream class, which can be read or retrieved in full at any time. Internally, this wraps the std::stringstream class in c++.

It must be noted, however, that this is the parent class for all other datastreams in nvgt. This means that any child datastream such as the file class can be cast to a generic datastream handle. In this case, the read/write functions for the casted handle will perform the function of the child stream which has been casted instead of on an internal string. This is the same for any other parent/child class relationship in programming, but it was mentioned here to avoid any confusion between the default datastream implementation and a datastream handle casted from a different stream.

The encoding argument, present in nearly all child datastream  constructors, controls what encoding if any strings should be converted to from UTF8 as they are written to the stream with the write_string() function or << operator while the binary property on the stream is set to true, as well as what encoding to convert from when reading them with read_string() or the >> operator. If set to an empty string (the default), strings are left in UTF8 when writing, and already expected to be in UTF8 in a stream when reading from it.

The byteorder argument, again present in nearly all child datastream constructors, controls what endianness is used when reading/writing binary data from/to a stream, that is the read_int/write_float/similar functions when the binary property on the stream is set to true. When a value takes more than one byte, the endianness or byte order controls whether the bytes of that value are read/written from left to right or right to left, or in proper terms whether the most significant byte of the value should be written first. The values that can be accepted here are:

* STREAM_BYTE_ORDER_NATIVE (default): The byte order used by the system the script is running on.

* STREAM_BYTE_ORDER_BIG_ENDIAN: The most significant byte is read/written first.

* STREAM_BYTE_ORDER_NETWORK: Same as STREAM_BYTE_ORDER_BIG_ENDIAN, provided because this is indeed a very common name for the big endian byte order as it is typically used for data transmission.

* STREAM_BYTE_ORDER_LITTLE_ENDIAN: The most significant byte is read/written last.

Usually, you can leave the byteorder value at the default for most streams. However in some situations where you are transmitting binary data between systems running on different architectures, it may be better to set the transmitting and receiving streams of such an application to a common byte order that is not system native.

Though this was mentioned above, it's worth reiterating once more that all other stream types contain all of the functions listed in this base datastream class unless otherwise noted, and thus are not documented multiple times in child classes.

If an initial_data argument is provided when constructing a datastream, the stream will be set at the beginning, ready to read the initial data rather than at the end. If you wish to append more data to the datastream after it is constructed, you should call the seek_end() method on it first.

### Example:

```NVGT
void main() {
	datastream ds1("This is a demonstration.");
	alert("example", ds1.read()); // Will display "This is a demonstration."
	datastream ds2;
	ds2.write("Hello there, ");
	ds2.write("good bye.");
	ds2.seek(0);
	alert("example", ds2.read()); // Will display "Hello there, good bye."
	// The following shows how this datastream can be used as an area to store encoded data.
	datastream encoded;
	hex_encoder h(encoded); // We attach the encoded datastream to a hex encoder.
	h.write("I am a hex string"); // "I am a hex string" in hex is written to the datastream object called encoded.
	h.close();
	encoded.seek(0);
	alert("example", hex_decoder(encoded).read()); // We attach a hex_decoder to the encoded datastream and read from it, thus this will display "I am a hex string".
}
```



### Methods
#### close

Close a datastream, freeing any associated resources and leaving the datastream in an inactive state.

bool close(bool close_connected = false);

##### arguments:

* bool close_connected = false: Whether to also close any streams that are connected to this one (see remarks).

##### Returns:

bool: true on success, false on failure such as if the stream is already closed.

##### Remarks:

Generally it is best to call this function when you are done working with any stream, particularly when dealing with files, encoders, or any stream that is opened in write mode. In reality there are a few streams, such as the default datastream class, where it is OK to not call the close method.

The reason that it is sometimes OK to not call the close function on a stream when you are done with it is because this function is automatically called in the internal destructor for any datastream, meaning when any datastream object is destroyed, it's close method will be called. For some streams like the default datastream class which is just wrapping a string, this is fine (you don't close a string, after all), but in many cases you will want to close a stream at a certain time before it is destroyed. For example closing an encoding stream may write a few final characters to a connected file stream as it is closing, meaning that the close method on the encoder must be called prior to the close function on the stream connected to it, something which you may not have control of when objects are getting destructed.

The close_connected argument controls whether to also close any streams that are connected to the stream that close is being called on. For the default datastream class that wraps a string or for any other datastream that doesn't connect to another one, this argument has no effect.

##### Example:

```NVGT
void main() {
	datastream ds;
	ds.close();
	alert("example", ds.active); // Will display false, as the stream is no longer active.
	alert("example", ds.write("this is a test")); // Will return 0 instead of a positive number of bytes written as the stream is not opened.
	ds.open();
	alert("example", ds.write("this is a test")); // Now returns 14, as expected.
	// Calling the close method a final time is not required for this example because it uses an instance of the default datastream class. It will be taken care of when the script exits.
}
```



#### close_all

Close a datastream as well as any that are connected to it.

bool close_all();

##### Returns:

bool: true if the stream and any connected to it could be closed, false otherwise.

##### Remarks:

This is exactly the same thing as calling the close method with the close_connected boolean argument set to true. On the default datastream class it will have no effect besides freeing the internal string, however you can look at the example below to see a case where there is an effect by calling close_all().

##### Example:

```NVGT
void main() {
	datastream ds;
	hex_encoder h(ds);
	h.write("hi");
	h.close_all(); // Will also close the datastream called ds because it is connected to the hex encoder.
	alert("example", ds.active); // Will display false, indicating that calling h.close_all() also caused ds.close() to implicitly be called.
}
```



#### get_pos

Retrieve the offset of a datastream.

int get_pos();

##### Arguments:

None.

##### Returns:

int: Returns the byte offset of the stream.

##### Example:

```NVGT
void main() {
	datastream ds;
	if (!ds.open("this is a demonstration")) {
		alert("Oh no", "Maybe this could happen for a file but it should never happen for a basic datastream!");
		exit();
	}
	ds.seek(10);
	alert("Position", ds.get_pos());
}
```



#### open

Open a datastream, connecting it to a source or another stream depending on type.

bool open(...);

##### Arguments:

Same as in the constructor for the datastream you wish to open (see remarks).

##### Returns:

bool: Returns true if the stream could be opened, false otherwise.

##### Remarks:

Most datastreams can be closed and then reopened, or can be created in an uninitialized state meaning they must be opened to begin with.

All datastreams can be constructed in an already initialized/opened state, and the constructors that allow this for each stream will contain the exact same arguments as that streams associated open() function, and each streams constructor topics is where such arguments are documented.

For example, the true signature for the open function on the default datastream class is bool open(string initial_data = "", string encoding = "", datastream_byteorder byteorder = STREAM_BYTE_ORDER_NATIVE) while the signature of the open function for the file datastream is bool open(string filename, string mode, string encoding = "", datastream_byte_order byteorder = STREAM_BYTE_ORDER_NATIVE).

As mentioned in the top level datastreams topic, the encoding and byteorder arguments are present in each stream and thus will not be redocumented for each one.

For all streams, this function will call the associated close() function prior to opening the requested resource if the stream is already active at this time. If it turns out that users do not desire this behaviour, it may be made optional or could get removed in the future.

##### Example:

```NVGT
void main() {
	datastream ds;
	if (!ds.open("this is a demonstration")) {
		alert("Oh no", "Maybe this could happen for a file but it should never happen for a basic datastream!");
		exit();
	}
	alert("example", ds.read()); // Will display "this is a demonstration".
}
```



#### read

Read raw bytes from a stream.

string read(uint amount = 0);

##### Arguments:

* uint amount = 0: The number of bytes to read, or 0 to read the entire stream. Only applicable for strings.

##### Returns:

string: The data that was read from the stream or an empty string on failure.

##### Remarks:

If the length of the string returned by this function is less than the number of bytes requested in the amount argument, either the end of the stream was reached or there was an error. You can check what happened by evaluating the fail or eof properties on the stream.

This is the lowest level method of reading from a stream. All other reading functions either read a certain datatype or until a certain condition is met.

This should not be confused with the read_string function.

Typically it is only useful to call this function if the good property on the stream is true, therefor you can query the stream's good property in a loop to see if you should continue reading data if you are trying to perform some sort of buffered reading of a stream.

##### Example:

```NVGT
void main() {
	datastream ds("Hello there, I am a string wrapped in a sstream!");
	alert("example", ds.read(6)); // Will display Hello followed by a space.
	alert("example", ds.read()); // Will display there, I am a string wrapped in a sstream!
}
```



#### read_double

Read raw bytes from a stream into a double.

double read_double();

##### Arguments:

None.

##### Returns:

double: The data that was read, or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds("Hello there, I am a string wrapped in a sstream!");
	alert("example", ds.read_double()); // Will return the first 8 bytes of the string as a double.
}
```



#### read_float

Read raw bytes from a stream into a float.

float read_float();

##### Arguments:

None.

##### Returns:

float: The data that was read, or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds("Hello there, I am a string wrapped in a sstream!");
	alert("example", ds.read_float()); // Will return the first 4 bytes of the string as a float.
}
```



#### read_int

Read raw bytes from a stream into a 32-bit integer.

int read_int();

##### Arguments:

None.

##### Returns:

int: The data that was read from the stream or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds("Hello there, I am a string wrapped in a sstream!");
	alert("example", ds.read_int()); // Will display the first 4 bytes of the string as an integer.
}
```



#### read_int16

Read raw bytes from a stream into a 16-bit integer.

int16 read_int16();

##### Arguments:

None.

##### Returns:

int16: The data that was read from the stream or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds("Hello there, I am a string wrapped in a sstream!");
	alert("example", ds.read_int16()); // Will display the first two bytes of the string as an integer.
}
```



#### read_int64

Read raw bytes from a stream into a 64-bit integer.

int64 read_int64();

##### Arguments:

None.

##### Returns:

int64: The data that was read from the stream or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds("Hello there, I am a string wrapped in a sstream!");
	alert("example", ds.read_int64()); // Will display the first eight bytes of the string as an integer.
}
```



#### read_int8

Read raw bytes from a stream into an 8-bit integer.

int8 read_int8();

##### Arguments:

None.

##### Returns:

int8: The data that was read from the stream or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds("Hello there, I am a string wrapped in a sstream!");
	alert("example", ds.read_int8()); // Will display the first byte of the string as an integer (72).
}
```



#### read_string

Read a string from a stream.

string read_string();

##### Arguments:

None.

##### Returns:

string: The data that was read from the stream or an empty string on failure.

##### Remarks:

This method behaves differently depending on the binary flag:

* If binary is true, it expects the number of bytes to read to be prepended to the string as a uint8.

* If binary is false, it will read a single word from the string using any whitespace as its boundary.

Typically it is only useful to call this function if the good property on the stream is true, therefor you can query the stream's good property in a loop to see if you should continue reading data if you are trying to perform some sort of buffered reading of a stream.

##### Example:

```NVGT
void main() {
	datastream ds("Hello there,\nI am a string wrapped in a sstream!");
	ds.binary=false;
	alert("example", ds.read_string()); // Returns "Hello".
	alert("example", ds.read_string()); // Returns "there,".
}
```



#### read_uint

Read raw bytes from a stream into a 32-bit unsigned integer.

uint read_uint();

##### Arguments:

None.

##### Returns:

uint: The data that was read from the stream or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds("Hello there, I am a string wrapped in a sstream!");
	alert("example", ds.read_uint()); // Will display the first four bytes of the string as an unsigned integer.
}
```



#### read_uint16

Read raw bytes from a stream into a 16-bit unsigned integer.

uint16 read_uint16();

##### Arguments:

None.

##### Returns:

uint16: The data that was read from the stream or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds("Hello there, I am a string wrapped in a sstream!");
	alert("example", ds.read_uint16()); // Will display the first two bytes of the string as an unsigned integer.
}
```



#### read_uint64

Read raw bytes from a stream into a 64-bit unsigned integer.

uint64 read_uint64();

##### Arguments:

None.

##### Returns:

uint64: The data that was read from the stream or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds("Hello there, I am a string wrapped in a sstream!");
	alert("example", ds.read_uint64()); // Will display the first eight bytes of the string as an unsigned integer.
}
```



#### read_uint8

Read raw bytes from a stream into an 8-bit unsigned integer.

uint8 read_uint8();

##### Arguments:

None.

##### Returns:

uint8: The data that was read from the stream or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds("Hello there, I am a string wrapped in a sstream!");
	alert("example", ds.read_uint8()); // Will display the first byte of the string as an unsigned integer (72).
}
```



#### seek

Seek to an offset in the datastream.

bool seek(int offset);

##### Arguments:

offset: The byte offset you wish to seek to.

##### Returns:

bool: Returns true if the stream could seek, false otherwise.

##### Remarks:

Note that most datastreams do not support seeking as this would result in needing to store more data in memory than we are comfortable with, however, file objects and raw datastreams that read from a string do support seeking. Other than these stream types, you should assume that seek operations are not supported unless otherwise documented.

##### Example:

```NVGT
void main() {
	datastream ds;
	if (!ds.open("this is a demonstration")) {
		alert("Oh no", "Maybe this could happen for a file but it should never happen for a basic datastream!");
		exit();
	}
		ds.seek(10);
alert("example", ds.read()); // Will display "demonstration".
}
```



#### write

Write raw bytes to a stream.

uint write(string content);

##### Arguments:

* content: The content that is to be written.

##### Returns:

uint: the number of bytes written.

##### Remarks:

If needed, you can use the returned value to verify whether the data you intended to write to the stream was written successfully by checking whether the return value of this function matches the length of the data you passed to it.

##### Example:

```NVGT
void main() {
	// This time we'll use a file which is another type of datastream to show how the functions in this datastream class work on it's children.
	file f("test.txt", "wb");
	string data = "This is a test file";
	bool success = f.write(data) == data.length();
	f.close();
	alert("Information", "The file with the data has been " + (success? "successfully" : "unsuccessfully") + " written");
}
```



#### write_double

Write the value of a double into a stream.

uint write_double(double value);

##### Arguments:

* value: The value that is to be written.

##### Returns:

uint: the number of bytes written.

##### Example:

```NVGT
void main() {
	datastream ds;
	ds.write_double(5.5);
}
```



#### write_float

Write the value of a float into a stream.

uint write_float(float content);

##### Arguments:

* content: The content that is to be written.

##### Returns:

uint: the number of bytes written.

##### Example:

```NVGT
void main() {
	datastream ds;
	ds.write_float(5.5);
}
```



#### write_int

Write the value of a 32-bit integer into a stream.

uint write_int(int content);

##### Arguments:

* content: The content that is to be written.

##### Returns:

uint: the number of bytes written.

##### Example:

```NVGT
void main() {
	datastream ds;
	ds.write_int(4);
}
```



#### write_int16

Write the value of a 16-bit integer into a stream.

uint write_int16(int16 content);

##### Arguments:

* content: The content that is to be written.

##### Returns:

uint: the number of bytes written.

##### Example:

```NVGT
void main() {
	datastream ds;
	ds.write_int16(4);
}
```



#### write_int64

Write the value of a 64-bit integer into a stream.

uint write_int64(int64 content);

##### Arguments:

* content: The content that is to be written.

##### Returns:

uint: the number of bytes written.

##### Example:

```NVGT
void main() {
	datastream ds;
	ds.write_int64(4);
}
```



#### write_int8

Write the value of an 8-bit integer into a stream.

uint write_int8(int8 content);

##### Arguments:

* content: The content that is to be written.

##### Returns:

uint: the number of bytes written.

##### Example:

```NVGT
void main() {
	datastream ds;
	ds.write_int8(4);
}
```



#### write_string

Write a string into a stream.

uint write_string(string content);

##### Arguments:

* content: The content that is to be written.

##### Returns:

uint: the number of bytes written.

##### Remarks:

This method behaves differently depending on the binary flag:

* If binary is true, it prepends the number of bytes to write as a uint8.

* If binary is false, it will merely write the entire string.

##### Example:

```NVGT
void main() {
	datastream ds;
	ds.binary=true;
	ds.write_string("Hello");
	alert("Test", ds.read());
}
```



#### write_uint

Write the value of a 32-bit unsigned integer into a stream.

uint write_uint(uint content);

##### Arguments:

None.

##### Returns:

uint: The data that was read from the stream or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds;
	ds.write_uint(8);
}
```



#### write_uint16

Write the value of a 16-bit unsigned integer into a stream.

uint write_uint16(uint16 content);

##### Arguments:

None.

##### Returns:

uint16: The data that was read from the stream or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds;
	ds.write_uint16(1);
}
```



#### write_uint64

Write the value of a 64-bit unsigned integer into a stream.

uint write_uint64(uint64 content);

##### Arguments:

None.

##### Returns:

uint64: The data that was read from the stream or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds;
	ds.write_uint64(50);
}
```



#### write_uint8

Write the value of an 8-bit unsigned integer into a stream.

uint write_uint8(uint8 content);

##### Arguments:

None.

##### Returns:

uint8: The data that was read from the stream or 0 on failure.

##### Example:

```NVGT
void main() {
	datastream ds;
	ds.write_uint8(12);
}
```




### Properties
####  active
This property will be true if a stream is opened and ready for use, false otherwise.

`const bool active;`



#### available

This property returns the number of bytes immediately available to be read from a stream.

const int available;

##### Remarks:

This property may not be implemented in all streams, for example decoders. If it is unavailable, it will return 0.

##### Example:

```NVGT
void main() {
	datastream ds("example");
	alert("example", ds.available); // Displays 7.
	ds.read(2);
	alert("example", ds.available); // Now shows 5, as 2 of the 7 bytes have been read.
}
```



#### bad

This property will be true if the previous function failed with a fatal error.

const bool bad;

##### Remarks:

This is good for checking the success or failure of the last operation. It differs from fail in that this is generally set in unrecoverable errors (such as device failure or unreadable data).

##### Example:

```NVGT
void main() {
	datastream ds("Hi");
	ds.read();
	alert("example", ds.bad); // If this returns true, something is seriously wrong.
}
```



#### binary
Set this property to true to work with binary data, or false to work with text. Defaults to true.

`bool binary;`



#### eof

This property will be true on a stream when it has no more data to read.

const bool eof;

##### Example:

```NVGT
void main() {
	datastream ds("hello");
	alert("example", ds.eof); // Will show false because we always start at the beginning of a default datastream, thus there is data to read.
	ds.read();
	alert("example", ds.eof); // Will now show true because any further .read calls will fail as we have reached the end of the stream.
	ds.seek(3);
	alert("example", ds.eof); // Will again show false because we are no longer at the end of the stream.
}
```



#### fail

This property will be true if the previous function failed.

const bool fail;

##### Remarks:

This is good for checking the success or failure of the last operation. It differs from bad in that this is generally set in recoverable errors (EOF, type mismatch and so on).

##### Example:

```NVGT
void main() {
	datastream ds;
	alert("example", ds.fail); // Will display false because we haven't done anything yet.
	ds.read(); // Error, nothing there.
	alert("example", ds.fail); // Will now display true because there was an error reading.
}
```



#### good

This property will be true when a datastream is ready to read or write, such as when the active property is true and the end of file has not been reached.

const bool good;

##### Remarks:

This property is specifically true so long as the stream is opened and the eof, fail, and bad properties all return false.

##### Example:

```NVGT
void main() {
	datastream ds("hello");
	alert("example", ds.good); // Will display true because there is data to read.
	ds.read();
	alert("example", ds.good); // Will now display false because the end of file has been reached, ds.eof is true now.
}
```





## file
The file datastream is used to read and write files stored on the hard disk.

1. `file();`
2. `file(const string path, const string mode);`

### Arguments (1):
* const string path: the filename to open.

### Arguments (2):
* const string path: the filename to open.
* const string mode: the mode to open as.

### Remarks:
Usually when the file object is first created, it will not be active, that is, it will not be associated with a file on disk. To activate it, use the following methods:

* Call the open function.
* use the second constructor.

Please note that both methods require the filename that is to be associated and the mode to open, with the only difference being that it is harder to tell whether the file was opened successfully if you use the constructor rather than the open method. Using the second constructor makes it 1 line shorter. The possible open modes will not be documented in this remarks, you can see it in `file::open` method.

Remember that as with all datastreams, all methods in the base datastream class will work on the file class unless noted otherwise and thus will not be redocumented here.


### Methods
#### open

This method will open a file for reading or writing.

bool file::open(string filename, string open_mode);

##### Arguments:

* string filename: the name of the file to open. This can be either an absolute or relative path.

* string open_mode: the mode to open, see remarks.

##### Returns:

bool: true on success, false on failure.

##### Remarks:

While on some operating systems (mostly windows) both the slash(`/`), and the backslash(`\`) can be used to specify the filename, it is very strongly recommended to use the / character for greatest cross platform compatibility.

The following is a list of valid open modes.

* a: append.

* w: write.

* r: read.

* r+: read and write.

For backwards compatibility with code that used a version of the file object from when there was a difference between text and binary file open modes, a b character is also accepted (for example rb) to indicate binary. The current stream implementation ignores this character other than to gracefully accept it rather than complaining that it is an invalid mode. You can use other text encoding APIs such as string_recode and the line_converting_reader if you really need to try recreating something similar to the old behavior.

The file will be created if the file does not exist if opened in either write or append mode. When opened in read mode, the file must exist in order to be successful.

##### Example:

```NVGT
void main() {
	file f;
	f.open("test.txt", "wb");
	f.write("This is a test");
	f.close();
	alert("Information", "The file has been written");
}
```




### Properties
#### size

Determine the size (in bytes) of the file that is currently associated with this stream.

const uint64 size;

##### Remarks:

This property will be 0 if no file is associated with this stream, in which case you can use the datastream::active property on it to check the difference between a 0 byte file and an eronious result.

When files are opened in write mode, there could be periods where the written data has not yet been flushed to disk in which case this property may have a value which is a little bit behind. Experiments seem to indicate that this rarely if never happens, however it's worth putting the note here just encase anyone runs into it.

Note that a file_get_size() function exists in the engine which is usually better than this property unless you need to do more with a file than just get it's size.

##### Example:

```NVGT
void main() {
	file f("size.nvgt", "rb");
	if (!f.active) {
		alert("oops", "couldn't load the file");
		return;
	}
	alert("size.nvgt is", f.size + "b");
	f.close();
}
```






