# User Data Storage and Retrieval (settings.nvgt)
## Classes
### settings
This class is designed to save and load data from files in various formats, specified by the company and product.

`settings();`

#### Remarks:
When this object is first constructed, it will not be active. To activate it you must call the `setup` method, specifying the company name, product name, and optionally the format you wish to use. Please see the setup method documentation for more information and a list of supported formats.


#### Methods
##### setup
This method will setup your company and/or product, and thus the object will be activated, allowing you to interact with the data of the product.

`bool settings::setup(const string company, const string product, const bool local_path, const string format = "ini");`

###### Arguments:
* const string company: the name of your company. This is the main folder for all your products related to this company.
* const string product: the name of your product. This will be the subfolder under the company.
* const bool local_path: toggles whether the data should be saved in the path where the script is being executed, or in the appdata.
* const string format = "ini": the format you wish to use, see remarks.

###### Returns:
bool: true on success, false on failure.

###### Remarks:
The following is a list of supported formats:
* `ini`: default format (.ini).
* `json`: JSON format (.json).
* `nvgt`: this format will use built-in dictionary (.dat).

Note that it does not currently allow you to modify the extentions, for instance, .savedata, .sd, etc. In the future it might be possible and will be documented as soon as it gets implemented.


##### close
This method closes the settings object and therefore the object will be deactivated. From then on you will no longer be able to interact with the data of the company and/or products anymore unless you resetup with `settings::setup` method.

`bool settings::close(bool save_data = true);`

###### Arguments:
* bool save_data = true: toggles whether the data should be saved before closing.

###### Returns:
bool: true on success, false on failure.


##### dump
This method will manually save the data.

`bool settings::dump();`

###### Returns:
bool: true on success, false on failure.

###### Remarks:
Especially if you have the `instant_save` property set to false, you need to call this function to save the data manually. Alternatively, the data will be saved if you close the object with `settings::close` method and set the `save_data` parameter to true, which is default.


##### exists
Determines whether the key exists in the data.

`bool settings::exists(const string&in key);`

###### Arguments:
* const string&in key: the key to look for.

###### Returns:
bool: true if the key exists, false otherwise.


##### has_other_products
Determines whether this company has other products (i.e it has more than 1 products).

`bool settings::has_other_products();`

###### Returns:
bool: true if the company has more than 1 products, false on failure.


##### read_number
Reads the data by a given key, number as value.

`double settings::read_number(const string&in key, double default_value = 0);`

###### Arguments:
* const string&in key: the key to look for.
* double default_value = 0: the value to return if the key could not be retrieved.

###### Returns:
double: the data of the key or default value if the key could not be retrieved.


##### read_string
Reads the data by a given key.

`string settings::read_string(const string&in key, const string&in default_value = "");`

###### Arguments:
* const string&in key: the key to look for.
* const string&in default_value = "": the value to return if the key could not be retrieved.

###### Returns:
string: the data of the key or default value if the key could not be retrieved.


##### remove_product
This method removes the current product.

`bool settings::remove_product();`

###### Returns:
bool: true on success, false on failure

###### Remarks:
This method will delete the directory of the current product if there are other products in the company. Otherwise, the company directory will be deleted.


##### remove_value
This method removes the key from the data.

`bool settings::remove_value(const string&in value_name);`

###### Arguments:
* const string&in value_name: the key to remove.

###### Returns:
bool: true on success, false on failure


##### write_number
this method writes into the data by a given key, number as value.

`bool settings::write_number(const string&in key, double number);`

###### Arguments:
* const string&in key: the key to write to.
* double number: the number to write.

###### Returns:
bool: true on success, false on failure


##### write_string
this method writes into the data by a given key.

`bool settings::write_string(const string&in key, const string&in value);`

###### Arguments:
* const string&in key: the key to write to.
* const string&in value: the value to write.

###### Returns:
bool: true on success, false on failure



#### Properties
##### active
Returns true if the settings object is active (i.e it is possible to use). You cannot use the settings object if this property is false.

`bool settings::active;`


##### company_name
The name of your company. This will be the main folder to save all products related to this company.

`string settings::company_name;`


##### encryption_key
The key to use if you want the data to be encrypted. By default, no encryption key is specified.

`string settings::encryption_key;`


##### instant_save
Toggles whether the data file should be automatically saved as soon as you add the data. true is default option. Turning this off will have to be saved manually using `settings::dump` method.

`bool settings::instant_save;`


##### local_path
Toggles whether the data should be saved in the path where the script is being executed, or in the appdata. false is default.

`bool settings::local_path;`


##### product
The name of your product.

`string settings::product;`






