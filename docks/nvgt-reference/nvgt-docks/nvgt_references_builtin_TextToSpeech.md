# Text-To-Speech
## Text to speech
This section contains references for the functionality that allows for speech output. Both direct speech engine support is available as well as outputting to screen readers.

### Notes on screen Reader Speech functions
This set of functions lets you output to virtually any screen reader, either through speech, braille, or both. In addition, you can query the availability of speech/braille in your given screen reader, get the name of the active screen reader, and much more!

On Windows, we use the [Tolk](https://github.com/dkager/tolk) library. If you want screen reader speech to work on Windows, you have to make sure Tolk.dll, nvdaControllerClient64.dll, and SAAPI64.dll are in the lib folder you ship with your games.


## classes
### tts_voice

This class provides a convenient way to communicate with all of the text-to-speech voices a user has installed on their system.

tts_voice();

#### Remarks:

NVGT implements a tiny [builtin fallback speech synthesizer](https://github.com/mattiasgustavsson/libs/blob/main/speech.h) that is used either when there is no speech engine available on the system, or if it is explicitly set with the tts_voice::set_voice() function. It sounds terrible, and is only intended for emergencies, after all understandable speech is better than no speech at all. It was used heavily when porting NVGT to other platforms, because it allowed focus to be primarily fixed on getting nvgt to run while individual tts engine support on each platform could be added later. If you don't want your end users to be able to select this speech synthesizer, pass a blank string to this constructor.

#### Example:

```NVGT
void main() {
	tts_voice v;
	v.speak_wait("Type some text and I'll repeat it. Leave the field blank to stop");
	string text = "";
	while (true) {
		text = input_box("Text", "Type some text to have the TTS speak.");
		if (text.empty()) break;
		v.speak(text);
	}
}
```



#### Methods
##### get_speaking

Check if the text to speech voice is currently speaking.

bool tts_voice::get_speaking();

###### Returns:

* bool: whether the tts voice is speaking. True if so, false if not.

###### Example:

```NVGT
void main() {
	tts_voice v;
	alert("Is it speaking right now?", v.get_speaking());
	v.speak("I'm now saying something, I think...");
	wait(250);
	alert("How about now?", v.get_speaking());
}
```



##### get_voice_count

Get a count of all available text to speech voices, including the builtin.

int tts_voice::get_voice_count();

###### Returns:

* int: the number of tts voices.

###### Remarks:

The default voice built into Nvgt is counted here so it's always one more than the available system voices.

###### Example:

```NVGT
void main() {
	tts_voice v;
	alert("result:", "You have "+v.get_voice_count()+" voices");
}
```



##### get_voice_name

Get the name of a voice at a particular index.

string tts_voice::get_voice_name(int index);

###### Parameters:

* int index: the index of the voice to get the name of.

###### Returns:

string: the name of the voice.

###### Example:

```NVGT
void main() {
	tts_voice v;
	if (v.voice_count < 1) {
		alert("Oh no", "Your system does not appear to have any TTS voices.");
		exit();
	}
	alert("The first voice on your system is", v.get_voice_name(0));
}
```



##### get_volume

Get the text to speech voice's volume (how loud it is).

int tts_voice::get_volume();

###### Returns:

int: the current volume in percentage.

###### Remarks:

0 is silent, 100 is loudest. If this hasn't been assigned, it will use the OS setting which may not be 100%. Beware if running old code, this is different from bgt having 0 be the max.

###### Example:

```NVGT
void main() {
	tts_voice v;
	v.set_volume(50);
	alert("the current volume is: ", ""+v.get_volume());
}
```



##### list_voices

List all the available voices of the tts_voice object.

string[]@ tts_voice::list_voices();

###### Returns:

string[]@: a handle to an array containing all the voice names (as strings).

###### Example:

```NVGT
void main() {
	tts_voice v;
	string[]@ voices = v.list_voices();
	alert("Your available text-to-speech voices are", join(voices, ", "));
}
```



##### refresh
Refreshes the list of TTS voices installed on the system this object knows about.

`bool tts_voice::refresh();`

###### Returns:
bool: true if the list was successfully refreshed, false otherwise.


##### set_rate

Set the text to speech voice's playback rate (how fast it speaks).

void tts_voice::set_rate(int rate);

###### Arguments:

* int rate: the desired speech rate.

###### Remarks:

-10 is slowest, 10 is fastest, with 0 being default speed, or 50 percent if you like. If this hasn't been manually assigned, it will use the OS setting which may not be 0. If moving in old bgt code, you may want to update it to use this method instead of the rate property.

###### Example:

```NVGT
void main() {
	tts_voice v;
	v.set_rate(0);
	v.speak("This is at fifty percent rate");
	v.set_rate(5);
	v.speak_wait("this is at seventy-five percent rate");
	//demonstrate setting it like it's a percentage, but note that it'll jump a bit because percentages have 100 values but there are only technically 21 choices, so implement this idea with an increment of 5 for best results.
	uint desired_rate=85;
	v.set_rate(desired_rate/5-10);
	int resulting_rate=v.get_rate();
	alert("after setting as 85 percent, the resulting rate now is:", resulting_rate);
}
```



##### set_voice
Set the voice of the TTS voice.

`bool tts_voice::set_voice(int index);`

###### Arguments:
* int index: index of the voice to switch to.

###### Returns:
bool: true if the voice was successfully set, false otherwise.


##### set_volume

Set the text to speech voice's volume (how loud it is).

void tts_voice::set_volume(int volume);

###### Arguments:

* int volume: the desired volume level.

###### Remarks:

0 is silent, 100 is loudest. If this hasn't been assigned, it will use the OS setting which may not be 100%. Beware if running old code, this is different from bgt having 0 be the max. It's better to use this instead of directly setting volume property.

###### Example:

```NVGT
void main() {
	tts_voice v;
	v.set_volume(50);
	v.speak("This is at 50 volume");
	v.set_volume(100);
	v.speak_wait("this is at 100 volume");
}
```



##### speak

Speak a string of text through the currently active TTS voice.

bool tts_voice::speak(const string &in text, bool interrupt = false);

###### Arguments:

* const string&in text: the text to be spoken.

* bool interrupt = false: whether or not to interrupt the previously speaking speech to speak the new string.

###### Returns:

bool: true if speech was successful, false otherwise.

###### Example:

```NVGT
void main() {
	tts_voice v;
	v.speak("Hello, world!");
	while (v.speaking) {}
}
```



##### speak_interrupt

Speaks a string (forcefully interrupting) through the currently active text-to-speech voice.

bool tts_voice::speak_interrupt(const string&in text);

###### Arguments:

* const string&in text: the text to speak.

###### Returns:

bool: true if the speech was generated successfully, false otherwise.

###### Example:

```NVGT
void main() {
	int orig_ticks = ticks();
	tts_voice v;
	v.speak("This is an incredibly long string that will eventually get cut off by a much worse one.");
	while (v.speaking) {
		if ((ticks() - orig_ticks) > 250)
			break;
	}
	v.speak_interrupt("You have been interrupted!");
	while (v.speaking) {}
}
```



##### speak_to_file

Outputs a string of text through the currently active TTS voice to a wave file.

bool tts_voice::speak_to_file(const string&in filename, const string&in text);

###### Arguments:

* const string&in filename: the filename to write to.

* const string&in text: the text to synthesize.

###### Returns:

bool: true if synthesis was successful and the file was written, false otherwise.

###### Example:

```NVGT
void main() {
	// This is actually quite broken currently, it only ever writes  a 4 KB wav file. I think the problem is probably in speaking to memory in general, also see test/speak_to_file.nvgt.
	string filename = input_box("Filename", "Enter the name of the file to save to (without the .wav extension).");
	if (filename.is_empty()) {
		alert("Error", "You didn't type a filename.");
		exit();
	}
	string text = input_box("Text", "Enter the text to synthesize.");
	if (text.is_empty()) {
		alert("Error", "You didn't type any text.");
		exit();
	}
	tts_voice v;
	v.speak_to_file(filename + ".wav", text);
	alert("Info", "Done!");
}
```



##### stop

Stop the TTS voice, if currently speaking.

bool tts_voice::stop();

###### Returns:

bool: true if the voice was successfully stopped, false otherwise.

###### Example:

```NVGT
void main() {
	tts_voice v;
	v.speak("Hello there!");
	wait(500);
	v.stop();
}
```




#### Properties
##### speaking

Is the tts_voice currently speaking?

bool tts_voice::speaking;

###### Example:

```NVGT
void main() {
	tts_voice v;
	v.speak("Hello there! This is a very long string that will hopefully be spoken for at least a couple seconds");
	wait(500);
	alert("Example", v.speaking ? "The TTS voice is currently speaking. Press OK to stop it" : "The TTS voice is not currently speaking");
}
```



##### voice

The number of the currently selected voice.

int tts_voice::voice;

###### Example:

```NVGT
void main() {
	tts_voice v;
	alert("Current voice index", v.voice);
	v.set_voice(0);
	alert("Current voice index", v.voice);
}
```



##### voice_count

Represents the total number of available tex-to-speech voices on your system.

int tts_voice::voice_count;

###### Example:

```NVGT
void main() {
	tts_voice v;
	alert("Your system has", v.voice_count + " text-to-speech " + (v.voice_count == 1 ? "voice" : "voices"));
}
```






## Functions
### screen_reader_braille

Brailles a string through the currently active screen reader, if supported.

bool screen_reader_braille(const string&in text);

#### Arguments:

* const string&in text: the text to braille.

#### Returns:

bool: true if the function succeeded, false otherwise.

#### Example:

```NVGT
void main() {
	screen_reader_braille("This message will only be brailled.");
}
```



### screen_reader_detect

Returns the name of the currently active screen reader as a string.

string screen_reader_detect();

#### Returns:

string: the name of the given screen reader, or a blank string if none was found.

#### Example:

```NVGT
void main() {
	string sr = screen_reader_detect();
	if (sr.is_empty())
		alert("Info", "No screen reader found.");
	else
		alert("Info", "The active screen reader is " + sr);
}
```



### screen_reader_has_braille

Determine if the active screen reader supports braille output.

bool screen_reader_has_braille();

#### Returns:

bool: true if the active screen reader supports braille, false otherwise.

#### Example:

```NVGT
void main() {
	bool has_braille  = screen_reader_has_braille();
	if (has_braille)
		alert("Info", "The currently active screen reader supports braille.");
	else
		alert("Info", "The currently active screen reader does not support braille.");
}
```



### screen_reader_has_speech

Determines if the active screen reader supports speech output.

bool screen_reader_has_speech();

#### Returns:

bool: true if the screen reader supports speech, false if not, or if no screen reader is active.

#### Example:

```NVGT
void main() {
	bool has_speech = screen_reader_has_speech();
	if (has_speech)
		alert("Info", "The active screen reader supports speech.");
	else
		alert("Info", "The active screen reader does not support speech.");
}
```



### screen_reader_is_speaking

Determine if the currently active screen reader (if any) is currently speaking.

bool screen_reader_is_speaking();

#### Returns:

bool: true if the currently active screen reader is speaking, false otherwise.

#### Remarks:

This function isn't foolproof, as some screen readers (e.g. NVDA) don't have a way to query this information.

#### Example:

```NVGT
void main() {
	screen_reader_speak("Hello there, this is a very long string that will hopefully be spoken!", true);
	wait(50);
	bool speaking = screen_reader_is_speaking();
	if (speaking)
		alert("Info", "The screen reader is speaking.");
	else
		alert("Info", "The screen reader is not speaking.");
}
```



### screen_reader_output

Speaks and brailles a string through the currently active screen reader, if supported.

bool screen_reader_output(const string&in text, bool interrupt = true);

#### Arguments:

* const string&in text: the text to output.

* bool interrupt = true: Whether or not the previously spoken speech should be interrupted or not when speaking the new string.

#### Returns:

bool: true if the function succeeded, false otherwise.

#### Example:

```NVGT
void main() {
	screen_reader_output("This message will be both spoken and brailled!", true);
}
```



### screen_reader_speak

Speaks a string through the currently active screen reader, if supported.

bool screen_reader_speak(const string&in text, bool interrupt = true);

#### Arguments:

* const string&in text: the text to speak.

* bool interrupt = true: Whether or not the previously spoken speech should be interrupted or not when speaking the new string.

#### Returns:

bool: true if the function succeeded, false otherwise.

#### Example:

```NVGT
void main() {
	screen_reader_speak("This message will only be spoken.", true);
}
```




## Global Properties
### SCREEN_READER_AVAILABLE

reports if a screen reader is currently available.

const bool SCREEN_READER_AVAILABLE;

#### Example:

```NVGT
void main() {
	if (SCREEN_READER_AVAILABLE)
		alert("Info", "A screen reader is available.");
	else
		alert("Info", "A screen reader is not available.");
}
```





