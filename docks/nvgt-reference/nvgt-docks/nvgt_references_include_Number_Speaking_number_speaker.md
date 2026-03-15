# Number Speaking (number_speaker.nvgt)
## classes
### number_speaker

The `number_speaker` object is used to facilitate natural and smooth number speech. It is best to use this class if you're developing a game with voice acting.

number_speaker();

#### Remarks:

The `number_speaker` class searches for sound files that match the spoken components of a number as closely as possible, separating words with an underscore. For instance, if the number is 72, it'll first check for a file named seventy_two.wav. If this file is not available, it'll search for seventy.wav and two.wav and combine them.

This system allows you to record as many number sounds as desired to achieve flawless spoken output. Alternatively, you can record only essential numbers, such as zero.wav to nineteen.wav, twenty.wav to ninety.wav, and optionally hundred.wav, thousand.wav, and million.wav. You can also record a file named minus.wav to distinguish between positive and negative numbers, as well as and.ogg to have the word "and" spoken if the include_and parameter is enabled.

#### Example:

```NVGT
#include "number_speaker.nvgt"
void main() {
	// Speak a number using speak_wait.
	number_speaker test;
	test.speak_wait(350);
}
```



#### methods
##### speak

This method will speak a number.

int number_speaker::speak(double the_number);

###### Arguments:

* double the_number: the number to speak.

###### Returns:

int: 0 on success, -1 on failure.

###### Remarks:

The speak method searches for sound files based on the values stored in the prepend and append properties, determining the most appropriate sound files to use by performing multiple searches based on the given number.

When this function is called, it returns immediately, allowing the script to continue running while the number is being spoken. To ensure that numbers are spoken smoothly and fluently, it is necessary to call the speak_next method continuously.

###### Example:

```NVGT
#include "number_speaker.nvgt"
void main() {
	number_speaker number;
	number.speak(350);
	while(number.speak_next()==1) {
		wait(5);
	}
}
```



##### speak_next

This method is used to check the status of a number that is currently being spoken or has already been spoken, and, if necessary, initiates the playback of the next number.

int number_speaker::speak_next();

###### Returns:

int: 0 if there are no more files to be played, 1 if there are more files to be played or if the last file is still playing, and -1 if an error occurs.

###### Remarks:

The speak_next method works in conjunction with the speak method and should be used continuously while the number is being spoken.

This method functions not only as a status indicator but also as a trigger, checking and playing numbers as needed. To ensure that the numbers are spoken smoothly and fluently, it is essential to perform this check at regular intervals, approximately every 5 milliseconds.

###### Example:

```NVGT
#include "number_speaker.nvgt"
void main() {
	// Speak a number using speak and speak_next.
	number_speaker test;
	test.speak(350);
	while(test.speak_next()==1) {
		wait(5);
	}
}
```



##### speak_wait

This method will speak a number and wait until the number is fully read before returning.

int number_speaker::speak_wait(double the_number);

###### Arguments:

* double the_number: the number to speak.

###### Returns:

int: 0 on success, -1 on failure.

###### Remarks:

The speak_wait method searches for sound files based on the values stored in the prepend and append properties, determining the most appropriate sound files to use by performing multiple searches based on the given number.

The speak_wait function pauses execution until the number has been fully spoken before returning. This means that the script execution is halted for the duration of the reading. To avoid this, you can use the speak and speak_next methods instead.

###### Example:

```NVGT
#include "number_speaker.nvgt"
void main() {
	// Speak a number using speak_wait.
	number_speaker test;
	test.speak_wait(350);
}
```



##### stop

This method stops any number that is currently being spoken.

void number_speaker::stop();

###### Example:

```NVGT
#include "number_speaker.nvgt"
void main() {
	// Speak a number using speak and speak_next, stopping it prematurely if the user presses space.
	number_speaker test;
	test.speak(350);
	while(test.speak_next()==1) {
		if(key_pressed(KEY_SPACE))
			test.stop();
		wait(5);
	}
}
```



##### set_sound_object

This method allows you to specify an existing sound object to be used for any auditory feedback in the number speaker.

bool number_speaker::set_sound_object(sound@ handle);

###### Arguments:

* sound@ handle: a reference to an existing sound object that will be utilized for all future sound output.

###### Returns:

bool: true on success, false on failure.

###### Remarks:

The object specified in this function will handle all future auditory feedback provided by the number speaker. If this method is not called, an internal sound object will be used by default for sound output.

###### Example:

```NVGT
#include "number_speaker.nvgt"
void main() {
	sound test;
	number_speaker number;
	number.set_sound_object(test);
	number.speak_wait(350);
}
```




#### properties
##### append
This string will be appended to any loaded number file. The default extension is .wav, so you only need to change this if your number files use a different extension.

`string number_speaker::append;`


##### prepend
This string will be prepended to any loaded number file. It is useful if your number files are stored in a separate directory or if the filenames include a specific prefix.

`string number_speaker::prepend;`


##### include_and
This boolean determines whether the word "and" should be included in the appropriate places in the output. If set to true, you must create a file named and.wav, unless the extension (e.g., the append property) is something other than .wav. The default value is false.

`bool number_speaker::include_and;`


##### pack_file
The pack file to use in the object.

`pack_file@ number_speaker::pack_file = null;`






