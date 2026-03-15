# Concurrency
This section contains the documentation for all mechanisms revolving around several things running at once, usually involving threads and their related synchronization facilities.

A warning that delving into this section will expose you to some rather low level concepts, the misapplication of which could result in your program crashing or acting oddly without the usual helpful error information provided by NVGT.

The highest level and most easily invoked method for multithreading in nvgt is the async template class, allowing you to call any script or system function on another thread and retrieve its return value later.



## Classes
### async

A template class that allows one to very easily call any function in nvgt on another thread and fetch that function's return value after the call has complete.

1. async\<T\>();

2. async\<T\>(const ?&in function, const ?&in arg1, const ?&in arg2, ...);

#### Template arguments:

* T: The return type of the function being called.

#### Arguments (2):

* const ?&in function: The function that should be called, passing anything that is not a function will result in an exception.

* const ?&in arg1: The function's first argument, you do not need to pass more arguments than needed.

* const ?&in arg2: The function's second argument, passing invalid or mismatched datatypes as any of these arguments will cause an exception.

* ... Up to 15 arguments.

#### Remarks:

Generally speaking, this is the most convenient method of applying multithreading to your nvgt application. While lower level methods of dealing with threads require the programmer to create functions with specific signatures that usually don't allow for return values, this class allows you to quite transparently call any function in the application from a function in your script to the alert box built into NVGT on another thread while still maintaining the return value of such a function for later retrieval.

For ease of use, the constructor of this class actually calls the function provided and passes the given arguments to it. Therefor, the standard use case for this class is to create an instance of it, then to first call instance.wait() or instance.try_wait(ms) before retrieving the instance.value variable when the function's return value is needed, after either instance.wait() returns or after instance.try_wait() returns true. Using the instance.complete/instance.failed properties with your own waiting logic is also perfectly acceptable and sometimes recommended.

The one drawback that makes this class look a little less pretty is that if you wish to call functions that are part of a class, you must create funcdefs for the signature of the function you want to call, then wrap the object's function in an instance of the funcdef. For example if a class contained a function bool load(string filename), you must declare funcdef void my_void_funcdef(string); and if you then had an instance of such a class called my_object, you must initialize the async object like async\<bool\>(my_void_funcdef(my_object.load), "my_file.txt"); however it is a relatively minor drawback.

Be aware that this class can throw exceptions if you do not pass arguments to the function correctly, this is because the function call happens completely at runtime rather than being prepared at compilation time like the rest of the script.

Internally, this function is registered with Angelscript multiple times with an expanding number of arguments, meaning that it is OK to pass only the number of arguments you need to a function you want to call even though this function's signature seems to indicate that the dynamically typed arguments here don't have a default value.

#### Example:

```NVGT
void main() {
	show_window("example");
	async<int>@ answer = async<int>(question, "exit program", "Do you want to exit the program?");
	// Now that the user sees the dialog, lets play a sound.
	sound s;
	s.load("c:/windows/media/ding.wav");
	s.play_looped();
	// We will move the sound around the stereo field just to drive home the point that we can execute our own code while the dialog is showing.
	int pan = 0;
	while(true) {
		wait(25); // A slower value than average for the sake of the pan effect, will make window a bit unresponsive though (use a timer).
		pan += random(-2, 2);
		if (pan < -100) pan = -100;
		else if (pan > 100) pan = 100;
		s.pan = pan;
		if (answer.complete) { // The async function has successfully finished and a return value is available.
			if (answer.value == 1) exit();
			else @answer = async<int>(question, "exit program", "Now do you want to exit the program?");
		}
	}
}
```



#### Methods
##### try_wait

Wait a given number of milliseconds for an async call to complete.

bool try_wait(uint milliseconds);

###### Arguments:

* uint milliseconds: The amount of time to wait, may be 0 to not wait at all.

###### Returns:

bool: True if the async call has finished, or false if it is still running after the given number of milliseconds has expired.

###### Remarks:

If you try waiting for 50ms but the async call finishes in 10ms, the try_wait call will only block for 10 out of the 50ms requested. In short, any blocking try_wait call is canceled prematurely with the try_wait function returning true if the call finishes while try_wait is in the middle of executing.

If the function has already finished executing or if this async object is not connected to a function (thus nothing to wait for), try_wait() will immediately return true without waiting or blocking at all regardless of arguments.

Similar to the async::wait function, you should be careful using this method in the same thread that show_window was called or if you do, make sure to call it with tiny durations and interspurse standard nvgt wait(5) or similar calls in your loops so that window messages and events continue to be handled.

###### Example:

```NVGT
void main() {
	// Pan a sound around while an alert box shows, no window.
	async<int> call(alert, "hi", "press ok to exit");
	sound s;
	s.load("c:/windows/media/ding.wav");
	s.play_looped();
	while (!call.try_wait(40)) { // We'll use the blocking provided by try_wait for our timer.
		s.pan += random(-3, 3);
	}
}
```



##### wait

Wait for the async function to finish executing.

void wait();

###### Remarks:

This is the simplest way to wait for the execution of an async function to complete, however it does not allow you to execute any of your own code while doing so. The execution of your program or the thread you called the wait function on will be completely blocked until the async function returns. This also means that window events cannot be received while the wait function is executing, so you should be very careful about using this from an environment with a game window especially on the thread that created it.

For more control such as the ability to execute your own code during the wait, check out the try_wait() function.

If the async object this function is called on is executed with a default constructor and thus has no function call in progress, this function will return immediately as there is nothing to wait for.

###### Example:

```NVGT
void main() {
	async<string> result(input_box, "name", "please enter your name");
	result.wait(); // Input_box creates a dialog on it's own thread so the remark about windowing doesn't apply in this situation.
	alert("test", "hello " + result.value); // May not focus automatically because from a different thread than the input box.
}
```




#### Properties
##### complete

Immediately shows whether an async function call has completed, meaning that either a result is available or that there has been an error.

const bool complete;

###### Remarks:

This is the best and prettiest looking method of checking whether an async call has completed or not without blocking. You can also call the try_wait() function with an argument of 0 for a similar effect, though this looks nicer and takes any uninitialized state of the object into account.

Usually this will be used when a loop has some other sort of waiting logic, such as the global nvgt wait() function we are all familiar with.

###### Example:

```NVGT
void main() {
	sound s; // Press space to play even while alert box is opened.
	s.load("c:/windows/media/ding.wav");
	async<int> call(alert, "test", "press ok to exit"); // May need to alt+tab to it, window is shown after.
	show_window("example"); // Shown after alert because otherwise alert will be child of the window.
	while(!call.complete) {
		wait(5);
		if (key_pressed(KEY_SPACE)) {
			s.stop();
			s.play();
		}
	}
}
```



##### exception

A string describing any exception that took place during an async function call.

const string exception;

###### Remarks:

If there has been no error or if the async object has no attached function call, a blank string will be returned.

###### Example:

```NVGT
funcdef void return_void_taking_uint(uint);
void main() {
	string[] my_empty_array;
	async<void> result(return_void_taking_uint(my_empty_array.remove_at), 0); // We are calling my_empty_array.remove_at(0) on another thread, sure to cause an exception because the array is empty.
	result.wait();
	alert("test", result.exception);
}
```



##### failed

Returns true if an async function call has thrown an exception.

const bool failed;

###### Remarks:

This is a shorthand version of executing the expression (async.try_wait(0) and async.exception != ""), provided for syntactical ease.

###### Example:

```NVGT
string throw_exception_randomly() {
	if (random_bool(50)) throw("oh no!");
	return "yo yo";
}
void main() {
	async<string> result(throw_exception_randomly);
	result.wait();
	if (result.failed) alert("oops", result.exception);
	else alert("success", result.value);
}
```



##### value

Contains the return value of a successful async function call.

const T& value;

###### Remarks:

Remember that this class is a template type, so T will adapt to whatever type was being used when the async object was constructed.

If a value is not yet available, the wait function will be internally called upon first access to this property, meaning that accessing this property could cause your program to block until data is available. You are meant to call the wait/try_wait functions or check the complete property first before accessing this.

If an async object is initialized with the default constructor meaning it has no function attached, for example async\<string\> result; accessing result.value will throw an exception because no data will ever be available in this context.

###### Example:

```NVGT
void main() {
	// Lets demonstrate the edge cases mentioned above as most examples in the documentation for this class show off this property being used normally.
	async<string> result1(input_box, "type text", "enter a value");
	alert("test", result1.value); // The main thread will block until result1.value is available. Be careful!
	async<sound@> result2; // This is not connected to a function, maybe the object could be reassigned to a result later.
	sound@ s = result2.value; // Will throw an exception!
}
```





### atomic_flag
An `atomic_flag` is a fundamental synchronization primitive that represents the simplest form of an atomic boolean flag that supports atomic test-and-set and clear operations. The `atomic_flag` type is specifically designed to guarantee atomicity without the need for locks, ensuring that operations on the flag are performed as indivisible actions even in the presence of concurrent threads. Unlike `atomic_bool`, `atomic_flag` does not provide load or store operations.

```nvgt
atomic_flag();
```

#### Remarks:
Unlike all other atomic types, `atomic_flag` is guaranteed to be lock-free.


#### methods
##### clear
Atomically changes the state of an `atomic_flag` to clear (false). If order is one of MEMORY_ORDER_ACQUIRE or MEMORY_ORDER_ACQ_REL, the behavior is undefined.

```nvgt
void clear(memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters:
* `order`: the memory synchronization ordering.


##### notify_all
Unblocks all threads blocked in atomic waiting operations (i.e., `wait()`) on this `atomic_flag`, if there are any; otherwise does nothing.

```nvgt
void notify_all();
```

###### Remarks:
This form of change detection is often more efficient than pure spinlocks or polling and should be preferred whenever possible.



##### notify_all
Unblocks at least one thread blocked in atomic waiting operations (i.e., `wait()`) on this `atomic_flag`, if there is one; otherwise does nothing.

```nvgt
void notify_one();
```

###### Remarks:
This form of change detection is often more efficient than pure spinlocks or polling and should be preferred whenever possible.


##### test
Atomically reads the value of this `atomic_flag` and returns it. The behavior is undefined if the memory order is `MEMORY_ORDER_RELEASE` or `MEMORY_ORDER_ACQ_REL`.

```nvgt
bool test(memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters:
* `order`: the memory synchronization ordering.

###### Returns:
The value atomically read.


##### test_and_set
Atomically changes the value of this `atomic_flag` to set (`true`) and returns it's prior value.

```nvgt
bool test_and_set(memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters:
* `order`: the atomic synchronization order.

###### Returns:
The prior value of this `atomic_flag`.


##### wait
Atomically waits until the value of this `atomic_flag` has changed. If order is either `MEMORY_ORDER_RELEASE` or `MEMORY_ORDER_ACQ_REL`, the behavior is undefined.

```nvgt
void wait(bool old, memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters:
* `old`: The old (current) value of this `atomic_flag` as of the time of this call. This function will wait until this `atomic_flag` no longer contains this value.
* `order`: memory order constraints to enforce.

###### Remarks:
This function is guaranteed to return only when the value has changed, even if the underlying implementation unblocks spuriously.




### atomic_T

The base class for all atomic types that NVGT has to offer.

#### Remarks:

An atomic type SHALL be defined as a data type for which operations must be performed atomically, ensuring that modifications are indivisible and uninterrupted within a concurrent execution environment. An atomic operation MUST either fully succeed or completely fail, with no possibility of intermediate states or partial completion.

When one thread writes to an atomic object and another thread reads from the same atomic object, the behavior MUST be well-defined and SHALL NOT result in a data race.

Operations on atomic objects MAY establish inter-thread synchronization and MUST order non-atomic memory operations as specified by the `memory_order` parameter. Memory effects MUST be propagated and observed according to the constraints of the specified memory ordering.

Within this documentation, the `atomic_T` class is a placeholder class for any atomic type. Specifically, `T` may be any primitive type except void, but MAY NOT be any complex type such as string. For example, `atomic_bool` is an actual class, where `bool` replaces `T`. Additionally, an `atomic_flag` class exists which does not offer load or store operations but is the most efficient implementation of boolean-based atomic objects, and has separate documentation from all other atomic types.

Please note: atomic floating-point types are not yet implemented, though they will be coming in a future release. However, until then, attempts to instantiate an atomic floating-point type will behave as though the class in question did not exist. This notice will be removed once atomic floating-point types have been implemented.

#### Methods
##### compare_exchange_strong
Atomically compares the value representation of this atomic object with that of `expected`. If both are bitwise-equal, performs an atomic read-modify-write operation on this atomic object with `desired` (that is, replaces the current value of this atomic object with `desired`); otherwise, performs an atomic load of this atomic object and places it's actual value into `expected`. If failure is either `MEMORY_ORDER_RELEASE` or `MEMORY_ORDER_ACQ_REL`, the behavior is undefined. 

1: `bool compare_exchange_strong(T& expected, T desired, memory_order success, memory_order failure);`
2: `bool compare_exchange_strong(T& expected, T desired, memory_order order = MEMORY_ORDER_SEQ_CST);`

###### Parameters (1):
* `T& expected`: reference to the value expected to be found in this atomic object.
* `T desired`: the value that SHALL replace the one in this atomic object if and only if it is bitwise-equal to `expected`.
* `memory_order success`: the memory synchronization ordering that SHALL be used for the read-modify-write operation if the comparison succeeds.
* `memory_order failure`: the memory synchronization ordering that SHALL be used for the load operation if the comparison fails.
* `memory_order order`: the memory synchronization order that SHALL be used for both the read-modify-write operation and the load operation depending on whether the comparison succeeds or fails.

###### Returns:
`true` if the atomic value was successfully changed, false otherwise.

###### Remarks:
This function is available on all atomic types.

Within the above function signatures, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

The operations of comparison and copying SHALL be executed in a bitwise manner. Consequently, no invocation of a constructor, assignment operator, or similar function SHALL occur, nor SHALL any comparison operators be utilized during these operations.

In contrast to the `compare_exchange_weak` function, this function SHALL NOT spuriously fail.

In scenarios where the use of the `compare_exchange_weak` function would necessitate iteration, whereas this function would not, the latter SHALL be considered preferable. Exceptions to this preference exist in cases where the object representation of type T might encompass trap bits or offer multiple representations for the same value, such as floating-point NaNs. Under these circumstances, `compare_exchange_weak` generally proves effective, as it tends to rapidly converge upon a stable object representation.


##### compare_exchange_weak:
Atomically compares the value representation of this atomic object with that of `expected`. If both are bitwise-equal, performs an atomic read-modify-write operation on this atomic object with `desired` (that is, replaces the current value of this atomic object with `desired`); otherwise, performs an atomic load of this atomic object and places it's actual value into `expected`. If failure is either `MEMORY_ORDER_RELEASE` or `MEMORY_ORDER_ACQ_REL`, the behavior is undefined. 

```nvgt
bool compare_exchange_weak(T& expected, T desired, memory_order success, memory_order failure);
bool compare_exchange_weak(T& expected, T desired, memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters:
* `T& expected`: reference to the value expected to be found in this atomic object.
* `T desired`: the value that SHALL replace the one in this atomic object if and only if it is bitwise-equal to `expected`.
* `memory_order success`: the memory synchronization ordering that SHALL be used for the read-modify-write operation if the comparison succeeds.
* `memory_order failure`: the memory synchronization ordering that SHALL be used for the load operation if the comparison fails.
* `memory_order order`: the memory synchronization order that SHALL be used for both the read-modify-write operation and the load operation depending on whether the comparison succeeds or fails.

###### Returns:
bool: `true` if the atomic value was successfully changed, false otherwise.

###### Remarks:
This function is available on all atomic types.

Within the above function signatures, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

The operations of comparison and copying SHALL be executed in a bitwise manner. Consequently, no invocation of a constructor, assignment operator, or similar function SHALL occur, nor SHALL any comparison operators be utilized during these operations.

In contrast to the `compare_exchange_strong` function, this function MAY fail spuriously. Specifically, even in instances where the value contained within this atomic object is equivalent to the expected value, the function is permitted to act as if the values are not equal. This characteristic allows the function to provide enhanced performance on certain platforms, particularly when employed within iterative loops.

In scenarios where the use of this function would necessitate iteration, whereas `compare_exchange_strong` would not, the latter SHALL be considered preferable. Exceptions to this preference exist in cases where the object representation of type T might encompass trap bits or offer multiple representations for the same value, such as floating-point NaNs. Under these circumstances, this function generally proves effective, as it tends to rapidly converge upon a stable object representation.


##### exchange
Atomically replaces the value of this object with `desired` in such a way that the operation is a read-modify-write operation, then returns the prior value of this object. Memory is affected according to `order`.

```nvgt
T exchange(T desired, memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters:
* `T desired`: the value to exchange with the prior value.
* `memory_order order`: the memory ordering constraints to enforce.

###### Returns
T: The prior value held within this atomic object before this function was called.

###### Remarks:
This function is available on all atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.


##### fetch_add
Atomically replaces the current value with the result of arithmetic addition of the value and `arg`. That is, it performs atomic post-increment. The operation is a read-modify-write operation. Memory is affected according to the value of `order`.

```nvgt
T fetch_add(T arg, memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters:
* `T arg`: the value to add to this atomic object.
* `memory_order order`: which memory order SHALL govern this operation.

###### Returns:
T: The prior value of this atomic object.

###### Remarks:
This function is only available on integral and floating-point atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.


##### fetch_and
Atomically replaces the current value with the result of bitwise ANDing the value of this atomic object and `arg`. The operation is a read-modify-write operation. Memory is affected according to the value of `order`.

```nvgt
T fetch_and(T arg, memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters:
* `T arg`: the right-hand side of the bitwise AND operation.
* `memory_order order`: which memory order SHALL govern this operation.

###### Returns:
The prior value of this atomic object.

###### Remarks:
This function is only available on integral atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.


##### fetch_or
Atomically replaces the current value with the result of bitwise ORing the value of this atomic object and `arg`. The operation is a read-modify-write operation. Memory is affected according to the value of `order`.

```nvgt
T fetch_or(T arg, memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters
* `T arg`: the right-hand side of the bitwise OR operation.
* `memory_order order`: which memory order SHALL govern this operation.

###### Returns:
T: The prior value of this atomic object.

###### Remarks:
This function is only available on integral atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.


##### fetch_sub
Atomically replaces the current value with the result of arithmetic subtraction of the value and `arg`. That is, it performs atomic post-decrement. The operation is a read-modify-write operation. Memory is affected according to the value of `order`.

```nvgt
T fetch_sub(T arg, memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters:
* `T arg`: the value to subtract from this atomic object.
* `memory_order order`: which memory order SHALL govern this operation.

###### Returns:
T: The prior value of this atomic object.

###### Remarks:
This function is only available on integral and floating-point atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.


##### fetch_xor
Atomically replaces the current value with the result of bitwise XORing the value of this atomic object and `arg`. The operation is a read-modify-write operation. Memory is affected according to the value of `order`.

```nvgt
T fetch_xor(T arg, memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters:
* `T arg`: the right-hand side of the bitwise XOR operation.
* `memory_order order`: which memory order SHALL govern this operation.

###### Returns:
T: The prior value of this atomic object.

###### Remarks:
This function is only available on integral atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.


##### is_lock_free
Checks whether the atomic operations on all objects of this type are lock-free.

```nvgt
bool is_lock_free();
```

###### Returns:
bool: true if the atomic operations on the objects of this type are lock-free, `false` otherwise.

###### Remarks:
This function is available on all atomic types.

All atomic types, with the exception of `atomic_flag`, MAY be implemented utilizing mutexes or alternative locking mechanisms as opposed to employing lock-free atomic instructions provided by the CPU. This allows for the implementation flexibility where atomicity is achieved through synchronization primitives rather than hardware-based atomic instructions.

Atomic types MAY exhibit lock-free behavior under certain conditions. For instance, SHOULD a particular architecture support naturally atomic operations exclusively for aligned memory accesses, then any misaligned instances of the same atomic type MAY necessitate the use of locks to ensure atomicity.

While it is recommended, it is NOT a mandatory requirement that lock-free atomic operations be address-free. Address-free operations are those that are suitable for inter-process communication via shared memory, facilitating seamless data exchange without reliance on specific memory addresses.

##### load
Atomically loads and returns the current value of the atomic variable. Memory is affected according to the value of `order`.  If order is either `MEMORY_ORDER_RELEASE` or `MEMORY_ORDER_ACQ_REL`, the behavior is undefined.

```nvgt
T load(memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters:
* `memory_order order`: which memory order to enforce when performing this operation.

###### Returns:
T: The value of this atomic object.

###### Remarks:
This function is available on all atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

This operation is identical to using the IMPLICIT CONVERSION OPERATOR, except that it allows for the specification of a memory order when performing this operation. When using the IMPLICIT CONVERSION OPERATOR, the memory order SHALL be `MEMORY_ORDER_SEQ_CST`.

##### notify_all
Unblocks all threads blocked in atomic waiting operations (i.e., `wait()`) on this atomic object if there are any; otherwise does nothing.

```nvgt
void notify_all();
```

###### Remarks:
This function is available on all atomic types.

This form of change detection is often more efficient than pure spinlocks or polling and should be preferred whenever possible.



##### notify_one
Unblocks at least one thread blocked in atomic waiting operations (i.e., `wait()`) on this  atomic object if there is one; otherwise does nothing.

```nvgt
void notify_one();
```

###### Remarks:
This function is available on all atomic types.

This form of change detection is often more efficient than pure spinlocks or polling and should be preferred whenever possible.


##### store
Atomically replaces the current value with `desired`. Memory is affected according to the value of `order`.  If order is either MEMORY_ORDER_ACQUIRE or MEMORY_ORDER_ACQ_REL, the behavior is undefined. 

```nvgt
void store(T desired, memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters:
* `T desired`: the value that should be stored into this atomic object.
* `memory_order order`: which memory ordering constraints should be enforced during this operation.

###### Remarks:
This function is available on all atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

This operation is identical to using the assignment operator, except that it allows for the specification of a memory order when performing this operation. When using the assignment operator, the memory order SHALL be `MEMORY_ORDER_SEQ_CST`.

##### wait
Atomically waits until the value of this atomic object has changed. If order is either `MEMORY_ORDER_RELEASE` or `MEMORY_ORDER_ACQ_REL`, the behavior is undefined.

```nvgt
void wait(T old, memory_order order = MEMORY_ORDER_SEQ_CST);
```

###### Parameters:
* `T old`: The old (current) value of this atomic object as of the time of this call. This function will wait until this atomic object no longer contains this value.
* `memory_order order`: memory order constraints to enforce.

###### Remarks:
This function is available on all atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

This function is guaranteed to return only when the value has changed, even if the underlying implementation unblocks spuriously.



#### Operators
##### opAddAssign
Atomically replaces the current value with the result of computation involving the previous value and `arg`. The operation is a read-modify-write operation. Specifically, performs atomic addition. Equivalent to `return fetch_add(arg) + arg;`.

```nvgt
T opAddAssign( T arg );
```

###### Returns:
T: The resulting value (that is, the result of applying the corresponding binary operator to the value immediately preceding the effects of the corresponding member function in the modification order of this atomic object).

###### Remarks:
This operator is only available on integral and floating-point atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

Unlike most compound assignment operators, the compound assignment operators for atomic types do not return a reference to their left-hand arguments. They return a copy of the stored value instead. 


##### opAndAssign
Atomically replaces the current value with the result of computation involving the previous value and `arg`. The operation is a read-modify-write operation. Specifically, performs atomic bitwise AND. Equivalent to `return fetch_and(arg) & arg;`.

```nvgt
T opAndAssign(T arg);
```

###### Returns:
The resulting value of this computation.

###### Remarks:
This operator is only available on integral atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

Unlike most compound assignment operators, the compound assignment operators for atomic types do not return a reference to their left-hand arguments. They return a copy of the stored value instead. 


##### opAssign
Atomically assigns desired to the atomic variable. Equivalent to `store(desired)`.

```nvgt
T opAssign(T desired);
```

###### Remarks:
This operator is available on all atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

Unlike most assignment operators, the assignment operators for atomic types do not return a reference to their left-hand arguments. They return a copy of the stored value instead.


##### opImplConv
Atomically loads and returns the current value of the atomic variable. Equivalent to `load()`.

```nvgt
T opImplConv();
```

###### Returns:
T: The current value of the atomic variable. 

###### Remarks:
This operator is available on all atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

##### opOrAssign
Atomically replaces the current value with the result of computation involving the previous value and `arg`. The operation is a read-modify-write operation. Specifically, performs atomic bitwise OR. Equivalent to `return fetch_or(arg) | arg;`.

```nvgt
T opOrAssign(T arg);
```

###### Returns:
T: The resulting value of this computation.

###### Remarks:
This operator is only available on integral atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

Unlike most compound assignment operators, the compound assignment operators for atomic types do not return a reference to their left-hand arguments. They return a copy of the stored value instead. 


##### opPostDec
Atomically decrements the current value. The operation is a read-modify-write operation. Specifically, performs atomic post-decrement. Equivalent to `return fetch_add(1);`.

```nvgt
T opPostDec(int arg);
```

###### Remarks:
This operator is only available on integral atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

Unlike most post-decrement operators, the post-decrement operators for atomic types do not return a reference to the modified object. They return a copy of the stored value instead. 


##### opPostInc
Atomically increments the current value. The operation is a read-modify-write operation. Specifically, performs atomic post-increment. Equivalent to `return fetch_add(1);`.

```nvgt
T opPostInc(int arg);
```

###### Remarks:
This operator is only available on integral atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

Unlike most post-increment operators, the post-increment operators for atomic types do not return a reference to the modified object. They return a copy of the stored value instead. 


##### opPreDec
Atomically decrements the current value. The operation is a read-modify-write operation. Specifically, performs atomic pre-decrement. Equivalent to `return fetch_sub(1) - 1;`.

```nvgt
T opPreDec();
```

###### Remarks: 
This operator is only available on integral atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

Unlike most pre-decrement operators, the pre-decrement operators for atomic types do not return a reference to the modified object. They return a copy of the stored value instead. 


##### opPreInc
Atomically increments the current value. The operation is a read-modify-write operation. Specifically, performs atomic pre-increment. Equivalent to `return fetch_add(1) + 1;`.

```nvgt
T opPreInc();
```

###### Remarks:
This operator is only available on integral atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

Unlike most pre-increment operators, the pre-increment operators for atomic types do not return a reference to the modified object. They return a copy of the stored value instead. 


##### opSubAssign
Atomically replaces the current value with the result of computation involving the previous value and `arg`. The operation is a read-modify-write operation. Specifically, performs atomic subtraction. Equivalent to `return fetch_sub(arg) + arg;`.

```nvgt
T opSubAssign( T arg );
```

###### Returns:
T: The resulting value (that is, the result of applying the corresponding binary operator to the value immediately preceding the effects of the corresponding member function in the modification order of this atomic object).

###### Remarks:
This operator is only available on integral and floating-point atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

Unlike most compound assignment operators, the compound assignment operators for atomic types do not return a reference to their left-hand arguments. They return a copy of the stored value instead. 


##### opXorAssign
Atomically replaces the current value with the result of computation involving the previous value and `arg`. The operation is a read-modify-write operation. Specifically, performs atomic bitwise XOR. Equivalent to `return fetch_xor(arg) ^ arg;`.

```nvgt
T opXorAssign(T arg);
```

###### Returns:
T: The resulting value of this computation.

###### Remarks:
This operator is only available on integral atomic types.

Within the above function signature, `T` is used as a placeholder for the actual type. For example, if this object is an `atomic_int`, then `T` SHALL be `int`.

Unlike most compound assignment operators, the compound assignment operators for atomic types do not return a reference to their left-hand arguments. They return a copy of the stored value instead.



#### Properties
##### is_always_lock_free
This property equals true if this atomic type is always lock-free and false if it is never or sometimes lock-free. 

```nvgt
bool get_is_always_lock_free() property;
```

###### Remarks:
This property is available on all atomic types. This property is read-only.




### mutex

This multithreading primitive allows for any number of threads to safely access a shared object while avoiding illegal concurrent access.

mutex();

#### Remarks:

It is not safe for 2 threads to try accessing the same portion of memory at the same time, that especially becomes true when at least one of the threads performs any kind of updates to the memory. One of the common and widely used solutions to this problem is basically to create a lock condition where, if one thread starts modifying a bit of shared data, another thread which wants to access or also modify that data must first wait for the initial accessing thread to complete that data modification before continuing.

The mutex class is one such method of implementing this mechanism. On the surface it is a simple structure that can be in a locked or unlocked state. If thread A calls the lock method on a mutex object which is already locked from thread B, thread A will block execution until thread B calls the unlock method of the mutex object which can then be successfully locked by thread A.

This is the most basic mutex class, though there are other derivatives. Most mutex classes have the ability to try locking a mutex for up to a given timeout in milliseconds before returning false if a lock could not be acquired within the given timeout.

Mutexes or most other threading primitives are not connected by default to any sort of data. You can use one mutex for 10 variables if you want and if it makes sense in your context.

Remember, you are beginning to enter lower level and much more dangerous programming territory when dealing with multiple threads. If you accidentally forget to unlock a mutex when you are done with it for example, any thread that next tries locking that mutex will at the least malfunction but is much more likely to just hang your app forever. Be careful!

#### Example:

```NVGT
// globals
mutex ding_mutex; // To control exclusive access to a sound object.
sound snd;
thread_event exit_program(THREAD_EVENT_MANUAL_RESET);
// This function plays a ding sound every 250 milliseconds, the sleeping is handled by trying to wait for the thread exit event.
void dinging_thread() {
	while(!exit_program.try_wait(250)) {
		ding_mutex.lock();
		snd.seek(0);
		snd.play();
		ding_mutex.unlock();
	}
}
void main() {
	snd.load("C:/Windows/media/chord.wav");
	show_window("mutex example");
	// Start our function on another thread.
	async<void>(dinging_thread);
	while (!key_pressed(KEY_ESCAPE)) {
		wait(5);
		if (key_pressed(KEY_L)) {
			// This demonstrates that if we lock the mutex on the main thread, the ding sound pauses for a second while it's own ding_mutex.lock() call waits for this thread to unlock the mutex.
			ding_mutex.lock();
			wait(1000);
			ding_mutex.unlock();
		}
		// A more real-world use case might be allowing the sounds volume to safely change.
		if (key_pressed(KEY_UP)) {
			mutex_lock exclusive(ding_mutex); // A simpler way to lock a mutex, the mutex_lock variable called exclusive gets deleted as soon as this if statement scope exits and the mutex is then unlocked.
			snd.volume += 1;
		} else if (key_pressed(KEY_DOWN)) {
			mutex_lock exclusive(ding_mutex);
			snd.volume -= 1; // We can be sure that these volume changes will not take place while the sound is being accessed on another thread.
		}
	}
	exit_program.set(); // Make sure the dinging_thread knows it's time to shut down.
}
```



#### methods
##### lock
Locks the mutex, waiting indefinitely or for a given duration if necessary for the operation to succeed.

1. `void lock();`
2. `void lock(uint milliseconds);`

###### Arguments (2):
* uint milliseconds: How long to wait for a lock to succeed before throwing an exception

###### Remarks:
With the mutex class in particular, it is safe to call the lock function on the same thread multiple times in a row so long as it is matched by the same number of unlock calls. This may not be the case for other types of mutexes.

Beware that if you use the version of the lock function that takes a timeout argument, an exception will be thrown if the timeout expires without a lock acquiring. The version of the function taking 0 arguments waits forever for a lock to succeed.


##### try_lock

Attempts to lock the mutex.

1. bool try_lock();

2. bool try_lock(uint milliseconds);

###### Arguments (2):

* uint milliseconds: The amount of time to wait for a lock to acquire.

###### Returns:

bool: true if a lock was acquired, false otherwise.

###### Remarks:

This is the method to use if you want to try locking a mutex without blocking your programs execution. The 0 argument version of this function will return false immediately if the mutex is already locked on another thread, while the version of the method taking a milliseconds value will  wait for the timeout to expire before returning false on failure.

Note that several operating systems do not implement this functionality natively or in an easily accessible manner, such that the version of this function that takes a timeout might enter what amounts to a `while(!try_lock()) wait(0);` loop while attempting to acquire a lock. If the operating system supports such a timeout functionality natively which will be a lot faster such as those using pthreads, that will be used instead.

###### Example:

```NVGT
// Press space to perform a calculation, and press enter to see the result only so long as the calculation is not in progress.
thread_event keep_calculating;
bool exit_program = false; // NVGT will wrap atomic flags later, for now we'll piggyback off the keep_calculating event.
mutex calculation_mutex;
int calculation;
void do_calculations() {
	while (true) {
		keep_calculating.wait();
		if (exit_program) return;
		// Lets increase the calculation variable for a bit.
		screen_reader_speak("calculating...", true);
		timer t;
		calculation_mutex.lock();
		while(t.elapsed < 1000) calculation++;
		calculation_mutex.unlock();
		screen_reader_speak("complete", true);
	}
}
void main() {
	async<void>(do_calculations); // Spin up our thread.
	show_window("try_lock example");
	while (!key_pressed(KEY_ESCAPE)) {
		wait(5);
		if (key_pressed(KEY_SPACE)) keep_calculating.set();
		if (key_pressed(KEY_RETURN)) {
			if (calculation_mutex.try_lock()) {
				screen_reader_speak(calculation, true);
				calculation_mutex.unlock();
			} else screen_reader_speak("calculation in progress", true);
		}
	}
	exit_program = true;
	keep_calculating.set();
}
```



##### unlock
Unlocks the mutex.

`void unlock();`

###### Remarks:
This function does nothing if the mutex is already unlocked.



#### mutex_lock
Lock a mutex until the current execution scope exits.

1. `mutex_lock(mutex@ mutex_to_lock);`
2. `mutex_lock(mutex@ mutex_to_lock, uint milliseconds);`

##### Arguments (2):
	* uint milliseconds: The amount of time to wait for a lock to acquire before throwing an exception.

##### Remarks:
Often it can become tedious or sometimes even unsafe to keep performing mutex.lock and mutex.unlock calls when dealing with mutex, and this object exists to make that task a bit easier to manage.

This class takes advantage of the sure rule that, unless handles become involved, an object created within a code scope will be automatically destroyed as soon as that scope exits.

For example:

```
if (true) {
	string s = "hello";
} // the s string is destroyed when the program reaches this brace.
```

In this case, the constructor of the mutex_lock class will automatically call the lock method on whatever mutex you pass to it, while the destructor calls the unlock method. Thus, you can lock a mutex starting at the line of code a mutex_lock object was created, which will automatically unlock whenever the scope it was created in is exited.

The class contains a single method, void unlock(), which allows you to unlock the mutex prematurely before the scope actually exits.

There is a very good reason for using this class sometimes as opposed to calling mutex.lock directly. Consider:

```
my_mutex.lock();
throw("Oh no, this code is broken!");
my_mutex.unlock();
```

In this case, mutex.unlock() will never get called because an exception got thrown meaning that the rest of the code down to whatever handles the exception won't execute! However we can do this:

```
mutex_lock exclusive(my_mutex);
throw("Oh no, this code is broken!");
exclusive.unlock()
```

The mutex_lock object will be destroyed as part of the exception handler unwinding the stack, because the handler already knows to destroy any objects it encounters along the way. However any code that handles exceptions certainly does not know it should specifically call the unlock method of a mutex, thus you could introduce a deadlock in your code if you lock a mutex and then run code that throws an exception without using this mutex_lock class.

A final hint, it is actually possible to create scopes in Angelscript and in many other languages as well without any preceding conditions, so you do not need an if statement or a while loop to use this class.

```
int var1 = 2;
string var2 = "hi";
{
	string var3 = "catch me if you can...";
}
string var4 = "Hey, where'd var3 go!";
```



### thread_event

This concurrency primative implements a method by which one or more threads can safely wait on another thread for the event to become signaled.

thread_event(thread_event_type type = THREAD_EVENT_AUTO_RESET);

#### Arguments:

thread_event_type type: The type of handling to perform when a waiting thread detects that the event has been set (see remarks).

#### Remarks:

This primative can be used to make one thread inexpensively sleep until another thread wakes it up, or can more simply be used for some threads to monitor when a condition has been completed on another thread in a safe manner.

It is not a good idea to just use standard booleans in multithreaded situations where you want one thread to know when another thread has completed it's work because threads could be reading from the boolean as it is being written to by a worker thread, causing an undefined result. The thread_event object is one way around this issue, as it can signal when a standard boolean is safe to access or sometimes avoid their usage entirely.

Quite simply one thread can call the set() method on an event, and if another thread has previously called the wait() method on the same event, that wait method will return thus resuming the first thread. If the event was created with the THREAD_EVENT_AUTO_RESET type, the event will also be set to unsignaled as the waiting thread wakes up. Otherwise, the reset() method must be called manually.

#### Example:

```NVGT
// Globals
thread_event program_event;
bool exit_program;
string message;
void message_thread() {
	while (true) {
		program_event.wait();
		if (exit_program) return;
		screen_reader_speak(message, true);
	}
}
void main() {
	show_window("press space to speak on another thread");
	async<void>(message_thread);
	while (!key_pressed(KEY_ESCAPE)) {
		wait(5);
		if (key_repeating(KEY_SPACE)) {
			message = "the date and time is " + calendar().format(DATE_TIME_FORMAT_RFC1123);
			program_event.set();
		}
	}
	exit_program = true;
	program_event.set();
}
```



#### Methods
##### reset
Resets an event to an unsignaled state.

`void reset();`

###### Remarks:
This method is usually only needed if THREAD_EVENT_MANUAL_RESET was specified when the event was created, however you could also cancel the signaling of an event if another thread hasn't detected the signal yet.

See the main event and mutex chapters for examples.


##### set
Causes an event to become signaled, waking up any threads waiting for this condition.

`void set();`

###### Remarks:
All existing examples that use events must call this method, so it will not be demonstrated in this chapter.


##### try_wait

Wait a given number of milliseconds for an event to become signaled.

bool try_wait(uint milliseconds);

###### Arguments:

* uint milliseconds: The amount of time to wait, may be 0 to not wait at all.

###### Returns:

bool: True if another thread has signaled the event, or false if the event is still unsignaled after the given number of milliseconds has elapsed.

###### Remarks:

The semantics of this function are exactly the same as mutex::try_wait(), accept that this function waits on an event instead of a mutex.

###### Example:

```NVGT
thread_event g_wait;
void test_thread() {
	screen_reader_speak("started", true);
	while (!g_wait.try_wait(1000)) screen_reader_speak("waiting...", true);
	screen_reader_speak("ah!", true);
	g_wait.set();
}
void main() {
	async<void>(test_thread);
	wait(3500);
	g_wait.set();
	g_wait.wait(); // So we'll know the other thread has finished speaking it's final message.
}
```



##### wait
waits for the event to become signaled, blocking indefinitely or for a given duration if required.

1. `void wait();`
2. `void wait(uint milliseconds);`

###### Arguments (2):
* uint milliseconds: How long to wait for the event to become signaled before throwing an exception

###### Remarks:
Beware that if you use the version of the wait function that takes a timeout argument, an exception will be thrown if the timeout expires without the event having become signaled. The version of the function taking 0 arguments waits forever for the event's set() method to be called.





## Enums
### `memory_order`
Specifies the constraints on the ordering and visibility of memory operations (reads and writes) in concurrent programming, determining how operations on shared memory are observed across different threads.

| Constant | Description |
| --- | --- |
| `MEMORY_ORDER_RELAXED` | An atomic operation with `MEMORY_ORDER_RELAXED` has no synchronization or ordering constraints beyond those imposed by the atomicity of the operation itself. It guarantees that the operation on the atomic variable is atomic and modifications to that variable are visible in some modification order consistent across threads, but it does not impose any inter-thread ordering constraints or create happens-before relationships. |
| `MEMORY_ORDER_ACQUIRE` | An atomic operation with `MEMORY_ORDER_ACQUIRE` on an atomic variable synchronizes with a release operation on the same variable from another thread. It ensures that all memory writes in other threads that release the same atomic variable become visible in the current thread before any subsequent memory operations (following the acquire operation) are performed. This establishes a happens-before relationship from the release to the acquire. |
| `MEMORY_ORDER_RELEASE` | An atomic operation with `MEMORY_ORDER_RELEASE` ensures that all preceding memory operations in the current thread are completed before the release operation is performed. It makes the effects of these prior operations visible to other threads that perform an acquire operation on the same atomic variable. The release operation synchronizes with an acquire operation on the same variable, establishing a happens-before relationship. |
| `MEMORY_ORDER_ACQ_REL` | An atomic operation with `MEMORY_ORDER_ACQ_REL` combines both acquire and release semantics. For operations that modify the atomic variable (read-modify-write operations), it ensures that all preceding memory operations in the current thread are completed before the operation (release semantics), and that all subsequent memory operations are not started until after the operation (acquire semantics). This enforces that the operation synchronizes with other acquire or release operations on the same variable, establishing happens-before relationships in both directions. |
| `MEMORY_ORDER_SEQ_CST` | An atomic operation with `MEMORY_ORDER_SEQ_CST` (sequential consistency) provides the strongest ordering guarantees. It ensures that all sequentially consistent operations appear to occur in a single total order that is consistent with the program order in all threads. This total order is interleaved with the program order such that each read sees the last write to that variable according to this order. It combines the effects of acquire and release semantics and enforces a global order of operations, establishing a strict happens-before relationship. |


### thread_event_type
These are the possible event types that can be used to successfully construct thread_event objects.
* THREAD_EVENT_MANUAL_RESET: Many threads can wait on this event because the `thread_event::reset()` method must be manually called.
* THREAD_EVENT_AUTO_RESET: Only one thread can wait on this event because it will be automatically reset as soon as the waiting thread detects that the event has become signaled.


### thread_priority
It is possible to set a thread's priority to the following values in NVGT:
* THREAD_PRIORITY_LOWEST
* THREAD_PRIORITY_LOW
* THREAD_PRIORITY_NORMAL
* THREAD_PRIORITY_HIGH
* THREAD_PRIORITY_HIGHEST



## Functions
### thread_current_id

Determine the operating system specific ID of the currently executing thread.

uint thread_current_id();

#### Returns:

uint: The ID of the thread that this function was called on.

#### Example:

```NVGT
void main() {
	alert("Current thread ID is", thread_current_id());
}
```



### thread_sleep
Sleeps the thread it was called from, but can be interrupted.

`bool thread_sleep(uint milliseconds);`

#### Arguments:
* uint milliseconds: the number of milliseconds to sleep the thread for.

#### Returns:
bool: true if the thread slept for the full duration, false if it was interrupted by `thread.wake_up`.

#### Remarks:
This function should only be called in the context of threads created within your script.


### thread_yield
Yields CPU to other threads.
void thread_yield();

#### Remarks:
This is a little bit like executing `wait(0);` accept that it doesn't pull the window, and there is absolutely no sleeping. It will temporarily yield code execution to the next scheduled thread that is of the same or higher priority as the one that called this function.




