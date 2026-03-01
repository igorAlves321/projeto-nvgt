# Containers
In this documentation, we consider a container to be any generic class that has the primary purpose of storing more than one value.


## Classes
### array
This container stores a resizable list of elements that must all be the same type. In this documentation, "T" refers to the dynamic type that a given array was instanciated with.
1. `T[]();`
2. `array<T>();`
3. `array<T>(uint count);`

#### Arguments (3):
* uint count: The initial number of items in the array which will be set to their default value upon array instanciation.

#### Remarks:
Items in an array are accessed using what's known as the indexing operator, that is, `arrayname[index]` where index is an integer specifying what item you wish to access within the array. The biggest thing to keep in mind is that unlike many functions in NVGT which will silently return a negative value or some other error form upon failure, arrays will actually throw exceptions if you try accessing data outside the array's bounds. Unless you handle such an exception with a try/catch block, this results in an unhandled exception dialog appearing where the user can choose to copy the call stack before the program exits. The easiest way to avoid this is by combining your array accesses with healthy usage of the array.length() method to make sure that you don't access out-of-bounds data in the first place.

Data in arrays is accessed using 0-based indexing. This means that if 5 items are in an array, you access the first item with `array[0]` and the last with `array[4]`. If you are a new programmer this might take you a second to get used to, but within no time your brain will be calculating this difference for you almost automatically as you write your code, it becomes second nature and is how arrays are accessed in probably 90+% of well known programming languages. Just remember to use `array[array.size() -1]` to access the last item in the array, not `array[array.length()]` which would cause an index out of bounds exception.

There is a possible confusion regarding syntax ambiguity when declaring arrays which should be cleared up. What is the difference between `array<string> items` and `string[] items` and when should either one be used?

At it's lowest level, an array is a template class, meaning it's a class that can accept a dynamic type `(array<T>)`. This concept also exists with the grid, async, and other classes in NVGT.

However, AngelScript provides a convenience feature called the default array type. This allows us to choose just one template class out of all the template classes in the entire engine, and to make that 1 class much easier to declare than all the others using the bracket syntax `(T[])`, and this array class happens to be our chozen default array type in NVGT.

Therefore, in reality `array<T>` and `T[]` do the exact same thing, it's just that the first one is the semantically correct method of declaring a templated class while the latter is a highly useful AngelScript shortcut. So now when you're looking at someone's code and you see a weird instance of `array<T>`, you can rest easy knowing that you didn't misunderstand the code and no you don't need to go learning some other crazy array type, that code author just opted to avoid using the AngelScript default array type shortcut for one reason or another.

You can also create an array using braces, like this:
`array<T> a={item1, item2, item3}`


#### Methods
##### back

Retrieve the last element in the array.

T& array::back();

###### Returns:

The last value in the array.

###### Remarks:

This method is functionally equivalent to `array[-1]`.

An exception will be thrown if the array is empty.

###### Example:

```NVGT
void main() {
	string[] items = {"Blah", "Bleh", "Blur"};
	alert("Last item", items.back());
}
```



##### empty

Determine whether or not the array is empty.

1. bool array::empty();

2. bool array::is_empty();

###### Returns:

bool: true if the array is empty, false if not.

###### Remarks:

This method is functionally equivalent to `array.length() == 0`.

###### Example:

```NVGT
void main() {
	string[] items;
	bool insert = random_bool();
	if (insert)
		items.insert_last(1);
	alert("The array is", items.empty() ? "empty" : "not empty");
}
```



##### erase

Removes an element of an array by a given position.

1. void array::remove_at(uint index);

2. void array::erase(uint index);

###### Arguments:

* uint index: the position to be removed.

###### Remarks:

Please note that the position value is zero-based, and failure to define the correct index will cause NVGT to throw an "index out of bounds" exception.

###### Example:

```NVGT
void main() {
	string[] names = {"HTML", "CSS"};
	names.remove_at(0);
	alert("Languages", join(names, ", "));
}
```



##### extend

Appends the items from another array into this array.

void array::extend(const array<T>& arr);

###### Arguments:

* array<T>& arr: The array to be inserted.

###### Example:

```NVGT
void main() {
	string[] names = {"HTML", "CSS"};
	string[] others = {"JavaScript", "PHP", "ASP"};
	names.extend(others);
	alert("Languages", join(names, ", "));
}
```



##### find

Search for an item in an array.

1. int array::find(const T&in value);

2. 	int array::find(uint start_at, const T&in value);

###### Arguments:

* uint start_at: An optional index to begin searching from.

* const T&in value: The value to search for.

###### Returns:

int: The index of the located item, or -1 if not found.

###### Remarks:

Be ware that this method will start getting slower the larger your array is, this is because this find method must search through every item in the array until it finds an item that equals what you are looking for.

Be sure to never write code like `string value = array[array.find("testing")];` or anything else where you call array.find() directly within the array's indexing operator. This is because array.find() could return -1, meaning that an index out of bounds exception will be thrown if you use the value returned by this function without verifying it first.

###### Example:

```NVGT
void main() {
	string text = "this is a sentence made up of many words, sort of?";
	string[]@ elements = text.split(" ,?.", false);
	int word = elements.find("sort");
	if (word < 0) alert("Oh no not found", "Someone should probably report this if they ever see it while running an unmodified version of this example...");
	else alert("found", "The word sort is at index " + word);
}
```



##### find_by_ref

Search for an object handle in an array.

1. int array::find_by_ref(const T&in value);

2. 	int array::find_by_ref(uint start_at, const T&in value);

###### Arguments:

* uint start_at: An optional index to begin searching from.

* const T&in value: The value to search for.

###### Returns:

int: The index of the located item, or -1 if not found.

###### Remarks:

Be ware that this method will start getting slower the larger your array is, this is because this find method must search through every item in the array until it finds an item that equals what you are looking for.

Be sure to never write code like `string value = array[array.find("testing")];` or anything else where you call array.find() directly within the array's indexing operator. This is because array.find() could return -1, meaning that an index out of bounds exception will be thrown if you use the value returned by this function without verifying it first.

###### Example:

```NVGT
void main() {
	string text = "this is a sentence made up of many words, sort of?";
	string[]@ elements = text.split(" ,?.", false);
	int word = elements.find_by_ref("sort"); // This should fail, as the string used to construct the word "sort" here is different to the actual string object holding the same word in the array.
	if (word < 0) alert("Not found", "We only find references here.");
	else alert("found... How did that happen?", "The word sort is at index " + word);
}
```



##### front

Retrieve the first element in the array.

T& array::front();

###### Returns:

The first value in the array.

###### Remarks:

This method is functionally equivalent to `array[0]`.

An exception will be thrown if the array is empty.

###### Example:

```NVGT
void main() {
	string[] items = {"Blah", "Bleh", "Blur"};
	alert("First item", items.front());
}
```



##### insert

Inserts an element or another array into an array at a given position, moving other items aside to make room if necessary.

1. void array::insert(uint index, const T&in value);

2. void array::insert(uint index, const array<T>& arr);

3. void array::insert_at(uint index, const T&in value);

4. void array::insert_at(uint index, const array<T>& arr);

###### Arguments (1, 3):

* uint index: the position to insert at.

* const T&in value: the element to be inserted.

###### Arguments (2, 4):

* uint index: the position to insert at.

* array<T>& arr: The array to be inserted.

###### Remarks:

This method adds an element to the given position of an array. If you pass index 0, the item will be inserted at the beginning of the aray, and if you pass the array's absolute length, the item will be inserted at the end. Any values less than 0 or greater than the array's absolute length will result in an index out of bounds exception being thrown.

###### Example:

```NVGT
void main() {
	string[] names = {"HTML", "CSS"};
	string[] others = {"JavaScript", "PHP"};
	names.insert_at(2, others);
	names.insert_at(3, "ASP");
	alert("Languages", join(names, ", "));
}
```



##### insert_last

Appends an element to an array.

1. void array::insert_last(const T&in element);

2. void array::push_back(const T&in element);

###### Arguments

* const T&in element: the element to be inserted.

###### Remarks

This method will add the specified element to the end of the array.

###### Example:

```NVGT
void main() {
	string[] names = {"HTML", "CSS"};
	names.insert_last("Java Script");
	alert("Languages", join(names, ", "));
}
```



##### length

Returns the number of items in the array.

1. uint array::length();

2. uint array::size();

###### Returns:

uint: the number of items in the array.

###### Remarks:

This method returns the absolute number of elements in the array, that is, without taking 0-based indexing into account. For example an array containing {1, 2, 3} will have a length of 3, but you must access the last element with the index 2 and the first element with index 0, rather than using 3 for the last item and 1 for the first.

###### Example:

```NVGT
void main() {
	int[] items;
	for (uint i = 0; i < random(1, 10); i++)
		items.insert_last(i);
	alert("The array contains", items.length() + " " + (items.length() == 1 ? "item" : "items"));
}
```



##### random

Returns a random element in the array.

1. const T& array::random() const;

2. const T& array::random(random_interface@ rng) const;

###### Remarks:

This method can be called without a parameter, in which case it will use the default random algorithm, with any of the several built-in random number generators, or any class that implements the random_interface.

###### Example:

```NVGT
void main() {
	string[] items = {"This", "is", "a", "test"};
	alert("Random word", items.random());
}
```



##### remove_last
Removes the last item from the array.

1. `void array::remove_last();`
2. `void array::pop_back();`

###### Remarks:
Calling this method on an empty array will throw an index out of bounds exception.


##### remove_range

Removes a group of items from an array, starting at a given  position and removing the specified number of items after it.

void array::remove_range(uint start, uint count);

###### Arguments:

* uint start: the index to start removing at.

* uint count: the number of items to remove.

###### Example:

```NVGT
void main() {
	string[] items = {"there", "are", "a", "few", "items", "that","will", "disappear"};
	alert("The array currently is", join(items, ", "));
	items.remove_range(1, 3);
	alert("The array is now", join(items, ", "));
}
```



##### reserve
allocates the memory needed to hold the given number of items, but doesn't initialize them.

`void array::reserve(uint length);`

###### Arguments:
* uint length: the size of the array you want to reserve.

###### Remarks:
This method is provided because in computing, memory allocation is expensive. If you want to add 5000 elements to an array and you call array.insert_last() 5000 times without calling this reserve() method, you will also perform nearly 5000 memory allocations, and each one of those is a lot of work for the OS. Instead, you can call this function once with a value of 5000, which will perform only one expensive memory allocation, and now at least for the first 5000 calls to insert_last(), the array will not need to repetitively allocate tiny chunks of memory over and over again to add your intended elements. The importance of this cannot be stressed enough for large arrays, using the reserve() method particularly for bulk array inserts can literally speed your code up by hundreds of times in the area of array management.


##### resize
Resizes the array to the specified size, and initializes all resulting new elements to their default values.

`void array::resize(uint length);`

###### Arguments:
* uint length: how big to resize the array to

###### Remarks:
If the new size is smaller than the existing number of elements, items will be removed from the bottom or the end of the aray until the array has exactly the number of items specified in the argument to this method.


##### reverse

Reverses the array, so the last item becomes the first and vice versa.

void array::reverse();

###### Remarks:

This method reverses the array in place rather than creating a new array and returning it.

###### Example:

```NVGT
void main() {
	string[] items = {"This", "is", "a", "test"};
	alert("The array is currently", join(items, ", "));
	items.reverse();
	alert("The reversed array is", join(items, ", "));
}
```



##### shuffle

Shuffles the contents of the array.

1. void array::shuffle();

2. void array::shuffle(random_interface@ rng);

###### Remarks:

This method can be called without a parameter, in which case it will use the default random algorithm, with any of the several built-in random number generators, or any class that implements the random_interface.

###### Example:

```NVGT
void main() {
	string[] items = {"This", "is", "a", "test"};
	items.shuffle();
	alert("Garble", join(items, " "));
}
```



##### sort
Sorts an array according to a custom algorithm.

`void array::sort(array::less&in, uint startAt = 0, uint count = uint(-1));`

###### Arguments:
* array::less&in: A callback that will be used for comparing items.
* uint startAt: The index to start sorting from (default is 0).
* uint count: The number of elements to sort (default is -1, meaning all elements will be sorted).

###### Remarks:
The callback function to define is implemented as:
`funcdef bool array<T>::less(const T&in a, const T&in b);`
where `t` refers to the array's datatype.

It should return true if A is considered less than B, or false otherwise.

Please note the signature must match exactly - parameters must be declared as `const &in` otherwise it will result in a compilation error.


##### sort_ascending
Sorts an array in ascending order.

`void array::sort_ascending();`
`void array::sort_ascending(uint startAt, uint count);`

###### Arguments (2):
* uint startAt: The index to start sorting from.
* uint count: The number of elements to sort.

###### Remarks:
To sort an array of objects, it is necessary for the class to overload the comparison operator by implementing opCmp.


##### sort_descending
Sorts an array in descending order.

`void array::sort_descending();`
`void array::sort_descending(uint startAt, uint count);`

###### Arguments (2):
* uint startAt: The index to start sorting from.
* uint count: The number of elements to sort.

###### Remarks:
To sort an array of objects, it is necessary for the class to overload the comparison operator by implementing opCmp.



#### Operators
##### opAssign

Overloads the = operator, allowing you to assign an array to another, already existing one.

array& opAssign(const array&in);

###### Arguments:

* const array&in: the array to assign.

###### Example:

```NVGT
void main() {
	string[] a = {"Apple", "Banana", "Cherry"};
	string[] b = a;
	alert("Fruity!", join(b, ", "));
}
```



##### opEquals

Overloads the == operator, checking if two arrays are equal.

bool array::opEquals(const array &in other);

###### Arguments:

* const array&in other: the array to compare.

###### Example:

```NVGT
void main() {
	string[] a = {"Apple", "Banana", "Cherry"};
	string[] b = a;
	if (a == b) alert("Equal", "We have two identical arrays. Hurray.");
}
```



##### opFor

Overloads the OpFor* loop iterators, allowing the foreach loop using a key and a value.

###### Example:

```NVGT
void main() {
	string[] a = {"Apple", "Banana", "Cherry"};
	foreach(string v, int k: a) {
		alert("Array", "Index "+k+"="+v);
	}
}
```



##### opIndex

Overloads the index operator, allowing you to access its elements using square brackets.

###### Example:

```NVGT
void main() {
	string[] a = {"Apple", "Banana", "Cherry"};
	alert("Array", "Index 1="+a[1]);
}
```





### dictionary
This container stores multiple pieces of data of almost any type, which are stored and referenced by unique keys which are just arbitrary strings.
1. `dictionary();`
2. `dictionary({{"key1", value1}, {"key2", value2}});`

#### Arguments (2):
* {{"key", value}}: default values to set in the dictionary, provided in the format shown.

#### Remarks:
The idea behind a dictionary, or hash map / hash table as they are otherwise called, is that one can store some data referenced by a certain ID or key, before later retrieving that data very quickly given that same key used to store it.

Though explaining the details and guts of how hash maps work internally is beyond the scope of this documentation, here is an [overly in depth wikipedia article](https://en.wikipedia.org/wiki/Hash_table) that is sure to teach you more than you ever wished to know about this data structure. Honestly unless you wish to write your own dictionary implementation yourself in a low level language and/or are specifically worried about the efficiency of storing vast amounts of similar data which could stress the algorithm, it's enough to know that the dictionary internally turns your string keys into integer hashes, which are a lot faster for the computer to compare than the characters in the key strings themselves. Combine this with clever use of small lists or buckets determined by even more clever use of bitwise operations and other factors, and what you're left with is a structure that can store thousands of keys while still being able to look up a value given a key so quickly it's like magic, at least compared to the least efficient alternative which is looping through your thousands of data points and individually comparing them in order to find just one value you wish to look up.

NVGT's dictionaries are unordered, meaning that the get_keys() method will likely not return a list of keys in the order that you added them. In cases where this is very important to you, you can create a string array along side your dictionary and manually store key names yourself and then loop through that array instead of the output of get_keys() when you want to enumerate a dictionary in an ordered fassion. Note, of course, that this makes the entire system less efficient as now deleting or updating a key in the dictionary requires you to loop through your string array and find the key that needs deleting or updating, and dictionaries exist exactly to avoid such an expensive loop, though the same efficiency is preserved when simply looking up a key in the dictionary without writing to it, which can be enough in many cases. While in most cases it's best to write code that does not rely on the ordering of items in a dictionary, this at least provides an option to choose between ordering and better efficiency, should you really need such a thing.

Look at the individual documented methods of this class for examples of it's usage.


#### Methods
##### delete

This method deletes the given key from the dictionary.

1. bool dictionary::delete(const string &in key);

2. bool dictionary::erase(const string &in key);

###### Arguments:

* const string &in key: the key to delete.

###### Returns:

bool: true if the key was successfully deleted, false otherwise.

###### Example:

```NVGT
void main() {
	dictionary data;
	data.set("nvgt", "An audiogame engine using AngelScript");
	alert("Information", data.delete("nvgt")); //true
	alert("Information", data.delete("nvgt")); //false because the key is already deleted, another word, it does not exist.
}
```



##### delete_all
This method deletes all keys from the dictionary.

1. `bool dictionary::delete_all();`
2. `bool dictionary::clear();`


##### exists

Returns whether a given key exists in the dictionary.

bool dictionary::exists(const string &in key);

###### Arguments:

* const string &in key: the key to look for.

###### Returns:

bool: true if the key exists, false otherwise.

###### Example:

```NVGT
void main() {
	dictionary data;
	data.set("nvgt", "An audiogame engine using AngelScript");
	alert("Information", data.exists("nvgt")); //true
	alert("Information", data.exists("gameengine")); //false
}
```



##### get

Gets the data from a given key.

bool dictionary::get(const string &in key, ?&out value);

###### Arguments:

* const string &in key: the key to look for.

* ?&out value: the variable for the value to be associated, see remarks.

###### Returns:

bool: true if the dictionary retrieves the value of the key, false otherwise.

###### Remarks:

Please note that the value parameter should be a variable to receive the value. This means that dictionary will write to the variable, not read from.

###### Example:

```NVGT
void main() {
	dictionary data;
	data.set("nvgt", "An audiogame engine using AngelScript");
	string result;
	if (!data.get("nvgt", result))
		alert("Error", "Failed to retrieve the value of the key");
	else
		alert("Result is", result);
}
```



##### get_keys

Returns a string array containing the key names in the dictionary.

string[]@ dictionary::get_keys();

###### Returns:

string[]@: the  list of keys in the dictionary on success, 0 otherwise.

###### Example:

```NVGT
void main() {
	dictionary data;
	data.set("nvgt", "An audiogame engine using AngelScript");
	string[]@ keys = data.get_keys();
	alert("Keys", join(keys, ", "));
}
```



##### get_size

Returns the size of the dictionary.

1. uint dictionary::get_size();

2. uint dictionary::size();

###### Returns:

uint: the size of the dictionary, another word, the total keys on success, 0 otherwise.

###### Example:

```NVGT
void main() {
	dictionary data;
	data.set("nvgt", "An audiogame engine using AngelScript");
	alert("Dictionary size is", data.get_size());
}
```



##### is_empty

Returns whether the dictionary is empty.

1. bool dictionary::is_empty();

2. bool dictionary::empty();

###### Returns:

bool: true if the dictionary is empty, false otherwise.

###### Example:

```NVGT
void main() {
	dictionary data;
	data.set("nvgt", "An audiogame engine using AngelScript");
	alert("Information", data.is_empty()); //false
	data.delete_all();
	alert("Information", data.is_empty()); //true
}
```



##### serialize
Serializes the dictionary into a string.

`string dictionary::serialize();`

###### Arguments:
None.

###### Remarks:
The format used for serializing is different to that used by BGT.

Please note the corresponding deserialize method is a standalone global function.


##### set
Sets the data into a given key.

`void dictionary::set(const string &in key, const ?&in value);`

###### Arguments:
* const string &in key: the key to use.
* const ?&in value: the value to set into this key.

###### Remarks:
If the key already exists in the dictionary, its value will be overwritten.



#### Operators
##### opIndex
Set or retrieve the value of a dictionary by its key.

`int opIndex(* const string &in key);`

###### Arguments:
* const string &in key: the key to use.

###### Remarks:
If the key doesn't exist in the dictionary, it will be created, similar to using the set method.

If the key already exists, its value will be overwritten.

A value can be set as follows:

```
my_dictionary["key"]=value;
```

A value can be retrieved, but requires explicit casting, as follows:

```
string string_value=string(my_dictionary["key_for_string_value"]);
int int_value=int(my_dictionary["key_for_int_value"]);
obj@ object_value=cast<obj>(my_dictionary["key_for_object_value"]);
```




### grid

This type is essentially just a more convenient 2d array. One place it's super useful is when representing a game board.

In this documentation, "T" refers to the dynamic type that a grid was instanciated with.

1. `grid<T>();`

2. `grid<T>(uint width, uint height);`

#### Arguments (2):

* uint width: the width of the grid.

* uint height: the height of the grid.

#### Remarks:

One of the things that makes this class especially convenient is its opIndex overload. It's possible to index into a grid like:

`my_grid[1, 2];`

to access the value at (1, 2) on your grid.

Besides the constructors listed above, you can also make a grid using the brace syntax, similar to arrays, like this:

`grid<T> g={{item1, item2}, {item3, item4}}`

#### Example:

```NVGT
void main() {
	grid<bool> game_board(10, 10); // a 10x10 grid of booleans.
	game_board[4, 4] = true; // set the center of the board to true.
	alert("The center of the board is", game_board[4, 4]);
}
```



#### Methods
##### height

Returns the current height of the grid.

uint grid::height();

###### Returns:

uint: the height  of the grid.

###### Example:

```NVGT
void main() {
	grid<int> g(random(1, 10), random(1, 10));
	alert("Grid height is", g.height());
}
```



##### resize

Resize a grid to the given width and height.

void grid::resize(uint width, uint height);

###### Arguments:

* uint width: the width you want to resize the grid to.

* uint height: the height you want to resize the grid to.

###### Example:

```NVGT
void main() {
	grid<int> g(5, 5);
	alert("Original width and height", g.width() + ", " + g.height());
	g.resize(random(1, 100), random(1, 100));
	alert("New width and height", g.width() + ", " + g.height());
}
```



##### width

Returns the current width of the grid.

uint grid::width();

###### Returns:

uint: the width of the grid.

###### Example:

```NVGT
void main() {
	grid<int> g(random(1, 10), random(1, 10));
	alert("Grid width is", g.width());
}
```




#### Operators
##### opIndex

Get or set the value of a grid cell given an x and a y.

T& grid::opIndex(uint row, uint column);

###### Arguments:

* uint row: the row (x value) to check.

* uint column: the column (y value) to check.

###### Returns:

T&: a reference to the value at the given position. It is of whatever type your grid holds.

###### Remarks:

This function can throw index out of bounds errors, exactly like arrays can, so be careful.

###### Example:

```NVGT
void main() {
	grid<int> the_grid;
	the_grid.resize(5, 5);
	for (uint i = 0; i < 5; i++) {
		for (uint j = 0; j < 5; j++) {
			the_grid[i, j] = random(1, 100);
		}
	}
	alert("Info", "The center is " + the_grid[2, 2]);
}
```






## Functions
### deserialize
Deserializes the contents of a string into a dictionary.

`dictionary@ deserialize(const string&in);`

#### Arguments:
* const string&in: The string to deserialize.

#### Remarks:
The format used for serializing/deserializing is different to that used by BGT.

The corresponding `serialize` function can be found as a method in the dictionary class.




