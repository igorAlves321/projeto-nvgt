# Legacy Sound Manager (sound_pool.nvgt)
## Classes
### sound_pool
This class provides a convenient way of managing sounds in an environment, with 1 to 3 dimensions. The sound_pool_item class holds all the information necessary for one single sound in the game world. Note that you should not make instances of the sound_pool_item class directly but always use the methods and properties provided in the sound_pool class.

`sound_pool(int default_item_size = 100);`

#### Arguments:
* int default_item_size = 100: the number of sound items to be initialized by default.

#### Methods
##### destroy_all
destroy all sounds.

`void sound_pool::destroy_all();`


##### destroy_sound
Destroy a sound.

`bool sound_pool::destroy_sound(int slot);`

###### Arguments:
* int slot: the slot of the sound you wish to destroy.

###### Returns:
bool: true if the sound is removed successfully, false otherwise.


##### pause_all
Pauses all sounds.

`void sound_pool::pause_all();`


##### pause_sound
Pauses the sound.

`bool sound_pool::pause_sound(int slot);`

###### Arguments:
* int slot: the sound slot you wish to pause.

###### Returns:
bool: true if the sound was paused, false otherwise.


##### play_1d
Play a sound in 1 dimension and return a slot.

`int sound_pool::play_1d(string filename, pack@ packfile, float listener_x, float sound_x, bool looping, bool persistent = false);`

###### Arguments:
* string filename: the file to play.
* pack@ packfile: the pack to use. This can be omitted.
* float listener_x: the listener coordinates in X form.
* float sound_x: the coordinates of the sound in X form.
* bool looping: should the sound play continuously?
* bool persistent = false: should the sound be cleaned up once the sound is finished playing?

###### Returns:
int: the index of the sound which can be modified later, or -1 if error. This method may return -2 if the sound is out of earshot.

###### Remarks:
If the looping parameter is set to true and the sound object is inactive, the sound is still considered to be active as this just means that we are currently out of earshot. A non-looping sound that has finished playing is considered to be dead, and will be cleaned up if it is not set to be persistent.


##### play_2d
Play a sound in 2 dimensions and return a slot.

1. `int sound_pool::play_2d(string filename, pack@ packfile, float listener_x, float listener_y, float sound_x, float sound_y, bool looping, bool persistent = false);`
2. `int sound_pool::play_2d(string filename, pack@ packfile, float listener_x, float listener_y, float sound_x, float sound_y, double rotation, bool looping, bool persistent = false);`
3. `int sound_pool::play_2d(string filename, float listener_x, float listener_y, float sound_x, float sound_y, bool looping, bool persistent = false);`
4. `int sound_pool::play_2d(string filename, float listener_x, float listener_y, float sound_x, float sound_y, double rotation, bool looping, bool persistent = false);`

###### Arguments:
* string filename: the file to play.
* pack@ packfile: the pack to use (optional).
* float listener_x, listener_y: the listener coordinates in X, Y form.
* float sound_x, sound_y: the coordinates of the sound in X, Y form.
* double rotation: the listener's rotation (optional).
* bool looping: should the sound play continuously?
* bool persistent = false: should the sound be cleaned up once the sound is finished playing?

###### Returns:
int: the index of the sound which can be modified later, or -1 if error. This method may return -2 if the sound is out of earshot.

###### Remarks:
If the looping parameter is set to true and the sound object is inactive, the sound is still considered to be active as this just means that we are currently out of earshot. A non-looping sound that has finished playing is considered to be dead, and will be cleaned up if it is not set to be persistent.


##### play_3d
Play a sound in 3 dimensions and return a slot.

1. `int sound_pool::play_3d(string filename, pack@ packfile, float listener_x, float listener_y, float listener_z, float sound_x, float sound_y, float sound_z, double rotation, bool looping, bool persistent = false);`
2. `int sound_pool::play_3d(string filename, pack@ packfile, vector listener, vector sound_coordinate, double rotation, bool looping, bool persistent = false);`

###### Arguments (1):
* string filename: the file to play.
* pack@ packfile: the pack to use. This can be omitted
* float listener_x, listener_y, listener_z: the listener coordinates in X, Y, Z form.
* float sound_x, sound_y, sound_z: the coordinates of the sound in X, Y, Z form.
* double rotation: the listener's rotation.
* bool looping: should the sound play continuously?
* bool persistent = false: should the sound be cleaned up once the sound is finished playing?

###### Arguments (2):
* string filename: the file to play.
* pack@ packfile: the pack to use. This can be omitted
* vector listener: the coordinates of listener in vector form.
* vector sound_coordinate: the coordinates of the sound in vector form.
* double rotation: the listener's rotation.
* bool looping: should the sound play continuously?
* bool persistent = false: should the sound be cleaned up once the sound is finished playing?

###### Returns:
int: the index of the sound which can be modified later, or -1 if error. This method may return -2 if the sound is out of earshot.

###### Remarks:
If the looping parameter is set to true and the sound object is inactive, the sound is still considered to be active as this just means that we are currently out of earshot. A non-looping sound that has finished playing is considered to be dead, and will be cleaned up if it is not set to be persistent.


##### play_extended
Play a sound and return a slot. This method has many parameters that can be customized.

`int sound_pool::play_extended(int dimension, string filename, pack@ packfile, float listener_x, float listener_y, float listener_z, float sound_x, float sound_y, float sound_z, double rotation, int left_range, int right_range, int backward_range, int forward_range, int lower_range, int upper_range, bool looping, double offset, float start_pan, float start_volume, float start_pitch, bool persistent = false, mixer@ mix = null, string[]@ fx = null, bool start_playing = true, double theta = 0);`

###### Arguments:
* int dimension: the number of dimension to play on, 1, 2, 3.
* string filename: the file to play.
* pack@ packfile: the pack to use.
* float listener_x, listener_y, listener_z: the listener coordinates in X, Y, Z form.
* float sound_x, sound_y, sound_z: the coordinates of the sound in X, Y, Z form.
* double rotation: the listener's rotation.
* int left_range, right_range, backward_range, forward_range, lower_range, upper_range: the range of the sound.
* bool looping: should the sound play continuously?
* double offset: the number of milliseconds for the sound to start playing at.
* float start_pan: the pan of the sound. -100 is left, 0 is middle, and 100 is right.
* float start_volume: the volume of the sound. 0 is maximum and -100 is silent.
* float start_pitch: the pitch of the sound.
* bool persistent = false: should the sound be cleaned up once the sound is finished playing?
* mixer@ mix = null: the mixer to attach to this sound.
* string[]@ fx = null: array of effects to be set.
* bool start_playing = true: should the sound play the moment this function is executed?
* double theta = 0: the theta calculated by `calculate_theta` function in rotation.nvgt include.

###### Returns:
int: the index of the sound which can be modified later, or -1 if error. This method may return -2 if the sound is out of earshot.

###### Remarks:
If the looping parameter is set to true and the sound object is inactive, the sound is still considered to be active as this just means that we are currently out of earshot. A non-looping sound that has finished playing is considered to be dead, and will be cleaned up if it is not set to be persistent.


##### play_stationary
Play a stationary sound and return a slot.

1. `int sound_pool::play_stationary(string filename, bool looping, bool persistent = false);`
2. `int sound_pool::play_stationary(string filename, pack@ packfile, bool looping, bool persistent = false);`

###### Arguments (1):
* string filename: the file to play.
* bool looping: should the sound play continuously?
* bool persistent = false: should the sound be cleaned up once the sound is finished playing?

###### Arguments (2):
* string filename: the file to play.
* pack@ packfile: the pack to use.
* bool looping: should the sound play continuously?
* bool persistent = false: should the sound be cleaned up once the sound is finished playing?

###### Returns:
int: the index of the sound which can be modified later, or -1 if error. This method may return -2 if the sound is out of earshot.

###### Remarks:
If the looping parameter is set to true and the sound object is inactive, the sound is still considered to be active as this just means that we are currently out of earshot. A non-looping sound that has finished playing is considered to be dead, and will be cleaned up if it is not set to be persistent.

This method will play the sound in stationary mode. This means that sounds played by this method have no movement updates as if they are stationary, and coordinate update functions will not work.

##### resume_all
Resumes all sounds.

`void sound_pool::resume_all();`


##### resume_sound
Resumes the sound.

`bool sound_pool::resume_sound(int slot);`

###### Arguments:
* int slot: the sound slot you wish to resume.

###### Returns:
bool: true if the sound was resumed, false otherwise.


##### sound_is_active
Determine whether the sound is active.

`bool sound_pool::sound_is_active(int slot);`

###### Arguments:
* int slot: the sound slot you wish to check.

###### Returns:
bool: true if the sound is active, false otherwise.

###### Remarks:
If the looping parameter is set to true and the sound object is inactive, the sound is still considered to be active as this just means that we are currently out of earshot. A non-looping sound that has finished playing is considered to be dead, and will be cleaned up.


##### sound_is_playing
Determine whether the sound is playing.

`bool sound_pool::sound_is_playing(int slot);`

###### Arguments:
* int slot: the sound slot you wish to check.

###### Returns:
bool: true if the sound is playing, false otherwise.


##### update_listener_1d
Updates the listener coordinate in 1 dimension.

`void sound_pool::update_listener_1d(float listener_x);`

###### Arguments:
* float listener_x: the X coordinate of the listener.


##### update_listener_2d
Updates the listener coordinate in 2 dimensions.

`void sound_pool::update_listener_2d(float listener_x, float listener_y, double rotation = 0.0);`

###### Arguments:
* float listener_x: the X coordinate of the listener.
* float listener_y: the Y coordinate of the listener.
* double rotation = 0.0: the rotation to use.


##### update_listener_3d
Updates the listener coordinate in 3 dimensions.

1. `void sound_pool::update_listener_3d(float listener_x, float listener_y, float listener_z, double rotation = 0.0, bool refresh_y_is_elevation = true);`
2. `void sound_pool::update_listener_3d(vector listener, double rotation = 0.0, bool refresh_y_is_elevation = true);`

###### Arguments (1):
* float listener_x: the X coordinate of the listener.
* float listener_y: the Y coordinate of the listener.
* float listener_z: the Z coordinate of the listener.
* double rotation = 0.0: the rotation to use.
* bool refresh_y_is_elevation = true: toggles whether `y_is_elevation` property should refresh from the `sound_pool_default_y_is_elevation` global property.

###### Arguments (2):
* vector listener: the coordinates of the listener in vector form.
* double rotation = 0.0: the rotation to use.
* bool refresh_y_is_elevation = true: toggles whether `y_is_elevation` property should refresh from the `sound_pool_default_y_is_elevation` global property.


##### update_sound_1d
Updates the sound coordinate in 1 dimensions.

`bool sound_pool::update_sound_1d(int slot, int x);`

###### Arguments:
* int slot: the slot of the sound you wish to update.
* int x: the X coordinate of the sound.

###### Returns:
bool: true if the sound is updated successfully, false otherwise.


##### update_sound_2d
Updates the sound coordinate in 2 dimensions.

`bool sound_pool::update_sound_2d(int slot, int x, int y);`

###### Arguments:
* int slot: the slot of the sound you wish to update.
* int x: the X coordinate of the sound.
* int y: the Y coordinate of the sound.

###### Returns:
bool: true if the sound is updated successfully, false otherwise.


##### update_sound_3d
Updates the sound coordinate in 3 dimensions.

1. `bool sound_pool::update_sound_3d(int slot, int x, int y, int z);`
2. `bool sound_pool::update_sound_3d(int slot, vector coordinate);`

###### Arguments (1):
* int slot: the slot of the sound you wish to update.
* int x: the X coordinate of the sound.
* int y: the Y coordinate of the sound.
* int z: the Z coordinate of the sound.

###### Arguments (2):
* int slot: the slot of the sound you wish to update.
* vector coordinate: the coordinate of the sound in vector form.

###### Returns:
bool: true if the sound is updated successfully, false otherwise.


##### update_sound_range_1d
Updates the sound range in 1 dimensions.

`bool sound_pool::update_sound_range_1d(int slot, int left_range, int right_range);`

###### Arguments:
* int slot: the slot of the sound you wish to update.
* int left_range: the left range to update.
* int right_range: the right range to update.

###### Returns:
bool: true if the sound is updated successfully, false otherwise.


##### update_sound_range_2d
Updates the sound range in 2 dimensions.

`bool sound_pool::update_sound_range_2d(int slot, int left_range, int right_range, int backward_range, int forward_range);`

###### Arguments:
* int slot: the slot of the sound you wish to update.
* int left_range: the left range to update.
* int right_range: the right range to update.
* int backward_range: the backward range to update.
* int forward_range: the forward range to update.

###### Returns:
bool: true if the sound is updated successfully, false otherwise.


##### update_sound_range_3d
Updates the sound range in 3 dimensions.

`bool sound_pool::update_sound_range_3d(int slot, int left_range, int right_range, int backward_range, int forward_range, int lower_range, int upper_range, bool update_sound = true);`

###### Arguments:
* int slot: the slot of the sound you wish to update.
* int left_range: the left range to update.
* int right_range: the right range to update.
* int backward_range: the backward range to update.
* int forward_range: the forward range to update.
* int lower_range: the bottom / lower range to update.
* int upper_range: the above / upper range to update.
* bool update_sound = true: toggles whether all the sound will be updated automatically.

###### Returns:
bool: true if the sound is updated successfully, false otherwise.


##### update_sound_start_values
Updates the sound start properties.

`bool sound_pool::update_sound_start_values(int slot, float start_pan, float start_volume, float start_pitch);`

###### Arguments:
* int slot: the slot of the sound you wish to update.
* float start_pan: the new pan to update.
* float start_volume: the new volume to update.
* float start_pitch: the new pitch to update.

###### Returns:
bool: true if the sound is updated successfully, false otherwise.



#### Properties
##### behind_pitch_decrease
The pitch step size to decrease when the sound is behind. Default is 0.25.

`float sound_pool::behind_pitch_decrease;`


##### max_distance
The maximum distance that the sounds can be heard. Default is 0 (disabled).

`int sound_pool::max_distance;`


##### pan_step
The pan step size, the sound's final pan or position in HRTF is calculated by multiplying the player's distance from the sound by this value. Default is 1.0.

`float sound_pool::pan_step;`


##### volume_step
The volume step size, the sound's final volume is subtracted by this number multiplied by the player's distance from the sound. Default is 1.0.

`float sound_pool::volume_step;`


##### y_is_elevation
Toggles whether the Y coordinate is the same as Z, or in otherwords whether the y coordinate determines up/down or forward/backwards in your game world. By default, it retrieves from the `sound_pool_default_y_elevation` global property.

`bool sound_pool::y_is_elevation = sound_pool_default_y_elevation;`






