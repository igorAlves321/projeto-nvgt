# Date and Time
## Classes
### datetime
This class stores an instance in time represented as years, months, days, hours, minutes, seconds, milliseconds and microseconds.

The class stores time independent of timezone, and thus uses UTC by default. You can use a calendar object in place of this one if you need to check local time, however it is faster to calculate time without needing to consider the timezone and thus any time difference calculations should be done with this object instead of calendar.

1. `datetime();`
2. datetime(double julian_day);
3. datetime(int year, int month, int day, int hour = 0, int minute = 0, int second = 0, int millisecond = 0, int microsecond = 0);

#### Arguments (2):
* double julian_day: The julian day to set the time based on.

#### Arguments (3):
* int year: the year to set.
* int month: the month to set.
* int day: the day to set.
* int hour = 0: the hour to set (from 0 to 23).
* int minute = 0: the minute to set (from 0 to 59).
* int second = 0: the second to set (0 to 59).
* int millisecond = 0: the millisecond to set (0 to 999).
* int microsecond = 0: the microsecond to set (0 to 999).



#### Methods
##### format

Formats the contents of a datetime object as a string given any number of format specifiers.

string format(string fmt, int timezone_difference = UTC);

###### Arguments:

* string fmt: A string describing how the datetime object should be formatted (see remarks).

###### Returns:

string: The formatted date/time.

###### Remarks:

The date time formatter in NVGT comes from the Poco C++ libraries, the below remarks other than anything directly mentioning NVGT were copied verbatim from the Poco documentation.

The format string is used as a template to format the date and is copied character by character except for the following special characters, which are replaced by the corresponding value.

* %w - abbreviated weekday (Mon, Tue, ...)

* %W - full weekday (Monday, Tuesday, ...)

* %b - abbreviated month (Jan, Feb, ...)

* %B - full month (January, February, ...)

* %d - zero-padded day of month (01 .. 31)

* %e - day of month (1 .. 31)

* %f - space-padded day of month ( 1 .. 31)

* %m - zero-padded month (01 .. 12)

* %n - month (1 .. 12)

* %o - space-padded month ( 1 .. 12)

* %y - year without century (70)

* %Y - year with century (1970)

* %H - hour (00 .. 23)

* %h - hour (00 .. 12)

* %a - am/pm

* %A - AM/PM

* %M - minute (00 .. 59)

* %S - second (00 .. 59)

* %s - seconds and microseconds (equivalent to %S.%F)

* %i - millisecond (000 .. 999)

* %c - centisecond (0 .. 9)

* %F - fractional seconds/microseconds (000000 - 999999)

* %z - time zone differential in ISO 8601 format (Z or +NN.NN)

* %Z - time zone differential in RFC format (GMT or +NNNN)

* %% - percent sign

###### Example:

```NVGT
void main() {
	datetime dt;
	alert("example", "The current date/time is " + dt.format("%Y/%m/%d, %h:%M:%S %A %Z"));
}
```



##### reset

Resets this datetime object to the current date and time.

void reset();

###### Remarks:

The expression d.reset() is equivalent to the expression d = datetime(); this is only a convenience function.

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(2024, 3, 9, 1, 24, 49);
	alert("The datetime object is currently set to", d.year + "/" + d.month + "/" + d.day + ", " + d.hour + ":" + d.minute + ":" + d.second);
	d.reset();
	alert("The datetime object is now set to", d.year + "/" + d.month + "/" + d.day + ", " + d.hour + ":" + d.minute + ":" + d.second);
}
```



##### set

Set the date and time of the datetime object.

datetime& datetime::set(int year, int month, int day, int hour = 0, int minute = 0, int second = 0, int millisecond = 0, int microsecond = 0);

###### Arguments:

* int year: the year to set.

* int month: the month to set.

* int day: the day to set.

* int hour = 0: the hour to set (from 0 to 23).

* int minute = 0: the minute to set (from 0 to 59).

* int second = 0: the second to set (0 to 59).

* int millisecond = 0: the millisecond to set (0 to 999).

* int microsecond = 0: the microsecond to set (0 to 999).

###### Returns:

datetime&: A reference to the datetime object allowing for chaining calls together.

###### Remarks:

This method will throw an exception if the date or time is invalid. You can use the datetime_is_valid global function which takes similar arguments to this one and returns a boolean if you want to verify any values before passing them to this method.

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(2024, 3, 9, 1, 24, 49);
	alert("The datetime object is currently set to", d.year + "/" + d.month + "/" + d.day + ", " + d.hour + ":" + d.minute + ":" + d.second);
}
```



##### week

Returns the currently set week number within the year of the datetime object.

int week(int first_day_of_week = 1);

###### Arguments:

* int first_day_of_week = 1: Determines whether 0 (sunday) or 1 (monday) begins the week.

###### Returns:

int: The week number within the year (0 to 53).

###### Remarks:

The first_day_of_week argument controls whether the week counter increases by 1 upon reaching Sunday or Monday. Passing other values to this function has undefined results.

Week 1 of the year begins in whatever week contains January 4th.

###### Example:

```NVGT
void main() {
	datetime dt(2016, 9, 17);
	alert("example", "week " + dt.week()); // Will display 37.
}
```




#### Operators
##### opAdd
Return a new datetime object with a duration of time represented as a timespan added to it.
`datetime opAdd(const timespan&in);`


##### opAddAssign
Add a duration represented as a timespan to a datetime object.
`datetime& opAddAssign(const timespan&in);`


##### opCmp
Compare a datetime object relationally to another one.
`int opCmp(const datetime& other);`


##### opEquals
Check if a datetime object is equal to another datetime object.
`bool opEquals(const datetime& other);`


##### opSub
1. Return a new datetime object with a duration of time represented as a timespan subtracted from it.
2. Return a duration represented by a timespan by subtracting 2 datetime objects from each other.
1. `datetime opSub(const timespan&in);`
2. `timespan opSub(const datetime&in);`


##### opSubAssign
Subtract a duration represented as a timespan from a datetime object.
`datetime& opSubAssign(const timespan&in);`



#### Properties
##### AM

A boolean which is true if the datetime object is set to an hour before noon (ante meridiem).

const bool AM;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(2024, 5, 8, 14, 18);
	alert("The datetime's AM value was set to", d.AM);
}
```



##### day

Represents the current day of the datetime object.

const uint day;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(2024, 5, 8);
	alert("The datetime's set day is", d.day);
}
```



##### hour

Represents the current hour (from 0 to 23) of the datetime object.

const uint hour;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(d.year, d.month, d.day, 13, 47, 19);
	alert("The set hour of the datetime object is", d.hour);
}
```



##### hour12

Represents the current hour (from 0 to 12) of the datetime object.

const uint hour12;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(d.year, d.month, d.day, 13, 47, 19);
	alert("In 12 hour time, the set hour of the datetime object is", d.hour12);
}
```



##### julian_day

Represents the current timestamp held by the datetime object in julian days.

const double julian_day;

###### Remarks:

The [julian day](http://en.wikipedia.org/wiki/Julian_day) measures, including decimal fractions, the amount of time that has passed (in years) since Monday, January 1st, 4713 BC at 12 PM Universal Time.

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(2024, 5, 8, 16, 17, 18);
	alert("The julian day represented by this datetime object is", d.julian_day);
}
```



##### microsecond

Represents the current microsecond of the datetime object.

const uint microsecond;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(d.year, d.month, d.day, 12, 47, 19, 217, 962);
	alert("The set microsecond value of the datetime object is", d.microsecond);
}
```



##### millisecond

Represents the current millisecond of the datetime object.

const uint millisecond;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(d.year, d.month, d.day, 12, 47, 19, 217);
	alert("The set millisecond value of the datetime object is", d.millisecond);
}
```



##### minute

Represents the current minute of the datetime object.

const uint minute;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(d.year, d.month, d.day, 12, 47, 19);
	alert("The set minute of the datetime object is", d.minute);
}
```



##### month

Represents the current month of the datetime object.

const uint month;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(2024, 5, 8);
	alert("The datetime's set month is", d.month);
}
```



##### PM

A boolean which is true if the datetime object is set to an hour after noon (post meridiem).

const bool PM;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(2024, 5, 8, 14, 18);
	alert("The datetime's set PM value is", d.PM);
}
```



##### second

Represents the current second of the datetime object.

const uint second;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(d.year, d.month, d.day, 12, 47, 19);
	alert("The set second of the datetime object is", d.second);
}
```



##### timestamp

Represents the datetime object as a timestamp object.

const timestamp timestamp;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(d.year, d.month, d.day, 12, 47, 19);
	alert("The current timestamp represented by the datetime object is", d.timestamp / SECONDS);
}
```



##### UTC_time

Determines the UTC based time point stored in the datetime object.

const int64 UTC_time;

###### Remarks:

UTC based time begins on October 15, 1582 at 12 AM and uses an accuracy of 100 nanoseconds.

###### Example:

```NVGT
void main() {
	datetime dt;
	alert("example", "The current UTC time value is " + dt.UTC_time);
}
```



##### weekday

Represents the current day of the week (from 0 to 6) calculated by the datetime object.

const uint weekday;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(2024, 5, 8);
	alert("The datetime's set day of the week is", d.weekday);
}
```



##### year

Represents the current year of the datetime object.

const uint year;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(2024, 5, 8);
	alert("The datetime's set year is", d.year);
}
```



##### yearday

Represents the current day of the year calculated by the datetime object.

const uint yearday;

###### Example:

```NVGT
void main() {
	datetime d;
	d.set(2024, 5, 8);
	alert("The datetime's set day of the year is", d.yearday);
}
```





### timestamp
Stores a unix timestamp with microsecond accuracy and provides methods for comparing them.
1. timestamp();
2. timestamp(int64 epoch_microseconds);

#### Arguments 2:
* int64 epoch_microseconds: the initial value of the timestamp

#### Remarks:
If a timestamp object is initialize with the default constructor, it will be set to the system's current date and time.
The unix epoch began on January 1st, 1970 at 12 AM UTC.


#### Methods
##### has_elapsed

determine whether the given number of microseconds has elapsed since the time point stored in this timestamp.

bool has_elapsed(int64 microseconds);

###### Arguments:

* int64 microseconds: the number of microseconds to check elapsed status of

###### Returns:

bool: Whether the given number of milliseconds has elapsed

###### Remarks:

This method serves as a shorthand version of executing `bool has_elapsed = timestamp() - this >= microseconds;`

###### Example:

```NVGT
void main() {
	timestamp ts;
	alert("test", "will you keep the alert box opened for 10 seconds?");
	if (ts.has_elapsed(10 * SECONDS)) alert("good job", "You kept the alert box opened for 10 seconds!");
	else alert("oh no", "looks like a bit of character development in regards to the trait of patience is in order...");
}
```



##### update

Reset this timestamp to the system's current date and time.

void update();

###### Example:

```NVGT
void main() {
	timestamp ts;
	ts -= 60 * SECONDS;
	alert("timestamp before reset", ts / SECONDS);
	ts.update();
	alert("current timestamp", ts / SECONDS);
}
```




#### Operators
##### opImplConv
Implicitly convert the timestamp to a 64 bit integer containing a raw microsecond accuracy unix epoch.
int64 opImplConv();



#### Properties
##### elapsed

Determine the difference of time in microseconds between this timestamp's value and now.

const int64 elapsed;

###### Remarks:

This property is a shorthand version of the expression `int64 elapsed = timestamp() - this;`

###### Example:

```NVGT
void main() {
	datetime dt(2013, 11, 29, 1, 2, 3);
	alert("example", dt.format(DATE_TIME_FORMAT_RFC850) + " was " + (dt.timestamp.elapsed / DAYS) + " days ago");
}
```



##### UTC_time

Determines a UTC based time point based on the value stored in the timestamp object.

const int64 UTC_time;

###### Remarks:

UTC based time begins on October 15, 1582 at 12 AM and uses an accuracy of 100 nanoseconds.

###### Example:

```NVGT
void main() {
	timestamp ts;
	alert("example", "The current UTC time value is " + ts.UTC_time);
}
```






## Functions
### datetime_days_of_month

Returns the number of days in a given month, a year is also required so that leap year can be handled correctly.

int datetime_days_of_month(int year, int month);

#### Arguments:

* int year: The year involved in this calculation due to leap year.

* month: The month to fetch the number of days of (from 1 to 12).

#### Returns:

int: The number of days in the month provided with leap year accounted for, or 0 if invalid/out of range arguments are provided.

#### Example:

```NVGT
void main() {
	for(int i = 1; i <= 12; i++) {
		alert("month " + i + " no leap year", datetime_days_of_month(2023, i));
		if (i == 2) alert("month " + i + " leap year", datetime_days_of_month(2024, i));
	}
	alert("invalid", datetime_days_of_month(2015, 17)); // Will show 0 (there are not 17 months in the year)!
}
```



### datetime_is_leap_year

Determine whether a given year is a leap year.

bool datetime_is_leap_year(int year);

#### Arguments:

* int year: The year to check the leap year status of.

#### Returns:

* bool: true if the given year is a leap year, false otherwise.

#### Example:

```NVGT
void main() {
	for(int year = 2019; year < 2026; year ++) {
		alert("example", year+" is " + (datetime_is_leap_year(year)? "a leap year!" : "not a leap year."));
	}
}
```



### datetime_is_valid

Check whether the components of a date/time are valid.

bool datetime_is_valid(int year, int month, int day, int hour = 0, int minute = 0, int second = 0, int millisecond = 0, int microsecond = 0);

#### Arguments:

* int year: the year to check.

* int month: the month to check (from 1 to 12).

* int day: the day to check (from 1 to 31).

* int hour = 0: the hour to check (from 0 to 23).

* int minute = 0: the minute to check (from 0 to 59).

* int second = 0: the second to check (0 to 59).

* int millisecond = 0: the millisecond to check (0 to 999).

* int microsecond = 0: the microsecond to check (0 to 999).

#### Returns:

bool: true if the given arguments make up a valid date and time, false otherwise.

#### Example:

```NVGT
void main() {
	alert("example 1", datetime_is_valid(2023, 2, 29)); // Will display false (not a leap year!)
	alert("example 2", datetime_is_valid(2020, 2, 29)); // Will display true, is a leap year.
	alert("example 3", datetime_is_valid(2020, 6, 31)); // Will display false (June has 30 days).
	alert("example 4", datetime_is_valid(2020, 7, 31, 13, 71, 59)); // Will display false (invalid time values).
}
```



### parse_datetime

Parse a string into a datetime object given a format specifier.

1. datetime parse_datetime(string fmt, string datetime_to_parse, int& timezone_difference);

2. datetime parse_datetime(string datetime_to_parse, int& timezone_difference);

#### Arguments:

* string fmt (1): The format specifier string.

* string datetime_to_parse: The string containing a date/time to parse according to the given format specifier, or automatically if one is not provided.

* int& timezone_difference: A reference to an integer which will store any timezone offset parsed from the provided string.

#### Returns:

datetime: A datetime object containing the parsed information.

#### Remarks:

This function may throw an exception if an invalid date/time is provided. You can use the global `bool datetime_is_valid_format(string str)` function to attempt validating user input before passing it as an argument here.

If you use the version of this function without a format specifier, it will try to automatically determine the format of the date/time using several available standard formats.

This function will clean the input string such as trimming whitespace before parsing is attempted.

Internally, this wraps the DateTimeParser functionality in the Poco c++ libraries. Their documentation says the following, copied verbatim, about this parsing engine, though note in NVGT DateTime:::makeUTC is called datetime.make_UTC, for example.

This class provides a method for parsing dates and times from strings. All parsing methods do their best to parse a meaningful result, even from malformed input strings.

The returned DateTime will always contain a time in the same timezone as the time in the string. Call DateTime::makeUTC() with the timeZoneDifferential returned by parse() to convert the DateTime to UTC.

Note: When parsing a time in 12-hour (AM/PM) format, the hour (%h) must be parsed before the AM/PM designator (%a, %A), otherwise the AM/PM designator will be ignored.

See the DateTimeFormatter class for a list of supported format specifiers.

In addition to the format specifiers supported by DateTimeFormatter, an additional specifier is supported: %r will parse a year given by either two or four digits. Years 69-00 are interpreted in the 20th century (1969-2000), years 01-68 in the 21th century (2001-2068).

Note that in the current implementation all characters other than format specifiers in the format string are ignored/not matched against the date/time string. This may lead to non-error results even with nonsense input strings. This may change in a future version to a more strict behavior.

If more strict format validation of date/time strings is required, a regular expression could be used for initial validation, before passing the string to DateTimeParser.

#### Example:

```NVGT
void main() {
	int tzd;
	datetime dt = parse_datetime("2024-03-19 13:19:51", tzd);
	alert("example", "the parsed time is " + dt.format("%W, %B %d %Y at %H:%M:%S"));
	dt = parse_datetime("%Y/%m/%d %H:%M:%S", "2024/03/19 13:19:51", tzd);
	alert("example", "the parsed time is " + dt.format("%W, %B %d %Y at %H:%M:%S"));
}
```



### timestamp_from_UTC_time

Create a timestamp object from a UTC time point.

timestamp timestamp_from_UTC_time(int64 UTC_time);

#### Arguments:

* int64 UTC_time: The UTC time point (see remarks).

#### Returns:

timestamp: A timestamp derived from the given value.

#### Remarks:

UTC based time begins on October 15, 1582 at 12 AM and uses an accuracy of 100 nanoseconds.

#### Example:

```NVGT
void main() {
	calendar c(2017, 2, 3, 4, 5, 6);
	alert("initial calendar", c.format(DATE_TIME_FORMAT_RFC1123));
	timestamp ts = timestamp_from_UTC_time(c.UTC_time);
	calendar c2 = ts;
	alert("new calendar", c2.format(DATE_TIME_FORMAT_RFC1123));
}
```




## Global Properties
### DATE_DAY

Returns the number of the current day through the month.

const int DATE_DAY;

#### Example:

```NVGT
void main() {
	alert("example", "It is day " + DATE_DAY + " of " + DATE_MONTH_NAME);
}
```



### DATE_MONTH

Returns the month set on the system, from 1 to 12.

const int DATE_MONTH;

#### Example:

```NVGT
void main() {
	alert("example", "the month is " + DATE_MONTH);
}
```



### DATE_MONTH_NAME

Returns the name of the current month.

const string DATE_MONTH_NAME;

#### Example:

```NVGT
void main() {
	alert("example", "the month is " + DATE_MONTH_NAME);
}
```



### DATE_WEEKDAY

Returns the number of the current day through the week.

const int DATE_WEEKDAY;

#### Example:

```NVGT
void main() {
	alert("example", "It is day " + DATE_WEEKDAY + " of the week");
}
```



### DATE_WEEKDAY_NAME

Returns the name of the current day.

const string DATE_WEEKDAY_NAME;

#### Example:

```NVGT
void main() {
	alert("example", "It is " + DATE_WEEKDAY_NAME + " today");
}
```



### DATE_YEAR

Returns the 4 digit year set on the system.

const int DATE_YEAR;

#### Example:

```NVGT
void main() {
	alert("example", "the year is " + DATE_YEAR);
}
```



### SCRIPT_BUILD_TIME

Contains the timestamp when the calling nvgt program was compiled.

const timestamp SCRIPT_BUILD_TIME;

#### Remarks:

This property will be set to the time when NVGT launched if it is accessed by a script running from source. Otherwise, it will contain a timestamp set to when the .nvgt script was compiled into an executable.

#### Example:

```NVGT
void main() {
	if (!SCRIPT_COMPILED) {
		alert("oops", "This only works in compiled scripts.");
		return;
	}
	alert("Script compiled on", datetime(SCRIPT_BUILD_TIME).format(DATE_TIME_FORMAT_RFC850));
}
```



### TIME_HOUR

Returns the current hour, in 24-hour format.

const int TIME_HOUR;

#### Example:

```NVGT
void main() {
	alert("Example", "It is currently " + TIME_HOUR + ":00");
}
```



### TIME_MINUTE

Returns the current minute.

const int TIME_MINUTE;

#### Example:

```NVGT
void main() {
	alert("Example", "It is currently " + TIME_HOUR + ":" + TIME_MINUTE);
}
```



### TIME_SECOND

Returns the current second.

const int TIME_SECOND;

#### Example:

```NVGT
void main() {
	alert("Example", "It is currently " + TIME_HOUR + ":" + TIME_MINUTE + ":" + TIME_SECOND);
}
```



### TIME_SYSTEM_RUNNING_MILLISECONDS

Represents the number of milliseconds since the system booted up.

uint64 TIME_SYSTEM_RUNNING_MILLISECONDS;

#### Remarks:

Note that unlike something like `GetTickCount()` from the Windows API, this value is given as an unsigned 64-bit integer, so it would take an almost impossible amount of uptime to make it overflow.

#### Example:

```NVGT
void main() {
	alert("Your computer has been up for", TIME_SYSTEM_RUNNING_MILLISECONDS + " MS");
}
```



### timer_default_accuracy

Set or retrieve the default accuracy used for timers.

uint64 timer_default_accuracy = MILLISECONDS;

#### Remarks:

Internally NVGT always uses a clock with microsecond accuracy to track time, meaning that microseconds is the highest accuracy that timer objects support. However in many cases, microsecond accuracy is not desired and causes a user to need to type far too many 0s than they would desire when handling elapsed time. Therefor NVGT allows you to set a devisor/multiplier that is applied to any timer operation as it passes between NVGT and your script.

The accuracy represented here is just a number of microseconds to divide values returned from timer.elapsed by before returning them to your script, as well as the number of microseconds to multiply by if one uses the timer.force function.

If this property is changed, any timers that already exist will remain unaffected, and only newly created timers will use the updated value.

Some useful constants are provided to make this property more useful:

* MILLISECONDS: 1000 microseconds

* SECONDS: 1000 MILLISECONDS

* MINUTES: 60 SECONDS

* HOURS: 60 MINUTES

* DAYS: 24 HOURS.

#### Example:

```NVGT
void main() {
	timer_default_accuracy = SECONDS;
	alert("example", "about to wait for 1100ms");
	timer t;
	wait(1100);
	alert("example", t.elapsed); // Will show 1.
	timer_default_accuracy = 250; // You can set this to arbitrary values if you so wish.
	timer t2;
	wait(1); // or 1000 microseconds.
	alert("example", t2.elapsed); // Will display a number slightly higher than 4 as the wait call takes some extra microseconds to return.
}
```



### TIMEZONE_BASE_OFFSET

Determine the system's timezone offset from UTC in seconds, excluding any daylight saving time alterations.

const int TIMEZONE_BASE_OFFSET;

#### Example:

```NVGT
void main() {
	alert(TIMEZONE_NAME, "base offset is " + TIMEZONE_BASE_OFFSET);
}
```



### TIMEZONE_DST_NAME

Retrieve the name of the timezone currently set on the system that is displayed when daylight saving time is in effect.

const string TIMEZONE_STANDARD_NAME;

#### Remarks:

This will always return the version of the timezone name that is shown when daylight saving time is active, even if daylight saving time is not actually in effect.

If the current timezone does not use daylight saving time, the value of this property is somewhat undefined but is most likely to equal TIMEZONE_STANDARD_NAME. The undefined value condition is a result of directly querying the operating system's API for this information, different platforms might react in slightly different ways to the absants of daylight savings support in a timezone.

#### Example:

```NVGT
void main() {
	alert("timezone example", "Currently in " + TIMEZONE_NAME + ", which is usually called " + TIMEZONE_STANDARD_NAME + " though it is known as " + TIMEZONE_DST_NAME + "when daylight saving time is in effect.");
}
```



### TIMEZONE_DST_OFFSET

Determine the DST alteration offset in seconds if daylight saving time is active in the system's current timezone.

const int TIMEZONE_DST_OFFSET;

#### Remarks:

If daylight saving time usually moves the clock an hour forward in your timezone when it is active, for example, this value will return 3600.

#### Example:

```NVGT
void main() {
	timespan t(TIMEZONE_DST_OFFSET, 0);
	alert(TIMEZONE_NAME, "The clock is being altered by " + t.hours + " hours, " + t.minutes + " minutes, and " + t.seconds + " seconds due to daylight saving time.");
}
```



### TIMEZONE_NAME

Retrieve the name of the timezone currently set on the system.

const string TIMEZONE_NAME;

#### Remarks:

This contains the value of either TIMEZONE_STANDARD_NAME or TIMEZONE_DST_NAME, depending on whether daylight saving time is currently in effect. If the timezone does not support daylight saving time, this always yields TIMEZONE_STANDARD_NAME.

#### Example:

```NVGT
void main() {
	alert("timezone example", "Currently in " + TIMEZONE_NAME + ", which is usually called " + TIMEZONE_STANDARD_NAME + " though it is known as " + TIMEZONE_DST_NAME + "when daylight saving time is in effect.");
}
```



### TIMEZONE_OFFSET

Determine the system's current timezone offset from UTC in seconds.

const int TIMEZONE_OFFSET;

#### Remarks:

This is also the sum of TIMEZONE_BASE_OFFSET + TIMEZONE_DST_OFFSET, provided for convenience.

#### Example:

```NVGT
void main() {
	alert(TIMEZONE_NAME, "offset from UTC: " + timespan(TIMEZONE_OFFSET, 0).format());
}
```



### TIMEZONE_STANDARD_NAME

Retrieve the name of the timezone currently set on the system that is displayed when daylight saving time is not in effect.

const string TIMEZONE_STANDARD_NAME;

#### Remarks:

This will always return the version of the timezone name that is shown when daylight saving time is not active, even if daylight saving time is truly in effect.

#### Example:

```NVGT
void main() {
	alert("timezone example", "Currently in " + TIMEZONE_NAME + ", which is usually called " + TIMEZONE_STANDARD_NAME + " though it is known as " + TIMEZONE_DST_NAME + "when daylight saving time is in effect.");
}
```





