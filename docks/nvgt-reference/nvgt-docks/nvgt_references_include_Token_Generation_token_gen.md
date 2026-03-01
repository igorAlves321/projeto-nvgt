# Token Generation (token_gen.nvgt)
## Token generation include
Allows you to easily generate random strings of characters of any length in a given mode, and possibly custom function if you want to generate only certain characters.


## Enums
### token_gen_flag
This enum holds various constants that can be passed to the mode parameter of the generate_token function in order to control what characters appear in results.

* TOKEN_CHARACTERS = 1: Allows for characters, a-zA-Z
* TOKEN_NUMBERS = 2: Allows for numbers, 0-9
* TOKEN_SYMBOLS = 4: Uses only symbols, \`\~\!\@\#\$\%\^\&\*\(\)\_\+\=\-\[\]\{\}\/\.\,\;\:\|\?\>\<

#### Remarks:
These are flags that should be combined together using the bitwise OR operator. To generate a token containing characters, numbers and symbols, for example, you would pass `TOKEN_CHARACTERS | TOKEN_NUMBERS | TOKEN_SYMBOLS` to the mode argument of generate_token. The default flags are `TOKEN_CHARACTERS | TOKEN_NUMBERS`.



## Functions
### generate_token

Generates a random string of characters (a token).

string generate_token(int token_length, int mode = TOKEN_CHARACTERS | TOKEN_NUMBERS)

#### Arguments:

* int token_length: the length of the token to generate.

* int mode = TOKEN_CHARACTERS | TOKEN_NUMBERS: allows you to specify which characters you would like in the generated token (see remarks).

#### returns:

String: a random token depending on the modes.

#### Remarks:

This function uses the `generate_custom_token` function to generate. The characters used to generate the token will depend on the modes you specified. See `token_gen_flags` enum constants for a list of supported modes that can be passed to the mode parameter.

#### Example:

```NVGT
#include "token_gen.nvgt"
void main() {
	alert("Info", "Your token is: " + generate_token(10));
	alert("Info", "Numbers only token is: " + generate_token(10, TOKEN_NUMBERS));
	alert("Info", "Characters only token is: " + generate_token(10, TOKEN_CHARACTERS));
}
```



### generate_custom_token

Generates a random string of characters (a token) while optionally allowing you to directly specify the characters you wish to use in the generation.

1. string generate_custom_token(int token_length, string[] values);

2. string generate_custom_token(int token_length, string characters);

#### Arguments (1):

* int token_length: the length of the token to generate.

* string[] values: an array of possible choices (a list of characters or even words) to generate from.

#### Arguments (2):

* int token_length: the length of the token to generate.

* string characters: a list of characters to generate.

#### returns:

String: a random token.

#### Remarks:

If the `values` array or `characters` string is empty or `token_length` is set to 0 or less, an empty string is returned.

#### Example:

```NVGT
#include "token_gen.nvgt"
void main() {
	alert("Info", "Your A to C token is: " + generate_custom_token(10, {"a", "b", "c"}));
	alert("Info", "A to C with capitals included token is: " + generate_custom_token(10, {"a", "b", "c", "A", "B", "C"}));
}
```





