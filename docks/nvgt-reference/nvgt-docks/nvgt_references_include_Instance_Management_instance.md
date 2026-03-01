# Instance Management (instance.nvgt)
## Instance Management
This include provides the `instance` class, which allows you to manage the way multiple instances of your game are handled. For example, you could use this class to check if your game is already running, or stop it from running until only one instance exists.


## Classes
### instance
#### Methods
##### wait_until_standalone
This method will make any instances of your game block until there's only one instance still alive.

`void instance::wait_until_standalone();`



#### Properties
##### is_already_running

Determines if an instance of the application is already running.

bool instance::is_already_running;

###### Example:

```NVGT
#include "instance.nvgt"
void main() {
	instance example("instance_checker_example");
	if (example.is_already_running) {
		alert("Info", "The script is already running.");
		exit();
	}
	alert("Info", "After you press OK, you'll have 15 seconds to run this script again to see the result");
	wait(15000);
}
```







