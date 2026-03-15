# Introduction to the Nonvisual Gaming Toolkit
Thank you for downloading the Nonvisual Gaming Toolkit (NVGT) by Sam Tupy Productions and contributors. We hope you find the time that you invest in this engine to be worthwhile!

The NVGT documentation contains:
* The NVGT user manual; containing everything from programming resources to general tutorials to example games,
* API references; Class/function references that specify exactly how to use each feature of the engine,
* Advanced topics; Documentation on the c++ side of the NVGT engine including how to build the engine from source, modify it's security functions, write documentation for the engine and more,
* Appendix; data tables that don't fit in the API references, miscellaneous topics, attributions and license agreements.

## Documentation status
It should be noted that this engine was only released to the public on May 31st 2024, and that the documentation is not yet complete as a result. Though the engine had been in development for years previously, the decision to open source it, and thus to write documentation for it, only took place a couple of months before the initial release. The choice was made to release the engine in an unpolished state specifically so that the community can help improve it, otherwise the engine would have remained private for years while only a couple of people worked in their spair time to complete the documentation. The engine is very usable and a growing community exists on Discord for any questions you might have, certainly we welcome all users! However those involved with the engine's development are also not personally advertising the engine yet due to it's unpolished state. Contributions to the documentation and other materials are therefore very appreciated, though you may want to hold off if you are the type looking for a particularly polished and pretty looking product at this time. Whether you decide to try the engine now or wait until the documentation is complete, we hope you enjoy your time engaging with NVGT and thank you for trying it!

## offline documentation
The latest version of this documentation can be downloaded for offline viewing in several formats using the following links.
* [nvgt.chm (compressed html help file)](https://nvgt.dev/docs/nvgt.chm)
* [nvgt-html.zip (rendered html)](https://nvgt.dev/docs/nvgt-html.zip)
* [nvgt-markdown.zip (github flavored markdown)](https://nvgt.dev/docs/nvgt-markdown.zip)
* [nvgt.txt (plain text)](https://nvgt.dev/docs/nvgt.txt)


# NVGT User Manual
## Getting Started
Welcome to the Nonvisual Gaming Toolkit! This user manual contains all of the information you will need to get up and running using this powerful engine! whether you are new at programming, someone who used to create games using the Blastbay Game Toolkit or an advanced programmer who just wants an easy, no-hassle method of creating games, you're sure to find what you need in this manual to not only get up and running, but to also develop some confidence in it's usage.


## Upgrading From BGT
Since for a while this is where most people who have heard of NVGT will likely start, we will begin by describing the relationship between NVGT and BGT, and more importantly the steps required to upgrade a BGT project to an NVGT one. If you have not heard of BGT or are completely new to game development and are wondering how NVGT can help you, you can probably skip this and move to the fresh start topic.

BGT stands for the Blastbay Gaming Toolkit, and is what initially inspired NVGT to be created after BGT was made into abandonware.

It is important to note that NVGT is not officially endorsed by BGT's developers and contributors, and NVGT is not in any way derived from BGT's source code. The only shared assets between NVGT and BGT are some of BGT's include files such as the audio_form and sound_pool used by many bgt games, which are released under a zlib license.

our goal is to make the transition as seamless as possible from BGT to NVGT, but here are some things you should know when porting an existing BGT game.

### Missing features
NVGT currently has some missing features compared with BGT. These may be added in the future, or have already been replaced with more flexible options.
* Security functions such as `file_encrypt`, `file_decrypt`, `file_hash` do not exist in NVGT. These may or may not be added, but in the meantime you can encrypt/decrypt/hash files manually by using string_aes_encrypt/decrypt/hash_sha256/sha512.

### Differences
#### Functional
Some functions which have the same name as those in BGT work slightly differently.
* `get_last_error`: Currently doesn't trigger in all the situations that BGT does.
* When refering to an array's length, use length as a method call and not as a property. For example, you would use `array.length();` rather than `array.length;`.
* Screen reader functions no longer need to specify the screen reader. If an active screen reader is detected it will automatically speak through there.
* Data encrypted with BGT cannot be decrypted with NVGT, and vice versa.
* The `sound::stream()` method does exist in NVGT, but it's simply an alias to `sound::load()`. For this reason it is recommended that you change all your `stream()` calls to `load()` instead. The `load` function performs an  efficient combination of streaming and preloading by default.
* `load()` contains a second optional argument to pass a pack file. `set_sound_storage()` is no longer used for the moment. However, you can set `sound_pool.pack_file` or even the global `sound_default_pack` property to a pack handle to get a similar effect.
* Take care to check any method calls using the `tts_voice` object as a few methods such as `set_voice` have changed from their BGT counterparts.
* When splitting a string, matching against \r\n is advised as BGT handles this differently. This will result in not having spurious line breaks at the ends of split text.
* The `settings` object no longer writes to the registry, but instead has been replaced by the settings.nvgt include which wraps the previous settings object API, but instead writes to configuration files in various formats.
* The dynamic_menu.bgt include is now called bgt_dynamic_menu.nvgt. This is because NVGT now includes it's own menu class called menu.nvgt.
* There is a type called `var` in the engine now, so you may need to be careful if your project contains any variables named var.
* It's worth noting that unlike BGT, NVGT by default attempts to fully package your game for you including sounds, libraries, documents and any other assets into a .zip file or similar on other platforms intended for distrobution. If you don't like this behavior, you can create a file next to nvgt.exe called config.properties and add the line build.windows_bundle = 0 which will cause NVGT to just produce a standalone executable like BGT did, though you now may need to copy some libraries from the lib folder for the compiled product to run. For more information, see the Compiling your Project for Distribution topic.
* In bgt, you could include pack files with the `#include` directive. In nvgt, we've decided that this should only include code. To embed packs, you can instead add the line `#pragma embed packname.dat` to your project, the extension can be any of your choosing for both code and packs this way.
* Unlike BGT, you can embed multiple packs into an exe. For BGT compatibility, therefore, opening a pack file called `*` will open the first available pack, but it is recommended that you specify a filename such as `*mypack.dat`.
* The `generate_profile` function returns a string which you can write into a file if desired.
* Encrypting/decrypting sounds is done with the `asset_encryptor`/`asset_decryptor` datastreams, rather than with `file_encrypt`/`file_decrypt` functions. You can play encrypted sounds by setting the `sound_default_decryption_key` property.

#### Nominal
The names of many functions have changed in NVGT. Some have even been moved into the objects they are linked to.

Below is a list starting with the BGT function and the NVGT equivalent:
* clipboard_copy_text: clipboard_set_text
* clipboard_read_text: clipboard_get_text
* generate_computer_id: generate_system_fingerprint
* is_game_window_active: is_window_active
* show_game_window: show_window
* screen_reader_is_running: screen_reader_detect (see function in API reference for differing usage)
* screen_reader_speak_interrupt: screen_reader_speak
* screen_reader_stop_speech: screen_reader_silence
* absolute: abs
* arc_cosine: acos
* arc_sine: asin
* arc_tangent: atan
* ceiling: ceil
* cosine: cos
* power: pow
* sine: sin
* square_root: sqrt
* tangent: tan
* serialize: dictionary.serialize
* string_compress: string_deflate
* string_contains: string.find
* string_decompress: string_inflate
* string_decrypt: string_aes_decrypt
* string_encrypt: string_aes_encrypt
* string_hash: separated into two functions (string_hash_sha256, string_hash_sha512)
* string_is_alphanumeric: string.is_alphanumeric
* string_is_digits: string.is_digits
* string_is_lower_case: string.is_lower
* string_is_upper_case: string.is_upper
* string_len: string.length
* string_replace: string.replace
* string_reverse: string.reverse_bytes
* string_split: string.split
* string_to_lower_case: string.lower
* string_to_number: parse_float/parse_double
* string_to_upper_case: string.upper
* The five substring functions string_left, string_mid, string_right, string_trim_left, string_trim_right, have been replaced with just two methods: string.substr and string.slice.

The following key constants are also different:
* KEY_PRIOR: KEY_PAGEUP
* KEY_NEXT: KEY_PAGEDOWN
* KEY_LCONTROL: KEY_LCTRL
* KEY_RCONTROL: KEY_RCTRL
* KEY_LWIN: KEY_LGUI
* KEY_RWIN: KEY_RGUI
* KEY_LMENU: KEY_LALT
* KEY_RMENU: KEY_RALT
* KEY_LBRACKET: KEY_LEFTBRACKET
* KEY_RBRACKET: KEY_RIGHTBRACKET
* KEY_NUMPADENTER: KEY_NUMPAD_ENTER
* KEY_DASH: KEY_MINUS

#### BGT compatibility helper
You can `#include "bgt_compat.nvgt"`, which implements a lot of aliases to BGT-compatible functions and classes. However when doing this, please be aware of the following limitations:
* Using built-in functions may improve performance so this is more or less a stop-gap to get you up and running quickly; however if you wish for your code to just run, bgt_compat will certainly be of use.
* Please note you will not be able to use this script if you have disabled global variables.
* Since the screen reader internal functions no longer require you to specify a screen reader, the reader parameter is ignored.
* The hardware_only parameter of generate_computer_id is ignored.


## Fresh start
This is the starting point for anyone who is interested in game development and who has found this engine, but who does not have much experience with programming concepts or the history of older game engines that are similar to this one.



## Effective Programming and Game Development with NVGT
Please note that this tutorial is still incomplete and though you should read it as a beginner to gain new information, you should be ware that it will cut off abruptly as the author has not come forward to complete what they started at this time.

### What is Game Development?
If you are an experienced programmer looking to get skilled up with NVGT as fast as possible, you can safely skip this section.

To someone who has never programmed before, the development of games might seem like an insurmountable task. This manual hopes to help with the steep learning curve of programming, and to get you ready to make the games of your dreams all on your own.

There are many things that need to be considered carefully in the development of a game. One of the most curious is programming; very quickly, programming stops aligning with real-world concepts. The precise instructions and rigid syntactic rules are often the bane of a new programmer's existence.

As you learn, you will begin to "speak" programming more intuitively. You will eventually realize that programming languages are nothing more than a readable abstraction over common paradigms: variables, functions, conditions, loops, data structures, and many more. Start thinking of programming as a new way to think and construct new ideas, rather than a way of expressing already-imagined thoughts and ideas.

And if you don't understand these paradigms yet, don't worry - reading this manual, my hope is that you will learn to make games with nvgt, but I have a secondary goal: by the end of this text, I hope that you will also be confident with programming in general, as well!

Especially in the world of audiogames, whose developers are often small teams at most, skill in game design is correlated with skill in programming; this manual will attempt to teach you both. However, game designing itself can also be made into a career!

When making games, you must first consider what your game will be: what are the rules of the game? What is the lore, if it has a story? Plan out your project in detail, so that it's easier to turn it into code later on. This is especially true of projects that have a plot, or at least backstory.

As well as coding and designing the game, sounds must also be found or created; many high-quality resources can be found for this, be they free or paid.

It is also the case that a released game is not necessarily a finished one: multiplayer games need administration to keep them running, and games might need to be maintained or updated to fix bugs that you did not encounter until post-launch.
### Your First NVGT Script
A script can also be considered one "unit" of code. You have probably seen many of these before: .py, .js, .vbs, perhaps .bgt, and now .nvgt. A script can be executed, meaning that the code contained within will be run by nvgt.

Usually, one game will consist of not just one, but many scripts, each of which has some specific function or purpose. For now, though, a single script will be sufficient for our needs.

A common tradition among programmers is to write a program that outputs "hello, world!" to the screen, to make sure whichever language they're using is working properly.

Let's do that now and say hello to NVGT!
Open a file in your text editor of choice (I recommend notepad++) and paste the following code inside:
```
void main(){
    alert("hello", "Hello, world!");
}
```
Now, save this file as hello.nvgt, and head over to it in your file explorer.

Press enter on it, and you should see a dialog box appear, with our message inside!

Congratulations - you've just written your first nvgt script!

This script might look simple, but there's actually quite a bit going on here. Let's analyze our various lines:

void main(){ - this is the beginning of a function (more on those later) which doesn't return anything, and takes no arguments, or parameters.

The { afterwards opens a code block. It's customary in many codebases to put the { on the line which opens the block, and to put the closing brace on a new blank line after the block ends.

Inside our block, we have one line: alert("hello", "Hello, world!");

Let's break it down:

alert() is a function in nvgt that opens a dialog box containing a message. It supports many arguments, but most are optional. Here, we have used the two that are not: title, and text.

We've separated our parameters by a comma and a space, similar to what we do when listing items in English, although we don't need to use "and" like we do in English, and there is only one rule to remember: a comma after every item, except the last.

Our parameters are enclosed in parentheses () but why? This tells NVGT what we'd like to do with the alert function: we would like to call it (calling meaning running the code inside based on some values). Finally, we end the line with a semicolon ; that tells NVGT this piece of code is finished.

Together, alert("hello", "Hello, world!"); is known as one statement, the smallest unit of code that can be executed.
As you can see, functions aren't so daunting after all!

However, there's one missing piece of this puzzle: what's the deal with the main() function?

Actually, it's arbitrary, although extremely common. Many programming languages (rust, c, c++, java, and NVGT, to name a few) require you to use the main() function as what's called the "entry point": in other words, NVGT will call the main function, just as we called the alert function. If it doesn't find the main function, it won't know where to start, and will simply give you an error stating as much.

It's very possible to write scripts without a main function. These are sometimes called modules, and sometimes called include scripts, helper scripts, or any number of other names. In NVGT, since a module is quite a different (and advanced) concept, we call them include scripts.

There's something interesting which nvgt can do with this script: not only can you run it, but you can also pack it into an exe file, ready to be shared with whoever you wish to have it. The advantage is that the exe will obfuscate your code and protect it from bad actors, which is especially useful for multiplayer projects!

Not just that, but anyone can run your game if you compile it, whether or not they have nvgt installed on their computers.

It's easy to do: when you've selected your script in windows explorer, don't run it. Instead, press the applications key (alternatively shift+f10 if you don't have one of those) and a "compile script (release)" option should appear.

Click it, and a new file should appear next to the script: hello.exe.

Running this file, you should get a similar effect to just running the script, but the code is now protected and can no longer be accessed.

Now that we've learned the basics of nvgt scripts, let's move on and create a simple program!
### Learning Project: Calculator

Let's make a calculator program with nvgt. We should be able to type mathematical expressions into it, and then get results out. We'll then build on our program by adding more features, and hopefully learn lots along the way!

You'll encounter many new programming concepts at once, so don't feel discouraged if you are lost. All will be explained!

In this chapter, we'll learn about many of the fundamental concepts of nvgt, and of programming as well! I will try to make this interesting, but learning the basics can admittedly be boring. It is not shameful if you need a coffee or two reading through this.

And once we've learned the basics, we'll create several versions of our project, each one better than the last!

I will first explain the nvgt and programming concepts we'll need to understand it, using some short examples. They are called snippets, and won't all actually run. They are just to demonstrate.
#### comments
Sometimes, you might want to document what a particularly complex bit of code does, or perhaps remind yourself to make it better later.

For these reasons and more, programming languages usually have some way of keeping some notes in your code that they will not attempt to execute.

These are usually called comments, and nvgt has three types of them:

The single-line comment is written with a //, and looks like this:
```
// Hello!
```
The multi-line comment is written slightly differently, enclosed by a /* and a */. It looks like this.
```
/*
Hello!
This is a multiline comment
Lorem ipsum
Dolor sit amet
*/
```
Lastly, the end-of-line comment is sort of like a single-line comment, but goes after a line of code. For example:
```
int drink_price=5; // should this be able to store fractional values?
```

As well as documenting your code, comments (especially multi-line ones) can be used to surround code which temporarily doesn't need to be run, or is broken for some reason.

This is called "commenting out" code. Code which is commented out will be ignored by the compiler, just like regular textual comments.

Example:
```
void main(){
//alert("hello", "hello, world!")
alert("how are you", "My name is NVGT!");
}
```
If you run this, you will only see the "how are you" dialog box, and not our "hello" one. You see, I made a little error when I was writing that line - can you spot why we might have commented it out?

#### include scripts
The truth about programming, as with anything, is that organization is the most important thing. Always remember this: reading code is more difficult than writing it.

As a programmer, your highest-priority task is to get the code working. But arguably just as important is to keep it working.

Imagine you are a version of yourself, with similar programming experience. However, you have never read your project's code before. If you can intuitively understand what all of its components do, then you have succeeded in writing readable code!

Another thing experienced programmers like to have is modularity. This philosophy dictates that as little of your code as possible should depend on other code.

I'll explain more about this later, but an include script is how one achieves modularity in nvgt: by using the #include directive at the top of your program, you can load in another file of code, adding its code to your own in doing so.

NVGT ships with a host of include scripts (or includes for short), which you are free to use to speed up the process of game development.

For example, the speech.nvgt include has functions for making your game speak out text, without needing to worry about what screen reader or sapi voice the user has.

If you wanted to use the speech.nvgt include, you would put it at the very top of your script, like this:
```
#include "speech.nvgt"
```

Why the #? In nvgt, # signifies what's called a preprocessor directive: usually one line of code, these are used before your program is run to change something about it.

NVGT has what's called an include path. It searches multiple folders for your include scripts, and if it can't find them, it will give you an error. It works a bit like this:
1. Search the directory of the script from which another script was included
2. Search the include folder in nvgt, in which all the built-in includes are stored.
[add more later here maybe]

Here is a full code example, which you can copy into an nvgt script and run.
```
#include "speech.nvgt"
void main(){
    speak("Hello from the NVGT speech include!");
}
```

#### variables
If you know about variables in algebra, then you will have a similar concept in your head to those in programming. They are, at their core, names of data.

Quite a few things in nvgt are variables: functions, normal variables, classes and many more.

In this section we will learn about how to make some simple variables, and how to change them.
##### integers (ints) and unsigned integers (uints)
In NVGT, there are two main types of numbers, integers and floating-point numbers.

The easiest to understand is an integer, otherwise known as a discrete number. We'll learn about those first, then move on to floats, the type we will make the most use of in our calculator project.

Here are some examples of declaring the two kinds of integers:
```
int x = 3;
x = -3;
uint y = 3;
y=-3; // Oh no!
```
As you can see, we used both kinds of integers. One is called an int, as we'd expect, but the other is called a uint. What does the u mean? You might have already guessed!

We'll talk about that in a second. And if you don't want to learn about binary now, it's enough to know that unsigned ints sacrifice the ability to store negative values for double+1 the positive number range.

First, let's break down our int declaration statement

`int` is the type of variable (int)

`x` and `y` are the "identifier" of a variable. In other words, its name.

`=` is the assignment operator. The first time you assign a value to a variable, it is called initialization.

After the =, a value is assigned to the variable. Then, the ; is used to end our statement, making it complete and ending the line.

You'll notice that only the first reference of a variable needs its type; this is because this is the declaration of the variable, whereas the second line is a reassignment of the same variable and does not need to be re-declared.

You can also declare what are called global variables. I'll give a full example to demonstrate this.
```
int unread_emails = 20;
void main(){
    alert("important", "You have " +unread_emails + " unread emails!");
}
```
As you can see, despite the fact that the global variable was not declared within the function (or its scope), we can still use it. This is because it's not declared in any function, and can thus be used from all functions in your program.

This author personally does not recommend much usage of globals. A more elegant way to use variables in lots of different functions at once will be demonstrated shortly. The exception is consts, which will also be discussed later.

To create the message, I used the string concatenation operator to glue one string, one variable, and another string together. This will be further explained in the section on Strings.

As we know, inside a function (but not outside) variables can be changed, or re-assigned. You might have realized that changing a variable's value in relation to itself (like giving the player some money or points) is a handy side effect, since you can simply reference a variable when re-assigning it, like this:
```
int level = 2;
level = level + 1;
```
But there is a simpler, more readable way of doing this, which saves lots of time (and cuts down on typos!). 

If you want to change a variable in relation to itself like this, you use what's called compound assignment.

This combines an operator, like an arithmetic operation or string concatenation, with the assignment operator.

For example, we could rewrite our previous code using compound assignment:
```
int level = 2;
level +=1;
```
As you can see, it's much cleaner!

Here's a full example to consolidate what we've learned. You can copy and paste it into an nvgt script and run it. We'll also demonstrate includes and comments again!
```
#include "speech.nvgt"
int g = 3; // a global variable
void main(){
    /*
    This program demonstrates integers in NVGT, by declaring one (a) and performing a variety of arithmetic operations.
    After each operation, the value of a will be spoken.
    */
    int a = 0; // This is the variable we'll use. 
    speak("a is now " + a);
    a+=2;
    speak("After adding 2, a is now " + a);
    a*=6;
    speak("After multiplying by 6, a is now " + a);
    a /=3;
    speak("After dividing by 3, a is now " + a);
    //something new!
    a -= g;
    speak("After subtracting g, a is now " + a);
}
```

##### bonus: binary 1100101 (or 101)
To understand signed and unsigned integers (and to understand integers) we must first understand binary. Otherwise known as base 2, it is a system based on 0s and 1s. It's most well known for appearing on terminals in poorly written movies about hackers, but it is integral to understand it as a programmer, so let's talk about it.

The unsigned integer version of binary is actually easier to explain, so we'll start with that one.

Consider a row of bits. In base 2, we can already surmise that the maximum possible value is 2^bits-1. NVGT's ints are 32-bit, although it does also support int64 and uint64 types if you want them.

The unsigned integer (uint) type in nvgt, thus, can store a maximum value of 4.294 billion. This is a huge number, and is suitable for most, if not all, requirements. The unsigned 64-bit integer type can store a value of up to 18.446 quintillion, which is more than two billion times the world population and more than a thousand times the amount of money in circulation in the entire economy, in US cents.

The first bit on the left is worth 2 raised to the n-1th power, where n is the number of bits.

If the bit is set to 0, it means no value is added to the total in base 10. If it's set to 1, you add its worth.

From left to right, each bit is worth half the bit before it. Let's give examples with 8 bits, since that's much easier to think about than 32 bits.

Consider this set of bits: 01100101

The leftmost bit in this group would be worth 128, since that's the value of 2^(8-1).

But it's set to 0, so we don't do anything

Right another bit, and we get a bit of worth 64, set to 1. So, we add 64.

Next, another 1 bit, with a value of 32, which we add, giving us 96.

Next, two 0 bits, each worth 16 and 8. We will ignore them.

Another 1 bit, worth 4. Let's add it, for a total of 100.

Then, a 0 bit, worth 2, and another 1 bit, worth 1. Adding the last 1 bit, we have our final total, 101.

This is all you need to know about unsigned binary representation.

##### float variables

The main difference between ints and floats is that floats can store fractional values, whereas ints are restricted to exclusively whole numbers. Although they do come with some drawbacks, this makes floats more suitable for tasks where a high level of precision is needed. They are also useful for dealing with imprecise, but extremely large, numbers.

There are two main types of floats in nvgt: float and double.

Float is a 32-bit (or single-precision) variable, and double is a 64-bit variant which can store a greater number of decimal digits and higher exponents.

In most cases, you should be okay to use a double, but this is not always required and is often not a good choice anyway.

The inner workings of floats are beyond the scope of this tutorial, but it's enough to know that computers don't think about fractional values like we do: the concept of decimal does not exist to them.

Instead, they use a binary representation, called the IEEE754 standard.

You cannot rely on floats storing a number perfectly. Sometimes, the IEEE754 standard has no exact representation for a number, and its closest equivalent must be used instead.

To demonstrate this, run this script. The result should be 1.21, but it isn't.
```
#include "speech.nvgt"
void main(){
    double result = 1.1 * 1.1;
    screen_reader_speak(result, false); // implicit cast from double to string
}
```
As you  can see, the value is very close, but not quite right. We even used the double type, with 64 bits of precision, but it wasn't enough.

There are several ways to get around this, but we don't need to worry about them for this project, so let's learn about another very useful type of variable: strings!

##### string variables
The easiest and most reliable way to think about string variables is that they are text. "hello" is a string, "this is a test" is a string, and "1" is a string (this last one is confusing but will be explained shortly).

We have actually seen string variables before. When we were making our hello world program, we used two of them for the title and text parameter to the alert function.

Now knowing about variables and their identifiers, you can probably see why we used quotes (") around them, and why that is necessary.

If we hadn't, "hello, world!" would've ended up being interpreted as two function parameters, the variable identifiers hello and world, neither of which existed in the program.

NVGT would not have liked this at all; in fact, it would've thrown numerous errors our  way in response.

So, quotes must enclose strings to let NVGT know that it should ignore the text inside - the computer doesn't need to know that it's text, only that it's data like text, which it can then show to the user for them to interpret.

It's almost, if not quite,  like delivering letters: you don't know or care about the information in a letter (and if you did, then your manager probably needs to talk to you!) but the letter's recipient does.

In the same way, NVGT will happily place text in quotes in strings, which can then be passed to functions, put into variables, or concatenated onto other variables or strings.

In this case, it was assigning them to the title and text variables, arguments of the alert function.

String variables are created using a similar syntax to the int variable we just saw:
```
string name = "Rory";
```
You can also create a string with multiple words:
```
string message = "How are you today?";
```
Or even a string with non-ascii characters:
```
string message2 = "Hello, and 你好 👋";
```
Just like integer variables, strings also have operations which can be performed on them. By far, the most common is concatenation.

Concatenation is the process of stringing strings together. The + symbol is used for this, and compound assignment with += is also supported.

Let's see how it works:
```
string sentence = "The quick brown fox";
sentence += " jumps over the lazy dog";
```
To give you some familiarity with string concatenation, let's go over a full example. Copy this into an NVGT script, and run it:
```
#include "speech.nvgt"
void main(){
    int a = 1;
    int b = 2;
    string c = "1";
    int d = 2;
    string result1 = a + b;
    string result2 = c + d;
    speak("a + b is " + result1);
    speak("c + d is " + result2);
}
```
The output should be:

a + b is 3

c + d is 12

Is that what you expected?

What's happening here is called casting, specifically implicit or automatic casting. In programming, casting means converting some value of one type (int) to another type (string).

When we calculate result1, we perform addition on a + b (1 + 2) and get 3, which makes sense.

But when we calculate result2, NVGT automatically converts d, an int, into a string, making it "2", so it can be concatenated.

It then ignores the data inside, and just adds it together. So, instead of having 1 + 2, you get "1" + "2" - which is just two pieces of data combined together into one string, making "12".

This is why strings are so useful: they can hold any data in a text-like form, and then the meaning of that data can be interpreted by something else. In this case, it is output to our screen readers, and we can interpret it; the sound waves by themselves do not hold any semantic information.

##### boolean variables (bool)
Leading up to a powerful idea called conditionals, boolean variables are another fundamental datatype in programming, and are usually present in some form in programming languages.

Named in honour of the mathematician and logician George Boole, the variables can store only two possible values: true or false - or 1 or 0, on or off, yes or no.

They are extremely powerful and there are quite a few things you can do with them, but most of them don't really make sense without conditionals. Still, we can give a basic example, using not (!), a logical operator:
```
void main(){
    bool state = true;
    speak("State is: " + state);
    state = !state;
    speak("Flipped, state is: " + state);
}
```
This shows how to declare a bool: it's fairly similar to other variables. Unlike strings, the values true or false do not need to be put in quotes, despite the fact that they are not variables in the traditional sense. These variables are actually consts, which means you can never accidentally overwrite their values; trying will yield an error.

That's all we'll learn about variables for now. We'll come back to them later on, but for our calculator project, this is all that we'll need to know.

##### Const Keyword
For this project, the last thing we will explore regarding variables is consts.

Const variables (or constants) are variables which can never change after they are first assigned. This must be done when they are initialized.

They are particularly useful in avoiding "magic numbers": using numbers directly in our code is bad!

Let's write some code to demonstrate:
```
#include "speech.nvgt"
void main(){
    speak("Welcome to the camping store! You need to have 30 dollars to buy a folding chair.");
}
```

This looks fine, but we're using this value in only one area of our code (mostly because there is only one place in which to use it, but that's beside the point).

Suppose, now, that we use the value 30 in many areas: not just telling the user how much it is to buy a chair, but also for the logic of buying and selling them itself.

This is also valid in that it works, but it is frowned upon.

Consider this: inflation is making everything more expensive these days, so what if we need to raise this price to 35 dollars next year?

The answer to that question is that it would be a coding nightmare! We would have to go through our code, painstakingly changing every reference of the value 30 to 35. But we could get it wrong: we might accidentally make one of the values 53, or change the number of centimeters in a foot from 30 to 35 in our frantic search - wouldn't it be much better if we only had to change the value once?

This is where consts will save the day!

Using them , we could rewrite our code like this:
```
#include "speech.nvgt"
const int price_folding_chair = 30;
void main(){
    speak("Welcome to the camping store! You need to have " + price_folding_chair + " dollars to buy a folding chair.");
}
```
Much better! Now we can use this value wherever we want to, and all we have to do to change it is update the one declaration at the top of the file!

#### conditionals and the if statement
The if statement is perhaps one of the most overwhelmingly useful pieces of code. Its ubiquity is almost unparalleled and a variation of it can be found in just about every programming language in use today.

Say you want to run some code, but only if a specific thing is true - the if statement is what you use. Let's give a full example:
```
#include "speech.nvgt"
void main(){
    int dice = random(1, 6);
    if(dice == 1)
        speak("Wow, you got " + dice + "! That's super lucky!");
    else if(dice < 4 )
        speak("You got " + dice + " - that's still pretty lucky, but aim for a 1 next time!");
    else
        speak("Ah, better luck next time. You got a " + dice + ".");
}
```
This small dice game is very simple. Roll a dice, and see how low a number you can get.

There are three options: you get a 1 (the luckiest roll), 2 or 3 (the 2nd luckiest), or 4-6 (which means you lose).

We can express these three options using the "if", "else if", and optional "else" constructions. They work like this:

if(conditional)

statement/block

else if(conditional)

statement/block

else if(conditional)

statement/block

else

statement/block

These are slightly different than normal statements, because they do not always have the ; where you would expect, at the end: if multiple lines are to be run (a block, surrounded by braces) then you use the ; on the last line of the block, before the }.

But what is a conditional?
A condition is any value that returns either true or false. This can be something which is already a bool variable, or the result of a comparison operator.
There are six comparison operators in nvgt, each of which takes two values and returns true or false based on their relationship.
| Operator | Purpose                                              | Opposite |
|----------|------------------------------------------------------|----------|
| ==       | Checks if two values are exactly equal               | !=       |
| !=       | Checks if two values are not exactly equal           | ==       |
| <=       | Checks if a value is less than or equal to another   | >        |
| >=       | Checks if a value is greater than or equal to another| <        |
| >        | Checks if a value is greater than another            | <=       |
| <        | Checks if a value is less than another               | >=       |

There are also four logical operators which work on bools, one of which we explored in the section on booleans. They are:
* && (and) returns true if the bools on the left and right are both true, but not neither or just one
* || (or) returns true if either or both of the bools on the left or right are true
* ^^ (xor) returns true only if one of the left and right bools is true, but not neither or both
* ! (not) returns the opposite of the bool on the right (it takes only one bool and nothing on the left)

Using these comparison operators and logical operators is how one creates conditionals to use in if statements, though remember that bools themselves can already be used directly.

This is all a lot of information at once, so here's a full example to demonstrate:
```
#include "speech.nvgt"
void main(){
    int your_level = 5;
    int monster_level=10;
    int your_xp=50;
    bool alive=true;
    if(alive)
        speak("You are alive!");
    if(monster_level<=your_level){
        speak("You manage to kill the monster!");
    }
    else{
        speak("The monster is higher level than you, so it kills you!");
        alive=false;
    }
    if(!alive)
        speak("You are no longer alive!");
    if(your_level*10==your_xp)
        speak("Your level is equal to a tenth of your experience points.");
}   
```
This example demonstrates an important distinction we touched upon earlier: if statements which use a block instead of a single statement need to have the block surrounded by braces.

Where a block might be used, a single statement can usually be used as well; the exception is functions, which must always use a block, whether or not it is a single line.

#### loops
While the if statement is used to create conditional checks for whether certain pieces of code will be run, loops are used to repeat sections of code more than once.

Loops have many uses, including infinite loops (which are already a well-known concept), loops that run a known number of times, and loops that we use to run through certain data structures like arrays.

For advanced programmers, NVGT does not support iterators; the traditional c-style for loop must be used to iterate through arrays, although this is substantially more convenient because one can query their length.

NVGT has three main types  of loop, which we will discuss in this section: while loops, while-do loops, and for loops. We will also discuss the break and continue statements.

##### While Loops
The most simple form of loop is the while loop. It is written almost exactly the same as the if statement, and runs exactly the same, except that it will check the condition and run the code over and over, checking before each run, until the condition is determined to be false.

Here is an example which you can run:
```
#include "speech.nvgt"
void main(){
    int counter = 1;
    while(counter <6){
        speak(counter);
        wait(1000);
        counter+=1;
    }
}
```
This should speak out the numbers 1 through 5, with a second's delay between each.

Just like if statements (as well as other types of loops), a while loop can also be written with only one line of code inside. If so, it does not need to be surrounded by braces.

The while loop is the standard way to write an infinite loop: a piece of code that will run forever, perhaps until broken out of with the break keyword.

To make an infinite loop, we simply use
```
true
```
as the condition, since it will logically always return true, every time.

##### Do-While Loops
In while loops, the condition is checked before the code is run. This means that, just like an if statement, there is always the possibility that the code may never run at all.

On the other hand, in do-while loops, the condition is checked after the code has run. As a result, code will always run at least one time.

It's often up to the programmer which type they think is best, and there is no real standard. Whichever is more convenient and maps best to the situation can be used, and neither has a performance advantage over the other.

Let's rewrite our counter example using a do-while loop:
```
#include "speech.nvgt"
void main(){
    int counter = 1;
    do{
        speak(counter);
        wait(1000);
        counter+=1;
    } while(counter < 6);
}
```
As you can see, since the condition is at the end, we need to check it based on the value after the counter as updated, instead of before.

If we had used
```
while(counter < 5);
```
as we had done with our while loop, the code would have only counted to 4, since the counter gets updated after it speaks its current value.

##### For Loops
One of the most-used types of loop is something similar to our counter example from earlier in this chapter.

There are a lot of lines here which for loops can compress into just one line; they make code easier to write as well as read later on.

For loops also have an additional unique property, which is extremely useful, but will be discussed in a moment after some background.

However, they are  admittedly difficult to grasp at first, because they're very different than both the while and do-while loops.

Consisting of four parts, a for loop might look like this:
```
for(declarations; condition; final)
statement/block
```

How it works:

1. The declarations code is run, and a variable (or more) is declared.
2. The loop starts to run.
3. At the beginning of each loop iteration, the condition is checked. If false, the loop stops, potentially even before it has run once.
4. Assuming the condition is true, The code inside the for loop is run.
5. After that code has finished, the final step is run.
6. Repeat steps 3-5

Note: all three parts of a for-loop are optional. For instance, you may omit the declaration by simply writing nothing before the first ;

As you can imagine, a for loop would help us rewrite our counter example in a much more readable way.

Let's go ahead and do this now:
```
void main(){
    for(uint i = 1; i < 6; i ++){
        screen_reader_speak(i, false);
        wait(1000);
    }
}
```

This example will yield the same results as the previous one, but it does it in a way which is more concise. Pretty code is very important for your sanity!

##### Break And Continue Statements
There are times when you might want to get out of loops completely. This is called "breaking out", and it's very easy to do:

```
break;
```
There are no additional components to this statement, as there are in some other languages such as rust.

This is particularly useful in infinite loops (typically created by simply using true as the condition in a while loop)

When this is done, the loop immediately ends, and will iterate no longer.

If you want to break out of a loop, but still want it to try and run again (IE. not run the rest of this iteration), the continue statement can help.

As is the break statement, the continue statement is simply written on a line by itself:
```
continue;
```
This immediately ends the current iteration. For while and do-while loops, nothing more happens, and the final component in a for loop is run. Then, the next iteration may begin.

The reason that for loops behave differently is by design. It is not possible to achieve this behaviour in any other way.

#### functions
Functions in nvgt are pieces of code that can be "called" or executed by other parts of the code. They take parameters (or arguments) as input, and output a value, called the "return value".

The return value is so named because it gives some critical piece of information back to the calling function, without which work cannot continue.

Let's use baking a cake as an example: in the process of baking a cake (simplifying greatly) you put the batter in the oven. The oven cooks the cake, and then you open it up and take a cooked cake out.

You can't do something else related to baking a cake while the oven is baking, because you don't have the cake: the oven does. In the same vein, only one function can be running at once, and we say that function is currently executing.

When a function ends, execution returns to the function from which it was called, just like taking the cake back out of the oven. It returns, along with execution, whatever is specified using a return statement (discussed shortly).

Here is a snippet for the purpose of example:
```
int add(int a, int b){
    return a + b;
}
```
Frankly, this code is a needless abstraction over an already-simple task (the addition operator) and you should almost never do it like this in production. Nonetheless, it's a good example of what a function can do. It takes data in, and then outputs some other data.

The way we declare functions is a little bit strange, and this example is packed with new ideas, so let's break it down piece by piece:

int add(

The beginning of the function's declaration, letting the compiler know that it is a function with the return datatype (int), the name (add) and the left parenthesis

int

the type of the first variable

a, 

the name (identifier) of the first parameter/argument variable, and a comma and space to separate it from the next variable, just as we use when calling functions

int b)

The declaration of the second parameter/argument variable, another integer, and a right parenthesis to tell the compiler there are no more parameter variables

{

The beginning of our function (remember, there must always be braces enclosing functions, even if the execution step is only one line in length.)

Then, the next line:

    return a + b;

This is the only line in our function, and returns an expression evaluating to an int variable. It adds the a and b variables' values together.

}

The end of our function, which lets the compiler know that we're back in the outer scope (probably global)

##### Bonus: Some notes About References (Advanced)

If you are new, you can skip this brief section for now, as it's discussed in another article in great depth for easier understanding.

There are a couple of  common misconceptions and mistakes made by even experienced coders when it comes to function parameters.

For performance, it may seem intuitive to declare your primitive functions as const x &in references, but this is almost always useless, except in the case of strings.

The reason for this is the fundamental property of a reference: a pointer itself is a value of 8 bytes storing a memory address. As opposed to most primitives (ints etc), there is no advantage, as the new bytes still need to be allocated - it is just a different value that is placed into them (the address instead of a copy of the value).

#### Arrays (Lists)
If you have programmed prior to reading this manual, you may have seen them before: an array is angelscript's equivalent to a vector or a list.

Via this powerful data structure, we can store lots of the same type of variable in one neat package.

In NVGT, arrays are dynamic. This means that you can add and remove from them at any time you'd like, as opposed to arrays in c or rust, which are trickier to expand or remove from.

Before we move on, here is a quick example:
```
void main(){
    int[] scores = {20, 30};
    scores.insert_last(50);
    screen_reader_speak("The scores of the players in this game are:", false);
    for(uint i = 0; i < scores.length(); i ++)
        screen_reader_speak(scores[i], false);
}
```

The variables in an array are called "items" or "elements", and you can imagine them as being stored in a line (ordered).

As a consequence, we can access the 1st, 2nd, or any other item in our line of elements, via "indexing".

Slightly more complicated to think about, however, is that arrays in NVGT use "0-based indexing".

This is true of most programming languages, with a notable exception being lua.

0-based indexing means that, instead of the 1st item being at index 1, it is at index 0. Item 2 would be at index 1, item 3 at 2, and item 20 at 19.

### To be Continued
Unfortunately, this game development tutorial is not yet complete, you should stop reading at this point if you are a beginner.
* classes (methods and properties)
* datastreams and files


## Toolkit Configuration
One highly useful aspect of NVGT is it's ever growing list of ways that an end user can configure the engine. Whether trying to add an extra include directory, tweak an Angelscript configuration property, choose how warnings and errors are printed, deciding whether to print output on successful compilation or any number of other changes, NVGT provides various options and directives that should help you to get it functioning much closer to the way you desire.

From `#pragma` directives to command line argument syntax to configuration files, this document attempts to keep track of all such available configuration options NVGT has to offer.

### Command line arguments
NVGT's compiler program has a variety of command line arguments you can pass to it which can alter it's behavior. Some of these options can also be set in configuration files, however an explicit command line option is very likely to override any contradictory options that are in a configuration file.

Generally, these command line options are self-documenting. If you open a command prompt or terminal and just run the nvgt application directly with no arguments, you will be informed that you should either provide an input file or run `nvgt --help` for usage instructions. You can also actually just run nvgt -h

In almost all cases, command line arguments have 2 methods of invocation, both a short form and a long form. The short form of a command usually consists of just a letter or two and is easier to type, while the long form of a command is always more descriptive and thus might be suited to an automation script where you want anyone reading such a script to be able to understand exactly what they are asking NVGT to do. What form you wish to use is completely up to you. In either case you should put a space between arguments, and mixing short and long form arguments is completely fine.

The short form of an argument always begins with a single hyphen character (-) followed by one or 2 letters. For example, `-C` would tell NVGT to compile your script with debug information. Some arguments take values, in which case the value shall follow directly after the argument when using short form invocations. For example you could set the platform to compile with using the `-pwindows` argument.

On the other hand, the long form of an argument begins with two hyphens followed by what usually amounts to a few words separated by hyphens. Usually it's just one or 2 words, but could be more in rare cases. For example, `--compile-debug` would tell NVGT to compile the given script with debug information. If an option takes an argument, you use an equals (=) character to define such a value. For example `--platform=windows` would tell NVGT to compile a script for the windows platform.

Finally, a special argument, two hyphens without any following text, indicates that any further arguments should be passed onto the nvgt script that is about to run.

#### Argument list
The following is a list of all available command line arguments, though note that it is best to directly run `nvgt --help` yourself encase this list is in any way out of date as nvgt's --help argument will always be more accurate because the text it prints is dynamically generated.
* -c, --compile: compile script in release mode
* -C, --compile-debug: compile script in debug mode
* -pplatform, --platform=platform: select target platform to compile for (auto|android|windows|linux|mac)
* -q, --quiet: do not output anything upon successful compilation
* -Q, --QUIET: do not output anything (work in progress), error status must be determined by process exit code (intended for automation)
* -d, --debug: run with the Angelscript debugger
* -wlevel, --warnings=level: select how script warnings should be handled (0 ignore (default), 1 print, 2 treat as error)
* -iscript, --include=script: include an additional script similar to the #include directive
* -Idirectory, --include-directory=directory: add an additional directory to the search path for included scripts
* -V, --version: print version information and exit
* -h, --help: display available command line options

### Configuration files
Both because command line arguments can become exhausting to type for every script execution, and because NVGT contains far too many configuration options to make command line arguments out of, NVGT also supports configuration files which can be used either on a global or a project level to further direct NVGT.

Configuration files can either be in ini, json or properties formats and are loaded from multiple locations. Values in these configuration files are usually separated into sections in some form. Settings controlling the user interface typically go in the application subsection, while directives that provide control over Angelscript's engine properties are in a subsection called scripting. The way these directives in various subsections are defined depends on the configuration format you choose, however you can use any combination of configuration formats at once to suit your needs. Though all supported configuration formats are more or less standard, you can find examples of and notes on each format below.

Configuration files at any given location have a priority attached to them to resolve directive conflicts. For instance, if a global configuration file and a project configuration file both contain the same option, the project file takes priority.

#### Loaded configuration files
The following configuration files are loaded listed in order of priority from highest to lowest:
* Script-dependent project configuration: script_basename.ini, script_basename.json or script_basename.properties in the same directory as the nvgt script about to be run, where script_basename is the name of the nvgt script without an extension (mygame.nvgt = mygame.properties)
* Script independent project configuration: .nvgtrc (ini format) in the same directory containing the nvgt script that is getting executed or in any parent
* Compiler dependent global configuration: exe_basename.ini, exe_basename.json and exe_basename.properties in NVGT's installed directory or any parent, where exe_basename is the name of nvgt's running executable without the extension (for example nvgt.json or nvgtw.ini)
* Compiler independent global configuration: config.ini, config.json and config.properties in NVGT's installed directory.

#### Supported configuration formats
NVGT supports 3 widely standard configuration formats, all of which have their own advantages and disadvantages. It is perfectly acceptable to create multiple configuration files with the same name but with different extension, all keys from all files will load and be combined. If the files nvgt.json and nvgt.ini both exist and both set the same key to a different value, however, the result is a bit less defined as to what key is actually used and typically depends on what file was internally loaded first by the engine.

It is entirely up to you what formats you want to use in your projects.

##### json
```
{"application": {
	"quiet": true
}, "scripting": {
	"compiler_warnings": 1,
	"allow_multiline_strings": true
}}
```
Likely the most widely used and most modern, NVGT can load configuration options from standard JSON formatted input.

This format receives the most points for standardization. Included directly within many higher level programming languages as preinstalled packages or modules, this is the easiest format to use if you need some code to generate or modify some configuration options used in your program. For example, a python script that prepares your game for distribution might write a gamename.json file next to your gamename.nvgt script that modifies some Angelscript engine options or changes debug settings before release, and sets them to other values during development.

Furthermore if NVGT ever includes an interface to set some of these options in a manner where they save, .json files would be the format written out by the engine.

The disadvantage to JSON though is that even though it is the most modern and widely recognised of nvgt's options, it's relatively the least human friendly of the formats. For example if a configuration option takes a path on the filesystem and one wants to manually set this option in NVGT, they would need to escape either the slash or backslash characters in the path if they go with the JSON option. Furthermore NVGT contains many boolean options that are just enabled by being present, where an option key has no needed value. While JSON of course supports setting a value to an empty string, it is certainly extra characters to type in order to just quickly tweak an NVGT option.

##### ini
```
[application]
quiet

[scripting]
	compiler_warnings = 1
	allow_multiline_strings
```
NVGT can also load configuration data from good old ini formatted text files.

This format is probably the least standardized of the ones NVGT supports, likely due to it's origin from closed source windows. While on the surface it is a very simple format, there are a few deviations that exist in various parsers as the syntax is not as set in stone as other formats. For example whether subsections can be nested, whether strings should be quoted, whether escaping characters is supported or whether a value is required with a key name are all up to an individual ini parser rather than a mandated standard. In this case, the ini parser that handles these configuration files does not require that a value be provided with a key name for simple boolean options, escaping characters is not supported and strings do not need to be quoted.

The biggest advantage to this format as it pertains to NVGT is the simplicity of setting several options in the same section without constantly redeclaring the sections name. One can just declare that they are setting options in the scripting section and can then begin setting various engine properties without typing the name "scripting" over and over again for each option.

The biggest disadvantage to this format is the inability to escape characters. For example, typing \n in a configuration string would insert the text verbatim instead of a newline character as might be expected.

##### properties
```
application.quiet
scripting.compiler_warnings=1
scripting.allow_multiline_strings
```
Finally, NVGT is able to load configuration options from java style .properties files.

The biggest advantage to this format is it's easy simplicity. The format just consists of a linear list of key=value pairs, though the =value is not required for simple boolean options that just need to be present to exist. Unlike ini, it also supports character escaping, causing \n to turn into a line feed character.

The only real disadvantage to this format over ini is the need to keep constantly redeclaring the parent section names whenever defining keys, for example you need to type scripting.this, scripting.that where as with ini and JSON you can specify that you are working within a section called scripting before adding keys called this and that.

#### Available configuration options
Many options listed here do not require a value, simply defining them is enough to make them have an effect. Cases where a value is required are clearly noted.

The available options have been split into sections for easier browsing. While the method for defining options changes somewhat based on configuration format, a line in a .properties file that contains one of these options might look like application.quiet or scripting.allow_multiline_strings, for example.

##### application
This section contains options that typically control some aspect of the user interface, as well as a few other miscellaneous options that don't really fit anywhere else.

* as_debug: enables the angelscript debugger (same as -d argument)
* compilation_message_template = string: allows the user to change the formatting of errors and warnings (see remarks at the bottom of this article)
* GUI: attempts to print information using message boxes instead of stdout/stderr
* quiet: no output is printed upon successful compilation (same as -q argument)
* QUIET: attempts to print as little to stdout and stderr as possible (though this option is still a work in progress)

##### build
This section contains options that are directly related to the compiling/bundling of an NVGT game into it's final package. It contains everything from options that help NVGT find extra build tools for certain platforms to those that define the name and version of your product.

* android_home string defaults to %ANDROID_HOME%: path to the root directory of the Android sdk
* android_install = integer default 1: should Android apks be installed onto connected devices if signing was successful, 0 no, 1 ask, 2 always
* android_jaava_home string defaults to %JAVA_HOME%: path to the root of a java installation
* android_manifest string defaults to prepackaged: path to a custom AndroidManifest.xml file that should be packaged with an APK file instead of the builtin template
* android_path string defaults to %PATH%: where to look for android development tools
* android_signature_cert = string: path to a .keystore file used to sign an Android apk bundle
* android_signature_password = string: password used to access the given signing keystore (see remarks at the bottom of this article)
* linux_bundle = integer default 2: 0 no bundle, 1 folder, 2 .zip, 3 both folder and .zip
* mac_bundle = integer default 2: 0 no bundle, 1 .app, 2 .dmg/.zip, 3 both .app and .dmg/.zip
* no_success_message: specifically hides the compilation success message if defined
* output_basename = string default set from input filename: the output file or directory name of the final compiled package without an extension
* precommand = string: a custom system command that will be executed before the build begins if no platform specific command is set
* `precommand_<platform>` = string: allows the execution of custom prebuild commands on a per-platform basis
* `precommand_<platform>_<debug or release>` = string: allows the execution of custom prebuild commands on a per-platform basis  with the condition of only exicuting on debug or release builds
* postcommand = string: a custom system command that will be executed after the build completes but before the success message
* `postcommand_<platform>` = string: allows the execution of custom postbuild commands on a per-platform basis
* `postcommand_<platform>_<debug or release>` = string: allows the execution of custom postbuild commands on a per-platform basis with the condition of only exicuting on debug or release builds
* product_identifier=string default com.NVGTUser.InputBasenameSlug: the reverse domain bundle identifier for your application (highly recommended to customize for mobile platforms, see compiling for distribution tutorial)
* product_identifier_domain = string defaults to com.NVGTUser: everything accept the final chunk of a reverse domain identifier (used only if build.product_identifier is default)
* product_name=string defaults to input file basename: human friendly display name of your application
* product_version = string default 1.0: human friendly version string to display to users in bundles
* product_version_code = integer default (UnixEpoch / 60): an increasing 32 bit integer that programatically denotes the version of your application (default is usually ok)
* product_version_semantic = string default 1.0.0: a numeric version string in the form major.minor.patch used by some platforms
* shared_library_excludes = string default "plist TrueAudioNext GPUUtilities systemd_notify sqlite git2 curl": Partial names of shared libraries that should not be copied from NVGT's source lib directory into the bundled product.
* shared_library_recopy: If this is set, any shared libraries will be copied from scratch instead of only if they're newer than already copied.
* windows_bundle = integer default 2: 0 no bundle, 1 folder, 2 .zip, 3 both folder and .zip
* windows_console: when compiling for windows, build with the console subsystem instead of GUI

##### scripting
This section contains options that directly effect the Angelscript engine, almost always by tweaking a property with the SetEngineProperty function that Angelscript provides.

The result is undefined if any value is provided outside suggested ranges.

For more information on these properties, the [Angelscript custom options documentation](https://www.angelcode.com/angelscript/sdk/docs/manual/doc_adv_custom_options.html) is a great resource. There are some engine properties shown on that page which NVGT does not support the configuration of, as a result of such properties being used internally by the engine to function properly.

* allow_multiline_strings: allow string literals to span multiple lines
* allow_unicode_identifiers: allow variable names and other identifiers to contain unicode characters
* allow_implicit_handle_types: experimentally treat all class instance declarations as though being declared with a handle (classtype@)
* alter_syntax_named_args = integer default 2: control the syntax for passing named arguments to functions (0 only colon, 1 warn if using equals, 2 colon and equals)
* always_impl_default_construct: create default constructors for all script classes even if none are defined for one
* compiler_warnings = integer default 0: control how Angelscript warnings should be treated same as -w argument (0 discard, 1 print and continue, 2 treat as error)
* do_not_optimize_bytecode: disable bytecode optimizations (for debugging)
* disallow_empty_list_elements: disallow empty items in list initializers such as {1,2,,3,4}
* disallow_global_vars: disable global variable support completely
* disallow_value_assign_for_ref_type: disable value assignment operators on reference types
* disable_integer_division: Defer to floatingpoint division internally even when only integer variables are involved
* expand_default_array_to_template: cause compilation messages which would otherwise contain something like string\[\] to instead contain array\<string\>
* heredoc_trim_mode = integer default 1: decide when to trim whitespace of heredoc strings (0 never, 1 if multiple lines, 2 always)
* ignore_duplicate_shared_interface: allow shared interfaced with the same name to be declared multiple times
* init_call_stack_size =  integer default 10: the size of the call stack in function calls to initially allocate for each script context
* init_stack_size =  integer default 4096: the initial stack size in bytes for each script context
* max_nested_calls = integer default 10000: specify the number of nested calls before a stack overflow exception is raised and execution is aborted
* max_stack_size = integer default 0 (unlimited): the maximum stack size in bytes for each script context
* max_call_stack_size = integer default 0: similar to max_nested_calls but can possibly include calls to system functions (angelscript docs is unclear)
* private_prop_as_protected: private properties of a parent class can be accessed from that class's children
* property_accessor_mode = integer default 3: control the support of virtual property accessors (0 disabled, 1 only for c++ registrations, 2 no property keyword required, 3 property keyword required)
* require_enum_scope: access to enum values requires prepending the enum name as in enumname::enumval instead of just enumval
* use_character_literals: cause single quoted one-character string literals to return an integer with that character's codepoint value

### `#pragma` directives
In a few cases, it is also possible to configure some aspects of NVGT's behavior directly from within nvgt scripts themselves using the `#pragma` preprocessor directive.

This directive is used to safely tell the engine about anything that doesn't directly have to do with your script code but also without causing some sort of compilation error due to bad syntax. A pragma directive could do anything, from embedding a file to selecting assets to choosing  to adding include directories and more.

The syntax for a pragma directive looks like `#pragma name value` or sometimes just `#pragma name` if the option does not require a value. In some cases when a value is to contain a long or complex enough string such as a path, you may need to surround the value in quotes such as `#pragma name "value."`

#### Available directives
* `#pragma include <directory>`: search for includes in the given directory (directive can be repeated)
* `#pragma stub <stubname>`: select what stub to compile using (see remarks at the bottom of this article)
* `#pragma embed <packname>`: embed the given pack into the compiled executable file itself
* `#pragma asset <pathname>`: copy the given asset/assets into the bundled product as resources
* `#pragma document <pathname>`: copy the given asset/assets into the bundled product as documents intended for the user to access rather than the programmer
* `#pragma plugin <plugname>`: load and activate a plugin given it's dll basename
* `#pragma compiled_basename <basename>`: the output filename of the compiled executable without the extension
* `#pragma bytecode_compression <level from 0 to 9>`: controls the compression level for bytecode saved in the compiled executable (0 disabled 9 maximum)
* `#pragma console`: produce the compiled executable on windows using the console subsystem for CLI based programs

### Remarks on complex options
This section contains any explanations of topics that were too bulky to fit in the documentation of each specific configuration option or article section.

#### application.compilation_message_template
This useful option allows you to control the format that errors and warnings are printed in. The default template looks like this, for example:

`file: %s\r\nline: %u (%u)\r\n%s: %s\r\n`

Most specifically, the format string is passed to the function Poco::format in the c++ codebase, and that function receives 5 dynamic arguments. string file, uint line, uint column, string message_type, string message_content.

It is not needed to understand how this c++ string formatting function works to customize the message template however, you can just reorder the arguments and add text to the following example template:

`%[1]u %[2]u %[0]s; %[3]s: %[4]s`

This example moves the line number and column to the beginning of the string, before printing the filename, the message type and the content all on a single line. NVGT automatically adds one new line between each engine message printed regardless of the template.

#### platform and stub selection
One possible area of confusion might be how the platform and stub directives fit together. In short, the stub option lets you choose various features or qualities included in your target executable while platform determines what major platform (mac, windows) you are compiling for.

Though explaining how NVGT's compilation process works is a bit beyond the scope of this article, the gist is that Angelscript bytecode is attached to an already compiled c++ program which is used to produce the final executable. There are several versions of the c++ program (we call that the stub) available with more that could appear at any time. For example a stub called upx will produce an executable that has already been compressed with the UPX executable packer, while a stub available on windows called nc will insure that the Angelscript compiler is not included in your target application. In the future we hope to include several more stubs such as one focusing much more on performance over file size, one focusing on minimal dependencies to insure no third party code attributions are needed, etc.

Internally, you can see this at play by looking in the stub directory of NVGT's installation. You can see several files with the format `nvgt_<platform>_<stubname>.bin`, or sometimes just `nvgt_<platform>.bin` which is the default stub for a given platform. Such files are used to create the final game executable produced by NVGT's compiler, and are selected exactly using the configuration pragmas and options described. If platform is set to windows and stub is set to nc, the file nvgt_windows_nc.bin is used to produce the compiled executable of your game. The only exception is if the platform is set to auto (the default), which will cause your executable to be compiled for the host platform you are compiling on.

#### bundle naming and versioning
NVGT includes several directives particularly in the build configuration section that allow you to control how your product is identified to end users and to the systems the app is running on. While some are purely for display, others are manditory in certain situations especially when you plan to distribute your app on networks like the app store, google play and similar. For more info on these directives, you should read the "configuring bundling facility" section of the compiling for distribution topic.

### Conclusion
Hopefully this tutorial has given you a good idea of how you can get NVGT to perform closer to how you would like in various areas from the user interface to the syntax handling. If you have any ideas as to configuration options you'd like to see added, please don't hesitate to reach out on github either with a discussion or pull request!


## Compiling your project for distribution
Once your game is ready to be distributed to others, you may want to turn it into a compiled binary executable, or perhaps even a complete bundle. The compilation procedure assembles all the individual nvgt files of your source code into a single file that can run natively on its targeted operating system without having Nvgt available to interpret it, and the bundling facility can then take that binary along with your sounds/assets, documentation, shared libraries/plugins as well as any other material your game requires and compress/bundle all of that into a complete package ready for you to directly share with the world.

### Here are some thoughts about reasons to do this:
* Doing this can let you make your work more of a closed-source affair which limits the ease at which someone can reverse engineer your work and hack in changes if that is something you don't want to happen, which is probably the case if your game isn't a free one for sure.
* The end user will just be able to run the executable file natively, no need to have Nvgt installed. Just like a regular program they download anywhere else!
* Fewer files, especially if you have a lot of scripts included. That all can turn into just one file, except for the libraries, which can clean up the directory considerably.
* Stability. No need to worry about whether someone's going to be trying to run your code on an older or newer version of Nvgt with script-breaking changes.

### Some thoughts about reasons not to do this:
* Your project is open for all to hack and slash at, with the code readily available.
* You want people to be able to review your work for what ever reason. Since the code is right there, they can read it if they know how and determine what the code does if they so choose.
* You're creating tutorials or test scripts for others to learn by or to provide examples for how to do something or get feedback, such as trying to find a bug or teaching others how to do something in Nvgt. Hey, that's kinda the same thing as item 2!

### What is an executable file?
This will be sometimes called a binary. It's a file that is a complete program directly compatible with the operating system for which it is intended. It can be launched directly, and is usually bundled along side sounds, shared libraries and other data required to run your game.

### What is a bundle?
A bundle, unlike a plain executable binary, is instead a full game package which contains everything your game needs to run including any sounds, shared libraries, and the aforementioned executable file. It might be a .zip that the user extracts, a .dmg on MacOS, a .apk file for android and similar for other supported platforms.

### What about all the different operating systems?
Since Nvgt is intended to be able to run on Windows, Linux, Mac OS and mobile platforms like Android and IOS, there will be different executables for each targeted operating system. On windows, the resulting binary will have a .exe extension like other programs you may have seen. On other platforms though, there is no standard file extension for executable files and on Android, you never see the executable directly but instead only the final .APK file as there is no reasonable way to run NVGT applications on mobile without fully bundling them first.

e.g. if you disable the bundling facility and then compile my_game.nvgt on Windows you'll get a my_game.exe but if you compile on linux, you'll just get a file called my_game. Keep this in mind when trying to compile on a non-windows platform. If you have a file called my_game.nvgt and next to it is a directory called my_game, the compilation process will fail because my_game already exists and is a directory!

When compiling on a non-windows platform, the executable permission bitt on the resulting file is automatically set for you.

### How to compile:
* on Windows, navigate to the main script file of your code (the one with the void main () function in it). For example it might be called my_game.nvgt
	* Right click the .nvgt file (you can use the context key or shift+f10) and expand the "Compile Script" sub menu. Each platform you'll see there has 2 options:
		* Choose "platform (debug)" if you will want extra debugging information to be included in the program. This can be handy if you're working on it still and want to gain all information about any crashes that may happen that you can get.
		* Choose "platform (release)" if you don't want the extra debug information. You probably should always use release for anything you don't want others to be able to hack and slash at, since the debug information could make it easier on them.
	* If you've disabled the bundling facility, ensure that the necessary library files are located in the same directory your new exe is, or within a lib folder there.
	* If you would rather, you can also run the nvgtw.exe program itself and use the buttons there to compile for any given platform.
* On Linux, cd to the path containing a .nvgt script.
	* Now run /path/to/nvgt -c scriptname.nvgt where scriptname.nvgt should of course be replaced with the name of your script file. You can select a platform with the -p argument E. -pwindows.
* On Mac OS, it's best to just click on the NVGT application directly.
	* After launching NVGT you can select compile a script in release/debug mode, choose a platform, and browse to your script file.
	* If, however, you wish to build on MacOS using the command line, cd to the directory containing a .nvgt script and run the command /applications/nvgt.app/Contents/MacOS/nvgt -c scriptname.nvgt, or alternatively open -a nvgt --args -c \`pwd\`/scriptname.nvgt

You will receive a popup or STDOut print letting you know how long the compilation took. You should find a new file in the same folder you just compiled that has the same name it does but with a different extension e.g. when compiling my_game.nvgt you'll have my_game.exe. Distribute this along with the necessary libraries in what ever form is required. You can set it all up with an installer, such as Inno Setup, or if your game will be portable you can just zip it up, etc.

### Configuring the bundling facility:
NVGT tries to provide a one-click bundling facility, that is, clicking the compile option on an NVGT script will directly create a package that you can distribute to your end users with little hastle. You don't need to go searching for libraries, you don't need too learn how app bundles on MacOS or Android APK files work, you can just build your game into a distribution ready package.

While this is a very powerful system that does work out of the box, it likely needs input from you if it is to produce the most optimal results. The facility needs to know where your assets are, it is best if it knows what version your game is / a good display name string for the app (used on various platforms), and various other options allow for anything from custom app manifest files to custom system commands that you can cause to be executed before or after a successful compile.

Other than including assets like sounds, most inputs to the bundling facility are provided via configuration options. Usually a file called .nvgtrc containing configuration directives is created along side a project, though it can also be called gamename.properties, gamename.json or gamename.ini where gamename is the name of your main nvgt script without the extension. You can learn more about the configuration subsystem specifically in the toolkit configuration tutorial, which includes a list of every available bundling option.

All of the bundling related options are in the build section of the configuration. So if you want to disable the bundling facility entirely on windows for your project, for example, you might add the line build.windows_bundle = 0 to your .nvgtrc file which would cause a standalone executable to be created when the game is compiled rather than a full bundle. If the bundling facility is not for you at all, you can disable it globally by creating a file alongside the nvgt.exe application itself called config.properties with the same key, more details and alternate configuration filenames are also described in the configuration tutorial.

Many of the directives here allow you to control how your product is identified to end users and to the systems the app is running on. While some are purely for display, others are manditory in certain situations especially when you plan to distribute your app on networks like the app store, google play and similar.

If you plan to release your game on MacOS, IOS, or Android, it is highly recommended that you create what's known as a reverse domain identifier for your app by setting the build.product_identifier property. It's called the reverse domain identifier because the format is like a website in reverse, such as com.samtupy.nvgt. In mild cases it might be used to group similar apps together E. the operating system or distribution service can implicitly tell that apps with an identifier starting with com.samtupy all belong to the same company, but in extreme cases this identifier might be used by the system as the main way your app is identified, such as on Android for example where the filesystem paths to the apps data folders actually include this identifier. The identifier can contain periods, uppercase / lowercase letters, and numbers, so long as a number is not the first character following a period. There should be at least 2 period delimited segments in this identifier (prefferably at minimum 3), and it might be a good idea to limit the first segment to popular top level domains like com, org, net etc. While in reality a couple of other characters like dashes and underscores might work in identifiers, they may not be as platform agnostic as the rules listed above. It is not important that the reverse website/app identifier you come up with here actually exists on the internet. If you do not provide this value, the default is com.NVGTUser.scriptname where scriptname is the name of the NVGT file passed to the compiler without the extension. It is possible, however, to only customize the com.NVGTUser part if you want NVGT to use the script filename to derive the rest of the identifier for you. So for example if you know that all games you'll be developing on your computer will be from the company com.epicdevelopers, you can set the key build.product_identifier_domain = com.epicdevelopers in nvgt's global config files. Now when you compile mygame.nvgt, the full reverse domain identifier for that app will be set to com.epicdevelopers.mygame.

Unfortunately, different operating systems and services use different versioning schemes. Windows and MacOS really want version numbers in major.minor.patch format, in fact the windows version resource actually contains 4 binary words in it's structure to store each period separated version component. While the parsed format isn't actually embedded into a binary structure on MacOS, it's still manditory as soon as you want to distribute your game in the app store, because that service reads such a property from the bundle to identify the version of the app to track updates. As such, the build.product_version_semantic property must be set for MacOS app store distributions, while on windows it is an optional display feature that will cause version information to show for your compiled executable. On the other hand, Android and the google play store use an integer version code to track when a given version of an APK is newer than any installed version. This simple requirement makes it very easy to manage this property automatically on android, it is done by dividing the unix timestamp in seconds by 60, you can also set the build.product_version_code property if you wish to control this manually. Finally, the build.product_version configuration option allows you to set, where possible, the version string that is actually displayed to end users.

Another configuration option worth mentioning is the build.shared_library_excludes property. This defaults to the string "plist TrueAudioNext GPUUtilities systemd_notify sqlite git2 curl", meaning that by default the shared libraries for plugins are not bundled. As such, you may need to replace this property with your own list of excludes if you use any of NVGT's plugins. We intend to make this step unnecessary, instead determining the list of plugin libraries based on the plugin pragmas contained in the script. So for example if you wanted to include the curl plugin at the moment, you might set the property build.shared_library_excludes = "plist TrueAudioNext GPUUtilities systemd_notify sqlite git2" in your project's configuration file.

To include assets like sounds and documents into your bundle, the asset and document pragmas are used. A pragma is a type of code statement, similar to `#include,` that allows you to feed NVGT various extra information about your game. For example if one wants to bundle the sounds.dat file with their product, they can add the line of code`#pragma asset sounds.dat` to the top level of one of any .nvgt files that make up the project, or `#pragma document changelog.txt` to include a text file intended for the user rather than the game to access.

The asset and document pragmas are very similar, on  most platforms indeed they do the same thing. The distinction is that in some cases it can be useful for NVGT to know whether an included asset is intended for access by the game or by the user. The changelog and readme documents for your game should be included as documents rather than assets, for example, because they are included outside the .app folder within a .dmg bundle on MacOS as opposed to assets which are placed in the MacOS/Content/Resources directory, which may be inconvenient for the user to access. Similar distinction is applied on other platforms when required/possible.

Sometimes you may have a file that you wish to include as an asset, but as a different name in the bundle than that of the file stored on disk. To do this, you can express the asset pragma like `#pragma asset sounds.dat;audio.dat` if you want sounds.dat to actually be called audio.dat in the bundle. The asset and document pragmas will copy/include directories recursively. For example if you have a folder called sounds, the code `#pragma asset sounds` will successfully include the entire sounds folder in your bundle.

### Libraries needed for distribution:
The following information can be helpful if you have disabled NVGT's bundling facility and you wish to package your compiled games yourself.

There are a few libraries (dependencies) that Nvgt code relies on. When running from source, Nvgt is just interpreting your .nvgt scripts and using the libraries found in its own installation folder. Generally, if all is normal that will be:
* On Windows, c:\Nvgt
* On Linux, where you extracted NVGT's tarball to.
* On Mac OS, `/Applications/nvgt.app/Contents`

Within that folder you should have a subfolder that is called "lib" (or "Frameworks" on macOS). Lib contains the redistributable dependencies Nvgt uses for certain functionality. When you run from source, the Nvgt interpreter uses this very folder. However, when you compile, you must provide the files in the same directory as the compiled program so that it can find them. You may copy the entire lib folder to the location of the compiled game, or you can optionally just copy the files directly there if you don't want a lib folder for some reason. In other words, you can have a subdirectory within the program's directory called lib with the files inside, or you can also just place the dlls right in the program's directory where the binary is. On windows, you can omit some of the dll files not needed by your code, and we plan to add more and more support for this on other platforms as time goes on. A list is provided below of the basic purpose and importance of each library so you can hopefully know what to omit if you don't want all of them. These files must be included where ever the program ends up, so installers need to copy those over as well, and they should be included in any zip files for portable programs, etc. Again remember that NVGT usually handles this for you and this step is only required if you wish to create your own bundles by hand.

At time of writing, the files are:
* bass.dll is required for the sound object and the tts_voice object, though will not be later once we switch from bass to the miniaudio library. The moment one of these objects exists in your script, your program will crash if this dll is not present.
* bassmix.dll is just as important as bass.dll and allows things like nvgt's mixer class to exist, where we can combine many bass channels into one. It is always required when bass.dll is used
* bass_fx.dll is used for reverb, filters, etc and is also required whenever bass.dll is used.
* nvdaControllerClient64.dll used to speak and Braille through the NVDA screen reader.
* SAAPI64.dll used to speak and Braille through the System Access screen reader.
* ZDSRAPI.dll used to speak and Braille through the ZDSR screen reader.
* git2.dll is the libgit2 library which allows people to programmatically access git repositories (can be good for adding version control to your online game's map world for example). You don't usually need it.
* git2nvgt.dll is the plugin for nvgt itself that wraps git2. So if your script does not include the line #pragma plugin git2nvgt, then you don't need either of the git2 dlls.
* nvgt_curl.dll is another plugin that wraps the libcurl library. It used to be the only way to do http requests, but it's now being phased out in favor of more portable options. It's only required if your script includes the line #pragma plugin nvgt_curl
* nvgt_sqlite.dll is similarly for interfacing with SQLite and is only needed if #pragma plugin nvgt_sqlite is defined.
* GPUUtilities.dll is used for the GPU acceleration of ray tracing used for geometric reverb in steam audio. It should always be completely optional.
* phonon.dll is steam audio, that's the HRTF and geometric reverb and cool things like that. You should only need it if you create a sound_environment class or set sound_global_hrtf=true in your script, but at time of writing, sound output using normal sound objects wasn't working as expected without this.
* TrueAudioNext.dll is more optional GPU acceleration for steam audio.
* systemd_notify.dll is a plugin wrapping the sd_notify linux function which can be useful if you are writing a systemd service. You probably do not need this otherwise.

These are organized here roughly in order of most critical to least, but it all depends generally on your project. The first few items are required for the game to even run, but the rest are only necessary if you're using them, and the documentation for using those plugins will ideally make that apparent.

### Detecting library availability
Sometimes, you might want to display a friendly error message to your users if a library is unavailable on platforms that allow you to do so rather than the application just crashing. You can do this with a function in NVGT called `bool preglobals()` which executes automatically similar to the main function but before any global variables that might tap into one of these libraries are ever initialized. It can return false to abort the execution of the application. Then, you can use the properties called SOUND_AVAILABLE and SCREEN_READER_AVAILABLE to safely determine if the subsystems could be loaded. The following code snippet would be OK, for example.
```
bool preglobals() {
	if (!SCREEN_READER_AVAILABLE) alert("error", "cannot load screen reader components");
	else if (!SOUND_AVAILABLE) alert("error", "cannot load soundsystem");
	else return true; // success
	return false; // one of the libraries failed to load.
}
```

### Crediting open source libraries
NVGT is an open source project that uses open source dependencies. While aside from bass (which we will replace) we have been very careful to avoid any open source components that forbids or restricts commercial usage in any way, we do not always avoid dependencies that ask for a simple attribution in project documentation such as those under a BSD license. We'd rather focus on creating a good engine which we can fix quickly that can produce some epic games with awesome features, without needing to discard a library that implements some amazing feature just because it's devs simply ask users to do little more than just admit to the fact that they didn't write the library.

To facilitate the proper attribution of such libraries, a file called 3rd_party_code_attributions.html exists in the lib folder. We highly recommend that you distribute this file with your game in order to comply with all attribution requirements which you can read about in the aforementioned document.

The idea is that by simply distributing this attributions document within the lib folder of your app, any user who is very interested in this information can easily find and read it, while any normal game player will not stumble upon random code attributions in any kind of intrusive manner. The attributions document is currently well under 100kb, so it should not bloat your distribution.

The existing file attributes all open source components in NVGT, not just those that require it. If you want to change this, you can regenerate the file by looking in the doc/OSL folder in NVGT's github repository to see how.

For those who really care about not distributing this file, we hope to provide extra stubs in the future which do not include any components that require a binary attribution. However, there is no denying that this goal is very costly to reach and maintain, while yielding absolutely no true reward for all the time spent sans not needing to distribute an html file with game releases which players and even most developers will not be bothered by anyway. As such, it might be a while before this goal comes to fruition, and we could decide at any point that it is not a viable or worthwhile project to attempt if we find that doing so in any way detriments the development of NVGT, such as by making a feature we want to add very difficult due to lack of available public domain libraries for that feature.


## Concurrency Tutorial

### Introduction to multithreading and parallelism in NVGT

Multithreading, often referred to as concurrency, is the process by which a program can divide tasks into separate, independent flows of execution. These tasks, known as threads, can run concurrently within a single process, allowing for more efficient use of resources and faster execution of complex programs. This approach differs from parallelism, where the tasks are executed simultaneously on multiple processors or computers.

Concurrency focuses on the structure and design of the program to handle multiple tasks that can overlap in execution. This is particularly useful in scenarios where tasks can be interleaved and do not need to run at exactly the same time, such as managing user interfaces, I/O operations, or handling multiple client requests in a server.

In contrast, parallelism aims to improve computational speed by executing multiple tasks simultaneously. This can be achieved through multi-core processors, where each core can execute a separate thread, or distributed systems, where tasks are distributed across different machines in a network.

While NVGT does not support parallelism as one might use it in other programming languages, it does support threads, and this article is all about that. The above distinctions are important, however, because they are quite different, and the way one would go about implementing parallelism is vastly different (and more complicated) than how one would implement concurrency. We denote the distinction explicitly here because often these terms are used interchangeably when they do, in fact, mean very different things, although on a single computer they can appear to be very similar. We will not be discussing parallelism any further in this article, however, as concurrency is the more important aspect here.

### Why is this so important?

By far, the easiest way to program is by sticking to synchronous execution, which is what happens by default unless any concurrency is specifically introduced by the programmer. Synchronous execution means that each statement in your code runs to completion before the next is executed. However as your game grows, you may find that it begins to execute slowly, which may temmpt you to quickly implement concurrency into your application.

This however poses a significant issue because NVGT supports three types of concurrency, and not knowing what method to use or when to use it can often result in slower or more buggy code than if either a different method of concurrency had been used, or if concurrency had not been used at all. People most often jump strait to threads to solve a problem of performance, when, 99 percent of the time, the performance degradation comes from an easily solvable issue in the person's code and not NVGT or a true need for threads or the lowest levels of concurrency. It can be not only bad practice but also detrimental to your program's development to use more advanced concurrency methods when a simple loop would have sufficed, but knowing when and how to spin up a thread when synchronous execution just won't cut it can also save the day in such cases. As such, this article attempts to explain:

* What exactly concurrency is;
* How to use concurrency correctly; and
* The golden rules of concurrency.

The above explainers are important because concurrency is easy to use improperly. Users of it who don't understand it are bound to make critical mistakes that can cause any number of things, such as:

* Sequential execution, i.e., absolutely no actual gain and a waste of resources
* Data races
* Deadlocks
* And worse

They'll also notice their code suffering very strange bugs or exhibiting very odd behaviors, all of which is very, very difficult to debug, let alone track down in the first place, especially on larger projects, and it's best that you be aware of these issues before ever considering threads.

### Three types of concurrency?

There are three types of concurrency that NVGT supports: async, coroutines, and threads. We'll discuss all of them in this article.

#### Note

Any plugins you load may add even more methods of concurrency or even parallelism. Though this article will help you use those extra methods correctly, you should always read the documentation of those plugins to get a firm grasp of how their extra methods work.

### Async

Async is the first type of concurrency, and one of the easiest to use. It's also one of the simplest to understand. Although async (may) use a thread (or even multiple) under the hood, it is entirely possible that it may not, and you, as the programmer, needn't care how it works as long as your able to do what needs to be done. In the majority of cases, this is probably the furthest you will ever need concurrency in your game.

Unlike the other two forms of concurrency, the engine insulates you (mostly) from the problems and mistakes of concurrency that you may make. This is particularly true for functions like `url_get` and `url_post` where the engine can complete the request while you do other things, or in any case that involves writing an asyncronous function that does not share any state with the rest of your program. Take, for example, this code:

```nvgt
async<string> result(url_get, "https://nvgt.dev");
```

This class is known as a templated class. Though it is beyond the scope of this article, the `string` part is the most important, besides the arguments of the constructor, which specify both the function to be executed and it's arguments. When you create (or instantiate) a class that's templated, NVGT generates the code for that specific class automatically for you, using the types you specify in the angle brackets. This is done on the fly and doesn't harm performance in any manner.

You may not realize it, but this constructor can take up to 16 parameters. (Woohoo, that's a lot!) When the constructor completes, `result` has some things of interest:

* The `value` property, which is (in this case) of type `string`, and contains the return result of the function invoked. If you change `string` above to, say, `int`, then this will be of type `int`, not `string`.
* A `complete` and `failed` property, which tells you if the task has finished executing, or failed in some manner, respectively.
* An `exception` property which provides you any information that you need if, during the execution of the function, it failed and threw one.
* A `wait()` method which pauses, or blocks, your code from continuing until the function completes or fails.
* a `try_wait` function, returning type `bool`, which takes a timeout and will block until either the timeout( also known as the deadline) expires or the task completes.

As stated previously, this is, for the majority of cases, the only thing you will need to reach for in your toolbox, and it's the highest level of concurrency available. The next two are much lower level, and give you more control, at the cost of raising the steaks by quite a bit. Even then, we strongly recommend reading the sections below about what can go wrong when 2 bits of code running at the same time try accessing the same global variable or bit of memory if you intend to write your own functions that are to be called with this async construct.

### Coroutines

A coroutine is a function that suspends itself at certain points. This suspension is called yielding, and using coroutines is known as cooperative multitasking.

In computer architecture and operating systems, there are generally two types of multitasking approaches. Multitasking, for those who are unsure of the definition (and no, we don't mean multitasking in normal human language), is the concurrent execution or handling of multiple computational processes by a CPU or other processing units within a computer system, such that multiple tasks are performed during overlapping time periods. The key definition is "overlapping time periods." The two types that are generally accepted are known as cooperative multitasking and preemptive multitasking.

Cooperative multitasking is the first type and works by requiring that a task executes until it reaches a point where it can allow another task to run; this is known as a yield point. When the task reaches this point, it makes a call to a function provided by the operating system, runtime environment, or whatever is running each task, telling it that it is ready to step aside and allow something else to run. In NVGT, this is done through the `yield()` function. Cooperative multitasking relies on each task being well-behaved and voluntarily yielding control, ensuring that all tasks get a chance to execute. This approach is simpler and can be more efficient in environments where tasks can be trusted to yield regularly. However, if a task fails to yield, it can cause the entire system to become unresponsive.

Preemptive multitasking, on the other hand, is used in all well-known operating systems. Preemptive multitasking works by allocating a task a certain amount of time to run, known as a time slice, and allowing it to run until that time slice ends. When the time slice has elapsed, the operating system forcefully suspends (or "preempts") the execution of the task and replaces it with another task, and the cycle repeats forever. Usually, time slices are very short (perhaps only a few microseconds) and so this gives the illusion that the computer is able to do many things simultaneously. In multicore and multiprocessor systems, this is actually true: the computer can and does do many things all at the same time since the multitasking can occur on all the processors at the same time. However, all that's really happening is that the system is constantly performing this song and dance on all the processors in your computer, all at the same time!

You may have noticed that we used the word "task" instead of "process" or "thread." This is because, in a computer, there are a few different types of "tasks," and they're all the same to the computer:

* Process: A fully loaded program that runs. It has code, data, assets, etc.
* Thread: A task within a process. It shares the code and data of its parent program and is able to access all the state within. More on this later.

So, how does this have anything to do with coroutines? Well, when you create a coroutine, you are engaging in cooperative multitasking. The coroutine will begin execution as soon as you call `create_coroutine` and will pause the execution of all your other code until you call `yield()`. So, you must remember to yield at some point! The best places to do this are in loops or when your function is about to do something that could take a while, for example, some network-based IO. If you don't, none of your other code can run!

However, the same applies to the rest of your code: it, too, must yield; otherwise, your coroutine will never be able to proceed!

Unlike threading, which involves preemptive multitasking, it is (theoretically) impossible for a coroutine that executes in this manner to cause data races or other concurrency problems. This is because only one flow of execution is allowed at any given moment. You can definitely make it appear that multiple things are happening at once if you yield enough, but you'll never be able to duplicate the kind of problems that threading has, so you usually don't need to worry about those. This does not, however, mean that coroutines are the go-to option for all scenarios.

Coroutines are particularly useful for scenarios where tasks need to perform lengthy operations without blocking the entire program. For instance, they are excellent for handling asynchronous I/O operations, long-running computations that need to provide intermediate results, and any situation where tasks need to cooperate smoothly without complex synchronization mechanisms.

There are some rules to remember when using coroutines, however:

* Ensure that your coroutines yield control back to the caller at appropriate points, particularly in loops or before performing lengthy operations.
* Do not perform blocking operations (like waiting for I/O) within a coroutine without yielding. Instead, yield control and resume the coroutine once the operation completes. The `async<T>` class can help with this: you can store it in a variable your code has access to, and when it completes, you can `yield` to allow one of your coroutines to continue.
* Always clean up resources before yielding or ensure that resources are properly managed upon resumption. This helps prevent resource leaks and ensures that the coroutine does not hold onto resources unnecessarily.
* Design your coroutines to work well with others.
* Thoroughly test your coroutines, particularly their yield and resume behavior. Debugging coroutines can be challenging due to their non-linear execution flow, so use logging and debugging tools to track their state and behavior.

To create a coroutine, call the `create_coroutine` function:

```nvgt
void create_coroutine(coroutine @func, dictionary @args);
```

Your coroutine should take the form:

```nvgt
void coroutine(dictionary@);
```

In both of these, `dictionary@` is a dictionary of arguments that the coroutine needs to execute. When your ready to yield, simply call `yield`:

```nvgt
void yield();
```

As an example, let's say we wanted to calculate the factors of an integer. Although this is fast for small numbers, it can very quickly become quite computationally expensive when the numbers are particularly large. We might define the coroutine as:

```nvgt
void generate_factors(dictionary@ args) {
    const uint64 number = uint64(args["n"]);
    uint64[] factors = {1, number}; // Initialize factors with 1 and the number itself.

    for (uint64 i = 2; i * i <= number; ++i) {
        if (number % i == 0) {
            factors.insert_last(i);
            if (i * i != number) {
                factors.insert_last(number / i);
            }
        }
        yield(); // Yield control after each iteration
    }

    factors.sort_ascending();

    for (uint64 i = 0; i < factors.length(); ++i) {
        println("%0".format(factors[i]));
        yield(); // Yield control after printing each factor
    }
}
```

Then, before we start our game loop:

```nvgt
dictionary args;
args["n"] = 100000;
create_coroutine(@generate_factors, @args);
```

Now, in our game loop, we need somewhere to yield:

```
while (true) {
    wait(1);
    yield();
    ...
}
```

### Threads

#### STOP!

Before you consider using threads, understand that they are the most complex and error-prone way to handle concurrency. Threads share state with your entire program, meaning they can easily cause data races and deadlocks if not managed correctly. These issues can make your game crash, behave unpredictably, or become very difficult to debug. Unless you have a specific, compelling reason to use threads, stick to `async` (or coroutines if you really need them).

#### Note

This section is extremely technical in places. This is because multi-threading can be difficult. Even after doing it for a few years you will begin to learn that there are subtle mistakes you can make without realizing it. After we get through the different methods of protecting your code, we'll get into how to use threads and the rules on using them properly. If you want to know how to use any of the synchronization primitives discussed here, the documentation is your friend, as well as the NVGT community.

#### Introduction

A thread is much different than a coroutine. A thread runs alongside your code, and could even run on other processors in the system. A thread introduces many other problems that coroutines don't: they share state with the rest of your game, meaning they have access to all the global variables the rest of your code does.

One of the most critical rules of threads is to avoid global or shared state. Global or shared state means any global variables that you have in your code, as well as any state that your thread may access that other threads (also) might access.

If two or more threads access shared state without any kind of protection, this is known as a data race. A data race occurs when two threads want to perform different operations on a variable, and it just so happens that they do it the same time, or close enough that it doesn't matter. For example, if thread 1 wants to read a sound handle and another thread wants to initialize it, it may just so happen that both operations overlap, causing the handle that thread 1 gets to be in some weird undefined state. Data races can have all kinds of dangerous consequences that could make your program crash, cause unpredictable behavior, and so on. It's even known to cause a write to a variable to mysteriously vanish!

Data races are also one of the hardest things for a programmer to debug. This is because it can't be predicted when they'll even occur. One run of your code might be fine, but the next run might cause the race, or it might only occur every 200 runs of your code. This is why protection is so important.

#### Protecting against data races

There are several ways of protecting your code against data races if you do share state:

* Locks or semaphores
* Atomic variables
* Events/condition variables
* Just don't share any state
* Message passing (which will be explained here after it is added to NVGT)

##### Locks and semaphores

A lock is a synchronization primitive used to manage access to a shared resource by multiple threads. When a thread wants to "acquire" the lock, it checks if another thread already holds it. If the lock is already acquired, the requesting thread is blocked until the lock becomes available. When the lock is released, the blocked thread can proceed. This mechanism prevents concurrent access to the resource, ensuring data consistency and integrity.

Semaphores are another important synchronization mechanism. A semaphore is a signaling mechanism that can be used to control access to a common resource by multiple threads in a concurrent system. Semaphores can be used to solve various synchronization problems, such as controlling access to a finite number of resources or coordinating the order of thread execution. Semaphores maintain a counter representing the number of available resources. Threads can increment the counter to signal the release of a resource or decrement it to wait for a resource. When the counter is zero, any thread attempting to decrement it is blocked until the counter is incremented by another thread.

There are several types of locks and synchronization mechanisms. One common type is the mutex, or mutual exclusion lock. A mutex ensures that only one thread can access a resource at a time. When a thread acquires a mutex, other threads attempting to acquire the same mutex are blocked until it is released. This is useful for protecting critical sections of code where shared resources are accessed or modified.

Spinlocks are another type of lock, where the thread repeatedly checks if the lock is available in a loop, or "spins," until it can acquire the lock. Spinlocks are efficient when the wait time is expected to be short, as they avoid the overhead of putting the thread to sleep and waking it up. However, they are not suitable for long wait times, as they consume CPU cycles while spinning.

Read-write locks, or RW locks, allow multiple threads to read a resource simultaneously but provide exclusive access for writing. This lock has two modes: read mode and write mode. Multiple readers can hold the lock concurrently, but a writer must wait until all readers have released the lock, and vice versa. This is particularly useful in scenarios where read operations are frequent and write operations are infrequent, as it allows for greater concurrency.

Recursive locks are designed to be acquired multiple times by the same thread without causing a deadlock. They keep track of the number of times they have been acquired by the thread and require the same number of releases to unlock completely. This is useful in scenarios where the same thread might need to re-enter a critical section of code.

Binary semaphores, also known as mutex semaphores, can have only two states: 0 or 1, representing locked or unlocked. They function similarly to mutexes but do not have ownership, meaning any thread can release them, not just the thread that acquired them. This is useful for simple synchronization tasks where the ownership of the lock is not important.

Lastly, counting semaphores can have a value greater than one, allowing them to manage a finite number of resources. They maintain a counter representing the number of available resources. Threads increment, or signal, the counter when a resource is released and decrement, or wait, the counter when a resource is acquired. This is useful for limiting access to a pool of resources, such as a fixed number of database connections.

###### Wait wait, deadlocks?

yeah, did I forget to tell you about those? A deadlock is where two or more threads are unable to proceed with their execution because each is waiting for the other to release a resource they need.

To understand deadlocks, consider an example where two threads, Thread A and Thread B, need access to two resources, Resource 1 and Resource 2. If Thread A acquires Resource 1 and Thread B acquires Resource 2, both threads might then try to acquire the resource held by the other. Thread A will wait for Resource 2 to be released by Thread B, while Thread B waits for Resource 1 to be released by Thread A. Since neither thread can release the resource it holds until it acquires the resource held by the other, they are both stuck, leading to a deadlock.

Four necessary conditions for a deadlock to occur are:

* At least one resource must be held in a non-shareable mode, meaning only one thread can use the resource at any given time.
* A thread holding at least one resource must be waiting to acquire additional resources currently held by other threads.
* Resources cannot be forcibly taken from the threads holding them; they must be released voluntarily by the holding thread.
* There must exist a set of threads such that each thread is waiting for a resource held by the next thread in the set, forming a circular chain.

Preventing or resolving deadlocks typically involves ensuring that at least one of these conditions cannot hold. Techniques include:

* Impose a strict order in which resources must be acquired and ensure that all threads adhere to this order.
* Allow deadlocks to occur, but have mechanisms to detect and recover from them, such as terminating one or more of the threads involved.
* Use algorithms that dynamically analyze resource allocation requests to ensure that they do not lead to deadlocks, such as the Banker's Algorithm.
* Implement timeouts for resource requests, forcing a thread to release its held resources if it cannot acquire the required resources within a certain period (this, by far, may be the easiest algorithm to implement).

##### Atomic variables

An atomic variable is a special type of variable used in concurrent programming to ensure that operations on the variable are completed without interruption. The key characteristic of atomic variables is that any operation performed on them -- such as reading, writing, or modifying -- must be completed entirely before any other operation can start. This means that the state of the variable is always consistent and predictable, even when multiple threads are accessing or modifying it simultaneously.

To understand this better, consider a scenario where multiple threads are trying to increment a shared counter variable. In a non-atomic scenario, one thread might read the value of the counter, and another thread might read the same value before the first thread has a chance to write the incremented value back, leading to both threads writing back the same value. This causes the counter to be incremented only once instead of twice, leading to incorrect results.

However, with an atomic variable, the increment operation is indivisible. This means that when one thread starts to increment the counter, no other thread can read or write to the counter until the increment operation is fully completed. The operation is guaranteed to either fully succeed or fail, but it cannot be partially completed. This prevents the problem of race conditions, where the outcome depends on the unpredictable sequence of thread execution.

Modern processors support atomic operations through special hardware instructions that ensure these operations are performed without interruption. These instructions include atomic read-modify-write operations, such as compare-and-swap (CAS) and fetch-and-add, which are used to implement atomic variables.

For example, consider the compare-and-swap (CAS) operation. It works by checking if the value of the variable is equal to an expected value. If it is, the value is replaced with a new value. If it isn't, the operation fails. This all happens in one atomic step, ensuring that no other thread can interfere between the check and the update.

##### Events/condition variables

Events are synchronization primitives used to signal between threads, allowing one thread to notify others about the occurrence of a specific condition. In the context of concurrency, an event can be set or reset, and threads can wait for an event to be set before proceeding. This is particularly useful when you need one or more threads to pause execution until a certain condition is met.

For instance, imagine a scenario where a worker thread is processing tasks from a queue. The worker thread can wait for an event that gets set when new tasks are added to the queue. Once the event is set, the worker thread wakes up and processes the new tasks. If there are no tasks, the worker thread goes back to waiting. This mechanism ensures efficient use of CPU resources, as the worker thread is not continuously polling the queue but instead waits for a signal.

Events can be manual-reset or auto-reset. A manual-reset event remains signaled until it is explicitly reset, allowing multiple waiting threads to be released. An auto-reset event automatically resets after releasing a single waiting thread, ensuring that only one thread is woken up per signal.

Condition variables are another synchronization mechanism used to block a thread until a particular condition is met. They are typically used in conjunction with mutexes. When a thread waits on a condition variable, it releases the associated mutex and enters a waiting state. When the condition is signaled, the mutex is reacquired, and the thread resumes execution.

The primary use case for condition variables is to manage complex thread interactions that require waiting for certain states or conditions. For example, in a producer-consumer scenario, a consumer thread might wait on a condition variable until there are items available in a buffer. The producer thread, after adding an item to the buffer, signals the condition variable to wake up the consumer thread.

Here’s a simplified example: a producer and consumer thread are started one after the other. The producer thread (which is what produces data for the consumer thread to act upon) acquires the mutex, adds an item to the buffer, signals the condition variable, and releases the mutex. By contrast, the consumer thread acquires the mutex, waits on the condition variable while the buffer is empty, processes the item from the buffer the condition variable has been signaled, and releases the mutex. The "mutex," in this  case, could (and should most likely be) a recursive mutex.

Condition variables support two main operations: `wait` and `notify`. The `wait` operation puts the thread into a waiting state and releases the mutex. The `notify_one` operation wakes up one waiting thread, while `notify_all` wakes up all waiting threads. These operations are critical for coordinating complex interactions and ensuring that threads only proceed when the required conditions are met.

Events are simpler to use when you need to signal one or more threads to proceed. They are particularly effective when dealing with straightforward signaling scenarios, such as waking up worker threads when a new task arrives.

Condition variables are more suitable for scenarios requiring complex synchronization, especially when multiple conditions and interactions between threads need to be managed. They provide more control over the waiting and signaling process, making them ideal for use cases like producer-consumer problems.

##### Not sharing any state

If all of the above has left you utterly confused and wondering what you've just read, that's okay; you have lots of other options. The simplest would be to just ignore this section entirely and to just not use threads at all. If you really, really, really do need threads, though, the best method would be to figure out how you don't need to share state. This might be quite difficult in some cases, but the less state you share, the less likely it is you'll need to worry about any of this stuff. If you do need to share state, all of the above is important to understand to do things properly.

#### Creating and managing threads

To create a thread, call the `thread` constructor and give it a name of your thread. This is usually an ID that you can use to look up the thread later. This will NOT start your thread, though; to do that, call `start` passing in both a function to execute and (optionally) a dictionary handle of arguments that that thread should receive.

Your thread callback should take as input a `dictionary@` which contains the arguments given in `start()`.

Once started, a thread immediately begins execution. Your original code that spawned the thread will continue executing after this function returns.

If you want to wait until the thread completes, call `join()` without any arguments. Alternatively, `join` can take a timeout which, if expires, causes the function to return `false`.

On the thread object there are a few other things you can do as well, such as changing the threads priority via the `priority` property.

##### Warning!

Do not change the priority of a thread unless you absolutely have to. Messing around with the thread priority of a thread -- particularly with threads which do a lot of computationally expensive work -- can cause your entire system to hang and have other undesireable side-effects!

#### Golden rules of threads

When using threads, always remember:

* Only use threads when you need to. Do not just use them because you feel they would make your code faster. More often than not, this will just cause your code to run slower.
* When using locks, hold the lock for the shortest time possible. The area in which a lock is acquired is known as a critical section, and you should do only what you neeed to do in these and then immediately release the lock. If you don't do this, you could cause resource leaks, sequential execution, deadlocks and all kinds of other problems.
* Do not acquire a lock at the start of a function. This may seem tempting, but it is wrong, and will cause your code to be far slower, if not eliminate the benefit of using threads entirely.
* Avoid recursive mutexes unless you know what you are doing.
* When acquiring a lock, there are two ways of doing so: `lock` and `try_lock`. If your able to, use `try_lock` which will return false if the lock cannot be acquired. If this does return false, go do something else and try acquiring the lock later.
* If your code consists of many threads that mostly perform reads of shared state and only a few cases where shared state is modified, use a reader-writer lock and not a mutually exclusive one.
* Do not mess with thread priorities.
* The less shared state your threads have to manage, the fewer synchronization issues you'll encounter. Where possible, avoid global variables or shared objects.
* For simple counters or flags, use atomic operations instead of locks to avoid the overhead and complexity of mutexes.
* Do not use busy-waiting (spinning) to wait for a lock or condition. This wastes CPU resources and can lead to performance issues. If you need to wait for a lock to be available for acquisition, call `lock` on it and allow the underlying operating system to do the waiting for you.
* Creating and destroying threads can be expensive. Reuse threads with thread pools or similar techniques to manage resources efficiently.
* Where possible, use higher-level concurrency constructs like `async<T>`. These abstractions often handle the complex details of synchronization for you.
* When using condition variables, always protect the condition check with a lock and use a loop to recheck the condition after waking up, as spurious wakeups can occur. That is, it is possible for your thread to be awoken when the condition variable hasn't actually been signaled.
* While using timeouts can prevent deadlocks, ensure that your program can handle the scenario where a timeout occurs gracefully.
* Clearly document the synchronization strategy in your code, including which locks protect which data. This helps maintainers understand the concurrency model and avoid introducing bugs.
* Concurrency bugs can be rare and hard to reproduce. Test your application under load to increase the chances of exposing synchronization issues early in development.

### Conclusion

This article provided a deep dive into the various concurrency mechanisms provided by NVGT. Though parts may have been terse, we still hope it helped. If you have any questions, don't hesitate to ask!


## Memory Management Information (incomplete)
What is a handle? What are references? What is the difference between the stack and the heap and when/why should I care? What is a value typed object? What is a primative datatype, and when should or shouldn't one use the @ character in their code? When should I worry about garbage collection and what even is that? How much is it wise to bother with all this stuff anyway?

If you've been having any such questions or similar, you've come to the right place. This tutorial will attempt to unravel and demystify all of the jargon behind various memory management techniques and structures as well as advice about when/how to use them. The goal is that by the end of this reading, you will have the knowledge to begin developing confidence particularly in the usage of handles and references in your games, while also learning a lot of interesting stuff about memory management along the way.

### It's automatic, mostly
One thing to keep in mind when developing games in NVGT is that most of the memory management is done for you automatically. If you are just getting in to game creation, you don't need to worry about memorising everything you read in this tutorial from the beginning because NVGT will make as many wise memory management decisions for you as it reasonably can, mostly with the use of reference counting based garbage collection (described below). There are certainly times when you specifically need to direct the compiler especially if you notice your game running slowly or being more abusive to ram usage than you would like, but truly you can code even a pretty advanced game in NVGT while only knowing a fraction of the knowledge contained in this tutorial.

### Reference counting
Since it's a pretty simple concept though admitedly with a potentially intimidating name and since it's the backbone to most of NVGT's memory management, we'll start by describing the concept of a reference counter.

The problem: If an object instance is created, how do we know when it is safe to destroy it? We don't want to delete the object before the programmer is done using it, after all.

The solution: An integer variable within the class called the reference counter stores the number of references your script maintains to an object. When a new variable is created in your script that references an object, it's reference counter increases by 1. When that variable goes out of scope or in some other way gets destroyed/reset, the counter decreases by 1. If the reference counter reaches 0, the object gets destroyed.

As you may have surmised, this does mean that it is possible to create 2 or more variables that actually point to the same object in memory so long as that object uses the reference counting model. For each variable that exists that points to the same object, the reference counter for that object increases. Such variables in nvgt/Angelscript are called handles, and we'll talk about those below in another section of this tutorial.

All Angelscript classes created by the NVGT programmer automatically use reference counting based memory management. As in most cases, the internal reference counter is hidden from the user.

Reference counting is pretty great and simple in many cases, but it has it's drawbacks which cause it to not be viable in all situations, particularly with some of the builtin core types NVGT provides. To understand why, lets define a couple of other low level concepts first.

### The stack
Memory allocation can be expensive and slow, and all functions usually require at least a few bytes of memory to do their work, such as to store local variables and other bookkeeping information required for the computer to return to the previous function. If a program were to allocate memory from the system every time a function was called, programs would execute very slowly and RAM modules may meat their end just a bit more quickly. So, how do we execute functions without allocating memory for each call?

The stack is the name for a chunk of memory allocated on program startup intended specifically to keep track of and manage function calls. Rather than allocating 32 bytes of memory from the system needed by a function every time that function is called, we instead use 32 bytes of the already allocated stack to store data for the function call. The only time the operating system actually needs to perform extra memory allocation is if the stack grows larger than what the system initially allocated to the process, in which case the operating system can perform rare memory allocations to make the stack larger up until the stack reaches the maximum stack size configured by the programmer or allowed by the OS, in which case the program will abort.

Though various platforms could have slightly different rules to the following, it works something like this. An integer called the stack pointer keeps track of where on the stack data should next be written, a little like the seekable position pointer of a file object. When a function requiring 32 bytes of memory is called, the stack pointer is subtracted by 32 and any byte between the new position of the stack pointer and the old one from before the function call is designated as safe space for the function to store the data it needs to execute. When the function returns, 32 gets added to the stack pointer thus restoring it to it's previous position from before the function call, and any following calls will thus overwrite the stack based memory used by the previous function because instead of reallocating memory over and over from the system per call, we just keep reusing the same already allocated memory over again, which is absolutely spades more efficient. 32 is of course an arbitrary number, all of this magical stack management including determining how much space a function will need on the stack is all done internally for you by the compiler and you rarely to never need to think about these internals, not unless you need to adjust your stack size for some reason or in this case, are trying to learn when reference counted objects and thus handles in Angelscript can and cannot be used.

### The heap
Did you notice one of the major drawbacks to the stack mentioned above? As soon as a function that uses the stack to store a variable returns, that memory is, for all intense and purposes, erased / inaccessible. It may be overwritten at any time. So even though the stack is great for avoiding many small memory allocations when performing calculations and calling functions, it can't actually store any long-term data. As you may see, it's only half the puzzle. So how do we solve this problem and establish long-term data storage?

Enter the heap. It's a memory area like the stack, but with vastly different characteristics. The heap is where most generic in-memory application data is stored. This is because with the heap, the programmer can ask the system to allocate any amount of memory at any time, and then to free/deallocate it at any later time. While it provides a vastly higher amount of flexibility as opposed to the stack (the data you stored on the heap won't disappear as soon as the function that stored it stops executing), it also means that now the programmer is responsible for managing how much memory they allocate and how well they use it. Unless you are very careful, misuse of the heap can make your program run slower than you'd like, or even introduce memory leaks because unless explicitly told, the system will not free any memory allocated on the heap until the entire program exits.

Remember though that memory allocation, especially in a way where the intricate low level internals of it are hidden from the programmer, is slow. If it wasn't, we might not need structures like the stack to perform fast calculations. Internally it's a complicated, clever and extensive system that manages the heap. A programmer can ask the system to allocate 30mb of memory on the heap and appear to get a nice, contiguous 30mb buffer that they can do what they like with. But internally, the system has potentially done a lot of magic to allocate that 30mb of RAM. Maybe it checked recently freed memory to see if an equal or larger sized block had been recently discarded and could be reused, it might have to locate enough free memory pages to construct a buffer of the given size, on some operating systems compression might even become involved as portions of the 30mb of data remain unaccessed for increasingly longer periods of time. This author certainly does not claim to be an expert on the subject. It's enough to know that because memory allocation onto the heap is actually quite complicated internally, overuse or misuse of it can be slow.

### Combining the stack and the heap
So on one hand, we can get really fast access to some memory on the stack, but it's limited and temporary as the memory a function uses is rendered unsafe the moment that the function returns. On the other hand we can get easy access to any amount of memory within reason at any time, but it can be significantly slower and involves mechanisms like reference counting or other techniques to make sure that there are neither memory leaks nor objects getting freed before they should be. There is no perfect solution, thus the existance of both.

We can use a somewhat flawed analogy to describe these systems. When thinking of the stack, you could imagine a container of disks or books or other flat items, with each item stacked neatly on top of the other. You can either place a new item on the top, or take one off, both of which are very quick operations. That's all you can do though, the container is too tight for you to magically grab the third item down in the stack without upending the entire container, or program as it were. Where as the heap, you could imagine either as a messy room for simplicity or as the most organized library you have ever seen for technicality. While you can both add and retrieve any item at any time, you first need to either sort through the mess on the floor or follow the organization system to the correct shelf to find it, and you never know when less frequently accessed parts of the library might be packed away into boxes to save space.

So in the end, the stack is where you should perform many small calculations, it's where things like vectors and small strings should be placed, primative function arguments can be passed via the stack after a certain point as well. The heap on the other hand is where either any large hunks of data should be stored, and/or any data where you might need more control over the memory management than what the stack allows for. Both the stack and the heap are very important, but for different reasons.

### Value typed objects
So now that we've taken a short jaunt through one of computing's proverbial low level sewer systems that few people want to think about in depth, lets get some badly needed fresh air and return to a much more comfortable higher level armed with some of that acquired knowledge. We'll make the transition by defining one more term.

Angelscript (the scripting engine NVGT uses) allows the definition/registration of 2 main types of objects internally, or in other words, allows builtin objects to be registered with 1 of 2 memory models. Those are reference typed objects, and value typed objects. A reference typed object is described in various sections regarding reference counting, so for now we'll focus on value typed objects.

Value typed objects are any type of object which is usually created with memory directly on the stack within a function call, or else directly inlined in memory as part of a class. They are always automatically destroyed as soon as the memory containing them is erased, such as when a function is returned or when a class instance containing them is destroyed. They cannot be created by an nvgt script, and can instead only be registered as builtin objects in NVGT's source code itself. Generally we try to avoid registering value typed objects due to the fact that you cannot make a handle to one of them, but as they are created on the stack rather than the heap, it can be more efficient to register certain object types, such as string, vector, random number generators, and a few other objects as value types as opposed to reference types, which usually require a memory allocation every time one is created. Generally it's best for an object to be a value type if it is likely to exist for a very short period of time. The biggest takeaway here is that you cannot create handles to certain builtin classes, and the reason is because they are value types that will get destroyed as soon as the memory containing them is freed. You can create handles to reference counted objects containing value typed properties, however.

### handles
A handle, in short, is a variable that points to any reference counted object instance that has been allocated on the heap. A handle itself is not really an object per say (though it may exist as such on some internal level), it is only a variable that points to one. You can have as many handles to the same object as you want, and every time a handle is created, the reference counter for that object increases. When a handle is destroyed, the reference counter for the object it points to decreases by 1. If the object's reference counter reaches 0, the object is destroyed. Handles themselves are registered as value types, meaning they exist directly on the stack or inlined within the memory of a class. So that means when a class instance containing a handle as a property gets destroyed, that handle contained therein automatically gets destroyed at the same time, causing the reference counter of any object it pointed to to be consequently decremented. Similarly any handles created as variables in a function are destroyed when that function returns, as the handles themselves exist on the stack even though the object the handle points to does not.

A handle is declared using the @ character following a class type. For example if I want to create a handle to a sound object, I can create a variable like this.
```
sound@ snd = null;
```
And can then do @snd = sound(); to assign the handle to point to a new sound object at any time or @snd = existing_sound; to similarly cause the handle to point to an existing sound object.

Hold up though, lets talk about this = null part, because that is important. Remember, a handle is not an object, it is only a pointer to an object. This means that the pointer can actually point at nothing, or null, when it is waiting to be assigned to. It can also be set to null at any time, which will decrement the reference counter of the object it used to point to while keeping the handle around, now not pointing to anything, waiting for reassignment. Why is this important? Well, what happens if we try executing the following code while the snd handle is set to null.
```
snd.load("test.ogg");
```
We get an unhandled null pointer access exception! The engine does not know what to do in this case because you have instructed it to call the load method on a theoretical sound object, but without giving the engine an actual sound object to call the method on! For this reason, it is always important to insure that an object handle you are about to access is not set to null before you do so. This is particularly important when functions return handles to objects, as the function could decide to return null.
```
if (@snd == null) alert("oops", "no sound object associated with this handle");
else snd.load("test.ogg");
```
So what's with the @ character again when checking whether the handle is null? To answer that question, consider this class.
```
class example {
	int number;
	bool opEquals(const example@ other) {
		return @other != null and this.number == other.number;
	}
	void opAssign(const example@ other) {
		if (@other != null) this.number = other.number;
	}
}
```
In this case, we have overloaded the == operator for the class, meaning we can execute `if (instance1 == instance2)`. We've also overloaded the assignment operator so that we can do `instance1 = instance2;` to assign the second object to the first.

The existance of assignment and comparison operators on a class means that when working with handles, we now must distinguish between when we are trying to call the comparison or assignment operator on the class a handle is pointed to, or whether we wish to directly compare or assign one handle to another. Thus, the statement @instance1 = instance2; causes the instance1 handle to point to the instance2 object where as instance1 = instance2; causes instance2 to assign/overwrite instance1 in memory. Similarly if we wish to determine whether a handle is null, we typically must check whether @instance == null, because if we execute instance == null; instead, we're checking whether the object that the instance handle is pointing to is comperable to the value of null by calling it's equality operator, meaning that if the handle is null (not pointing at an object), you'll get the same null pointer exception if you omit the @ character when checking if a handle is null. Angelscript has provided a keyword to get around this ambiguity (at least in the case of comparison) that helps you not need to remember where and where not to put @ characters. You can execute if (instance is null) as an alternative to if (@instance == null), or even if (instance1 is instance2), to compare two handles (meaning checking whether both handles point to  the same object) while insuring that you are never accidentally comparing with the object pointed to by the handle instead.


## Subscripting tutorial
Subscripting is the concept of loading external Angelscript code into your game and executing it. This has many applications, including allowing you to make editional levels for your game that aren't directly included, and allowing your game admins to modify how certain items work. This tutorial contains a small example of the basic features of subscripting. We'll go over the ways to load code, find functions, and share methods between the nvgt scripts and your subscripts. For brevity, if I say nvgt code I am talking about the actual .nvgt scripts that are loaded by nvgt.exe and/or compiled. When I say the subscript, I'm talking about the code that the nvgt code is loading (E.G. a shared script in STW).

### Angelscript's Execution Flow
This section will talk just a bit about Angelscript's execution flow as it will help make these concepts a bit clearer. You won't specifically need to remember all of this, but it should give you a bit more of a framework for understanding what you do need to know.

The lowest level of executing an Angelscript is the engine, you don't need to worry about this (I create it in C++). NVGT only uses one Angelscript engine instance for all scripts, be that nvgt code or subscript code. The engine is where we register all of the c++ functions that nvgt can use, for example `key_pressed` or the string class. The only important note is that these functions are registered with different access masks (allowing you to control what functions subscript code have access to), we'll talk about that later.

The next step of code execution in Angelscript is to tell the engine to start what's known as a module for us. A module is basically a container for code. You feed the module code in as many sections (or files) as you want, then tell the module to build the code, making the module contain compiled bytecode now ready for execution. NVGT itself only uses one module called "nvgt_game", meaning that the "nvgt_game" module contains all the code contained in any .nvgt files that are included. Once the module of code has been compiled, the module is now aware of what functions, classes etc that the code contains. This means we can search for a function by name in a module, then call that function. When subscripting is involved, the nvgt code actually creates a second module at the request of the programmer (you'll see this below). Thus, the subscripting code runs in a different Angelscript module than the nvgt code does, and the most important point of this entire line is that the code in one angelscript module cannot immedietly access code in another module. If you start a new module for subscripting, the code in that module will not automatically have access to the variables or functions in the nvgt_game module, not unless you exclusively share each one.

### Sharing Code
There are 2 ways to share functions from the nvgt code to the subscript's code. Both have advantages and disadvantages, and unfortunately, neither are perfect. I'll be the first to admit that sharing functions with subscripts is actually the most annoying part of subscripting by far, though it is the type of thing where you set it up once and it's behind you sans any new functions you wish to share. The following are the considerations:

#### Shared code
Angelscript does have this concept called shared code. If a module declares something as shared, other modules can easily access it using the "external" keyword in Angelscript. Lets create a small shared class for this example.
```
shared class person {
	string name;
	int age;

	person(string name, int age) {
		this.name = name;
		this.age = age;
	}
}
```

Now, so long as the top of our subscripting code contains the line
`external shared class person;`
We can successfully create and use instances of the person class in the subscripting code. So this all sounds great, what's the big problem with it? Oh how sad I was when I found out. Basically shared code cannot access non-shared code! Say that the person class shown above had a function in it that accessed a non-shared global variable in the nvgt code called score, the class will now fail to compile because the shared code of the person class cannot access the non-shared variable score. This is a horifying limitation in my opinion that makes the shared code feature much less intuitive to use. A slight saving grace is that at least non-shared code can call shared code E. non-shared code in the nvgt_game module can make instances of the person class just fine, but the person class (being shared code) can't access, for example, the non-shared list of person objects in your game that the person class wants to add instances of itself to. Luckily, there is a much better option in most cases.

#### Imported functions
Angelscript shared modules provide the concept of importing a function from one module to another. Say you have a non-shared function in your game called `background_update`. If at the top of your subscripting code you include the line
`import void background_update() from "nvgt_game";`
and so long as you make one extra function call when building the module with subscripted code in it (`script_module.bind_all_imported_functions()`), the subscripting code can now successfully call the `void background_update()` function even though it is not shared in the nvgt code. The only disadvantage to this system is that it only works for functions! There is no such ability to say, import a class.

This all means that you will certainly need to combine these 2 methods of sharing code to share all of what you desire. For example you need to use the shared code feature to share a class interface with the subscripting code, but then since shared code can't access non-shared code, you need to use an imported function to actually retrieve an instance of that class (such as the player object) from the nvgt code.

### Full Example
Below you'll find a completely categorized example of how subscripting works, incapsilating all the concepts we've discussed thus far.

#### Code to be shared with the subscripts
```
// A global array for person objects.
person@[] people; // Shared code doesn't work with global variables, so you can't share this.

shared class person {
	string name;
	int age;

	person(const string& in name, int age) {
		this.name = name;
		this.age = age;
	}
}

// Say we want the subscripting code to be able to create a new person.
person@ new_person(const string& in name, int age) {
	person p(name, age);
	people.insert_last(p);
	return p;
}

// Or in some cases, this is the closest you'll get to sharing a global variable, so long as it supports handles.
person@[]@ get_people() property { return @people; }
```

#### Imports
Now lets create a section of code that imports the functions. This way, the user who writes subscripting code doesn't have to do it.

```
string imports = """import person@ new_person(const string& in, int) from "nvgt_game";
import person@[]@ get_people() property from "nvgt_game";
external shared class person;
""";
```

#### Subscript code
```
string code = """void test() {
	person@ p = new_person("Sam", 21);
	new_person("reborn", -1);
	alert("test", people[0].name);
}

// This function needs arguments.
int64 add(int n1, int n2) {
	return n1 + n2; // normal int can be passed as argument but not yet for return values, consider it a beta bug.
}

// This function will be used to demonstrate how to catch script exceptions.
void throw_exception() {
	throw ("oh no!");
}
""";
```

#### Calling the subscript
```
#include "nvgt_subsystems.nvgt" // To limit the subscript's access to certain nvgt core functions.

void main() {
	// Create a new module.
	script_module@ mod = script_get_module("example", 1); // The second argument can be 0 (only if exists), 1 (create if not exists), and 2 (always create).
	// Add the code sections, usually it's a section per file though they can come from anywhere.
	mod.add_section("imports", imports);
	mod.add_section("code", code);
	// Remember when I talked about an access mask earlier that allows you to limit what core engine functions can be called by the subscript? Now is the time to set that. If the function permissions aren't set at build time, there will be compilation errors and/or wider access than you intended. An access mask is just an integer that is used to store single bit flags as to whether the subscript should have access to a given set of functions. You can see the full list in nvgt_subsystems.nvgt. You can simply binary OR the ones you want to grant access to in this next call, all others will be disabled.
	mod.set_access_mask(NVGT_SUBSYSTEM_SCRIPTING_SANDBOX | NVGT_SUBSYSTEM_UI);
	// Now we need to build the module. We should collect any errors here which are returned in a string array. You should display them if the build function returns something less than 0.
	string[] err;
	if (mod.build(err) < 0) {
		alert("error", join(err, "\r\n\r\n"));
		exit();
	}
	// Next, if any functions are being shared via the imported functions method, we need to bind their addresses from this nvgt_game module to our example module. Don't worry it's just one line + error checking, but what is happening behind the scenes in this next call is that we are looping through all functions that have been imported, and we're searching for them by declaration in the nvgt_game module. When we find them, we tell the example module the function's address.
	if (mod.bind_all_imported_functions() < 0) {
		alert("error", "failed to bind any imported functions");
		exit();
	}
	// Cool, we're ready to go! Everything above this point you can consider an initialization step, code up to this point executes rarely, usually you'll want to store a handle to the script_module object somewhere and other parts of your code will repeatedly perform the steps below as calls are needed. Some wrapper functions that make calling common function types even easier are supplied later in this tutorial. We're about to start calling functions now. We can either retrieve a function by declaration, by index or by name.
	script_function@ func = mod.get_function_by_decl("void test()"); // This is useful because we can limit the returned function by return type and argument types, meaning that if 2 functions with the same name but different arguments exist, you will know you get the correct one.
	if (@func == null) {
		alert("error", "can't find function");
		exit();
	}
	// This looks a bit bulky, but it won't in actual usage when you don't need to show UI upon this error. Lets call the function!
	func({}); // Usually a dictionary of arguments is passed, this function takes none. Soon I think we'll be able to use funcdefs to call functions from shared code completely naturally, but we're not there yet and so now we use a dictionary, properly demonstrated in the next call.
	// Now lets demonstrate how to pass function arguments and how to fetch the return value. We'll skip the error check here we know the add function exists.
	@func = mod.get_function_by_name("add"); // Notice the lack of signature verification here.
	dictionary@ r = func.call({{1, people[0].age}, {2, people[1].age}}); // Notice how we can access those person objects created from the subscript.
	// The return value will be stored in a key called 0, and the other values will maintain the indexes that you passed to them encase the function has modified a value using an &out reference.
	int64 result = 1;
	r.get(0, result);
	alert("add test", result);
	// Usually it's good to check for errors when calling functions, unfortunately. In time this may be compressed so that a default error handler may exist or something of the sort, for now, this is possible.
	err.resize(0);
	@func = mod.get_function_by_name("throw_exception");
	func({}, err);
	if (err.size() > 0) alert("test", join(err, "\r\n"));
}
```

#### Useful wrapper functions
Finally, I'll leave you with some useful functions that show how it's very easy to wrap the calling of common functions. As I said above later I plan to make it possible to call functions with funcdefs if I am able, but we're not yet there. For now, you can use a version of these. They will not run out of the box as they are copied from stw, but they should be all the example needed.

```
dictionary shared_function_cache; // It's useful to cache function lookups in a dictionary for performance, else Angelscript needs to keep looping through all shared functions to find the matching signature.

script_function@ find_shared_function(const string& in decl) {
	script_function@ ret = null;
	if (shared_function_cache.get(decl, @ret)) return @ret;
	@ret = script_mod_shared.get_function_by_decl(decl);
	shared_function_cache.set(decl, @ret);
	return @ret;
}

dictionary@ call_shared(const string& in decl, dictionary@ args = null, string[]@ errors = null) {
	script_function@ func = find_shared_function(decl);
	return call_shared(func, args, errors);
}

dictionary@ call_shared(script_function@ func, dictionary@ args = null, string[]@ errors = null) {
	if (@func != null) {
		bool internal_error_log = false;
		if (@errors == null) {
			internal_error_log=true;
			@errors = string[]();
		}
		@args = func.call(args, @errors);
		if (@errors != null and internal_error_log and errors.length() > 0)
			log_scripting("error", errors[0], errors.length()>1? errors[1] : "", errors.length()>2? errors[2] : "", "");
	}
	return args;
}

void call_shared_void(script_function@ func, dictionary@ args = null, string[]@ errors = null) {
	call_shared(func, args, errors);
}

bool call_shared_bool(script_function@ func, dictionary@ args = null, string[]@ errors = null, bool default_value = false) {
	@ args = call_shared(func, args, errors);
	if (@args != null) return dgetb(args, 0);
	return default_value;
}

double call_shared_number(script_function@ func, dictionary@ args = null, string[]@ errors = null, double default_value = 0.0) {
	@ args = call_shared(func, args, errors);
	if (@args != null) return dgetn(args, 0, default_value);
	return default_value;
}

string call_shared_string(script_function@ func, dictionary@ args = null, string[]@ errors = null, string default_value = "") {
	@ args = call_shared(func, args, errors);
	if (@args != null) return dgets(args, 0);
	return default_value;
}
```



# API References
This section contains several complete class and function API references that allow the creation of games and other applications. To see examples of how any of these objects or functions work together with any great detail, you should look in the NVGT User Manual instead of the API references. However if you are trying to find the name of a specific function or browse the complete list of what this engine has to offer, you have come to the right place!


## Builtin Script API
* [Containers](nvgt_references_builtin_containers.md)
* [Datatypes](nvgt_references_builtin_datatypes.md)
* [Streams](nvgt_references_builtin_streams.md)
* [Audio](nvgt_references_builtin_audio.md)
* [Concurrency](nvgt_references_builtin_concurrency.md)
* [Data Manipulation](nvgt_references_builtin_data_manipulation.md)
* [Date and Time](nvgt_references_builtin_date_and_time.md)
* [Environment](nvgt_references_builtin_environment.md)
* [Filesystem](nvgt_references_builtin_filesystem.md)
* [Math](nvgt_references_builtin_math.md)
* [Networking](nvgt_references_builtin_networking.md)
* [Profiling and Debugging](nvgt_references_builtin_profiling_and_debugging.md)
* [Pseudorandom Generation](nvgt_references_builtin_pseudorandom_generation.md)
* [Security](nvgt_references_builtin_security.md)
* [Text-To-Speech](nvgt_references_builtin_texttospeech.md)
* [User Interface](nvgt_references_builtin_user_interface.md)

## Bundled Includes API
* [Auditory User Interface (form.nvgt)](nvgt_references_include_auditory_user_interface_form.md)
* [Basename Clearing (clear_compiled_basename.nvgt)](nvgt_references_include_basename_clearing_clear_compiled_basename.md)
* [BGT Compatibility Layer (bgt_compat.nvgt)](nvgt_references_include_bgt_compatibility_layer_bgt_compat.md)
* [Character Controller Subsystem (basic_character_controller.nvgt)](nvgt_references_include_character_controller_subsystem_basic_character_controller.md)
* [Character Rotation (rotation.nvgt)](nvgt_references_include_character_rotation_rotation.md)
* [Dictionary Retrieval (dget.nvgt)](nvgt_references_include_dictionary_retrieval_dget.md)
* [INI Reader and Writer (ini.nvgt)](nvgt_references_include_ini_reader_and_writer_ini.md)
* [Instance Management (instance.nvgt)](nvgt_references_include_instance_management_instance.md)
* [Legacy Sound Manager (sound_pool.nvgt)](nvgt_references_include_legacy_sound_manager_sound_pool.md)
* [Menu Interface (menu.nvgt)](nvgt_references_include_menu_interface_menu.md)
* [Music System (music.nvgt)](nvgt_references_include_music_system_music.md)
* [Number Speaking (number_speaker.nvgt)](nvgt_references_include_number_speaking_number_speaker.md)
* [Size Conversions (size.nvgt)](nvgt_references_include_size_conversions_size.md)
* [Statistic Management (stat_set.nvgt)](nvgt_references_include_statistic_management_stat_set.md)
* [Token Generation (token_gen.nvgt)](nvgt_references_include_token_generation_token_gen.md)
* [touch gesture management (touch.nvgt)](nvgt_references_include_touch_gesture_management_touch.md)
* [User Data Storage and Retrieval (settings.nvgt)](nvgt_references_include_user_data_storage_and_retrieval_settings.md)

## Plugins
* [git2nvgt](nvgt_references_plugin_git2nvgt.md)
* [nvgt_curl](nvgt_references_plugin_nvgt_curl.md)
* [nvgt_sqlite](nvgt_references_plugin_nvgt_sqlite.md)
* [systemd_notify](nvgt_references_plugin_systemd_notify.md)


# Advanced Topics for C++ Developers
This section contains information that is useful for anyone who wishes to interact in any way with NVGT's source code. Whether someone wants to perform a simple sourcecode build, develop an NVGT plugin dll, learn how to contribute to the engine or just learn about how NVGT works internally, you'll find such information here. The topics that will be discussed here will generally not be applicable for those who just want to develop games using NVGT using the installer downloaded from nvgt.dev.


## Building NVGT for Android
To build NVGT for Android, you will need the Android SDK. The easiest way to get this at least on Windows is if you have Visual Studio to download the Mobile Development workload, or else to install Android Studio.

As with other platforms, most of the work regarding building libraries has been done for you, you can download [droidev.zip](https://nvgt.dev/droidev.zip) here, and extract it similarly to how it is described above for other platforms. Look at jni/example-custom.mk to learn how to set a custom location to this directory.

On some systems, the Android SDK requires a bit of setup to use it extensively enough to build NVGT. If you are using Android Studio directly or if anything else has configured your Android SDK for you it is unlikely you'll need any of this, but in case you need to set up your SDK manually especially on Windows, here are a few notes:
1. The Android SDK on Windows must not be in a directory containing spaces, or at least must not be invoked with one. For example, the Mobile Development workload on Visual Studio by default installs the tools in "C:\Program Files (x86)\Android". So to use it, you may need to symlink the folder with a command run as administrator like `mklink /d C:\android "C:\Program Files (x86)\Android"`.
2. It may also be a good idea to run the Gradle tool (described below) as administrator if you get any weird access denied errors when trying to do it otherwise, you'll see it's trying to write to some file within the Android SDK directory which may require administrative rights to access depending on where it is installed. If you keep getting errors even after doing this, run `gradlew -stop` to kill any old Gradle daemons that were running without privileges.
3. There are a couple of environment variables you may need to set before building. These are the `ANDROID_NDK_HOME`, `ANDROID_HOME`, and `JAVA_HOME` variables which help locate the Android development tools for anything that needs them. An example of setting them at least for Windows is in other/droidev.bat.
4. If at any point you need to run sdkmanager to accept licenses on Windows, run it... yep, as admin. Otherwise you will be informed that the licenses have been successfully accepted, but when you try using the tools, you'll be told to accept them again.
5. It should be noted that both Visual Studio and Android Studio install a functioning Java runtime environment for you, so you don't have to go hunting for one. On Visual Studio, this may be at "C:\Program Files (x86)\Android\openjdk\jdk-17.0.8.101-hotspot", and for Android Studio it may be at "C:\Android\Android Studio\jre". Sadly these paths might change a bit over time (especially the JDK version in the Visual Studio path), so you may need to look up the latest paths if you are having trouble.

Once the Android SDK is set up, cd to the jni directory and run `gradlew assembleRunnerDebug assembleStubRelease`

On platforms other than Windows you may need to run `./gradlew` instead of `gradlew`.

If you want to install the runner application to any devices connected in debug mode, you can run `gradlew installRunnerDebug`.

Do not directly install the stub APK on your device, only do that for the runner application. In regards to the stub, after the Gradle build command succeeds, there is now a file in release/stub/nvgt_android.bin which should be moved into the stub folder of your actual NVGT installation, allowing NVGT to compile .APK files from game source code.



## Building NVGT for linux

### Building with the `build_linux.sh` script
There is a [script to build NVGT on Linux](https://raw.githubusercontent.com/samtupy/nvgt/main/build/build_linux.sh) (tested on Debian and Ubuntu). It tends to build pretty portably so you can run it basically anywhere, and it will attempt to successfully download all required dependencies and build them for you. The result will be a fully built NVGT.

Internally, this script is used within our GitHub Actions to make builds of NVGT. It is also used within our local testing environments.

#### Notes
* This script will currently only run on systems where `apt` and `pip` are installed, and does not support any other package managers.
* This script will create and activate a [virtual environment](https://docs.python.org/3/library/venv.html).

This script can be ran in two modes:
* Adding `ci` as an argument causes the dependencies to be downloaded in the current working directory inside a `deps` folder (useful if you already are working from within NVGT's source directory).
* If `ci` is not present, the script will assume NVGT is not downloaded and will clone NVGT into the current directory before attempting to build it.

#### Example of Running the script with the `ci` argument
It is assumed you are in a freshly-cloned NVGT, so that your working directory ends with `nvgt`.
```
chmod +x build/build_linux.sh
./build/build_linux.sh ci
```

It will then attempt to download all required packages and build NVGT. This will take some time.

#### Example of Running the script without the `ci` argument
Insure you are in a working directory where you are okay with the script making a few folders; in particular `deps` and `nvgt`. This is where all of the downloading, building, etc. will occur. The below example assumes that build_linux.sh is in the same directory, but it does not assume NVGT is already downloaded.
```
chmod +x build_linux.sh
./build_linux.sh
```

### Building NVGT manually
If you wish to build manually, some rather old instructions are below. At this time, it would probably be much more beneficial to read the `build_linux.sh` script or [readme.md](https://github.com/samtupy/nvgt) for much more updated commands; the below commands are here for reference and aren't updated often.

Please keep in mind that this is a very very rough draft, I've only done this once before when I built nvgt's server components for stw. This will attempt to describe, even for a user who doesn't use linux much, how to build nvgt at least on Ubuntu 22.04 LTS.

### tools
You will need the GNU compiler collection / GNU make / a few other tools. You can see if you already have these on your installation by running `gcc`, `g++`, `make`. If this fails, run `sudo apt install build-essential gcc g++ make autoconf libtool`.

### commands
```bash
mkdir deps && cd deps
git clone https://github.com/codecat/angelscript-mirror
cd deps/angelscript-mirror/sdk/angelscript/projects/gnuc
make
sudo make install

sudo apt install libssl-dev libcurl4-openssl-dev libopus-dev libsdl2-dev
sudo apt remove libsdl2-dev
```

### Note
The first command installs a version of SDL that is too old, but still installs loads of deps. Now we will build sdl.

`cd deps`

Before continuing, download sdl into a folder called SDL.

```bash
mkdir SDL_Build
cd SDL_Build
cmake ../SDL
cmake --build .
sudo cmake --install .

cd deps
git clone https://github.com/pocoproject/poco
cd poco
./configure --static --no-tests --no-samples --cflags=-fPIC
make -s -j2
```

### Note
The 2 in `make -j2` is how many CPU cores you would like to use when building. Change this to the number of CPU cores you would like to use. If you do not know how many cores your system has, you can use the `lscpu` command on many distributions to check.

```bash
sudo make install

cd deps
git clone https://github.com/lsalzman/enet
cd enet
autoreconf -vfi
./configure
make
sudo make install

cd deps
git clone https://github.com/bulletphysics/bullet3
cd bullet3
./build_cmake_pybullet_double.sh
cd cmake_build
sudo cmake --install .
```

```bash
cd deps
git clone https://github.com/libgit2/libgit2
cd libgit2
mkdir build
cd build
cmake ..
cmake --build .
sudo cmake --install .
```

You will need scons, which you can get by running pip3 install scons.

### Finally...
cd to the root of the nvgt repository and extract https://nvgt.dev/lindev.tar.gz to a lindev folder there.

scons -s

Enjoy!


## Building NVGT for MacOS

### Building with the `build_macos.sh` script
There is a [script to build NVGT on macOS](https://raw.githubusercontent.com/samtupy/nvgt/main/build/build_macos.sh). It will build pretty portably so you can run it basically anywhere (assuming you have Homebrew and the Xcode command line tools). It will attempt to successfully download all required dependencies and build them for you. The result will be a fully built NVGT.

Internally, this script is used within our GitHub Actions to make builds of NVGT. It is also used within our local testing environments.

#### Notes
* This script will create and activate a [virtual environment](https://docs.python.org/3/library/venv.html).

This script can be ran in two modes:
* Adding `ci` as an argument causes the dependencies to be downloaded in the current working directory inside a `deps` folder (useful if you already are working from within NVGT's source directory).
* If `ci` is not present, the script will assume NVGT is not downloaded and will clone NVGT into the current directory before attempting to build it.

#### Example of Running the script with the `ci` argument
It is assumed you are in a freshly-cloned NVGT, so that your working directory ends with `nvgt`.
```
chmod +x build/build_macos.sh
./build/build_macos.sh ci
```

It will then attempt to download all required packages and build NVGT. This will take some time.

#### Example of Running the script without the `ci` argument
Insure you are in a working directory where you are okay with the script making a few folders; in particular `deps` and `nvgt`. This is where all of the downloading, building, etc. will occur. The below example assumes that build_macos.sh is in the same directory, but it does not assume NVGT is already downloaded.

```
chmod +x build_macos.sh
./build_macos.sh
```


### Building NVGT manually
If you wish to build manually, some rather old instructions are below. At this time, it would probably be much more beneficial to read the `build_macos.sh` script or [readme.md](https://github.com/samtupy/nvgt) for much more updated commands; the below commands are here for reference and aren't updated often.

Assuming xcode and homebrew are installed:

```bash
pip3 install scons
brew install autoconf automake libgit2 libtool openssl sdl2 bullet

mkdir deps
git clone https://github.com/codecat/angelscript-mirror
cd "angelscript-mirror/sdk/angelscript/projects/cmake"
mkdir build; cd build
cmake ..
cmake --build .
sudo cmake --install .

cd deps
git clone https://github.com/lsalzman/enet
cd enet
autoreconf -vfi
./configure
make
sudo make install

cd deps
git clone https://github.com/pocoproject/poco
cd poco
./configure --static --no-tests --no-samples
make -s -j<n> where <n> is number of CPU cores to use
sudo make install

cd deps
git clone https://github.com/libgit2/libgit2
cd libgit2
mkdir build
cd build
cmake ..
cmake --build .
sudo cmake --install .

cd nvgt
scons -s
```


## Debugging Scripts
One very useful feature of NVGT is the ability to debug the scripts that you write. This means being able to pause script execution at any time (either triggered manually or automatically), view what's going on and even make changes or inject code, and then resume the execution. You can even execute one statement in your code at a time to get an idea of exactly what it is doing.

### The -d or --debug option
To debug a script in nvgt, it is required that you use the command line version of nvgt (nvgt.exe). On platforms other than Windows, only a command line version is available.

There is a command line argument you must pass to nvgt.exe along with the script you want to run in order to debug it, which is either -d, or --debug depending on what you prefer.

So for example, open a command prompt or terminal and change directory to the place where you have stored your game. You could then run, for example, `nvgt -d mygame.nvgt` assuming a correct installation of nvgt, which would cause mygame.nvgt to be launched with the Angelscript debugger getting initialized.

### the debugging interpreter
When you run a script with the debugger, it will not start immediately. Instead, you will be informed that debugging is in progress, that the system is waiting for commands, and that you can type h for help.

If the last line on your terminal is \[dbg\]\> , you can be sure that the system is waiting for a debug command.

If you press enter here without first typing a command, the last major debugger action is repeated. This is not necessarily the last command you have typed, but is instead the last major action (continue, step into, step over, step out). The default action is to continue, meaning that unless you have changed the debugger  action, pressing enter without typing a command will simply cause the execution of your script to either begin or resume where it left off.

Pressing ctrl+c while the debug interpreter is open will exit out of nvgt completely similar to how it works if the debugger is not attached. Pressing this keystroke while the interpreter is not active will perform a user break into the debugger, meaning that your script will immediately stop executing and the debug interpreter will appear.

To list all available commands, type h and enter. We won't talk about all of the commands here, but will discuss a few useful ones.

### Useful debugging commands
* c: set debugger action to continue, execute until next breakpoint or manual break
* s: set debugger action to step into, only execute the next instruction
* n: set debugger action to step over, execute until next instruction in current function
* o: set debugger action to step out, execute until the current function returns
* e \<return-type\> \<expression\>: Evaluate a simple code statement, anything from a simple math expression to calling a function in your script.
* p \<value\>: print the value of any existing variable
* l: list various information, for example "l v" would list local variables
* b: set a function or file breakpoint, type b standalone for instructions
* a: abort execution (more graceful version of ctrl+c)

### registered debugging functions
If you are working with a troublesome bit of code, you may find that breaking into the debugger at a specific point is a very helpful thing to do. For this situation, NVGT has the `debug_break()` function.

This function will do nothing if called without a debugger attached or from a compiled binary, so it is OK to leave some calls to this around in your application so long as you are aware of them for when you run your script with the debugger. This function will immediately halt the execution of your script and cause the debugger interpreter to appear.

You can also programmatically add file and function breakpoints with the functions `void debug_add_file_breakpoint(string filename, int line_number)` and `void debug_add_func_breakpoint(string function_name)`.

### breakpoints
To describe breakpoints, we'll break (pun intended) the word into it's 2 parts and describe what the words mean in this context.
* When debugging, a break means pausing your script's execution and running the debugging interpreter.
* In this context, a point is either a file/line number combo or a function name which, if reached, will cause a debugger break.

For example if you type the debug command "b mygame.nvgt:31" and continue execution, the debugging interpreter will run and the script execution will halt before line31 of mygame.nvgt executes.

It is also possible to break into the debugger whenever a function is about to execute, simply by passing a function name instead of a file:line combo to the b debug command.

### notes
* It is worth noting that when the debugger interpreter is active, your script's execution is completely blocked. This means that any window you have shown will not be processing messages. Some screen readers don't like unresponsive windows that well, so be careful when breaking into the debugger while your game window is showing! Maybe in the future we can consider a setting that hides the game window whenever a debug break takes place.
* This debugger has not been tested very well in a multi-threaded context, for example we do not know what happens at this time if 2 threads call the debug_break() function at the same time. We intend to investigate this, but for now it's best to debug on the main thread of your application. In particular no commands exist as of yet to give contextual thread information.


## Notes on NVGT's documentation generator

### format of the src directory

* topics may be in .md or .nvgt format at this time. When NVGT becomes a c++ library as well, we may add ability to perform basic parsing of .h files.
* Directories are subsections and can be nested.
* Sections and subsections, starting at NVGTRepoRoot/doc/src, are scanned for topics with the following rules in mind:
    * If a .index.json file exists, this file is loaded and parsed to create the topic list. The json is a list containing either strings or 2-element lists. If a string, just indicates a topic filename. If a list, the first element is a topic filename string and the second is a topic display name string if the topic filename isn't adequate.
    * If a .index.json file does not exist, topics/subsections are loaded in alphabetical order. A topic C will appear before a subsection F.
    * Unless a .index.json file specifies a topic display name, the topic filename minus the extension is used as the topic name. Punctuation characters at the beginning of the display name are removed to provide for more flexible sorting. A subsection !C will show before a subsection F, but !C will display C thus allowing for multiple sorting levels without a .index.json file.
    * If there is a .MDRoot file present in a directory, the contents of that directory are output in new markdown/html documents instead of being appended to the main/parent documents, and a link to the new document is appended to the parent one.
    * If a topic filename contains an @ character right before the extension, that document is treated as a new markdown root document in the final output instead of being appended to the main/parent document, this is just a way to invoque the same as above but for a single file.
    * If a topic filename contains a + before the extension, the first line in the file minus markdown heading indicators will be used as the topic display name instead of a titlecased topic filename.
* .nvgt files contain embedded markdown within comments. Most markdown syntax is the same, except that nvgt's docgen script replaces single line breaks with double lines so that each line is a markdown paragraph. Start a docgen comment with /**, and start a docgen comment with the above mentioned linefeed behavior disabled with /**\.
* Another embedded markdown comment within .nvgt files is the "// example:" comment, which will be replaced with "## example" in markdown.
* When parsing a .nvgt file, a "# topicname" markdown directive is added to the top of the output to avoid this redundant step in example functions.
* The docgen program creates a .chm file which requires parsing this markdown into html, and there may be reasons for removing embedded markdown indentation anyway. This resulted in an indentation rule where tabs are stripped from the document when passed to the python markdown package, spaces are not and can be used for things like nested lists.
* If the very first topic in any category begins with a heading with the same name as the containing category, the heading name is stripped from the markdown and html output of the documentation, and the heading indentation of that topic is set to that of the parent category. This allows one to easily create intro sections for categories without creating duplicate headings with the same name. The heading is stripped after the single html/chm version of that topic is printed, as such a heading should remain in the chm documentation.

### Installing the Microsoft HTML help compiler
Because of it's simple format and easy distribution, we still prefer to generate the NVGT documentation as a .chm file (compressed HTML help). Unfortunately, the link to the html help workshop installer has been broken by Microsoft for a couple of years now. Fortunately, the installer for this program was archived from Microsoft's official website by the wayback machine. Until we get a better link, you should be able to [download it here](http://web.archive.org/web/20200312222543/http://download.microsoft.com/download/0/A/9/0A939EF6-E31C-430F-A3DF-DFAE7960D564/htmlhelp.exe), though it should be noted that only those wishing to rebuild nvgt's documentation from source will need this program.


## Plugin Creation
Does NVGT not provide the function you need, and do you know a bit of c++? If so, perhaps NVGT plugins are exactly what you're looking for!

This document will describe all there is to know about creating nvgt plugins, both dynamically and statically.

### What is a plugin in the context of NVGT?
An NVGT plugin, in it's most basic form, is simply a module of code that is executed during the script loading part of the engine initialization process, one which can extend the functionality of NVGT by directly gaining access to and registering functions with it's internal Angelscript engine.

Plugins are not just limited to functions, but classes, enums, funcdefs and anything else one could register normally using the Angelscript scripting library.

### Types of plugin builds
A plugin can either be a shared library (.dll / .dylib / .so) that gets loaded when needed, or a static library (.lib / .a) that is linked directly into a custom build of NVGT. Both methods have different advantages and disadvantages.

Dynamically loaded plugins, those built into a shared library, are easier to get working with NVGT because it's far easier to create such a plugin without at all altering NVGT's build process or adding things to it. You could use your own build system and your own environment, so long as the proper ABI is exposed to NVGT in the end and an up-to-date version of Angelscript is used within your plugin. However, a smart player may figure out how to replace your plugin dll with some sort of malicious copy, your dll plugin could be duplicated and reused in other projects, you'll have an extra dll file to release with your game distribution etc.

Static plugins on the other hand, while a bit tougher to build, are certainly more rewarding in the end. From plugin code being packaged directly into your binary to a smaller distribution size because of no duplicated crt/other code in a dll to direct integration with NVGT's build system, there are several advantages that can be observed when choosing to create a static plugin.

If one chooses to follow every step of the existing NVGT plugin creation process that is used internally by engine developers, you can set up your plugin such that it can easily be built either dynamically or statically depending on the end-user's preference.

### The basic idea
In short, the idea here stems from a pretty simple base. The user creates a .cpp file that includes the nvgt_plugin.h header that can do any magic heavy lifting needed, then the user just defines an entry point using a macro declared in nvgt_plugin.h. This entry point receives a pointer to the asIScriptEngine instance used by NVGT, which the plugin developer can do anything they please with from registering custom functions to installing some sort of custom profiler. The entry point can return true or false to indicate to NVGT whether the plugin was able to successfully initialize.

This plugin entry point always takes one argument, which is a structure of data passed to it by NVGT. The structure contains the Angelscript engine pointer as well as pointers to several other Angelscript functions that may be useful, and may be expanded with pointers to other useful interfaces from NVGT as well. One just simply needs to call a function provided by nvgt_plugin.h called prepare_plugin passing to it a pointer to the aforementioned structure before their own plugin initialization code begins to execute.

To link a static plugin with the engine assuming the nvgt's build script knows about the static library file, one need only add a line such as static_plugin(\<plugname\>) to the nvgt_config.h file where \<plugname\> should be replaced with the name of your plugin.

### small example plugin
```
#include <windows.h>
#include "../../src/nvgt_plugin.h"

void do_test() {
	MessageBoxA(0, "It works, this function is being called from within the context of an NVGT plugin!", "success", 0);
}

plugin_main(nvgt_plugin_shared* shared) {
	prepare_plugin(shared);
	shared->script_engine->RegisterGlobalFunction("void do_test()", asFUNCTION(do_test), asCALL_CDECL);
	return true;
}
```

#### picking it apart
We shall forgo any general comments or teaching about the c++ language itself here, but instead will just focus on the bits of code that specifically involve the plugin interface.

The first thing that you probably noticed was this include directive which includes "../../src/nvgt_plugin.h". Why there? While this will be described later, the gist is that NVGT's build setup already has some infrastructure set up to build plugins. NVGT's github repository has a plugin folder, and in there are folders for each plugin. This example is using such a structure. We will talk more in detail about this later, but for now it is enough to know that nvgt_plugin.h does not include anything else in nvgt's source tree, and can be safely copy pasted where ever you feel is best for your particular project (though we do recommend building plugins with NVGT's workspace).

The next oddity here, why doesn't the plugin_main function declaration include a return type? This is because it is a macro defined in nvgt_plugin.h. It is required because the name of the entry point will internally change based on whether you are compiling your plugin statically or dynamically. If you are building your plugin as a shared library, the function that ends up exporting is called nvgt_plugin. However since one of course cannot link 2 static libraries with the same symbol names in each to a final executable, the entry point for a static plugin ends up being called nvgt_plugin_\<plugname\> where \<plugname\> is replaced with the value of the NVGT_PLUGIN_STATIC preprocessor define (set at plugin build time). In the future even dynamic libraries may possibly contain the plugin name in their entry point function signatures such that more than one plugin could be loaded from one dll file, but for now we instead recommend simply registering functions from multiple plugins in one common entry point if you really want to do that.

Finally, remember to call prepare_plugin(shared) as the first thing in your plugin, and note that if your entry point does not return true, this indicates an error condition and your plugin is not loaded.

### NVGT's plugin building infrastructure
As mentioned a couple of times above, NVGT's official repository already contains the infrastructure required to build plugins and integrate them with NVGT's existing build system, complete with the ability to exclude some of your more private plugins from being picked up by the repository. While it is not required that one use this setup and in fact one may not want to if they have a better workspace set up for themselves, we certainly recommend it especially if you are making a plugin that you may want to share with the NVGT community.

#### The plugin directory
In nvgt's main repository, the plugin directory contains all publicly available plugins. Either if you have downloaded NVGT's repository outside of version control (such as a public release artifact) or if you intend to contribute your plugin to the community by submitting a pull request, you can feel free to use this directory as well.

Here, each directory is typically one plugin. It is not required that this be the case, other directories that are not plugins can also exist here, however any directory within the plugin folder that contains a file called _SConscript will automatically be considered as a plugin by the SConstruct script that builds NVGT.

The source code in these plugins can be arranged any way you like, as it is the _SConscript file you provide that instructs the system how to build your plugin.

An example _SConscript file for such a plugin might look like this:
```
# Import the SCons environment we are using
Import("env")

# Create the shared version of our plugin if the user has not disabled this feature.
if ARGUMENTS.get("no_shared_plugins", "0") == "0":
	env.SharedLibrary("#release/lib/test_plugin", ["test.cpp"], libs = ["user32"])

# If we want to make a static version along side our shared one, we need to specifically rebuild the object file containing the plugin's entry point with a different name so that SCons can maintain a proper dependency graph. Note the NVGT_PLUGIN_STATIC define.
static = env.Object("test_plugin_static", "test.cpp", CPPDEFINES = [("NVGT_PLUGIN_STATIC", "test_plugin")])
# now actually build the static library, reusing the same variable from above for fewer declarations.
static = env.StaticLibrary("#build/lib/test_plugin", [static])

# Tell NVGT's SConstruct script that the static version of this plugin needs symbols from the user32 library.
static = [static, "user32"]

# What is being returned to NVGT's SConstruct in the end is a list of additional static library objects that should be linked.
Return("static")
```

Note that while the above example returns the user32 library back to NVGT's build script, it should be noted that most system libraries are already linked into nvgt's builds. The example exists to show how an extra static library would be passed to NVGT from a plugin if required, but this should only be done either as a reaction to a linker error or if you know for sure that your plugin requires a dependency that is not automatically linked to NVGT, examples in the git2, curl or sqlite3 plugins.

#### the user directory
NVGT's github repository also contains another root folder called user. This is a private scratchpad directory that exists so that a user can add plugins or any other code to NVGT that they do not want included in the repository.

First, the repository's .gitignore file ignores everything in here accept for readme.md, meaning that you can do anything you like here with the peace of mind that you won't accidentally commit your private encryption plugin to the public repository when you try contributing a bugfix to the engine.

Second, if a _SConscript file is present in this directory, NVGT's main build script will execute it, providing 2 environments to it via SCons exports. The nvgt_env environment is what is used to directly build NVGT, for example if you need any extra static libraries linked to nvgt.exe or the stubs, you'd add one by importing the nvgt_env variable and appending the library you want to link with to the environment's LIBS construction variable.

Last but not least, if a file called nvgt_config.h is present in the user folder, this will also be loaded in place of the nvgt_config.h in the repo's src directory.

You can do whatever you want within this user directory, choosing to either follow or ignore any conventions you wish. Below is an example of a working setup that employs the user directory, but keep in mind that you can set up your user directory any way you wish and don't necessarily have to follow the example exactly.

##### user directory example
The following setup is used for Survive the Wild development. That game requires a couple of proprietary plugins to work, such as a private encryption layer.

In this case, what was set up was a second github repository that exists within the user directory. It's not a good idea to make a github repository out of the root user folder itself because git will not appreciate this, but instead a folder should be created within the user directory that could contain a subrepository. We'll call it nvgt_user.

The first step is to create some jumper scripts that allow the user folder to know about the nvgt_user repository contained inside it.

user/nvgt_config.h:
```
#include "nvgt_user/nvgt_config.h"
```
and

user/_SConscript:
```
Import(["plugin_env", "nvgt_env"])
SConscript("nvgt_user/_SConscript", exports=["plugin_env", "nvgt_env"])
```

Now, user/nvgt_user/nvgt_config.h and user/nvgt_user/_SConscript will be loaded as they should be, respectively.

In the nvgt_user folder itself we have _SConscript, nvgt_plugin.h, and some folders containing private plugins as well as an unimportant folder called setup we'll describe near the end of the example.

nvgt_config.h contains the custom encryption routines / static plugin configuration that is used to build the version of NVGT used for Survive the Wild.

The user/nvgt_user/_SConscript file looks something like this:
```
Import("plugin_env", "nvgt_env")

SConscript("plugname1/_SConscript", variant_dir = "#build/obj_plugin/plugname1", duplicate = 0, exports = ["plugin_env", "nvgt_env"])
SConscript("plugname2/_SConscript", variant_dir = "#build/obj_plugin/plugname2", duplicate = 0, exports = ["plugin_env", "nvgt_env"])
# nvgt_user/nvgt_config.h statically links with the git2 plugin, lets delay load that dll on windows so that users won't get errors if it's not found.
if nvgt_env["PLATFORM"] == "win32":
	nvgt_env.Append(LINKFLAGS = ["/delayload:git2.dll"])
```
And finally an _SConscript file for nvgt_user/plugname\* might look something like this:
```
Import(["plugin_env", "nvgt_env"])

static = plugin_env.StaticLibrary("#build/lib/plugname2", ["code.cpp"], CPPDEFINES = [("NVGT_PLUGIN_STATIC", "plugname2")], LIBS = ["somelib"])
nvgt_env.Append(LIBS = [static, "somelib"])
```
As you can see, the decision regarding the custom plugins used for Survive the Wild is to simply not support building them as shared libraries, as that will never be needed from the context of that game.

The only other item in the private nvgt_user repository used for Survive the Wild is a folder called setup, and it's nothing but a tiny all be it useful convenience mechanism. The setup folder simply contains copies of the user/_SConscript and user/nvgt_config.h files that were described at the beginning of this example, meaning that if nvgt's repository ever needs to be cloned from scratch to continue STW development (such as on a new workstation), the following commands can be executed without worrying about creating the extra files that are outside of the nvgt_user repository in the root of the user folder:

```bash
git clone https://github.com/samtupy/nvgt
cd nvgt/user
git clone https://github.com/samtupy/nvgt_user
cp nvgt_user/setup/* .
```

And with that, nvgt is ready for the private development of STW all with the custom plugins still being safely in version control! So long as the cwd is outside of the nvgt_user directory the root nvgt repository is effected, and once inside the nvgt_user directory, that much smaller repository is the only thing that will be touched by git commands.

Remember, you should use this example as a possible idea as to how you could potentially make use of NVGT's user directory, not as a guide you must follow exactly. Feel free to create your own entirely different workspace in here or if you want, forgo use of the user directory entirely.

#### Angelscript addon shims
When creating a shared/dynamic plugin made up of more than 1 cpp file, you must `#define NVGT_PLUGIN_INCLUDE` and then `#include "nvgt_plugin.h"` before you `#include <angelscript.h>`. This is to make sure that any additional units you build will use the manually imported Angelscript symbols that were passed to the plugin from NVGT, a multiple defined symbol error might appear otherwise or if your code compiles, 2 different versions of the Angelscript functions could be used which would be very unsafe. To make it easier to include Angelscript addons into your plugins, little shims are provided for the common addons in the nvgt repository in the ASAddon/plugin directory. You can simply compile ASAddon/plugin/scriptarray.cpp, for example, and the scriptarray plugin will safely be included into your plugin. nvgt_plugin.h should still be included before scriptarray.h in any of your plugin source files, however.

When compiling a static plugin, you do not need to bother linking with these addon shims, because in that case your plugin's static library will be linked with NVGT when NVGT is next recompiled, and NVGT already contains working addons.

### plugin dll loading
A common sanario is that you may wish to make a plugin that then loads another shared library. This happens already in nvgt, particularly with the git2 plugin. The plugin itself is called git2nvgt, but it loads git2.dll. This calls for some consideration.

NVGT applications generally put their libraries in a lib folder to reduce clutter in the applications main directory. This isn't required, and in fact if you want to move all shared objects out of the lib folder and put them along side your game executable, you actually tend to avoid the small issue mentioned here. The problem is that sometimes, we need to explicitly tell the operating system about the lib directory at runtime (right now true on windows) in order for it to find the shared libraries there.

For shared/dynamic plugins, this isn't really an issue. NVGT has launched, informed the system of the lib directory, and loaded your plugin in that order meaning that any dll your plugin imports can already be located and imported just fine.

With static plugins, on the other hand, we must work around the fact that the operating system will generally try loading all libraries that the program uses before any of that program's code executes, and will show the user an error message and abort the program if it can't find one. Returning to the git2 example from earlier, if you were to ship this plugin with your game, a file would exist called lib/git2.dll on windows. When the static library git2nvgt.lib is created, it will add git2.dll to it's import table but with no knowledge of the lib folder at that point. When the custom build of NVGT which includes this plugin tries to run, an error message will appear because git2.dll can't be found, on account of NVGT never being able to tell the system about the lib directory before the operating system evaluates nvgt's import table and tries to load the libraries found within.

The solution, at least on windows, is delayed dll loading. It is demonstrated above in the user directory example, but it's easy to gloss over considering it's level of importants. If you add the linkflag `/delayload:libname.dll` to your static plugin's build script, now NVGT's code is allowed to execute meaning it can tell the system about the lib directory, and then the dll will load the first time a function is called from it. On MacOS/clang, there is the linkflag -weak_library which does something similar, used like `-weak_library /path/to/library.dylib`.

Delay loading does has the disadvantage that the app tends to crash if the dll is not present when it is needed rather than giving the user a nice error message, but you can work around that by manually loading the dll with the LoadLibrary function on windows / similar facilities on other platforms then immediately unloading it just to see if the system will be able to find it, and you can choose to show an error message in that case if you wish.

### cross platform considerations
If you are only building plugins for projects that are intended to run on one platform, this section may be safely skipped. However if your game runs on multiple platforms and if you intend to introduce custom plugins, you probably don't want to miss this.

There are a couple of things that should be considered when creating plugins intended to run on all platforms, but only one really big one. In short, it is important that a cross platform plugin's registered Angelscript interface looks exactly the same on all platforms, even if your plugin doesn't support some functionality on one platform. For example if your plugin has functions foo and bar but the bar function only works on windows, it is important to register an empty bar function for any non-windows builds of your plugin rather than excluding the bar function from the angelscript registration of such a plugin build entirely. This is especially true if you intend to, for example, cross compile your application with the windows version of NVGT to run on a linux platform.

The reasoning is that Angelscript may sometimes store indexes or offsets to internal functions or engine registrations in compiled bytecode rather than the names of them. This makes sense and allows for much smaller/faster compiled programs, but what it does mean is that NVGT's registered interface must appear exactly the same both when compiling and when running a script. Maybe your plugin with foo and bar functions get registered into the engine as functions 500 and 501, then maybe the user loads a plugin after that with boo and bas functions that get registered as functions 502 and 503. Say the user makes a call to the bas function at index 503. Well, if the foo bar plugin doesn't include a bar function on linux builds of it, now we can compile the script on windows and observe that the function call to bas at index 503 is successful. But if I run that compiled code on linux, since the bar function is not registered (as it only works on windows), the bas function is now at index 502 instead of 503 where the bytecode is instructing the program to call a function. Oh no, program panic, invalid bytecode! The solution is to instead register an empty version of the bar function on non-windows builds of such a plugin that does nothing.

### Angelscript registration
Hopefully this document has helped you gather the knowledge required to start making some great plugins! The last pressing question we'll end with is "how does one register things with NVGT's Angelscript engine?" The angelscript engine is a variable in the nvgt_plugin_shared structure passed to your plugins entry point, it's called script_engine.

The best reference for how to register things with Angelscript is the Angelscript documentation itself, and as such, the following are just a couple of useful links from there which should help get you on the right track:
* [registering the application interface](https://www.angelcode.com/angelscript/sdk/docs/manual/doc_register_api_topic.html)
* [registering a function](https://www.angelcode.com/angelscript/sdk/docs/manual/doc_register_func.html)
* [registering global properties](https://www.angelcode.com/angelscript/sdk/docs/manual/doc_register_prop.html)
* [registering an object type](https://www.angelcode.com/angelscript/sdk/docs/manual/doc_register_type.html)

Good luck creating NVGT plugins, and feel free to share some of them to the community if you deem them worthy!



# appendix
This section contains miscellaneous documents such as license agreements, lists of static information, etc.


## To do list
NVGT is still a relatively young project with many areas that need improvement, and there are also several long-term goals for this project that are not yet realized. This document attempts to keep track of any intended development activity that has not yet taken place, both for existing NVGT developers and for anyone looking to find a way to help contribute to the engine.

### User facing items
Items in this section generally effect end-users in some way and are not related directly to the codebase. Items may include classes we intend to add to the engine or areas of the website we wish to improve.

#### Documentation
There has been absolutely loads of work so far put into documenting NVGT's API reference and feature set, but the task is not complete. Any contributions to the docs are welcome.

#### examples
We have been holding off on these until the API stabalizes so that we don't teach people things that are soon to be changed and because we're limited to a public domain sound catelog, but we need to create several example projects that can help get people started with NVGT. Not just for the docs, but full runnable projects in the other repository. They should range from basic card game to small platformer to online client where people can walk around.

#### Joystick object
The joystick class in NVGT is still a no-op interface. There has already been a bit of code to begin the process of wrapping SDL's joystick support, but it is not yet complete.

#### tone_synth
Another object from BGT we have not yet reimplemented, though the beginnings of tone generation will appear in miniaudio.

#### Speech dispatcher and the `tts_voice` object
Currently, NVGT's Speech Dispatcher implementation for Linux only works with the screen reader speech functions. At this time, we are still considering if we should implement it into the `tts_voice` object as well.

#### VSCode extension
A plan that has existed for a few months now is to create a VSCode extension for Angelscript that works with NVGT scripts. To facilitate this we have wrapped a function called script_dump_engine_configuration, an example of which you can see in test/quick/dump_engine_config.nvgt. This function dumps a complete reference of everything registered in the engine, enough to compile scripts. This will, once time permits to learn the needed components, allow us to create an extension for VSCode that allows everything from symbol lookup to intellisense. As of 0.89.0 many of the function and method parameters have been properly named, which helps us get just a bit closer to this goal.

#### JAWS keyhook
There has been loads of progress made with NVGT's JAWS keyhook, and it should now work in almost all senarios. The only thing to be aware of is that if JAWS crashes, you may have to alt+tab a couple of times. Other than that though, the keyhook is stable and useable!

#### SDL dialog boxes
At the moment, we are using SDL's message box system to show simple dialogs rather than implementing it on our own. However, this implementation is not ideal for 3 reasons.
1. shortcuts with an ampersand don't work, we can't create a button called `&yes` that works with alt+y.
2. Copying text does not work with ctrl+c.
3. No internationalization, yes and no buttons are English on non-English windows.
Either we will see if SDL will improve message boxes soon, or switch to something else.

#### Switch to miniaudio (in progress)
Currently we use the Bass audio library for sound output, which functionally speaking does work great. However Bass is not open source, and a commercial license must be purchased from [Un4seen](https://www.un4seen.com/bass.html) in order to sell commercial projects. For NVGT, this is not ideal and Bass was only used because it worked quite well at the time that NVGT was only being used to bolster Survive the Wild development with no opensource intentions. Instead, we plan to switch to [miniaudio](https://github.com/mackron/miniaudio) which is open source and in the public domain, and thus which will solve such commercial licensing issues. There has been much progress here and we are hopefully to have miniaudio integrated soon.

#### Recording from a microphone
Especially since Survive the Wild has implemented voice chat support, people rightfully wonder how to record audio in NVGT. Survive the Wild does this with a plugin specifically designed for it's voice chat. The API is not one which we wish to support publicly as it is very limited and confined to stw's use case. This should come soon as miniaudio implementation has made much progress.

#### Subscripting improvements
* NVGT allows a scripter to execute Angelscript code from within their Angelscript code, such as the python eval function. The user is given control of what builtin NVGT functions and classes these subscripts have access to, but it's still a bit rough. Basically Angelscript provides us with this 32 bit DWORD where we can map certain registered functions to bitflags and restrict access to them if a calling module's access bitmask doesn't include a flag the functions were registered with. However this means that we have 32 systems or switches to choose from, so either we need to assign builtin systems to them in a better way, or investigate this feature Angelscript has which is known as config groups and see if we can use them for permission control. C++ plugins in particular complicate this issue.
* Register asIScriptObject and asITypeInfo which would allow people to traverse script classes and execute functions in them.

#### Provide user facing pack file encryption
Currently pack file encryption uses internal methods requiring a user to rebuild NVGT to change the encryption routines, but there is full intention of also adding a `pack.set_encryption` so that users of NVGT can also manage how their packs are encrypted. A secondary SQL based pack file object has been contributed to the project which does include this functionality though we still intend to make it a part of the smaller, primary pack object. A contributor is in the process of implementing this functionality to be included with miniaudio.

#### CI improvements
NVGT is now set up to work with the Github releases page for it's next release, and at this time anyone can fork the project and run the release action to build the latest development version of the engine. However, the process isn't yet automated and we'd like to set up builds on some sort of schedule so that users can download the latest development NVGT for all platforms by just clicking a link. We also need to separate the public version docs with the development version docs on the website instead of showing the development version all the time, which is seriously confusing users of the public builds of the engine.

#### anticheat
We have some pull requests open regarding anticheat particularly on windows, those should be finished up and merged.

#### Angelscript version checks
One issue we run into relatively often is that someone will try building NVGT from source and then will report bytecode load errors to us because they're running from an outdated stub or something similar. We should encode the Angelscript version string into the bytecode payload and verify it upon application load. This way if bytecode gets attached to the wrong stub, we can catch it with a graceful error message instead of showing some random bytecode load aerror.

#### get_last_error()
One area of NVGT that still needs heavy improvement is error handling. Some things use exceptions, some libraries have a get_error function, some things may use the backwards compatibility function get_last_error() etc. We need to find a way to unify this as much as possible into one system.

#### library object
NVGT does have a library object similar to BGT which allows one to call into most standard dlls. However NVGT's library object is still rougher than BGT's and could do with some work, particularly we may switch to libffi or dyncall or something like that. This object in nvgt is so sub-par because the engine's open source nature combined with the c++ plugins feature deprioritised the fixing of this system to the point where it remained broken beyond the official prerelease of NVGT. The library object functions, but one may have an issue for example when working with various types of pointers.

#### dictionary serialization
Currently, NVGT's dictionaries can only serialize bool, int, double and string. This is highly limiting. In Angelscript we can traverse the properties of any class instance and even read the properties from it. Therefor, at least so long as a class inherits from a certain base of some kind, the user should be able to serialize and deserialize full objects including graceful handling for class structures changing over time.

#### force_key methods
A rare request is that we add bgt's force_key_down/force_key_up methods and friends to the engine, this is a good idea and we will do so. We are very close now with the new simulate_key_down and simulate_key_up functions, the only difference between these and the force methods is that the player still controls the keyboard E. simulate arrow down then real arrow down followed by real arrow up means arrow released, where as with bgt force methods the arrow key would stay forced down until manually reset.

#### nvgt.dll
A very long-term goal is to export as much of the engine as possible into a cdll so that it's features can be integrated into anyone's programs in other languages.

#### Very basic graphics
No work has been done here yet, but a goal of ours is to utilize sdl / sdlttf to allow audio game developers to draw at least basic text to the screen, if not much more.

#### wrap more of Poco
Poco is a massive library with many useful classes that touch on many areas, from networking to a process launcher to our datetime facility to several other utilities. We want to wrap much more of this library, including but not limited to:
* configuration facility, it supports various formats and is extensible.
* SMTP, we can send emails directly from nvgt game servers if we wrap this.
* more sockets, we've registered raw tcp socket and web_socket, we should register the datagram socket, dialog socket, raw socket and more, though some are pretty low priority.
* ProcessRunner and pipes or at least something similar to it, people want to capture process output.
* Logging facility potentially. Do we need it or do I just think it's cool?
* Notification queues for interthread communication.
* UUID, I've held off because it forces us to use their bsd3 licensed random number generator but it could still be useful.

#### audio_form rewrite
While the current audio form will always be here for backwards compatibility, it is unfortunately very old code which keeps gaining appendage after appendage after hack after hack in order to keep working propperly. It is a nightmare to integrate into a game translation system, control objects are private, it's just getting hardre to maintain. We need to provide a new audio form instead of encouraging people to use the existing one. Someone has started working on one, but it is in early stages given my last update on the situation.

#### input_box on Linux and Mobile
The input_box function is currently only implemented on Windows and MacOS, we need to get it working on all platforms.

#### reactphysics3d
We're working on integrating a physics engine into NVGT for much more advanced games. There are many of these out there, we chose reactphysics3d because it builds on all of our desired platforms, it's not utterly massive, it seems to contain many of the features we can imagine needing, and it does not come with a huge learning curve. Much work has been put into implementing reactphysics, though  most of it is on a different branch at this time called rp3d.

#### tts_voice parameter scaling
In bgt, tts_voice parameters went from -10 to 10 for rate and pitch, and -100 to 0 for volume. However in NVGT, this currently differs per platform. We need to set up a couple of conversion functions that make bgt's old values work across the board, though possibly in floatingpoint so as to give NVGT users more precision if they desire it.

#### package managers
This is a long-term goal, but consider figuring out how to create an apt repo / get on homebrew / other package managers for easy installs of NVGT.

#### IOS
NVGT now has Android support, leaving one more target platform which is IOS!

#### MacOS Code Signing
This is likely to be fixed very soon: Currently, it is not possible to code sign MacOS app bundles generated by NVGT, and the binaries in them do not have an executable bit set at this time. Once these issues are resolved, a vast portion of remaining MacOS issues will be resolved.

#### Authenticode signing for official installers
Currently nvgt's official installers are unsigned and I am hoping to fix that.

#### Android touchups
Android support is getting pretty stable, but there are a couple of areas that still need improvement. We still need to finish asset management, and so until that is done you must embed a pack file into your app for sounds to be played. More improvements to tts_voice will follow as well, you can only use the default voice at this time and parameter ranges may need adjustment. The gesture support though functional is still very young, and needs more testing and expansion.

### Code improvements
This section specifically lists tasks we wish to perform related to NVGT's c++ code, repository, or other backend. Other than performance, items here should rarely effect application functionality but are instead designed to allow developers to engage in a bit less painful wincing when reading or contributing to NVGT's code.

#### types.h
Due to lack of experience towards the beginning of this project's development, our types are currently all over the place. There are random and completely unneeded mixes of asUINT, uint32_t, unsigned long, unsigned int, Poco::UInt32 and more all over the project. Instead we need to create types.h that define preferably types similar to angelscript (uint8, uint16, uint32, uint64) which we can use in the project, or at least we need to choose an existing set like Poco's or Angelscript's and stick with it consistently.

#### Naming of globals
Along the same line, partly due to initial closed source intentions and also partly do to the use of sample Angelscript code, some of NVGT's global symbols are not named ideally. The best example right now is g_CommandLine vs. g_command_line_args. We need to decide on a scheme and stick to it unless forced by a dependency, and then do a quick symbol renaming session in vscode.

#### Rewrite system_fingerprint.cpp
Currently we are using parts of an apache2 licensed library for system fingerprint generation. Not only is it a bit rough but it also uses several architecture specific assembly instructions at times when we probably don't need any. We should rewrite this to use our own system instead comprised of calls into Poco, SDL and other libraries that can return various bits of system information, or at the very least find a solid tiny dependency that can handle it for us. Legacy functions will still be provided.

#### increased plugin security
Currently, one can achieve mischief by replacing a game's plugin dll with a hacked or modified version which uses the plugin's access to the underlying Angelscript engine to access sensative information within a game's loaded bytecode. While in the end we cannot prevent this entirely (it's a given downside when developing a plugin system like this that is still extensaable), but what we cann do is make it annoying. A pull request is already in progress which attempts to add cryptographic signatures to the plugin dlls loaded by a game which are verified by NVGT, at least applying an extra layer of annoyance/difficulty to anyone's attempt to go hacking around with an NVGT plugin, and it just needs some cleaning up/a bit of fixing before we can merge it. Anyone who is extremely worried about this will need to build NVGT from source with staticly linked plugins.

#### Automated process to build platform specific dev packages
Currently when someone wants to build NVGT, they download something like windev.zip or macosdev.tar.gz or droidev.zip etc. That is helpful because many people who are in the middle between something like NVGT and getting started with C++ probably only want to change a few lines of NVGT and rebuild it. It's also helpful for speeding up our CI. However the problem is that these packages are manually maintained, when in reality we should be using something like vcpkg to set these up via a CI action of some sort.

#### rewrite random.cpp somewhat
At the moment, I directly register the c interfaces of the public domain rnd.h library we are using with Angelscript. This however has created some undesirable issues, for example it's not possible to select a default rng, array.random() has several overloads for each type because they don't have a base class etc. Instead, create a base random interface with whatever generaters we want inheriting from it, then allow the user to select the default generator instance that the random() function uses.

#### test cases
NVGT has a test runner, but it only tests a minimal subset of the engine at this time. Once we have more tests, we will hook the test runner up to the CI so we can instantly see if something goes wrong with the engine.


## Changelog
This document lists all major changes that have taken place in NVGT since we started keeping track.

### New in 0.89.1-beta (10/09/2024):
* Fixes copying of shared libraries while bundling on MacOS which was resulting in an assertion violation from Poco.
* Fixes MacOS not changing to the directory of scripts launched from finder or the open command.
* Hopefully we've finally resolved all of the MacOS includes resolution issues, there should be no more manually adding include paths to your scripts or command line invocations!
* Fixes the enter key not pressing the default button in audio form lists.
* Linux cross compilation should work again, the Linux build script was pulling down the wrong version of Angelscript.
* `#pragma platform` has been deprecated, you should use the command line / menu options / UI to specify platforms instead.
* Adds preprocessor macros to check platform! You can surround code in `#if android ... #endif` for example, or `#if_not windows ... #endif` as well. You can even use this to specify custom includes or pragmas just on certain platforms.

### New in 0.89.0-alpha (10/09/2024):
* NVGT has now switched to using InnoSetup for it's installer, adding several new options such as adding to path, start menu icons etc.
* Added the script_function::get_namespace() method as well as script_function::retrieve() which takes a native function handle derived from a funcdef.
* Including pack files via the `#include` directive has been removed in favor of being able to include scripts of any extension, you should use the `#pragma embed` directive to do this instead.
* NVGT games now run on intel as well as arm mac computers!
* The calendar object is now registered as a reference type with Angelscript meaning it now supports handles, for BGT backwards compatibility. The other datetime classes are still value types.
* Added bool sdl_set_hint(const string&in hint, const string&in value, sdl_hint_priority priority = SDL_HINT_NORMAL) and string sdl_get_hint() functions, allowing the user to customize over 200 different SDL options from screen orientation to the video backend used and many more.
* Adds atomic types, or in other words more concurrency primitives.
* The array class can now work with negative indicies to access elements starting at the end of arrays, For example `array[-1]` now returns the last element in the array.
* Registered SYSTEM_PERFORMANCE_COUNTER and SYSTEM_PERFORMANCE_FREQUENCY properties as well as nanosleep and nanoticks functions, still needs documentation.
* ini.nvgt include is now free of bgt_compat! Added quick test for it.
* Fixed a bug in instance.nvgt include regarding automatic mutex name generation.
* The compiler now includes a status window that continues getting updated with messages reporting what is currently happening during compilation.
* Adds refresh_window() function, allowing manual pulling for windows events encase you want to use your own sleeping methods.
* Adds input_forms.nvgt include with functions to quickly retrieve information using an audio form, test/example in test/interact/test_input_forms.nvgt.
* Introduce new menu system based on audio form, in menu.nvgt. As a result, the old dynamic menu has been renamed to bgt_dynamic_menu.nvgt to make it clear what one is legacy.
* Registered some new vector functions such as cross, length2, distance and distance2 etc.
* datastream.available is now an uint64 rather than int.
* The ghost settings object in bgt_compat.nvgt was removed, as a new settings.nvgt include was contributed to the project! While the new settings object does not currently support the windows registry, this is made up for by several useful features such as encryption, data format selection, default values and more. You can read the top of settings.nvgt for a full list of changes. The new settings.nvgt script is `#included` by default in bgt_compat to avoid any compatibility issues.
* Though this effort is still somewhat on going, most parameters of NVGT's builtin functions and methods have been properly named. Not only does this mean that passing named arguments works, but it is also a small step closer to a VSCode or similar plugin.
* screen_reader_output/speak now have their interrupt booleans set to true by default.
* Though a more advanced (multi-selection / non-blocking) API for this will be added in the future, simple open_file_dialog, save_file_dialog, and select_folder_dialog functions have now been added.
* There are now 2 new functions which have yet to be documented, bool simulate_key_down(uint key) and bool simulate_key_up(uint key). These directly post SDL keydown/up events to the event queue.
* Any key_up events with matching keycodes as any key_down event in the same frame will now be moved to the next frame. This previously only happened with a few specialized events (namely voice over arrow keys and windows clipboard history), but now this is done in all scenarios meaning that the Mac touch bar and other on screen or touch based keyboards should now function properly.
* adds is_console_available function.
* Fixed a serious bug in pack::add_memory that caused adding large files to usually fail.
* Adds the `string generate_custom_token(int token_length, string characters);` function to token_gen.nvgt include.
* Add virtual_dialogs.nvgt include.
* Add datastream.sync_rw_cursors property (true by default).
* tts_dump_config and tts_load_config in speech.nvgt include can now save screen reader usage setting.
* ADDED ANDROID PLATFORM SUPPORT, NVGT RUNS ON MOBILE! This includes gesture detection (touch.nvgt include or query_touch_device function), screen reader speech through Android's accessibility event API, and android TextToSpeech engine support through  the tts_voice class! The support is still young and there are many improvements still to be made (only the default tts voice can be used right now and the only way to embed sounds is by using the `#pragma embed pack.dat` feature for example), but even running small nvgt scripts from source is possible at this point with NVGT's Android runner application, and one-click APK bundling is possible!
* NVGT now has a bundling facility! It can create .apk packages for android (assuming the needed android tools are available), it can create MacOS app bundles on all platforms though only a .dmg on Mac (.app.zip on other platforms), and it can copy Windows/Linux libraries into place as well as bundle your asset files like sounds, readme and changelog all to create a fully distributable package in one click! It can even run custom prebuild and postbuild shell commands in case the bundling facility isn't quite doing enough for your needs. More information is in the compiling for distribution document. This means as an aside that NVGT's compiler application is significantly larger, as it must include the MacOS and Linux libraries on windows, the Windows and Linux libraries on Mac etc for the purposes of creating a fully functional app bundle no matter what platform it is compiled on.
* The compile script submenu has changed, it now contains options to compile for all platforms you have stubs for!
* Trying to embed a pack that doesn't exist no longer makes NVGTW.exe silently exit.
* Added the is_window_hidden function.
* NVGT's UI application now has a launcher dialog instead of informing the user that no input file was provided. You can run scripts, compile scripts including platform selection, or do a few other things such as viewing the command line arguments/version information.
* The directory_delete function now includes a recursive boolean argument.
* Upgrades NVGT to SDL3!
* Switched to UniversalSpeech static, no more Tolk.dll required for screen reader output!
* form.nvgt modifications:
    * The `form::is_disallowed_char` method will now always return true if the character is not allowed. This also automatically checks whether the control index is being used as either blacklist or whitelist, the `use_only_disallowed_characters` parameter.
    * Pasting text will now fail if the clipboard contains disallowed characters.
    * Fixes a bug regarding the go to line dialog and the column being set 1 character to the left from where it should be.
    * Adds the ability to create custom control type labels.
    * Added Link control type.
    * If you alt tab to the application from another program while in an audio form, it reannounces the current focus control.
    * Added Floating points support in sliders and Fixed home/end bug with sliders.
    * Adds set_list_properties method.
    * Added word deletion.
    * You can now serialize the `audioform_keyboard_echo` property.
    * Once an input field is popped out, You can use the F2 key to change between echo modes. The changed echo mode will be spoken out loud, as well as updating the `audioform_keyboard_echo` property.
    * The `reset` method now takes a new parameter, true by default, which resets the form's echo mode to default. This is useful to retrieve the value of the `audioform_keyboard_echo` property.
    * The go to line functionality can now be used on non multiline input fields as well. In non multiline fields, the line number field will be invisible.
    * Added a new method that allows you to toggle the go to line functionality. `bool set_enable_go_to_index(int control_index, bool enabled);`
* Added a new parameter in sound_pool's `update_listener_3d` function called `refresh_y_is_elevation` (bool) which toggles whether the sound pool should refresh the global `sound_pool_default_y_is_elevation` property. This makes it possible to constantly change the global property for the sound elevation.
* token_gen.nvgt can now generate different token types, see the `token_gen_flag` enum.
* Add string::is_whitespace method.
* Fix small memory leak in pathfinder due to not releasing callback data reference on path calculation failure.
* Add SCRIPT_BUILD_TIME property.
* Fixes missing const qualifier in mixer::set_fx which was causing random memory corruption on some systems and in some situations.
* Slightly improves include path resolution when running nvgt scripts on Macos.
* Speed improvements to find_files and find_directories especially on windows.
* Datastreams can now be implicitly created from strings.
* Add var::opCmp method.
* Documentation:
    * Updates compiling for distribution tutorial to talk about bundling facility.
    * Talk about Angelscript addons and delayed dll loading in plugin creation tutorial.
    * Documents TIMEZONE_* properties and refresh_window() function, update wait.nvgt to indicate that it calls refresh_window().
    * Document settings.nvgt include.
    * Document the number_speaker.nvgt include.
    * Partially document timestamp class, still needs operators and maybe a couple other things.
    * Completely documented thread_event class as well as concurrency enums.
    * update datetime property examples to say "set thing" instead of "current thing," document julian_day property.
    * Documents timestamp_from_UTC_time function.
    * Documents thread_current_id and thread_yield.
    * documents sound_global_pack property.
    * Various minor polishing for a few functions in data manipulation, audio, and user interface.
    * documented set_application_name, focus_window, is_window_hidden, and get_window_text. Also removed joystick_count from the documentation as it was an old SDL2 function.
    * Update pack documentation to note a confusion with get_file_offset vs. offset parameter as well as fixing inconsistent parameter name in read_file.
    * Added many more docs for the pack object, documented file_copy function.
    * Updates toolkit configuration tutorial to include all new options.
    * Added a note in the introduction topic that indicates the incomplete state of the docs.
    * Update contributors.
    * Array: `insert_at`, `remove_at`, most other methods with their examples.
    * dictionary, almost everything accept the indexing operator.
    * Environment global properties: `PLATFORM`, `PLATFORM_DISPLAY_NAME`, `PLATFORM_VERSION`, `system_node_name`, and `system_node_id`.
    * file datastream, including write method in the datastream documentation.
    * Token Gen documentation updated, including its enum constants.
    * Adds a not yet complete memory management tutorial.
    * Todo updated.
    * Fixed return type of network::connect and resolve syntax error in tts_voice constructor reference, other various syntax and formatting.
    * Audio game development tutorial has been slightly updated.
    * audio_form documentation is now mostly complete.

### New in 0.88.0-beta (07/01/2024):
* several improvements to the audio form:
    * fix the go to line dialog, it had broken a few versions ago when converting the form to no longer need bgt_compat.
    * adds method `bool is_disallowed_char(int control_index, string char, bool search_all=true);` which checks whether the given characters are allowed. It is also possible to make the search_all parameter to true or false to toggle whether the method should search to match full text, or every character. You can also omit the control_index parameter, in which case the method is used internally in the control class.
    * adds method `bool set_disallowed_chars(int control_index, string chars, bool use_only_disallowed_chars=false, string char_disallowed_description="");` which sets the disallowed characters in a given control. Setting the use_only_disallowed_chars parameter to true will restrict to use only characters that have been set into this list. The char_disallowed_description parameter is also optional and sets the description or the text to speak when the user types the character that isn't allowed. Default is set to empty, meaning there will be silent when the user types the not allowed character. Setting the chars parameter to empty string will clear the list, thus setting to its original state.
    * Adds methods is_list_item_checked and get_checked_list_items, also made the get_list_selections function return a handle to the array.
    * Add a type of list called tab panel. This does not include the ability to assign controls to each tab automatically right now, but instead just the facility to create a list that acts more like a tab control.
* adds blocking functions to and exposes the pause functionality in the music manager include.
* adds a boolean to sound.play (true by default) which controls whether to reset the loop state on sound resume, so it's now possible to pause a looping sound and resume it without knowing whether the sound loops.
* add functions to var type such as is_integer, is_boolean, is_string and more to determine what is stored in the var, also var.clear().
* Added `sound_pool_default_y_elevation` property into sound_pool. This property will be useful to set default `y_is_elevation` property of each sound pool without having to change later for every sound pool you declare. Note, however, that it will only work for sound_pools declared after the variable is set, for example a global sound_pool variable will likely initialize before any function in your code could set the property.
* improve passing arguments to async calls.
* Fix critical bug if using network_event by handle that could allow the static none event to get value assigned to! Also better type info caching during the creation of some arrays.
* improve the speed of stream::read() when the stream size can be determined, which can be done automatically for files.
* users should no longer need to install libgit2 and openssl in order to run NVGT games on MacOS!
* Implement the recently contributed AVTTSVoice class into nvgt's tts_voice object, meaning we now have AVSpeechSynthesizer support for MacOS in NVGT! Temporary caveats:
    * Though this works well enough for people to start playing with, it still needs more testing. In particular, too much switching of voices followed by speech could cause a tts_voice object to break, calling refresh would probably fix it. Exact condition to reproduce unknown.
    * We also still need to figure out how to clamp the MacOS rate/pitch/volume parameters into the -10 to +10 that is typically used in the tts_voice class, so parameter adjustment may be rough for a short time.
    * The contributed class provides methods to handle languages, but the nvgt tts_voice class does not yet have these, as such voices just have raw names for now until we brainstorm more API.
    * For now this class speaks using the operating system directly and does not interact with bass, and so speak_to_memory is not yet supported. This will be addressed as the AVSpeech API does give us methods to do this.
* It is now possible to open .nvgt scripts directly within finder with the MacOS app bundle!
* array.insert_last can now take a handle to another array.
* Documentation:
    * major spell checking session as well as some formatting.
    * array::insert_last method.
    * sound::loaded_filename method.
    * string::format method.
    * get_characters function
    * idle_ticks function.
    * mutex class
    * concurrency article
    * Game programming tutorial updates
    * Clarifies some information in the distrobution topic.
    * Include direct links to MacOS and Linux build scripts.
    * Minor updates to contributors topic.
    * Updates to the todo and bgt upgrading topics.

### New in 0.87.2-beta (06/17/2024):
* Hopefully removed the need for the user to run `xattr -c` on the mac app bundle!
* Fix an accidental UTF8 conversion issue introduced into screen reader speech that took place when implementing speech dispatcher.
* NVGT will no longer fail if a plugin pragma with the same plugin name gets encountered multiple times.
* Fix minor error in bgt_compat's set_sound_storage function where the filename stored was not caching for display properly.
* Improve the downloads page to include release dates and headings for old versions as well as file sizes, yes we do still intend to integrate with github releases.
* Fix the broken SCREEN_READER_AVAILABLE property on windows.
* New documentation on compiling a game for distribution.

### New in 0.87.1-beta (06/16/2024):
* This patches an issue with the speech dispatcher support on linux where calling screen_reader_unload() would cause a segmentation fault if it had not loaded to begin with due to no libspeechd being available.
* Fixed a severe lack of debugging information issue where if a plugin could not load on linux, no error information was printed and instead the app silently exited.
* Fix an issue where some error messages that printed to stdout were not following up with a new line.
* Another enhancement to the network object which avoids an extra memory allocation every time a network_event of type event_none was created.

### New in 0.87.0-beta (06/16/2024):
* The jaws keyhook works even better than it did before and is nearing full functionality, though you may still need to alt+tab a few times in and out of the game window if JAWS restarts.
* Various improvements to the network object:
    * added packet_compression boolean which allows the user to toggle enet's builtin packet compressor allowing nvgt network objects to be backwards compatible with BGT if this is enabled!
    * Added packets_received and packets_sent properties.
    * network.destroy takes an optional boolean argument (flush = true) which can make sure any remaining packets are dispatched before the host is destroyed.
    * bytes_received and bytes_sent properties no longer wrap around after 4gb due to enet tracking that information using 32 bit integers.
* Add support for speech dispatcher on Linux and other BSD systems!
* You can now use the directive `#pragma embed packname.dat` as an alternative to `#including` your pack files.
* Fix broken quoted strings when handling pragma directives, resolving issues with the `#pragma include` option.
* Mostly finishes making it possible to configure various Angelscript engine properties as well as other NVGT options using configuration files, just needs polishing.
* bgt_compat's string_to_number function now trims whitespace to comply with bgt's standard, our new faster parse_float doesn't do that anymore in the name of performance.
* Fix issues with sound::push_memory():
    * actual audio files can be pushed to the function without modifying any other arguments other than the data string.
    * Calling sound.load() with a blank filename is no longer required before push_memory functions.
* Some polishing to the Angelscript integration:
    * If a global variable fails to initialize, the exception that caused it is now properly shown in the compilation error dialog.
    * There should hopefully be no more cases where a compilation error dialog can show up after a script executes successfully and throws an exception. Instead if the user enables the warnings display, they should properly see warnings before the script executes.
    * Set up the infrastructure to be able to store a bit of extra encrypted information along side the bytecode payload in compiled programs, for now using that to more securely store the list of enabled plugins as well as the serialized Angelscript properties.
    * Scripts no longer compile if they do not contain a valid entry point.
* Updated to the latest Angelscript WIP code which resolves a bytecode load error that had been reported.
* Revert the code changes to mixer::set_fx back to NVGT's first public release as the refactor did not go well and continued introducing unwanted side effects.
* Fixed bugs in find_directories and find_files on Unix platforms, the functions should now behave like on windows.
* Adds idle_ticks() function (works on windows and MacOS at present) which returns the number of milliseconds since the user has been idle.
* Update Angelscript's script builder addon which makes it possible to use unicode characters in script include paths.
* Add multiplication operators to strings, for example `string result = "hello" * 10;`
* There is a new way to list files and directories, a function called glob. Not only can it return all files and directories in one call, but you can even provide wildcards that enter sub directories. The function is documented in the reference.
* New additional version of json_array and json_object.stringify() which takes a datastream argument to write to.
* json_array and json_object now have get_array and get_object methods that directly return casted json_array@ or json_object@ handles.
* Added default_interrupt property in the high level Speech.nvgt include to set default interrupting for all the speech.
* Documentation: configuration tutorial, much of tts_voice object and other minor improvements.

### New in 0.86.0-beta (06/08/2024):
* running nvgtw.exe or the mac app should now show a message box at least rather than silently exiting.
* Improves the functionality of the JAWS keyhook. We likely still have more to go before it's perfect, but it is at least far better than it was before.
* pack::open is now set to read mode by default and will try closing any opened pack rather than returning false in that case.
* Added sound.loaded_filename property to determine the currently loaded filename of a sound object.
* Added string.reserve() function.
* Added  get_window_os_handle() function.
* Fix issues in sound::set_fx in regards to effect deletion.
* NVGT's datetime facilities now wrap Poco's implementations. Documentation is not complete, but the 4 new classes are datetime, timestamp, timespan, and calendar (which wraps LocalDateTime) in Poco and is called calendar for bgt backwards compatibility. Global functions include parse_datetime, datetime_is_leap_year and more, and all classes include a format method to convert the objects into strings given a format specifier.
* Converted most filesystem functions to wrap Poco's implementations.
* Fix potential issue with network where packets don't destroy on send failure.
* Added string_create_from_pointer to library functions.
* Though the sound pool will soon be superseded by better methods of handling sounds, it has received various improvements nevertheless:
    * Add y_is_elevation property. When this is set to false, the positioning works as normal, E.G. x is left/right, y is back/forward, and Z is up/down. When it's set to true, y is now up/down and Z is back/forward. This is useful for 2D platforming games for example, or games where y is up/down and Z is back/forward rather than the reverse. At some point this will be built into the engine so that it can be used on sound objects directly.
    * Fix a bug when using the new sound_default_pack global property.
    * Cleaned up the constructors and play_extended functions a bit.
    * bgt_compat.nvgt is no longer required to used this include.
* Adds a new function to dynamic_menu (add_multiple_items) that accepts an array of arrays. Each subarray must have at least 1 element. The first element is the text, the second element is the name. (#31)
* Fix a couple of issues in the url_post implementation.
* Register the Angelscript math complex addon.
* fix missing include of bgt_compat in dynamic_menu.nvgt
* fix number_to_words implementation appending null character to the end of it's output string
* Adds a set_sound_storage function to bgt_compat.nvgt which takes advantage of the new sound_default_pack property.
* Still a long long ways to go, but minor docs updates and a couple of new test cases.

### New in 0.85.1-beta (06/03/2024):
* The restart method on timers will now unpause them.
* Dramatically increase the speed of floating point string parsing.
* The form and speech includes no longer require  bgt_compat!
* adds sound_default_pack property.
    * For example, you can now create a pack object, execute the expression @sound_default_pack = my_pack; and from that point all sounds in the engine will use the default pack you have set unless you explicitly override it.
* Modified number conversion in sound mixer classes to use more efficient string -> number handling
* Fixed typo in doc for BSL license
* Start on the documentation for the pack object
* include form.nvgt in the speech.nvgt include by default.
* Add includes/number_speaker.nvgt (a port of bgt's class); makes it very easy to self-voice numbers!
* There are now a few more test cases as well as the beginnings of a benchmarking framework which will begin leading to several speed improvements such as the floating point processor mentioned above!

### New as of 05/31/2024:
* complete rewrite of NVGT entry point to use a Poco application. This includes much cleanup and organization and adds several features:
    * There is now proper command line parsing, help printing, config file loading for when we want to use it, and more.
    * This also introduces the change that on windows, there is now nvgt.exe and nvgtw.exe that gets built, one with the windows subsystem and one without.
    * Script files and nvgt's binary will check for config files with the basename of file + .ini, .properties, or .json.
* The above changes mean that we now implement the Angelscript debugger since the nvgt compiler is now always available in console mode.
* NVGT now uses symantic versioning, for example 0.85.0.
* Fixed script return code.
* NVGT finally has a cross-platform installer (NSIS on Windows and a .dmg file on macOS).
* The timer class once present in `bgt_compat.nvgt` is finally in the core of the engine!
* it is now possible to embed packs into executables! 
* The way Windows binaries load has been changed, meaning that UPX or any other binary compressor that supports overlays can now be used on your compiled NVGT binaries!
* The timer resolution should be much more accurate on Windows.
* Added a new, optional `uint timeout` parameter to the `network.request()` method.
* Improved documentation.

### New as of 05/25/2024:
* Wrapped `thread_pool` and `thread_event` from Poco.
* New function: `script_engine_dump_configuration()`.
* We now have an ftp_client class.
* raw memory allocation functions and memory_reader/writer datastreams to use them.
* May need more testing, but added the `async` class, for easily running a function on a thread and getting its return value.
* Many more docs.

### New as of 05/08/2024:
* Added a plugin to send notifications to systemd on Linux.
* Many more docs.
* `string.split()` should now reserve memory properly.
* Wrapped Poco for HTTP/HTTPS requests.
* Fix ancient bugs in soundsystem including too many functions registered as const and `close()` returning true on no-op.

### New as of 04/18/2024:
* The var type now has PostEnc and PostDec operators.
* UTF8 fixes: sound.load, and compiled applications can now execute if they contain non-english characters in their filenames.
* All code that I wish to share has been forked into what will hopefully be nvgt's long-standing repository which will eventually have it's privacy status switched to public!
* NVGT now has a build system! I know it's not the fastest one around, but needing a  middle ground between learning even more new things and using what I already know, I chose SCons purely because of the familiar pythonic environment and not needing to learn yet another new set of syntax rules. I'm just glad we're no longer building the engine using a series of shell scripts!
* Added basic steam audio reverb integration! It needs a lot of work and is far from being production ready (seriously this could slow your game to a crawl until I'm done with this), but nevertheless it is still around for testing!

### New leading up to 02/20/2024:
* NVGT now finally has a documentation structure!
* Unifying the file object into stream classes.

### New as of 01/06/2024:
* Misc sound system improvements (including the ability to set the pitch of a sound as low as 5).
* Fix memory leak.
* Remove sound_environment class for now.
* Should load bassflac.dll and bassopus.dll if present
* JSON Support.
* Better multithreading support with more primitives.
* More functions in the string class.
* New methods of operating system detection.
* Instance class removed from engine and replaced with include/instance.nvgt which wraps a named_mutex.
* Regular expressions now use PCRE2 via poco including lower level regexp class.
* Alert and question now use SDL message boxes (not sure what I think of this).
* Other misc changes.

### Note for changes before 01/06/2024:
Changes were roughly untracked before this time, but there is a rather large list of somewhat sorted changes below as committed to nvgt_bin (a repository where the NVGT testers could access and test NVGT). These are sorted by month where possible to make them easier to sort, but keep in mind that commits to nvgt_bin usually occurred all at once so that building NVGT was easier for all platforms. As such, expect these lists (while somewhat sorted) to become rather large! Additionally, some of these changes may be ambiguous due to being based off of nvgt_bin's commit messages only. At this time, it was assumed anyone using this engine had direct contact with Sam to ask questions.

### New as of 12/10/2023:
* Using more poco libraries including basic json implementation.
* Improvements to the sound crash.
* Fixes instances where the engine was not handling UTF8 properly.
* Performance increases such as updated hashmap and making network object faster.
* First and probably unstable implementation of a plugin system.
* Attempts to improve 3d pathfinding.
* Example of subscripting.
* More misc changes.

### New as of 07/24/2023:
* Switch to sdl2 for keyboard/windowing (new key_repeating / get_preferred_locales() / urlopen() functions as a result).
* Switch random number generators (see random_* classes).
* Fixed random_get/set_state().
* Now using Poco c++ libraries for various encode/decode/hash operations as well as better TIMEZONE_* properties and more (thus dropped cppcodec).
* UTF8 support.
* Multithreading support including mutex class.
* Library object.
* Basic msgpack support (see packet and string.unpacket functions).
* md5/sha1/sha224/sha384 hashing added as well as HOTP function (see TOTP.nvgt example).
* libgit2 support.
* Bytecode compression (#pragma bytecode_compression 0-9).
* Multiple windows stubs including Enigma Virtual Box.
* Reduced sound crashes
* Resolved a tts_voice crash.
* More misc.

### New as of 04/24/2023:
* Improvements to db_props include.
* New system information functions for custom system fingerprint or error tracking.
* Improvements to coordinate_map.
* Subscripting can now compile to bytecode.
* Fixed vector division scaling operators.
* Improved reliability of timer queue.
* Many more minor bugfixes.

### New as of 02/22/2023:
* Fixes major rotation issue
* Sqlite has more functions.
* db_props updated.
* Minor readme updates.
* scriptstuff reference issue fixes.
* Pathfinder micro speed improvement.
* file_hard_link and file_hard_link_count.
* More.

### New as of 01/17/2023:
* Sans speech and windowing, NVGT runs on Linux!
* Updated Bass/SteamAudio.
* SQLite3 wrapper.
* Improvements to subscript execution.

### New as of 10/21/2022:
* Script_module and script_function classes.
* Reduced sound crash.
* speed improvements and more.

### New as of 09/20/2022:
* Updated sound docs.
* Added sound_default_mixer property.

### New as of 09/09/2022:
* If you call the wait() function with long duration, the window no longer hangs.
* Fix string_hash() issue.
* Updated some BGT to NVGT gotchas.

### New as of 09/08/2022:
* Fixes string_split().

### New as of 09/07/2022:
* Upgrades SteamAudio to 4.11.
* Reduces sound crash.

### New as of 09/02/2022:
* Fixed bug in crypto.
* Sound crash now much more rare.
* String coordinate_map_area::type replaced with any@ coordinate_map_area::primary_data.
* Other misc.

### New as of 08/20/2022:
* print() function should now be lowercase again.
* Many very minor fixes and improvements.

### New as of 07/01/2022:
* Partially recoded pack streaming system to hopefully reduce sound crashes.
* Various random speed improvements and fixes.

### New as of 06/30/2022:
* Fixes a few speed issues with includes.
* adds ini.list_wildcard_sections().

### New as of 06/02/2022:
* Mostly works on making sound/pack more threadsafe.
* Make ini loading robust.
* Documents thread lock functions.

### New as of 05/26/2022:
* Documentation and test for include/music.nvgt.
* Updated readme a bit.
* Working on sound callbacks.
* Enabled bass_asyncfile for faster sound playback.

### New as of 05/22/2022:
* Updated INI.

### New as of 05/21/2022:
* sound.set_length() for streaming sounds.

### New as of 05/15/2022:
* Fixed run function regarding filenames with spaces.
* FTP uploads.
* MLSD directory listings with internet_request.

### New as of 05/08/2022:
* Bullet3 vectors.
* size_to_string updates.
* Other misc.

### New as of 04/26/2022:
* Sound preloading.
* byteshift encryption.
* timer_queue.exists and timer_queue.is_repeating.
* Minor speed improvements.



## Contributors
This file contains the names of anyone who has helped contribute to the NVGT engine in any significant way along with short descriptions of how these people have contributed. For a list of third party code used in the engine, you can view the Third Party Licenses topic. A huge thanks goes out to everyone listed here!

* [Patrick W](https://github.com/braillescreen): some docs, build scripts, beta testing, and miscellaneous organization.
* [Quin Gillespie](https://github.com/trypsynth): responsible for a growing number of API references documentation topics, beta testing.
* [Rory Michie](https://github.com/RoryMichie): Has done much work on the NVGT user manual.
* [Tyler Spivey](https://github.com/tspivey): rewrote the executable loader on Windows to work with packers such as UPX, helped make documentation look more presentable.
* [Harry Min Khant](https://github.com/harrymkt): Wrote several documentation articles particularly in the references section, improvements to nvgt includes.
* [Ethin Probst](https://github.com/ethindp): major optimizations to parts of the code, rewrote sound effect parsing, libspeechd and Android TTS engine integration, atomics, innosetup installer, docs.
* [Ivan Soto](https://github.com/ivansoto0): Several major includes such as input_forms.nvgt, settings.nvgt, touch.nvgt etc as well as various improvements to smaller ones such as bgt_compat, input_forms and others.
* [Valiant8086](https://github.com/valiant8086): Documentation on game distribution.
* [Gruia Chiscop](https://github.com/GruiaChiscop): AVSpeech implementation.
* [Hamza Ahmad](https://github.com/literary-programmer): Contributed virtual_dialogs.nvgt include, Improvements to form.nvgt.
* [Abdullah Tepeli](https://github.com/colonel-official): Delete-by-word support for the audio_form include.
* [Caturria](https://github.com/caturria): Much help with miniaudio implementation and bgt backwards compatibility, from a rewritten pack file with encryption to miniaudio vfs wiring to pathfinder/tts_voice fixes and more.
* Beta testers including but not limited to Patrick Wilson, Quin G, Steven D, Lucas Brown, Liam Erven, DJWolfy, Lukáš Hosnedl, Jonathan859, Remi, Pragma and Day Garwood, without the valuable feedback and suggestions provided by these people NVGT would have never gotten this far.
* Last but not least, nothing is worth maintaining or developing without users, and so thank you to everyone who uses this engine and gives it their feedback, time and attention!


## License agreement
NVGT - NonVisual Gaming Toolkit

Copyright (c) 2022-2025 Sam Tupy

[nvgt.dev](https://nvgt.dev)

This software is provided "as-is", without any express or implied warranty. In no event will the authors be held liable for any damages arising from the use of this software.

Permission is granted to anyone to use this software for any purpose, including commercial applications, and to alter it and redistribute it freely, subject to the following restrictions:

1. The origin of this software must not be misrepresented; you must not claim that you wrote the original software. If you use this software in a product, an acknowledgment in the product documentation would be appreciated but is not required.
2. Altered source versions must be plainly marked as such, and must not be misrepresented as being the original software.
3. This notice may not be removed or altered from any source distribution.


[Third Party Code Attributions](nvgt_appendix_third_party_code_attributions.md)


