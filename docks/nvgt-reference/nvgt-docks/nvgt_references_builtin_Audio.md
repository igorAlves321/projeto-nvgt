# Audio
## Classes
### sound
#### Methods
##### close

Closes an opened sound, making the sound object available to be reloaded with a new one.

bool sound::close();

###### Returns:

bool: true if the sound could be closed, false otherwise for example if there is no sound opened.

###### Example:

```NVGT
void main() {
	sound s;
	s.load("C:/windows/media/ding.wav");
	alert("example", s.close()); // Will display true since a sound was previously opened.
	alert("example", s.close()); // Will now display false since the previous operation freed the sound object of any attached sound.
}
```



##### load
Loads a sound file with the specified settings.

1. `bool sound::load(string filename, pack@ soundpack = null, bool allow_preloads = true);`
2. `bool sound::load(sound_close_callback@ close_cb, sound_length_callback@ length_cb, sound_read_callback@ read_cb, sound_seek_callback@ seek_cb, string data, string preload_filename = "");`

###### Arguments (1):
* string filename: the name/path to the file that is to be loaded.
* pack@ soundpack = null: a handle to the pack object to load this sound from, if any.
* bool allow_preloads = true: whether or not the sound system should preload sounds into memory on game load.

###### Arguments (2):
* sound_close_callback@ close_cb: the close callback to use with the sound (see remarks).
* sound_length_callback@ length_cb: the length callback to use with the sound (see remarks).
* sound_read_callback@ read_cb: the read callback to use with the sound (see remarks).
* sound_seek_callback@ seek_cb: the seek callback to use with the sound (see remarks).
* string data: the audio data of the sound.
* string preload_filename = "": the name of the file to be preloaded (if any).

###### Returns:
bool: true if the sound was successfully loaded, false otherwise.

###### Remarks:
The syntax for the sound_close_callback is:
> void sound_close_callback(string user_data);

The syntax for the sound_length_callback is:
> uint sound_length_callback(string user_data);

The syntax for the sound_read_callback is:
> int sound_read_callback(string &out buffer, uint length, string user_data);

The syntax for the sound_seek_callback is:
> bool sound_seek_callback(uint offset, string user_data);


##### load_url

Load the specified URL.

bool sound::load_url(string url);

###### Arguments:

* string url: the URL to load (should be the direct link to a sound or stream).

###### Returns:

Bool: True if the URL was successfully loaded; false otherwise.

###### Example:

```NVGT
void main() {
	sound s;
	bool success = s.load_url("https://example.com/my_sound.mp3");
	alert("Result", "The sound was " + (success == false? "not " : "") + "successfully loaded.");
}
```



##### pause
Pauses the sound.

`bool sound::pause();`

###### Returns:
bool: true if the sound was paused, false otherwise.


##### play
Starts playing the sound.

`bool sound::play();`

###### Returns:
bool: true if the sound was able to start playing, false otherwise.


##### play_looped
Starts playing the sound repeatedly.

`bool sound::play_looped();`

###### Returns:
bool: true if the sound was able to start playing, false otherwise.


##### play_wait
Starts playing the sound, blocking the calling thread until it's finished.

`bool sound::play_wait();`

###### Returns:
bool: true if the sound has successfully loaded and finished playing, false otherwise.


##### seek
Seeks to a particular point in the sound.

`bool sound::seek(float ms);`

###### Arguments:
* float ms: the time (in MS) to seek to.

###### Returns:
bool: true if the seeking was successful, false otherwise.


##### set_position
Sets the sound's position in 3d space.

`bool sound::set_position(float listener_x, float listener_y, float listener_z, float sound_x, float sound_y, float sound_z, float rotation, float pan_step, float volume_step);`

###### Arguments:
* float listener_x: the x position of the listener.
* float listener_y: the y position of the listener.
* float listener_z: the z position of the listener.
* float sound_x: the x position of the sound.
* float sound_y: the y position of the sound.
* float sound_z: the z position of the sound.
* float rotation: the rotation of the listener (in radians).
* float pan_step: the pan step (e.g. how extreme the panning is).
* float volume_step: the volume step (very similar to pan_step but for volume).

###### Returns:
bool: true if the position was successfully set, false otherwise.


##### stop
Stops the sound, if currently playing.

`bool sound::stop();`

###### Returns:
bool: true if the sound was successfully stopped, false otherwise.



#### Properties
##### active
Determine if the sound has successfully been loaded or not.

`bool sound::active;`


##### length
Get the length of a sound (in milliseconds).

`float sound::length;`


##### loaded_filename
Obtain the path of sound file that has been loaded.

`string sound::loaded_filename;`


##### paused
Determine if the sound is paused.

`bool sound::paused;`


##### playing
Determine if the sound is currently playing.

`bool sound::playing;`


##### sliding
Determine if a sound is sliding or not.

`sound::sliding;`





## Functions
### get_sound_input_devices

Return an array of strings listing all input sound devices on the system.

string[]@ get_sound_input_devices();

#### Returns:

string[]@: A handle to an array listing all available input devices.

#### Remarks:

After listing devices with this function, you can set the sound_input_device global engine property to whatever index in the returned array contains the name of the device you want to set.

This list will always include a no sound device. If you don't want the user to be able to select it, feel free to not allow them to move their cursor to that item or not add it to your menus etc, but remember to pay attention to the index difference this may create when setting the sound_output_device property, namely just remember that setting sound_output_device = 0 will set the system to no sound, and setting the device to 1 will always be the first real device in the system, or the default device at least on windows.

#### Example:

```NVGT
void main() {
	string[]@ devices = get_sound_input_devices();
	devices.remove_at(0); // Don't allow the user to select no sound.
	alert("devices", "The following devices are installed on your system: " + join(devices, ", "));
}
```



### get_sound_output_devices

Return an array of strings listing all output sound devices on the system.

string[]@ get_sound_output_devices();

#### Returns:

string[]@: A handle to an array listing all available output devices.

#### Remarks:

After listing devices with this function, you can set the sound_output_device global engine property to whatever index in the returned array contains the name of the device you want to set.

This list will always include a no sound device. If you don't want the user to be able to select it, feel free to not allow them to move their cursor to that item or not add it to your menus etc, but remember to pay attention to the index difference this may create when setting the sound_output_device property, namely just remember that setting sound_output_device = 0 will set the system to no sound, and setting the device to 1 will always be the first real device in the system, or the default device at least on windows.

#### Example:

```NVGT
void main() {
	string[]@ devices = get_sound_output_devices();
	devices.remove_at(0); // Don't allow the user to select no sound.
	alert("devices", "The following devices are installed on your system: " + join(devices, ", "));
}
```




## Global Properties
### sound_default_mixer
Represents the default mixer object for all your sounds to use.

`mixer@ sound_default_mixer;`


### sound_default_pack
The default value passed to the second argument of sound::load, in other words, a handle to an open pack object that all future sounds will load from unless otherwise specified individually.

`pack@ sound_default_pack = null;`


### sound_global_hrtf
Controls weather to use steam audio's functionality. If this property is set to false, the sound_environment class will be quite useless and sounds will use very basic panning.

`bool sound_global_hrtf;`

Changes take nearly instant effect from the time this property is modified.




