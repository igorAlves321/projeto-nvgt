# Statistic Management (stat_set.nvgt)
## Classes
### stat_set
#### Methods
##### add
Adds a stat to the set.

`stat@ stat_set::add(const string&in name, var@ value, const string&in text = "", stat_callback@ callback = null, dictionary@ user = null);`

###### Arguments:
* const string&in name: the name of the stat to add.
* var@ value: the starting value for this stat.
* const string&in text = "": an optional text template to be used when getting the value of this stat. In this template, use %0 anywhere you want to output the raw value of the stat itself.
* stat_callback@ callback = null: an optional callback to call every time the value of this stat is requested. One of text or callback has to be provided in order for a stat to work correctly.
* dictionary@ user = null: Not touched by the stat_set itself, allows the linkage of any user values to a stat to help with display.

###### Returns:
stat@: a handle to the newly added stat object.


##### delete
Deletes a stat from the set.

`bool stat_set::delete(const string&in name);`

###### Arguments:
* const string&in name: the name of the stat to be deleted.

###### Returns:
bool: true if the stat was successfully located and deleted, false otherwise.


##### exists
Determine if a stat with the given name exists in the set.

`bool stat_set::exists(const string&in stat_name) const;`

###### Arguments:
* const string&in stat_name: name of the statt to check for.

###### Returns:
bool: true if a stat with the specified name exists in the `stat_set`, false otherwise.


##### reset
Clears all stats from the set.

`void stat_set::reset();`


##### update
Updates a particular stat with a new value.

`void stat_set::update(const string&in name, var@ value);`

###### Arguments:
* const string&in name: the name of the stat to be updated.
* var@ value: the new value of the stat.



#### Operators
##### opIndex
Allows for the easy access of stats with `[...]` syntax.

`stat@ stat_set::opIndex(const string&in stat_name) const;`

###### Arguments:
* const string&in stat_name: the name of the stat you want to access.

###### Returns:
stat@: a handle to a stat with the given name, or null if no stat could be found.



#### Properties
##### size
Returns the number of stats in the set.

`int stat_set::size;`






