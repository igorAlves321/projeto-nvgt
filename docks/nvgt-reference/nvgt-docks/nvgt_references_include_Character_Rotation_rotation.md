# Character Rotation (rotation.nvgt)
## character rotation
This include contains functions for moving a rotating character in a 2D or 3D game.

### Disclaimer:
Though these have been improved over the years and though I do use this myself for Survive the Wild and my other games, it should be understood that I started writing this file in BGT when I was only 12 or 13 years old and it has only been getting improved as needed. The result is that anything from the math to the coding decisions may be less than perfect, putting it kindly. You have been warned!


## Functions
### calculate_theta

Calculate the radians value for a given angle in degrees.

double calculate_theta(double deg);

#### Arguments:

* double deg: the angle to convert, in degrees.

#### Returns:

double: the specified angle in radians.

#### Example:

```NVGT
#include "rotation.nvgt"
void main() {
	alert("Info", "45 degrees in radians is " + calculate_theta(45));
}
```



### get_1d_distance

Get the distance between two points on the x axis.

double get_1d_distance(double x1, double x2);

#### Arguments:

* double x1: the first point.

* double x2: the second point.

#### Returns:

double: the distance between the two points on the x axis.

#### Example:

```NVGT
#include "rotation.nvgt"
void main() {
	double x1 = 2.0;
	double x2 = 6.8;
	alert("The distance between " + x1 + " and " + x2 + " is", get_1d_distance(x1, x2));
}
```



### get_2d_distance

Get the distance between two x/y points.

double get_2d_distance(double x1, double y1, double x2, double y2);

#### Arguments:

* double x1: the first x point.

* double y1: the first y point.

* double x2: the second x point.

* double y2: the second y point.

#### Returns:

double: the distance between the two points.

#### Remarks:

This function uses the Euclidean distance formula, meaning it will return the possible closest distance between the two points.

#### Example:

```NVGT
#include "rotation.nvgt"
void main() {
	double x1 = 2.0, y1 = 0.3;
	double x2 = 6.8, y2 = 9.45;
	alert("The distance between (" + x1 + ", " + y1 + ") and (" + x2 + ", " + y2 + ") is", get_2d_distance(x1, y1, x2, y2));
}
```



### get_3d_distance

Get the distance between two x/y/z points.

double get_3d_distance(double x1, double y1, double z1, double x2, double y2, double z2);

#### Arguments:

* double x1: the first x point.

* double y1: the first y point.

* double z1: the first z point.

* double x2: the second x point.

* double y2: the second y point.

* double z2: the second z point.

#### Returns:

double: the distance between the two points.

#### Remarks:

This function uses the Euclidean distance formula, meaning it will return the possible closest distance between the two points.

#### Example:

```NVGT
#include "rotation.nvgt"
void main() {
	double x1 = 2.0, y1 = 0.3, z1 = 0.0;
	double x2 = 6.8, y2 = 9.45, z2 = 1.942;
	alert("The distance between (" + x1 + ", " + y1 + ", " + z1 + ") and (" + x2 + ", " + y2 + ", " + z2 + ") is", get_2d_distance(x1, y1, x2, y2));
}
```




## Global Properties
### direction constants
This is a list of the various direction constants present in the rotation include. Each constant will be listed, as well as what it represents.

* int north: 0 degrees.
* int northeast: 45 degrees.
* int east: 90 degrees.
* int southeast: 135 degrees.
* int south: 180 degrees.
* int southeast: 225 degrees.
* int west: 270 degrees.
* int northwest: 315 degrees.
* int half_up: 45 degrees (upwards).
* int straight_up: 90 degrees (upwards).
* int half_down: 135 degrees (downwards).
* int straight_down: 180 degrees (downwards).


### pi

Holds 32 digits of PI.

const double pi;

#### Example:

```NVGT
#include "rotation.nvgt"
void main() {
	alert("32 digits of PI is", pi);
}
```





