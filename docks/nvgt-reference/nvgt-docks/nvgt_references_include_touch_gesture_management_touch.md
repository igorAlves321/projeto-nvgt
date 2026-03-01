# touch gesture management (touch.nvgt)
## Classes
### touch_gesture_manager

Detects and then converts raw touch screen finger data into gesture events which can be detected by your application or even converted to keyboard input.

touch_gesture_manager();

#### Remarks:

This is the highest level interface NVGT offers to accessing touch screens. It looks at what fingers are touching the screen and where, and by monitoring that data over time, derives gestures such as swipes and taps from that data before passing them along to whatever interface you register to receive them.

An interface is included by default (see the touch_keyboard_interface class), which convertes these events into simulated keyboard input for you so that adding touch support to your game becomes as simple as mapping gesture names to keycode lists.

The basic usage of this class is to create an instatnce of it somewhere, before attaching any number of touch_interface instances to the manager and finally calling manager.monitor() within the loops of your programs to receive gesture events.

#### Example:

```NVGT
#include"touch.nvgt"
#include"speech.nvgt"
touch_gesture_manager touch;
void main() {
	show_window("touch screen test");
	//attach multiple keys to a single gesture.
	int[] t = {KEY_TAB, KEY_LSHIFT};
	touch_keyboard_interface testsim(touch, {{"swipe_left1f", KEY_LEFT}, {"swipe_right1f", KEY_RIGHT}, {"swipe_up1f", KEY_UP}, {"swipe_down1f", KEY_DOWN}, {"double_tap1f", KEY_RETURN}, {"tripple_tap1f", t}, {"swipe_left2f", KEY_ESCAPE}, {"swipe_right2f", KEY_Q}, {"double_tap2f", KEY_SPACE}});
	touch.add_touch_interface(testsim);
	dictionary@d = {{"double_tap1f", KEY_X}, {"double_tap2f", KEY_Z}};
	// Demonstrate registering an interface for only a portion of the screen.
	touch.add_touch_interface(touch_keyboard_interface(touch, d, 0.5, 1.0, 0.5, 1.0));
	while (!key_pressed(KEY_ESCAPE) and !key_pressed(KEY_AC_BACK)) {
		wait(5);
		touch.monitor();
		if (key_pressed(KEY_LEFT)) speak("left");
		if (key_pressed(KEY_RIGHT)) speak("right");
		if (key_pressed(KEY_DOWN)) speak("down");
		if (key_pressed(KEY_UP)) speak("up");
		if (key_pressed(KEY_TAB)) {
			speak("tripple tap");
			if (key_down(KEY_LSHIFT) or key_down(KEY_RSHIFT)) speak("you are holding down shift", false);
		}
		if (key_pressed(KEY_SPACE)) speak("double tap 2 fingers");
		if (key_pressed(KEY_ESCAPE)) exit();
		if (key_pressed(KEY_Q)) speak("swipe right 2 fingers");
		if (key_pressed(KEY_RETURN)) speak("you just double tapped the screen!", false);
		if (key_pressed(KEY_X)) speak("You just double tapped another part of the screen!");
		if (key_pressed(KEY_Z)) speak("You just double tapped with 2 fingers on another part of the screen!");
	}
}
```



#### Methods
##### add_touch_interface
Adds a single interface to the list of interfaces that will receive touch events.

```bool add_touch_interface(touch_interface@ interface);```

## Arguments:
* touch_interface@ interface: The interface to add to the manager.

## Returns:
bool: True if the interface was successfully added, false otherwise.

## Remarks:
You can add multiple interfaces to a gesture manager because different interfaces can receive different events for various parts of the screen. An interface can simply return false in its is_bounds method at any time to pass the gesture event to the next handler in the chain. Gesture interfaces are evaluated from newest to oldest.


##### clear_touch_interfaces
Removes all interfaces from the manager.

```void clear_touch_interfaces();```

## Remarks:
This method clears all registered touch interfaces, effectively disabling all gesture handling until new interfaces are added.


##### is_available

Determine whether any touch devices are available to receive events from.

bool is_available();

###### Returns:

bool: true if at least one touch device is available on the system, false otherwise.

###### Remarks:

It is worth noting that due to circumstances outside our control, sometimes touch devices don't appear in the list until after you have touched them at least once. Therefor you should not use this method at program startup to determine with finality that no touch device is available, but could instead use it during program lifetime to monitor for whether touch support appears or disappears.
```NVGT
#include "touch.nvgt"
// Example:
touch_gesture_manager touch;
void main() {
	wait(1000); // Give the user some time to touch the screen to make sure it appears.
	if (!touch.is_available()) alert("warning", "This system does not appear to support touch screen devices");
}
```



##### monitor
Check for the latest touch events.

```void monitor();```

## Remarks:
This function must be called in all of your game's loops in order for the system to work properly. Not doing this will lead to undefined behavior.

##### set_touch_interfaces
Sets the list of interfaces that will receive touch events.

```bool set_touch_interfaces(touch_interface@[] interfaces, bool append = false);```

## Arguments:
* touch_interface@[]@ interfaces: A list of interfaces that will receive touch events.
* bool append = false: Determines whether to append to the list of existing interfaces vs. replacing it.

## Returns:
bool: True if a change was made to the interface list, false otherwise.

## Remarks:
You can pass multiple interfaces to a gesture manager because different interfaces can receive different events for various parts of the screen. An interface can simply return false in its is_bounds method at any time to pass the gesture event to the next handler in the chain. Gesture interfaces are evaluated from newest to oldest.



#### Properties
##### flick_velocity_threshold
The minimum velocity (normalized distance per second) required to trigger a flick gesture instead of a regular swipe.

```float flick_velocity_threshold = 1.5f;```

## Remarks:
Flick gestures are faster versions of swipes that can trigger different actions in your interface.


##### hold_jitter_threshold
The maximum distance (normalized 0.0-1.0) a finger can move while still being considered stationary for long press detection.

```float hold_jitter_threshold = 0.05f;```

## Remarks:
If a finger moves more than this distance from its starting position, long press and hold events will not trigger.


##### long_press_time
The minimum time in milliseconds a finger must remain stationary to trigger a long press.

```uint long_press_time = 600;```

## Remarks:
Default value is 600 milliseconds. The finger must not move beyond the hold_jitter_threshold during this time.


##### multi_tap_timeout
The maximum time in milliseconds between consecutive taps to be considered part of a multi-tap sequence.

```uint multi_tap_timeout = 600;```

## Remarks:
Default value is 600 milliseconds. This controls how quickly users must perform double-taps, triple-taps, etc.


##### swipe_min_dist
The minimum distance (normalized 0.0-1.0) a finger must travel to be considered a swipe.

```float swipe_min_dist = 0.1f;```

## Remarks:
This value is in normalized coordinates where 1.0 represents the full width or height of the screen.


##### swipe_segment_threshold
The minimum distance (normalized 0.0-1.0) before detecting a new swipe direction in a compound swipe.

```float swipe_segment_threshold = 0.1f;```

## Remarks:
This controls how sensitive the system is to direction changes during compound swipes (e.g., L-shaped swipes).


##### tap_max_delay
The maximum time in milliseconds between a finger going down and up to be considered a tap.

```uint tap_max_delay = 250;```

## Remarks:
Default value is 250 milliseconds. Increase this if users are having trouble registering taps.




### touch_interface
Base class for creating custom touch gesture handlers.

```touch_interface(touch_gesture_manager@ parent, float minx = TOUCH_UNCOORDINATED, float maxx = TOUCH_UNCOORDINATED, float miny = TOUCH_UNCOORDINATED, float maxy = TOUCH_UNCOORDINATED);```

## Arguments:
* touch_gesture_manager@ parent: A handle to the manager this interface will be attached to.
* float minx, maxx, miny, maxy = TOUCH_UNCOORDINATED: The bounds of this interface in normalized coordinates (0.0-1.0), default is entire screen.

## Remarks:
This is the base class that all touch interfaces inherit from. You can extend this class to create custom gesture handlers with specialized behavior. The class provides virtual methods for all gesture types that you can override in derived classes.

Any method starting with the word "on_" that you see in the methods list for this base class is meant to be overwridden, such as on_long_press, on_double tap etc.


#### Methods
##### on_compound_swipe
Handles compound swipe gestures.

```void on_compound_swipe(touch_screen_finger@ finger, int[] directions);```

## Arguments:
* touch_screen_finger@ finger: The finger that performed the compound swipe.
* int[] directions: Array of direction values representing the path of the swipe.

## Remarks:
Compound swipes occur when a finger changes direction during a single swipe gesture, such as an L-shaped or Z-shaped motion.


##### on_double_tap
Handles double tap gestures.

`void on_double_tap(touch_screen_finger@ finger, uint finger_count);`

###### Arguments:
* touch_screen_finger@ finger: The primary finger that triggered this gesture.
* uint finger_count: The number of fingers that this gesture consists of.


##### on_flick
Handles flick gestures.

`void on_flick(touch_screen_finger@ finger, int direction, float velocity);`

###### Arguments:
* touch_screen_finger@ finger: The finger that performed the flick.
* int direction: The direction of the flick (see swipe_touch_directions enum).
* float velocity: The velocity of the flick in normalized units per second.

###### Remarks:
Flicks are detected when a swipe's velocity exceeds `flick_velocity_threshold`.


##### on_hold
Handles hold gestures.

`void on_hold(touch_screen_finger@ finger, uint finger_count);`

###### Arguments:
* touch_screen_finger@ finger: The primary finger that triggered this gesture.
* uint finger_count: The number of fingers that this gesture consists of.

###### Remarks:
Triggered continuously while a finger continues to be held down after a long press has been detected.


##### on_long_press
Handles long press gestures.

`void on_long_press(touch_screen_finger@ finger, uint finger_count);`

###### Arguments:
* touch_screen_finger@ finger: The primary finger that triggered this gesture.
* uint finger_count: The number of fingers that this gesture consists of.

###### Remarks:
Triggered once when a finger has been held down for longer than `long_press_time` without moving beyond `hold_jitter_threshold`.


##### on_released_finger
Called when a finger is lifted from the screen.

`void on_released_finger(touch_screen_finger@ finger);`

###### Arguments:
* touch_screen_finger@ finger: The finger that was just released.

###### Remarks:
This is useful for cleanup operations, such as releasing simulated keys.


##### on_single_tap
Handles single tap gestures.

`void on_single_tap(touch_screen_finger@ finger, uint finger_count);`

###### Arguments:
* touch_screen_finger@ finger: The primary finger that triggered this gesture.
* uint finger_count: The number of fingers that this gesture consists of.


##### on_swipe_down
Handles swipe down gestures.

`void on_swipe_down(touch_screen_finger@ finger);`

###### Arguments:
* touch_screen_finger@ finger: The primary finger that triggered this gesture.



##### on_swipe_down_left
Handles swipe down-left gestures.

`void on_swipe_down_left(touch_screen_finger@ finger);`

###### Arguments:
* touch_screen_finger@ finger: The primary finger that triggered this gesture.

###### Remarks:
These diagonal swipe methods are only triggered when `touch_enable_8_way_swipes` is set to true.


##### on_swipe_down_right
Handles swipe down-right gestures.

`void on_swipe_down_right(touch_screen_finger@ finger);`

###### Arguments:
* touch_screen_finger@ finger: The primary finger that triggered this gesture.

###### Remarks:
These diagonal swipe methods are only triggered when `touch_enable_8_way_swipes` is set to true.


##### on_swipe_left
Handles swipe left gestures.

`void on_swipe_left(touch_screen_finger@ finger);`

###### Arguments:
* touch_screen_finger@ finger: The primary finger that triggered this gesture.


##### on_swipe_right
Handles swipe right gestures.

`void on_swipe_right(touch_screen_finger@ finger);`

###### Arguments:
* touch_screen_finger@ finger: The primary finger that triggered this gesture.


##### on_swipe_up
Handles swipe up gestures.

`void on_swipe_up(touch_screen_finger@ finger);`

###### Arguments:
* touch_screen_finger@ finger: The primary finger that triggered this gesture.


##### on_swipe_up_left
Handles swipe up-left gestures.

`void on_swipe_up_left(touch_screen_finger@ finger);`

###### Arguments:
* touch_screen_finger@ finger: The primary finger that triggered this gesture.

###### Remarks:
These diagonal swipe methods are only triggered when `touch_enable_8_way_swipes` is set to true.


##### on_swipe_up_right
Handles swipe up-right gestures.

`void on_swipe_up_right(touch_screen_finger@ finger);`

###### Arguments:
* touch_screen_finger@ finger: The primary finger that triggered this gesture.

###### Remarks:
These diagonal swipe methods are only triggered when `touch_enable_8_way_swipes` is set to true.


##### on_triple_tap
Handles triple tap gestures.

`void on_tripple_tap(touch_screen_finger@ finger, uint finger_count);`

###### Arguments:
* touch_screen_finger@ finger: The primary finger that triggered this gesture.
* uint finger_count: The number of fingers that this gesture consists of.



#### Properties
##### allow_passthrough
Determines whether gestures should continue to be processed by other interfaces after this one handles them.

```bool allow_passthrough = false;```

## Remarks:
When set to true, gesture events will be passed to the next interface in the chain even after this interface processes them. This allows multiple interfaces to respond to the same gesture.




### touch_keyboard_interface
Convert gesture events to simulated keyboard input.

```touch_keyboard_interface(touch_gesture_manager@ parent, dictionary@ map, float minx = TOUCH_UNCOORDINATED, float maxx = TOUCH_UNCOORDINATED, float miny = TOUCH_UNCOORDINATED, float maxy = TOUCH_UNCOORDINATED);```

## Arguments:
* touch_gesture_manager@ parent: A handle to the manager you intend to add this interface to.
* dictionary@ map: A mapping of gestures to keycode lists (see remarks).
* float minx, maxx, miny, maxy = TOUCH_UNCOORDINATED: The bounds of this interface, default for entire screen or custom.

## Remarks:
This interface works by receiving a mapping of gesture names or IDs to lists of keycodes that should be simulated.

The basic format of gesture IDs consists of a gesture name followed by a number of fingers and the letter f. For example, to detect a 2 finger swipe right gesture, you would use the key "swipe_right2f" in the mapping dictionary.

## Available gesture names:

**Basic swipes (4-way):**
* swipe_left
* swipe_right
* swipe_up
* swipe_down

**Diagonal swipes (8-way, requires `touch_enable_8_way_swipes = true`):**
* swipe_up_left
* swipe_up_right
* swipe_down_left
* swipe_down_right

**Taps:**
* single_tap (or just use the numbered versions below)
* double_tap
* tripple_tap
* 4_tap, 5_tap, etc. (for higher tap counts)

**Advanced gestures:**
* flick_left, flick_right, flick_up, flick_down (fast swipes)
* long_press (finger held down without movement)
* Compound swipes (e.g., "swipe_left_up" for an L-shaped gesture)

## Example gesture mappings:
```nvgt
dictionary@ gestures = {
    {"swipe_left1f", KEY_LEFT},           // 1-finger swipe left
    {"swipe_right2f", KEY_RIGHT},         // 2-finger swipe right
    {"double_tap1f", KEY_RETURN},         // Double tap with 1 finger
    {"tripple_tap2f", KEY_ESCAPE},        // Triple tap with 2 fingers
    {"long_press1f", KEY_SPACE},          // Long press with 1 finger
    {"flick_up1f", KEY_PAGEUP}            // Quick flick upward
};
```



## Constants
### TOUCH_UNCOORDINATED
```
const float TOUCH_UNCOORDINATED = -10.0f;
```

#### Remarks:
Special value used to indicate that a touch interface should respond to the entire screen rather than a specific bounded region.



## Enums
### swipe_touch_directions
```
enum swipe_touch_directions {
    swipe_touch_direction_left = 0,
    swipe_touch_direction_right,
    swipe_touch_direction_up,
    swipe_touch_direction_down,
    swipe_touch_direction_up_left,
    swipe_touch_direction_up_right,
    swipe_touch_direction_down_left,
    swipe_touch_direction_down_right
}
```

#### Remarks:
These values represent the possible directions for swipe gestures. The diagonal directions are only used when `touch_enable_8_way_swipes` is enabled.



## Global Properties
### touch_enable_8_way_swipes
```
bool touch_enable_8_way_swipes = false;
```

#### Remarks:
When set to true, enables detection of 8-way directional swipes (including diagonals: up_left, up_right, down_left, down_right). When false, only 4-way swipes are detected (up, down, left, right).




