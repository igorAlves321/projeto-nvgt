# Security
## Functions
### string_aes_decrypt

Decrypts a string using the AES 256 bit CBC algorithm.

string string_aes_decrypt(const string&in the_data, const string&in the_key)

#### Arguments:

* const string&in the_data: The data to be decrypted.

* const string&in the_key: The key to decrypt the data with.

#### Returns:

string: decrypted text on success or an empty string on failure.

#### Remarks:

The Advanced Encryption Standard (AES) is a publicly available algorithm for encrypting data which is trusted world wide at the time of implementation into NVGT. This algorithm takes as input some plain text or binary data, then converts that data into unreadable bytes given an encryption key known only to the programmer. Only with the correct encryption key can the data returned from this function be converted (deciphered) back into the original, unencrypted data.

For anyone interested in more details or who wants more control over the AES encryption such as by providing your own initialization vector, see the aes_encrypt datastream class which gives this control. In the case of this high level encryption function, NVGT will derive an initialization vector from the encryption key provided using hashes, bitwise math, and any other custom security functions a c++ programmer wishes to add to their own version of NVGT. For most users, this is not a concern and most will not even need to know what an initialization vector is to safely use the encryption provided by this function.

#### Example:

```NVGT
void main() {
	string encrypted_text = string_aes_encrypt(string_base64_decode("SGVsbG8sIEkgYW0gYSBzdHJpbmch"), "nvgt_example_key_for_docs"); // We encrypt our example string after decoding it with base64; only encoded as such to prevent seeing unreadable characters.
	string decrypted_text = string_aes_decrypt(encrypted_text, "wrong_nvgt_example_key_for_docs");
	// Show that the text could not be decrypted because the wrong key was provided.
	alert("example", decrypted_text); // The dialog will be empty because decrypted_text is an empty string due to decryption failure.
	// Now show how the text can indeed be decrypted with the proper key.
	decrypted_text = string_aes_decrypt(encrypted_text, "nvgt_example_key_for_docs");
	alert("example", decrypted_text);
}
```



### string_aes_encrypt

Encrypts a string using the AES 256 bit CBC algorithm.

string string_aes_encrypt(const string&in the_data, const string&in the_key)

#### Arguments:

* const string&in the_data: The data to be encrypted.

* const string&in the_key: The key to encrypt the data with.

#### Returns:

string: Encrypted ciphertext on success or an empty string on failure.

#### Remarks:

The Advanced Encryption Standard (AES) is a publicly available algorithm for encrypting data which is trusted world wide at the time of implementation into NVGT. This algorithm takes as input some plain text or binary data, then converts that data into unreadable bytes given an encryption key known only to the programmer. Only with the correct encryption key can the data returned from this function be converted (deciphered) back into the original, unencrypted data.

For anyone interested in more details or who wants more control over the AES encryption such as by providing your own initialization vector, see the aes_encrypt datastream class which gives this control. In the case of this high level encryption function, NVGT will derive an initialization vector from the encryption key provided using hashes, bitwise math, and any other custom security functions a c++ programmer wishes to add to their own version of NVGT. For most users, this is not a concern and most will not even need to know what an initialization vector is to safely use the encryption provided by this function.

#### Example:

```NVGT
void main() {
	string plaintext = "Hello, I am a string!";
	string encrypted_text = string_aes_encrypt(plaintext, "nvgt_example_key_for_docs");
	// Prove that the text was encrypted by showing a base64 encoded version of it to the user. We encode the encrypted data for display because it may contain unprintable characters after encryption.
	alert("example", string_base64_encode(encrypted_text));
	string decrypted_text = string_aes_decrypt(encrypted_text, "wrong_nvgt_example_key_for_docs");
	// Show that the text could not be decrypted because the wrong key was provided.
	alert("example", decrypted_text); // The dialog will be empty because decrypted_text is an empty string due to decryption failure.
	// Now show how the text can indeed be decrypted with the proper key.
	decrypted_text = string_aes_decrypt(encrypted_text, "nvgt_example_key_for_docs");
	alert("example", decrypted_text);
}
```




## Global Properties
### memory_scan_detected
Determines if an application is scanning the address space of your game.

```nvgt
const atomic_flag memory_scan_detected;
```

#### Remarks
This flag is set internally by the engine whenever `wait()` or `refresh_window()` are called and it can be determined by the engine that an external process is reading the virtual address space of the process. In some circumstances, writing to the address space by an external process may trigger this check. It is strongly recommended that you perform this check immediately after invoking either `wait()` or `refresh_window()`, as the flag is volatile and may change from iteration to iteration.


### speed_hack_detected
Attempts to determine if speed-hacking technology is being used.

```nvgt
const atomic_flag speed_hack_detected;
```

#### Remarks
This check is performed by the engine every time `wait()` and `refresh_window()` is called and this flag is set whenever the engine can determine that speed-hacking technology is being used. Speed-hacking typically works by hooking low-level operating system timer and time measurement routines to alter the duration of a tick. For the purposes of this description, a tick is an operating system-defined duration which determines how quickly a monotonically increasing timer routine's internal value changes every time that value is requested by the engine. It is strongly recommended that you perform this check immediately after invoking either `wait()` or `refresh_window()`, as the flag is volatile and may change from iteration to iteration.

##### Warning
This check is an extention to, and NOT a substitute for, existing speed-hacking detection technology employed by the engine and by any technology you incorporate into your own game. It MUST NOT be solely relied upon to determine if speed-hacking technology is being used. Although the engine does attempt to be as comprehensive as possible without impacting performance to an unreasonable degree, any reasonably advanced adversary will be able to bypass this check.



