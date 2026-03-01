# Character Controller Subsystem (basic_character_controller.nvgt)
## Basic character controller include

An abstract character controller that implements a complete framework for 3D character movement without relying on a full physics engine. It accepts input flags for moving forward, backward, strafing, turning, jumping, and toggling crouch, and maintains state flags for conditions such as being grounded, crouching, and running. Internally, the class manages position, velocity, and orientation vectors along with previous states for these quantities.

It contains methods that update rotation by computing target and current yaw angles, adjusting the forward and right directional vectors accordingly. Vertical movement is handled by applying gravitational acceleration and jump impulses when grounded. Horizontal movement combines input-based directional movement with acceleration, deceleration, and different speed settings for walking, running, and crouching. The class also applies friction--varying between ground and air--and computes step cycles based on distance traveled.

Additional features include methods for rotating the character by specific degrees, turning around, and snapping to preset angular increments, as well as helper functions that translate yaw values into directional text. Callbacks are provided for position, rotation, vertical and horizontal movement updates, and friction application.

### Usage

This class is an abstract base class (ABC). As such, it cannot be directly instantiated. To use it, create a class deriving from `basic_character_controller`. Be sure to call the superclasses constructor within the subclasses constructor, as the superclasses constructor initializes core state and computes general attributes to get you started.

In your subclass, you are strongly encouraged to override at least one of the callbacks enumerated below. The callbacks notify your application about state changes from within the class and allow you to intercept these changes. For all callbacks returning `bool`, excepting `should_run`, returning `false` will cause the operations performed before that callback is called to be undone. However, other operations performed for each frame will be unaffected unless explicitly specified.

Do not call any base class callback from within a callback. The behavior is unspecified if this occurs.

When instantiating your derived class, set any of the below input signals to cause the character controller to take an action. Clear the input signal to cause the action to be halted in the next frame.

You will also need to compute delta time. Delta time is the duration between frames.

#### A note on handedness

Handedness defines the orientation convention for three-dimensional coordinate systems. In a left-handed system, the forward direction is defined as the positive Z-axis and the right direction is computed by taking the cross product of the upward vector with the forward vector. In a right-handed system, the forward direction is defined as the negative Z-axis and the right direction is computed by reversing the order of the cross product used in a left-handed system. The controller defaults to a right-handed coordinate system.

The handedness can be controlled by using the `coordinate_handedness` enumeration. When inheriting from this class, implementors can either control the handedness at instantiation time by passing the mode to the superclasses constructor, or they can alter it on the fly by setting the `handedness` property to the desired mode.

### Input signals

The basic character controller is independent of any specific input system. This allows it to be used by both human and machine operators; for example, the player could have a character controller class, as could an AI character in your game.

To facilitate movement and other operations, you set any of the following input signals. As long as they are true, the appropriate action will be called per frame.

| **Input Signal** | **Description** |
| ---------------- | --------------- |
| `move_forward`   | Causes the character to accelerate in the direction it is facing. |
| `move_backward`  | Causes the character to accelerate in the opposite direction to which it is facing. |
| `turn_left`      | Causes the character to rotate counterclockwise around its vertical axis. |
| `turn_right`     | Causes the character to rotate clockwise around its vertical axis. |
| `strafe_left`    | Causes the character to move sideways to the left relative to its facing direction. |
| `strafe_right`   | Causes the character to move sideways to the right relative to its facing direction. |
| `jump`           | Applies an upward force that moves the character vertically. |

### Callbacks

This class implements several callbacks. Override them to change the behavior of the character.

| **Callback**            | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|-------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `on_position_changed`     | Called after updating the character’s position. By default, this callback verifies the vertical coordinate and, if it is below zero, clamps the vertical position to zero, resets the vertical velocity to zero, and sets the grounded flag to true. If the callback returns false, the entire position update is reverted to the prior state.                                                       |
| `on_rotation_changed`     | Called after the rotation values (yaw, forward, and right vectors) have been updated. The default implementation does nothing and returns true. If a subclass returns false from this callback, the rotation update is undone and the previous orientation is restored.                                                                                                                                                                                                                                                                      |
| `on_vertical_movement`    | Called following any modification to the vertical component of the velocity, such as when applying gravity or jump impulses. The default behavior is to return true and to do nothing. Returning false will revert the vertical component back to its previous value.                                                                                                                           |
| `on_horizontal_movement`  | Called after adjustments are made to the horizontal components of the velocity based on movement inputs. By default, the function returns true and does nothing. If it returns false, the horizontal movement update is restored to the previous horizontal velocity state. |
| `on_friction_applied`      | Called after friction is applied to the current velocity to dampen motion. The default implementation returns true and does nothing. If a subclass returns false, the velocity changes resulting from friction are undone.                                                                                                                               |
| `on_step_cycle`           | Called when the cumulative horizontal distance traveled reaches a specified step threshold, typically used to signal step cycle events (such as footstep sounds). The default implementation is a no-op. Undoing this operation is not supported.                                                                                                                                                                                                                             |
| `should_run`              | Evaluated to determine if the character should be in a running state based on current movement and input flags. The default behavior returns false, meaning the character does not transition into a running state. This callback is purely evaluative, does not modify state, and its return value affects only the choice of movement speed during horizontal motion calculations. |

### Fields

When implementing callbacks or the constructor of a subclass, many fields are made available to grant you access to the internal state of the character. These fields are as follows:

| **Field**           | **Description**                                                                                                                                           |
|---------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `is_grounded`         | Boolean indicating whether the character is in contact with the ground.                                                                                 |
| `is_crouching`        | Boolean indicating whether the character is in a crouched state.                                                                                          |
| `is_running`          | Boolean indicating whether the character is in a running state.                                                                                           |
| `position`            | Vector representing the current position of the character in the game world.                                                                              |
| `velocity`            | Vector representing the current rate of change of the character's position.                                                                               |
| `forward`             | Vector representing the current forward direction of the character.                                                                                     |
| `up`                  | Vector representing the upward direction relative to the character, commonly used as a vertical reference.                                                  |
| `right`               | Vector representing the rightward direction, computed as the normalized cross product of the up vector and the forward vector.                             |
| `old_position`        | Vector storing the character's position from the previous update cycle.                                                                                   |
| `old_velocity`        | Vector storing the character's velocity from the previous update cycle.                                                                                   |
| `old_forward`         | Vector storing the character's forward direction from the previous update cycle.                                                                          |
| `old_up`              | Vector storing the character's up direction from the previous update cycle.                                                                               |
| `old_right`           | Vector storing the character's right direction from the previous update cycle.                                                                            |
| `max_speed`           | Float representing the maximum speed that can be reached by the character.                                                                                |
| `walk_speed`          | Float defining the target speed when the character is walking.                                                                                            |
| `run_speed`           | Float defining the target speed when the character is running.                                                                                            |
| `crouch_speed`        | Float defining the target speed when the character is crouching.                                                                                          |
| `acceleration`        | Float that defines the rate at which the character's velocity increases when movement input is applied.                                                     |
| `deceleration`        | Float that defines the rate at which the character's velocity decreases when movement input is not applied.                                                 |
| `air_control`         | Float multiplier that scales the acceleration when the character is airborne, affecting maneuverability in the air.                                          |
| `rotation_speed`      | Float that defines the rate of angular change (rotation) of the character's orientation, measured in radians per second.                |
| `current_speed`       | Float representing the current magnitude of the character's horizontal movement speed.                                                                     |
| `jump_force`          | Float representing the magnitude of the upward impulse applied when the character jumps.                                                                   |
| `gravity`             | Float representing the acceleration due to gravity that affects the character's vertical velocity, measured in meters per second squared (`m/s^2`).                                                        |
| `ground_friction`     | Float representing the frictional force applied to the character while it is in contact with the ground, reducing its horizontal velocity.                 |
| `air_friction`        | Float representing the frictional force applied to the character while airborne, reducing its horizontal velocity.                                          |
| `player_height`       | Float representing the current height of the character, which can be modified by actions like crouching. Currently unused internally.                                                    |
| `crouch_height`       | Float defining the character's height when in a crouched state. Currently unused internally.                                                                                            |
| `stand_height`        | Float defining the character's height when standing upright. Currently unused internally.                                                                                              |
| `mass`                | Float representing the character's mass, in kilograms. Currently unused internally.                                        |
| `step_distance`       | Float used as an incremental measure for calculating the distance required to complete one step cycle.                                                     |
| `distance_traveled`   | Float accumulating the horizontal distance the character has moved since the last reset of the step cycle.                                                   |
| `step_cycle`          | Float representing the progress through the current step cycle, often normalized to a value between 0 and 1.                                                  |
| `run_step_length`     | Float defining the distance threshold for a single step cycle when the character is running.                                                               |
| `walk_step_length`    | Float defining the distance threshold for a single step cycle when the character is walking.                                                               |
| `crouch_step_length`  | Float defining the distance threshold for a single step cycle when the character is crouching.                                                             |
| `yaw`                 | Float representing the current rotational angle (yaw) of the character around the vertical axis, in degrees. You should normally not neeed to change this field; doing so will cause an (unnatural) "snapping" effect, which you may not typically want.                                                           |
| `target_yaw`          | Float representing the desired yaw toward which the character is currently rotating, in degrees. To naturally rotate the character to a given yaw, set this field and allow the character to reach that yaw over time.                                                                |
| `old_yaw`             | Float storing the yaw angle from the previous update cycle.                                                                                              |


## Classes
### basic_character_controller
#### Methods
##### `realign_to_nearest_degree`

Instructs the controller that it should reorient itself such that it is facing the closest valid compass point to it's current yaw.

```nvgt
void realign_to_nearest_degree(const float step=2.8125) final;
```

###### Parameters

* `const float step`: Used for snapping degrees to the nearest compass point, this parameter allows you to change the granularity of snapping behaviors.



##### `rotate_left_by`

Instructs the controller that it should begin rotation of the character to the left by the given amount on it's vertical axis.

```nvgt
void rotate_left_by(const float degree, const float step = 2.8125, const bool snap = false) final;
```

###### Parameters

* `const float degree`: the amount by which to rotate the character, in degrees.
* `const float step`: Used for snapping degrees to the nearest compass point, this parameter allows you to change the granularity of snapping behaviors.
* `const bool snap`: Determines whether the target yaw will be snapped to the nearest valid compass point, or whether it will be used as is.

###### Remarks

The methods `rotate_left_by` and `rotate_right_by` update the character's yaw by subtracting or adding a specified angle, respectively. When the `snap` parameter is enabled, the input angle is adjusted, or "snapped", to the nearest multiple defined by the `step` parameter. By default, the system uses a `step` value of `2.8125` degrees, which results from dividing 360 degrees by 128, corresponding to a Mariner’s compass with 128 discrete points. For cases where a different level of angular granularity is preferred, the `step` value can be recalculated; for instance, using `360/4` (`90.0` degrees) restricts rotation to the four cardinal directions, or using `360/8` (`45.0` degrees) allows both cardinal and intercardinal directions. Once the angle is snapped (if applicable), the method updates the target yaw, which is used in subsequent rotation updates to interpolate the actual yaw toward the target value.

##### `rotate_right_by`

Instructs the controller that it should begin rotation of the character to the right by the given amount on it's vertical axis.

```nvgt
void rotate_right_by(const float degree, const float step = 2.8125, const bool snap = false) final;
```

###### Parameters

* `const float degree`: the amount by which to rotate the character, in degrees.
* `const float step`: Used for snapping degrees to the nearest compass point, this parameter allows you to change the granularity of snapping behaviors.
* `const bool snap`: Determines whether the target yaw will be snapped to the nearest valid compass point, or whether it will be used as is.

###### Remarks

The methods `rotate_left_by` and `rotate_right_by` update the character's yaw by subtracting or adding a specified angle, respectively. When the `snap` parameter is enabled, the input angle is adjusted, or "snapped", to the nearest multiple defined by the `step` parameter. By default, the system uses a `step` value of `2.8125` degrees, which results from dividing 360 degrees by 128, corresponding to a Mariner’s compass with 128 discrete points. For cases where a different level of angular granularity is preferred, the `step` value can be recalculated; for instance, using `360/4` (`90.0` degrees) restricts rotation to the four cardinal directions, or using `360/8` (`45.0` degrees) allows both cardinal and intercardinal directions. Once the angle is snapped (if applicable), the method updates the target yaw, which is used in subsequent rotation updates to interpolate the actual yaw toward the target value.

##### `toggle_crouch`

Toggles whether the character is in a crouching state.

```nvgt
void toggle_crouch() final;
```



##### `turn_around`

Instructs the controller that the character should perform a full 180-degree rotation to the right.

```nvgt
void turn_around() final;
```

###### Remarks

This function is most useful when the character is facing a cardinal direction.

##### `update`

Instructs the controller that a new frame is about to begin and it should perform all necessary actions to realize field/property changes.

```nvgt
void update(const float delta_time) final;
```

###### Parameters

* `const float delta_time`: the difference between the time of the previous frame and this new frame. This value should be reasonably consistent; drastic changes will cause dramatic changes in the controller's internal state.

###### Remarks

This function should be called once per iteration of your game loop. Your loop should take as little time as possible, and there should be as little time between `update` calls as you can manage. This function should be called *after* making any changes to public properties or fields; calling it *before* changes are made will work, but changes will not be realized until the subsequent frame.

Warning: do not insert extreme delays between calls to this function. If the delta time is too extreme, the simulation and physics will be unpredictable.



#### Properties
##### `grounded`

Determines if the player is on the ground for simulation purposes.

```nvgt
void set_grounded(const bool grounded) property final;
```

###### Remarks

What is defined as the "ground" is left up to subclasses. For sane behavior, the "ground" is, by default, a vertical axis of 0 in the position vector. However, you are free to change this by overriding the `on_position_changed` callback. To lock the player at whatever you determine is the ground:

1. Set the vertical axis with respect to position and velocity to zero. Do not modify any other axis of either vector.
2. Set this property to true.

Note that gravity will always be applied, regardless of whether the player is on the ground or airborn. When overriding the `on_position_changed` callback, always implement some form of ground detection; should you fail to do so, the character will fall forever.

##### `handedness`

Determines whether this controller uses a left-or right-handed coordinate system. The default is to use a right-handed coordinate system.

```nvgt
coordinate_handedness get_handedness() property final;
void set_handedness(const coordinate_handedness value) property final;
```

###### Remarks

For information on handedness and exactly how this alters the behavior of the controller, see the introduction to this class.

When changing this property, the forward and right vectors are automatically recomputed. No other properties are modified.

It is strongly recommended that the handedness of the controller only be altered when operating in a setting where a left-handed coordinate system is required (e.g., for operating with an audio engine which defaults to it). Changing this property should be rare in practice.

It is safe to assume that the value of this property is always in a valid state.

###### Exceptions

An assertion failure occurs if neither of the valid enumeration values is provided to the setter of this property. An assertion failure also occurs in the constructor if an invalid value is supplied.

##### `target_yaw`

Determines the target yaw to which the character should rotate.

```nvgt
void set_target_yaw(const float value) property;
float get_target_yaw() property;
```

###### Remarks

This property can be used to instruct the controller to orient the player to any arbitrary yaw. If the value exceeds 360 or is negative, the behavior is undefined. The controller will attempt to automatically correct for this problem when handling rotation, but depending on this behavior is strongly discouraged.

Note that setting this property does not immediately cause a rotation to occur. Rotation will be performed per frame (that is, every time `update` is called with a steady `delta_time`). This ensures that rotation feels natural to the player. If you wish to cause an immediate rotation, expose a way for your character controller subclass to force `yaw` to a specific value. This behavior is, however, discouraged, but it should not break the simulation if you do so.

##### `yaw`

Determines the current yaw of the character.

```nvgt
float get_yaw() property;
private void set_yaw(const float value) property;
```

###### Remarks

Setting this property is explicitly disallowed to subclasses because it is typically a very unusual thing to do. Although it does not break the simulation, it is not normally something implementors should contemplate. There are alternative methods of achieving this, such as setting the rotation speed to a very high value. If you do wish to be able to set this property, you are free to override this function.




## Enums
### `coordinate_handedness`

Determines the handedness of the coordinate system used by this controller.

| Constant | Description |
| --- | --- |
| `COORDINATE_HANDEDNESS_LEFT` | Instructs this controller to use a left-handed coordinate system. |
| `COORDINATE_HANDEDNESS_RIGHT` | Instructs this controller to use a right-handed coordinate system. |



## Functions
### `nearest_compass_point`

Snaps the provided yaw to the closest compass point based on `step`.

```nvgt
float nearest_compass_point(const float deg, const float step = 2.8125);
```

#### Parameters

* `const float deg`: the yaw that should be adjusted.
* `const float step`: the granularity of the adjustment performed.


### `snap_to_degree`

Attempts to snap the degree to any of the given points. The behavior is undefined if no points are provided.

```nvgt
float snap_to_degree(const float deg, const float[] snaps);
```

#### Parameters

* `const float deg`: the current yaw
* `const float[] snaps`: the list of valid compass points to pick from.

#### Remarks

The points that callers provide should be whole numbers only. Fractional numbers may work, but are not guaranteed.

#### Exceptions

An assertion error is triggered if the provided yaw is less than 0 or greater than 360.

### `translate_yaw_to_direction`

Translates the given yaw to a direction string.

```nvgt
string translate_yaw_to_direction(const float yaw);
```

#### Parameters

* `const float yaw`: the yaw to translate to a direction.

#### Returns

`string`: the direction string that this yaw would correspond to.

#### Remarks

This function uses the Mariner's compass, which has 128 points and has some direction strings not typically scene outside specific applications or domains. This function includes these rarer points for completeness.

This function is a utility function provided so that it is one less thing you need to implement.



