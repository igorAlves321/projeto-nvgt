# Pseudorandom Generation
## Classes
### random_interface
Defines the class structure that is available in NVGT's object based pseudorandom number generators. A class specifically called random_interface does not exist in the engine, but instead this reference describes methods available in multiple classes that do exist (see remarks).
1. random_interface();
2. random_interface(uint seed);
#### Arguments (2):
* uint seed: The number used as the seed/starting point for the RNG, passing the same seed will yield the same sequence of random numbers.
#### Remarks:
NVGT contains several different pseudorandom number generators which can all be instantiated as many times as the programmer needs.

These generators all share pretty much exactly the same methods by signature and are interacted with in the same way, and so it will be documented only once here. Small topics explaining the differences for each actual generator are documented below this interface.

These classes all wrap a public domain single header library called [rnd.h](https://github.com/mattiasgustavsson/libs/blob/main/rnd.h) by mattiasgustavsson on Github. The explanations for each generator as well as the following more general explanation about all of them were copied verbatim from the comments in that header, as they are able to describe the generators best and already contain links to more details.

The library includes four different generators: PCG, WELL, GameRand and XorShift. They all have different characteristics, and you might want to use them for different things. GameRand is very fast, but does not give a great distribution or period length. XorShift is the only one returning a 64-bit value. WELL is an improvement of the often used Mersenne Twister, and has quite a large internal state. PCG is small, fast and has a small state. If you don't have any specific reason, you may default to using PCG.


#### Methods
##### next

Return the next random number from the generator.

uint next();

###### Returns:

uint or uint64 depending on generator: The next random number (can be any supported by the integer type used).

###### Example:

```NVGT
void main() {
	random_pcg r;
	alert("info", r.next());
}
```



##### nextf

Return the next random floating point number from the generator.

float nextf();

###### Returns:

float: The next random float (between 0.0 and 1.0).

###### Example:

```NVGT
void main() {
	random_gamerand r;
	alert("info", r.nextf());
}
```



##### range

Return the next random number from the generator with in a minimum and maximum range.

int range(int min, int max);

###### Arguments:

* int min: The minimum number that could be generated (inclusive).

* int max: The maximum number that could be generated (inclusive).

###### Returns:

int: A random number within the given range.

###### Remarks:

This function always works using 32 bit integers regardless of the generator used.

###### Example:

```NVGT
void main() {
	random_xorshift r;
	alert("info", r.range(1, 10));
}
```



##### seed

Seed the random number generator with a new starting point value.

void seed(uint new_seed = random_seed());

arguments:

* uint new_seed = random_seed(): The seed to use (may be uint64 depending on generator, if so will default to random_seed64).

###### Remarks:

All pseudorandom number generators typically need to start from one tiny bit of real-world randomness or obscure value to properly get going.

By default, nvgt's random number generators are seeded by reading 4 random bytes from the operating system using it's provided API to do so. If you call this seed() function with no arguments, the rng will be re-seeded with a new random seed.

However, particularly when dealing with game recordings or online play, it can be useful to take control of the random number generator and cause it to replay values. This can be done by setting the seed of an RNG to a predetermined and reused value. This is because the rng is guaranteed to return the same set of numbers for a given seed, as the seed serves as the starting point for the RNG.

A common method for example may be to fetch the value of the ticks() or random_seed() function yourself, store the result in a variable, and use that variable to seed an rng. If you want someone else on the network to generate the same numbers for your online game, you need only to transmit that same stored ticks() or random_seed() value over the wire and have the receiver also seed the rng to that value. Now both clients are using the same seed, and from that point they will generate random numbers that are the same, so long as of course one end of the party doesn't somehow jump the gun and generate a random number that the other end does not, as now the clients would be out of sync. This is exactly why these random_xxx classes were provided, because it may be needed to generate different random numbers on each client while insuring that some special numbers (such as enemy spawns) always remain the same. Just create multiple random_xxx instances and share the seed with one while doing whatever you want with the other.

###### Example:

```NVGT
	void main() {
		uint seed = random_seed();
		random_well r(seed);
		int num = r.range(1, 100);
		alert("example", "the number is " + num);
		r.seed(seed); // Restore our original seed from before generating the number.
		alert("The new number will still be " + num, r.range(1, 100));
		r.seed(); // internally choose a random seed.
		alert("unknown number", r.range(1, 100));
}
```





### random_gamerand
GameRand

Based on the random number generator by Ian C. Bullard:

http://www.redditmirror.cc/cache/websites/mjolnirstudios.com_7yjlc/mjolnirstudios.com/IanBullard/files/79ffbca75a75720f066d491e9ea935a0-10.html

GameRand is a random number generator based off an "Image of the Day" posted by Stephan Schaem. More information here:

http://www.flipcode.com/archives/07-15-2002.shtml


Look at nvgt's random_interface documentation above to learn how to use this class.

### random_pcg
PCG - Permuted Congruential Generator

PCG is a family of simple fast space-efficient statistically good algorithms for random number generation. Unlike many  general-purpose RNGs, they are also hard to predict.

More information can be found here: 

http://www.pcg-random.org/

Look at nvgt's random_interface documentation above to learn how to use this class.

### random_well
WELL - Well Equidistributed Long-period Linear

Random number generation, using the WELL algorithm by F. Panneton, P. L'Ecuyer and M. Matsumoto.

More information in the original paper: 

http://www.iro.umontreal.ca/~panneton/WELLRNG.html

This code is originally based on WELL512 C/C++ code written by Chris Lomont (published in Game Programming Gems 7) and placed in the public domain. 

http://lomont.org/Math/Papers/2008/Lomont_PRNG_2008.pdf


Look at nvgt's random_interface documentation above to learn how to use this class.

### random_xorshift
XorShift 

A random number generator of the type LFSR (linear feedback shift registers). This specific implementation uses the XorShift+ variation, and returns 64-bit random numbers.

More information can be found here: 

https://en.wikipedia.org/wiki/Xorshift


Look at nvgt's random_interface documentation above to learn how to use this class.


## Functions
### random

Generates a pseudorandom number given a range.

int random(int min, int max);

#### Arguments:

* int min: the minimum possible number to generate.

* int max: the maximum possible number to generate.

#### Returns:

int: a random number in the given range.

#### Remarks:

Note that this function is a pseudorandom number generator. To learn more, click [here](https://en.wikipedia.org/wiki/Pseudorandom_number_generator).

#### Example:

```NVGT
void main() {
	alert("Example", random(1, 100));
}
```



### random_bool

Generates a true or false value pseudorandomly.

bool random_bool(int percent = 50);

#### Arguments:

* int percent = 50: the likelihood (as a percent from 0-100) of generating a true value. Defaults to 50.

#### Returns:

bool: either true or false.

#### Remarks;

Note that this function is a pseudorandom number generator. To learn more, click [here](https://en.wikipedia.org/wiki/Pseudorandom_number_generator).

#### Example:

```NVGT
void main() {
	alert("Example", random_bool() ? "true" : "false");
}
```



### random_character

Generates a random ascii character.

string random_character(const string&in min_ascii, const string&in max_ascii);

#### Arguments:

* const string&in min_ascii: the minimum possible ascii character to be generated.

* const string&in max_ascii: the maximum possible ascii character.

#### Returns:

string: a random ascii character in the given range.

#### Remarks:

If you pass a string with more than one byte in it to either of the arguments in this function, only the first byte is used.

Note that this function uses a pseudorandom number generator. To learn more, click [here](https://en.wikipedia.org/wiki/Pseudorandom_number_generator).

#### Example:

```NVGT
void main() {
	alert("Your random alphabetical character is", random_character("a", "z"));
}
```



### random_seed

Returns 4 or 8 random bytes from the operating system usually used for seeding random number generators.

1. uint random_seed();

2. uint64 random_seed64();

#### Returns (1):

uint: A 4 byte random number.

#### Returns (2):

uint64: An 8 byte random number.

#### Remarks:

A more detailed description on seeding random number generators is in the documentation for the random_interface::seed function.

To retrieve the random bytes in the first place, this function uses cryptographic APIs on windows and /dev/urandom on unix.

#### Example:

```NVGT
void main() {
	uint seed = random_seed();
	alert("32 bit seed", seed);
	uint64 seed64 = random_seed64();
	alert("64 bit seed", seed64);
}
```





