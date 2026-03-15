# Math
## Classes
### aabb

A class representing an axis-aligned bounding box (AABB).

aabb();

#### Remarks:

AABBs are numbers representing the corners of a fixed, non-rotating, rectangular box. This is useful for such functions as collision detection, defining world regions and so on.

#### Example:

```NVGT
void main() {
	aabb box1;
	aabb box2;
	box1.min = vector(1, 1, 1);
	box1.max = vector(5, 5, 5);
	box2.min = vector(2, 2, 2);
	box2.max = vector(4, 4, 4);
if (box1.contains(box2)) alert("Boxed in a box!", "Box1 contains box2.");
}
```



#### Methods
##### apply_scale

Scales the box by multiplying both min and max directly with the given scale vector. This causes the box to scale relative to the origin (0,0,0), meaning both its size and position will change if it's not centered at the origin.

void aabb::apply_scale(const vector&in scale);

###### Arguments:

* scale: A vector containing the factors to scale by.

###### Example:

```NVGT
void main() {
	aabb b;
	b.min = vector(1, 3, 5);
	b.max = vector(3, 5, 7);
	b.apply_scale(vector(2, 2, 2));
	alert("The bottom left corner of the box is located at", round(b.min.x, 0)+", "+round(b.min.y, 0)+", "+round(b.min.z, 0)); // 2, 6, 10
	alert("The top right corner of the box is located at", round(b.max.x, 0)+", "+round(b.max.y, 0)+", "+round(b.max.z, 0)); // 6, 10, 14
}
```



##### contains

Checks whether another AABB is fully contained within this one.

bool aabb::contains(const aabb&in other) const;

Checks whether the given point lies inside this AABB, optionally with a margin of error (epsilon).

bool contains(const vector&in point, float epsilon = EPSILON) const

###### Arguments (1):

* other: Another AABB to compare.

###### Arguments (2):

* point: The point to check for.

* epsilon: Error tolerance level (default is constant EPSILON, which should be fine for most cases).

###### Remarks (1):

Unlike the test_collision method, this method tests whether one box is fully contained inside another. If any part of the inner box is outside the boundaries of the first, this method will return false.

###### Remarks (2):

EPSILON is a very small floating point constant (1.19e-7) used to allow tolerance in equality or boundary checks due to rounding errors in floating point math. Changing this to a smaller value (such as 0) could lead to subtle bugs when comparing floating point values, while changing it to a larger value could provide incorrect results. It is therefore recommended to leave this parameter untouched unless you are changing it for a specific edge case.

###### Example:

```NVGT
void main() {
	aabb b1;
	aabb b2;
	b1.min = vector(1, 1, 1);
	b1.max = vector(5, 5, 5);
	b2.min = vector(3, 3, 3);
	b2.max = vector(5, 5, 5);
	// Both these conditions should be true.
	if (b1.contains(b2)) alert("Boxed in a box!", "box1 contains box2.");
	if (b1.contains(vector(1,2,3))) alert("Point found!", "box1 contains point 1,2,3.");
}
```



##### inflate

Expands the box by the given amounts in all directions. This means that the total size increases by twice the given values.

void aabb::inflate(float x, float y, float z);

###### Arguments:

* x: Value to inflate X axis.

* y: Value to inflate Y axis.

* z: Value to inflate Z axis.

###### Example:

```NVGT
void main() {
	aabb b;
	b.min = vector(1, 3, 5);
	b.max = vector(2, 4, 6);
	b.inflate(1, 1, 1);
	alert("The bottom left corner of the box is located at", round(b.min.x, 0)+", "+round(b.min.y, 0)+", "+round(b.min.z, 0));
	alert("The top right corner of the box is located at", round(b.max.x, 0)+", "+round(b.max.y, 0)+", "+round(b.max.z, 0));
}
```



##### inflate_with_point

Expands the box only if necessary to ensure the given point is contained within it. If the point is already inside, nothing changes.

void aabb::inflate_with_point(const vector&in point);

###### Arguments:

point: The point to include.

###### Example:

```NVGT
void main() {
	aabb b;
	b.min = vector(1, 3, 5);
	b.max = vector(3, 5, 7);
	b.inflate_with_point(vector(3, 6, 9)); // Only the max should change here.
	alert("The bottom left corner of the box is located at", round(b.min.x, 0)+", "+round(b.min.y, 0)+", "+round(b.min.z, 0));
	alert("The top right corner of the box is located at", round(b.max.x, 0)+", "+round(b.max.y, 0)+", "+round(b.max.z, 0));
}
```



##### merge

Sets this AABB to be the bounding box that contains both aabb1 and aabb2.

void aabb::merge(const aabb&in aabb1, const aabb&in aabb2);

###### Arguments:

* aabb1: The first box to merge.

* aabb2: The second box to merge.

###### Example:

```NVGT
void main() {
	aabb b1;
	aabb b2;
	aabb b3;
	b1.min = vector(0, 0, 0);
	b1.max = vector(50, 500, 5000);
	b2.min = vector(1, 3, 5);
	b2.max = vector(5, 5, 5);
	b3.min = vector(9, 9, 9);
	b3.max = vector(12, 15, 18);
	b1.merge(b2, b3); // Completely changes the size to merge 2 and 3 into 1.
	alert("The bottom left corner of the box is located at", round(b1.min.x, 0)+", "+round(b1.min.y, 0)+", "+round(b1.min.z, 0));
	alert("The top right corner of the box is located at", round(b1.max.x, 0)+", "+round(b1.max.y, 0)+", "+round(b1.max.z, 0));
}
```



##### merge_with

Expands this AABB to fully contain both itself and the other AABB.

void aabb::merge_with(const aabb&in aabb);

###### Arguments:

aabb: The AABB to merge.

###### Example:

```NVGT
void main() {
	aabb b1;
	aabb b2;
	b1.min = vector(1, 3, 5);
	b1.max = vector(5, 5, 5);
	b2.min = vector(9, 9, 9);
	b2.max = vector(12, 15, 18);
	b1.merge_with(b2);
	alert("The bottom left corner of the box is located at", round(b1.min.x, 0)+", "+round(b1.min.y, 0)+", "+round(b1.min.z, 0));
	alert("The top right corner of the box is located at", round(b1.max.x, 0)+", "+round(b1.max.y, 0)+", "+round(b1.max.z, 0));
}
```



##### raycast

Casts a ray at the box and, if it intersects, gives you the exact point where it hits.

bool aabb::raycast(const ray&in ray, vector&out hit_point);

###### Arguments:

* ray: The ray to cast.

* hit_point (out): Stores the hit point where the ray collided with the box.

###### Example:

```NVGT
void main() {
	aabb b;
	b.min = vector(1, 1, 1);
	b.max = vector(10, 10, 2);
	vector start = vector(50, 50, 1);
	vector target = vector(5, 5, 1);
	ray r(start, target, 100);
	vector hit;
	if (b.raycast(r, hit)) alert("Boom!", "We collided at "+round(hit.x, 0)+", "+round(hit.y, 0)+", "+round(hit.z, 0)+".");
}
```



##### test_collision

Checks if the position of one box would collide or overlap with another.

bool aabb::test_collision(const aabb&in aabb) const;

###### Arguments:

aabb: The box to compare with.

###### Remarks

Where the contains() method checks whether one box is fully contained within another, this method merely checks whether two boxes are touching.

###### Example:

```NVGT
void main() {
	aabb b1;
	aabb b2;
	b1.min = vector(5, 5, 0);
	b1.max = vector(10, 10, 0);
	b2.min = vector(1, 1, 0);
	b2.max = vector(5, 5, 0);
	if (b1.test_collision(b2)) alert("Bang!", "We collided.");
}
```



##### test_collision_triangle_aabb

Checks whether a triangle (given by 3 points) intersects the AABB.

bool aabb::test_collision_triangle_aabb(const array<vector>@ points) const;

###### Arguments:

points: The points of the triangle.

###### Remarks:

This method would be the same as placing the minimum and maximum vectors of the triangle inside another AABB and calling test_collision.

Note that if the input parameter doesn't represent a triangle (I.E. have exactly three points), the method will throw an exception.

###### Example:

```NVGT
void main() {
	vector[] points;
	points.insert_last(vector(2, 2, 0));
	points.insert_last(vector(8, 2, 0));
	points.insert_last(vector(5, 5, 0));
	aabb b;
	b.min = vector(1, 1, 0);
	b.max = vector(12, 15, 5);
	if (b.test_collision_triangle_aabb(points)) alert("Bang!", "We collided.");
}
```



##### test_ray_intersect

Checks whether a ray (straight line) intersects the box, given a starting point, direction, and distance.

bool aabb::test_ray_intersect(const vector&in ray_origin, const vector&in ray_direction, float ray_max_fraction);

###### Arguments:

* ray_origin: The starting position.

* ray_direction: The direction you expect to move.

* ray_max_fraction: The maximum distance you expect to travel.

###### Remarks

This is useful for weapon aiming or pathfinding systems.

###### Example:

```NVGT
void main() {
	aabb b;
	b.min = vector(1, 1, 1);
	b.max = vector(10, 10, 2);
	vector start = vector(50, 50, 1);
	vector target = vector(5, 5, 1);
	vector dir = (target - start);
	dir.normalize();
	if (b.test_ray_intersect(start, dir, 100)) alert("Boom!", "We collided.");
}
```




#### Properties
##### center

A read-only property representing the center of the box, calculated based on min and max.

vector aabb::center const;

###### Example:

```NVGT
void main() {
	aabb b;
	b.min = vector(1, 3, 5);
	b.max = vector(5, 3, 7);
	alert("The center of the box is located at", round(b.center.x, 0)+", "+round(b.center.y, 0)+", "+round(b.center.z, 0));
}
```



##### extent

A read-only property representing the extent of the box, calculated based on min and max.

Note that "extent" calculates from min, not from center. Therefore in this case, extent is synonymous with size.

vector aabb::extent const;

###### Example:

```NVGT
void main() {
	aabb b;
	b.min = vector(1, 3, 5);
	b.max = vector(5, 3, 7);
	alert("The extent of the box is located at", round(b.extent.x, 0)+", "+round(b.extent.y, 0)+", "+round(b.extent.z, 0)); // 4,0,2.
}
```



##### max

Represents the maximum coordinates (top right corner) of the box.

vector aabb::max const;

###### Example:

```NVGT
void main() {
	aabb b;
	b.max = vector(5, 3, 7);
	alert("The top right corner of the box is located at", round(b.max.x, 0)+", "+round(b.max.y, 0)+", "+round(b.max.z, 0));
}
```



##### min

Represents the minimum coordinates (bottom left corner) of the box.

vector aabb::min const;

###### Example:

```NVGT
void main() {
	aabb b;
	b.min = vector(1, 3, 5);
	alert("The bottom left corner of the box is located at", round(b.min.x, 0)+", "+round(b.min.y, 0)+", "+round(b.min.z, 0));
}
```



##### volume

A read-only property representing the volume of the box, calculated based on min and max.

Note that "volume" here refers to total number of points, and is defined as extent.x * extent.y * extent.z.

float aabb::volume const;

###### Example:

```NVGT
void main() {
	aabb b;
	b.min = vector(1, 2, 3);
	b.max = vector(2, 4, 6);
	alert("The volume of the box is", b.volume); // 6.
}
```





### complex

A class representing a complex number, composed of a real part `r` and an imaginary part `i`.

1. complex();

2. complex(const complex&in other);

3. complex(float r, float i = 0.0);

#### Arguments (3):

* float r: The real part of the complex number.

* float i = 0.0: The imaginary part of the complex number. Defaults to 0 if not specified.

#### Remarks:

The complex class supports basic arithmetic operations (add, subtract, multiply, divide) and can be compared for equality. It also provides access to magnitude (`abs()`), and utilities for working with real/imaginary order via `ri` and `ir` properties.

#### Example:

```NVGT
void main() {
	complex a(2, 3); // 2 + 3i
	complex b(1, -1); // 1 - i
	complex c = a + b; // (2+1, 3-1) = (3, 2)
	alert("result", "real: " + c.r + ", imag: " + c.i);
}
```



#### Functions
##### abs

Returns the absolute value (magnitude) of the complex number.

float complex::abs() const;

###### Example:

```NVGT
void main() {
	complex c(3, 4);
	alert("Magnitude =", c.abs());
}
```




#### Operators
##### opAdd

Adds two complex numbers and returns the result.

complex complex::opAdd(const complex&in other) const;

###### Arguments:

* const complex&in other: the complex number to add.

###### Returns:

complex: a new complex object containing the value of the addition.

###### Example:

```NVGT
// Helper function to print a complex number.
string to_string(const complex&in c) {
	return "(" + c.r + ", " + c.i + ")";
}
void main() {
	complex a(1, 2);
	complex b(3, 4);
	complex c = a + b;
	alert("a + b =", to_string(c));
}
```



##### opAddAssign

Adds another complex number to this one.

complex& complex::opAddAssign(const complex&in other);

###### Arguments:

* const complex&in other: the complex number to add.

###### Returns:

complex&: a reference to the complex number being operated on.

###### Example:

```NVGT
// Helper function to print a complex number.
string to_string(const complex&in c) {
	return "(" + c.r + ", " + c.i + ")";
}
void main() {
	complex a(1, 2);
	complex b(3, 4);
	a += b;
	alert("a + b =", to_string(a));
}
```



##### opDiv

Divides this complex number by another and returns the result.

complex complex::opDiv(const complex&in other) const;

###### Arguments:

* const complex&in other: the complex number to divide by.

###### Returns:

complex: a new complex object containing the value of the division.

###### Example:

```NVGT
// Helper function to print a complex number.
string to_string(const complex&in c) {
	return "(" + c.r + ", " + c.i + ")";
}
void main() {
	complex a(1, 2);
	complex b(3, 4);
	complex c = a / b;
	alert("a / b =", to_string(c));
}
```



##### opDivAssign

Divides this complex number by another.

complex& complex::opDivAssign(const complex&in other);

###### Arguments:

* const complex&in other: the complex number to divide by.

###### Returns:

complex&: a reference to the complex number being operated on.

###### Example:

```NVGT
// Helper function to print a complex number.
string to_string(const complex&in c) {
	return "(" + c.r + ", " + c.i + ")";
}
void main() {
	complex a(1, 2);
	complex b(3, 4);
	a /= b;
	alert("a / b =", to_string(a));
}
```



##### opEquals

Checks if two complex numbers are equal.

bool complex::opEquals(const complex&in other) const;

###### Arguments:

* const complex&in other: the complex number to compare to.

###### Returns:

bool: true if the two complex numbers are equal, false otherwise.

###### Example:

```NVGT
void main() {
	complex a(1, 2);
	complex b(1, 2);
	alert("a equals b?", a == b);
}
```



##### opMul

Multiplies two complex numbers and returns the result.

complex complex::opMul(const complex&in other) const;

###### Arguments:

* const complex&in other: the complex number to multiply with.

###### Returns:

complex: a new complex object containing the value of the multiplication.

###### Example:

```NVGT
// Helper function to print a complex number.
string to_string(const complex&in c) {
	return "(" + c.r + ", " + c.i + ")";
}
void main() {
	complex a(1, 2);
	complex b(3, 4);
	complex c = a * b;
	alert("a * b =", to_string(c));
}
```



##### opMulAssign

Multiplies this complex number by another.

complex& complex::opMulAssign(const complex&in other);

###### Arguments:

* const complex&in other: the complex number to multiply with.

###### Returns:

complex&: a reference to the complex number being operated on.

###### Example:

```NVGT
// Helper function to print a complex number.
string to_string(const complex&in c) {
	return "(" + c.r + ", " + c.i + ")";
}
void main() {
	complex a(1, 2);
	complex b(3, 4);
	a *= b;
	alert("a * b =", to_string(a));
}
```



##### opSub

Subtracts a complex number from this one and returns the result.

complex complex::opSub(const complex&in other) const;

###### Arguments:

* const complex&in other: the complex number to subtract.

###### Returns:

complex: a new complex object containing the value of the subtraction.

###### Example:

```NVGT
// Helper function to print a complex number.
string to_string(const complex&in c) {
	return "(" + c.r + ", " + c.i + ")";
}
void main() {
	complex a(5, 6);
	complex b(2, 3);
	complex c = a - b;
	alert("a - b =", to_string(c));
}
```



##### opSubAssign

Subtracts another complex number from this one.

complex& complex::opSubAssign(const complex&in other);

###### Arguments:

* const complex&in other: the complex number to subtract.

###### Returns:

complex&: a reference to the complex number being operated on.

###### Example:

```NVGT
// Helper function to print a complex number.
string to_string(const complex&in c) {
	return "(" + c.r + ", " + c.i + ")";
}
void main() {
	complex a(5, 6);
	complex b(2, 3);
	a -= b;
	alert("a - b =", to_string(a));
}
```




#### Properties
##### i

Represents the imaginary component of the complex number.

float complex::i;

###### Example:

```NVGT
void main() {
	complex c(0, 1);
	alert("The imaginary part is", c.i);
}
```



##### ir

Accesses the complex number in imaginary-real order.

complex complex::ir [property];

###### Example:

```NVGT
// Helper function to print a complex number.
string to_string(const complex&in c) {
	return "(" + c.r + ", " + c.i + ")";
}
void main() {
	complex c(1, 2);
	alert("Imaginary-Real =", to_string(c.ir));
}
```



##### ri

Accesses the complex number in real-imaginary order.

complex complex::ri;

###### Example:

```NVGT
// Helper function to print a complex number.
string to_string(const complex&in c) {
	return "(" + c.r + ", " + c.i + ")";
}
void main() {
	complex c(1, 2);
	alert("Real-Imaginary =", to_string(c.ri));
}
```





### vector

A class containing x, y and z coordinates, usually used to represent a 3d point in space.

1. vector();

2. vector(const vector& in vec);

3. vector(float x, float y = 0.0, float z = 0.0);

#### Arguments (3):

* float x: The initial x point or coordinate this vector represents.

* float y = 0.0: The initial y point or coordinate this vector represents.

* float z = 0.0: The initial z point or coordinate this vector represents, defaulted to 0 because it may not be needed in some 2d applications.

#### Remarks:

An advantage with vectors is that they contain basic addition and scaling operators.

#### Example:

```NVGT
void main() {
	vector v1(5, 5, 5);
	vector v2(10, 10, 0);
	vector v3 = v1 + v2;
	alert("example", "the new vector is "+v3.x + ", " + v3.y + ", " + v3.z); // will show that the vector is 15, 15, 5.
}
```



#### Methods
##### cross

Returns the cross product of two vectors.

vector vector::cross(const vector&in other);

###### Arguments:

* other: The second vector to calculate from.

###### Remarks

The cross product provides a third vector which is Perpendicular to (at right-angles with) the first two vectors. This is useful for working out relative directions (such as forwards, right, up) based on the world's orientation.

###### Example:

```NVGT
void main() {
	vector v1(0, 1, 0); // Forwards
	vector v2(0, 0, 1); // Up
	vector v3=v1.cross(v2); // right
	alert("Cross", v3.x+", "+v3.y+", "+v3.z);
}
```



##### dot

Returns the dot product of two vectors.

float vector::dot(const vector&in other);

###### Arguments:

* other: The vector to sum.

###### Remarks

The dot product is a measure of how much two vectors point in the same direction. This is often used in physics for checking if an object is moving into or away from a surface, measuring forces, or calculating angles.

* Returns a positive value if both vectors point roughly in the same direction.

* Returns zero if the vectors are perpendicular (at right angles, not pointing the same way at all).

* Returns a negative value if the vectors point in opposite directions.

The dot product is calculated as (ax * bx) + (ay * by) + (az * bz).

###### Example:

```NVGT
void main() {
	vector v1(1, 2, 3);
	vector v2(4, 5, 6);
	alert("Dot", v2.dot(v1)); // (1 * 4) + (2 * 5) + (3 * 6) = 32.
}
```



##### length

Retrieves the Euclidean length of the vector.

float vector::length();

###### Arguments:

None.

###### Remarks

It is important to emphasize this function returns the vector's Euclidian length (also known as its magnitude). This is calculated as sqrt((x * x) + (y * y) + (z * z)), which gives the distance from the origin (0, 0, 0) to the point represented by the vector.

While this may sound abstract at first, it's extremely useful in many common scenarios. Some examples are:

* Measuring distance: Use the length to find out how far a vector reaches from the origin. The vector (3, 4, 0) has a length of 5.0, meaning it's 5 units away in space.

* Calculating speed: If a vector represents velocity, the length gives you the speed (how fast something is moving), while the vector's direction shows where it's going.

* Collision detection: To determine how close two points are, subtract one position from another to get a direction vector, then use the length to measure the distance.

If you are looking for the total size (I.E. number of units, volume etc), you will manually need to calculate this by using x * y * z.

###### Example:

```NVGT
void main() {
	vector v1(3, 4, 0);
	alert("Length", v1.length());
}
```



##### length_square

Retrieves the square length of the vector.

float vector::length_square();

###### Arguments:

None.

###### Remarks

This is similar to length except it does not perform the square root calculation.

###### Example:

```NVGT
void main() {
	vector v1(3, 4, 0);
	alert("Length", v1.length_square());
}
```



##### normalize

Normalizes the vector so that its Euclidian length is 1.

vector& vector::normalize();

###### Arguments:

None.

###### Remarks

Vector normalization is useful when you need to find out the direction something is pointing rather than where it goes. This is especially useful in 3D or physics-based games, where movement and aiming often happen in arbitrary directions rather than along fixed axes.

Warning: Calling normalize() on a zero vector (0, 0, 0) will return a vector whose values are NAN due to division by zero. Be sure to check the vector's length before normalizing.

###### Example:

```NVGT
void main() {
	vector v1(3, 4, 0);
	v1.normalize();
	alert("Vector", "(" + v1.x + ", " + v1.y + ", " + v1.z + ")");
}
```



##### set

Set new values on a vector.

void vector::set(float x, float y, float z);

###### Arguments:

* float x: The new x point or coordinate this vector represents.

* float y: The new y point or coordinate this vector represents.

* float z: The new z point or coordinate this vector represents.

###### Example:

```NVGT
void main() {
	vector v1(5, 5, 5);
	v1.set(10, 12, 14);
	alert("example", "the new vector is "+v1.x + ", " + v1.y + ", " + v1.z); // will show that the vector is 10, 12, 14.
}
```



##### setToZero

Reset the vector to 0, 0, 0.

void vector::setToZero();

###### Arguments:

None.

###### Example:

```NVGT
void main() {
	vector v1(5, 5, 5);
	v1.setToZero();
	alert("example", "the new vector is "+v1.x + ", " + v1.y + ", " + v1.z); // will show that the vector is 0, 0, 0.
}
```




#### Operators
##### opAdd

Overloads the + operator, allowing you to add a vector to another.

vector& vector::opAdd(const vector &in other);

###### Arguments:

* const vector&in other: the vector to add.

###### Example:

```NVGT
void main() {
	vector v1(2, 3, 5);
	vector v2(5, 4, 2);
	vector v3 = v1 + v2;
	alert("The third vector =", "(" + v3.x + ", " + v3.y + ", " + v3.z + ")");
}
```



##### opAddAssign

Overloads the += operator, allowing you to add a vector to another, already existing one.

vector& vector::opAddAssign(const vector &in other);

###### Arguments:

* const vector&in other: the vector to add.

###### Example:

```NVGT
void main() {
	vector v1(2, 3, 5);
	vector v2(5, 4, 2);
	v1 += v2;
	alert("The first vector =", "(" + v1.x + ", " + v1.y + ", " + v1.z + ")");
}
```



##### opAssign

Overloads the = operator, allowing you to assign a vector to another, already existing one.

vector& vector::opAssign(const vector &in other);

###### Arguments:

* const vector&in other: the vector to assign.

###### Example:

```NVGT
void main() {
	vector v1;
	vector v2(1.2, 2.3, 9.3);
	v1 = v2;
	alert("The first vector =", "(" + round(v1.x, 2) + ", " + round(v1.y, 2) + ", " + round(v1.z, 2) + ")");
}
```



##### opDiv

Overloads the / operator, allowing you to divide two vectors, or divide one vector by a scalar.

vector& vector::opDiv(const vector &in other);

vector& vector::opDiv(float scalar);

###### Arguments (1):

* const vector&in other: the vector to divide by.

###### Arguments (2):

* float scalar: The scalar to divide by.

###### Remarks

Dividing two vectors will, as you might imagine, divide each axis independently. On the other hand, dividing by a scalar will divide all axes by that scalar.

###### Example:

```NVGT
void main() {
	vector v1(3, 12, 24);
	vector v2=v1/3;
	alert("The second vector =", "(" + v2.x + ", " + v2.y + ", " + v2.z + ")");
}
```



##### opDivAssign

Overloads the /= operator, allowing you to divide one vector by a scalar.

vector& vector::opDivAssign(float scalar);

###### Arguments:

* float scalar: The scalar to divide by.

###### Remarks

Dividing by a scalar will divide all axes by that scalar.

###### Example:

```NVGT
void main() {
	vector v1(3, 12, 16);
	v1 /= 3;
	alert("The first vector =", "(" + v1.x + ", " + v1.y + ", " + v1.z + ")");
}
```



##### opEquals

Overloads the == operator, checking if two vectors are equal.

bool vector::opEquals(const vector &in other);

###### Arguments:

* const vector&in other: the vector to compare.

###### Example:

```NVGT
void main() {
	vector v1(2, 3, 5);
	vector v2(5, 4, 2);
	if(v1 != v2)
	alert("Compared", "Vectors are not equal.");
}
```



##### opImplConv

Allows the vector to be turned into a string.

string vector::opImplConv() const;

###### Remarks

Note this currently does not trim redundant decimal places from the output.

###### Example:

```NVGT
void main() {
	vector v(2, 3, 5);
	alert("Vector", v);
}
```



##### opIndex

Overloads the [] operator, allowing you to access the axes via their indexes.

bool vector::opIndex(int index);

###### Arguments:

* int index: the index of the axis to query.

###### Remarks

The axis index is represent by a number: x = 0, y = 1, z = 2.

###### Example:

```NVGT
void main() {
	vector v(2, 3, 5);
	alert("Vector", v[0]+", "+v[1]+", "+v[2]);
}
```



##### opMul

Overloads the * operator, allowing you to multiply two vectors, or multiply one vector by a scalar.

vector& vector::opMul(const vector &in other);

vector& vector::opMul(float scalar);

###### Arguments (1):

* const vector&in other: the vector to multiply.

###### Arguments (2):

* float scalar: The scalar to multiply by.

###### Remarks

Multiplying two vectors will, as you might imagine, multiply each axis independently. On the other hand, multiplying by a scalar will multiply all axes by that scalar.

###### Example:

```NVGT
void main() {
	vector v1(1, 4, 8);
	vector v2=v1*3;
	alert("The second vector =", "(" + v2.x + ", " + v2.y + ", " + v2.z + ")");
}
```



##### opMulAssign

Overloads the *= operator, allowing you to multiply one vector by a scalar.

vector& vector::opMulAssign(float scalar);

###### Arguments:

* float scalar: The scalar to multiply by.

###### Remarks

Multiplying by a scalar will multiply all axes by that scalar.

###### Example:

```NVGT
void main() {
	vector v1(1, 4, 8);
	v1*=3;
	alert("The first vector =", "(" + v1.x + ", " + v1.y + ", " + v1.z + ")");
}
```



##### opSub

Overloads the - operator, allowing you to subtract a vector from another.

vector& vector::opSub(const vector &in other);

###### Arguments:

* const vector&in other: the vector to subtract.

###### Example:

```NVGT
void main() {
	vector v1(12, 10, 8);
	vector v2(5, 3, 1);
	vector v3 = v1 - v2;
	alert("The third vector =", "(" + v3.x + ", " + v3.y + ", " + v3.z + ")");
}
```



##### opSubAssign

Overloads the -= operator, allowing you to subtract a vector from another.

vector& vector::opSubAssign(const vector &in other);

###### Arguments:

* const vector&in other: the vector to subtract.

###### Example:

```NVGT
void main() {
	vector v1(12, 10, 8);
	vector v2(5, 3, 1);
	v1 -= v2;
	alert("The first vector =", "(" + v1.x + ", " + v1.y + ", " + v1.z + ")");
}
```




#### Properties
##### is_finite

Checks if a vector is considered finite (I.E. it has finite components).

bool vector::is_finite const;

###### Example:

```NVGT
void main() {
	vector v(5, 4, 8);
	alert("Is finite?", v.is_finite);
}
```



##### is_unit

Checks if a vector has a length of 1 (I.E. the vector is normalised).

bool vector::is_unit const;

###### Remarks

This method is more accurate than checking each axis for 0 directly, as it takes into account the inaccuracies that can be caused by floating point arithmetic.

###### Example:

```NVGT
void main() {
	vector v(5, 4, 8);
	v.normalize();
	alert("Is unit?", v.is_unit);
}
```



##### is_zero

Checks if a vector is 0.

bool vector::is_zero const;

###### Remarks

This method is more accurate than checking each axis for 0 directly, as it takes into account the inaccuracies that can be caused by floating point arithmetic.

###### Example:

```NVGT
void main() {
	vector v(0, 0, 0);
	alert("Is zero?", v.is_zero);
}
```



##### max_axis

Returns the index of the axis which contains the maximum value.

int vector::max_axis const;

###### Remarks

The axis index is represent by a number: x = 0, y = 1, z = 2.

###### Example:

```NVGT
void main() {
	vector v(5, 7, 4);
	alert("maximum axis", v.max_axis);
}
```



##### max_value

Returns the maximum value of the vector.

float vector::max_value const;

###### Example:

```NVGT
void main() {
	vector v(5, 7, 4);
	alert("maximum value", v.max_value);
}
```



##### min_axis

Returns the index of the axis which contains the minimum value.

int vector::min_axis const;

###### Remarks

The axis index is represent by a number: x = 0, y = 1, z = 2.

###### Example:

```NVGT
void main() {
	vector v(5, 7, 4);
	alert("Minimum axis", v.min_axis);
}
```



##### min_value

Returns the minimum value of the vector.

float vector::min_value const;

###### Example:

```NVGT
void main() {
	vector v(5, 7, 4);
	alert("Minimum value", v.min_value);
}
```



##### x

Represents the x coordinate of the vector.

float vector::x const;

###### Example:

```NVGT
void main() {
	vector v(2.9);
	alert("The x value of the vector is", round(v.x, 2));
}
```



##### y

Represents the y coordinate of the vector.

float vector::y const;

###### Example:

```NVGT
void main() {
	vector v(2.9, 19.2);
	alert("The y value of the vector is", round(v.y, 2));
}
```



##### z

Represents the z coordinate of the vector.

float vector::z const;

###### Example:

```NVGT
void main() {
	vector v(2.9, 19.2, 4.1);
	alert("The z value of the vector is", round(v.z, 2));
}
```






## Functions
### abs

Returns the absolute value of a value.

double abs(double x);

#### Arguments:

* double x: The value whose absolute value is to be calculated.

#### Returns:

double: the absolute value of the given value.

#### Example:

```NVGT
void main() {
	alert("Example", "The absolute value of -5 is " + abs(-5));
}
```



### acos

Returns the arc cosine of a value in radians.

double acos(double x);

#### Arguments:

* double x: The value whose arc cosine is to be calculated.

#### Returns:

double: the arc cosine of the given value.

#### Example:

```NVGT
void main() {
    alert("Example", "The arc cosine of 0.5 is " + acos(0.5) + " radians");
}
```



### asin

Returns the arc sine of a value in radians.

double asin(double x);

#### Arguments:

* double x: The value whose arc sine is to be calculated.

#### Returns:

double: the arc sine of the given value.

#### Example:

```NVGT
void main() {
    alert("Example", "The arc sine of 0.5 is " + asin(0.5) + " radians");
}
```



### atan

Returns the arc tangent of a value in radians.

double atan(double x);

#### Arguments:

* double x: The value whose arc tangent is to be calculated.

#### Returns:

double: the arc tangent of the given value.

#### Example:

```NVGT
void main() {
    alert("Example", "The arc tangent of 1 is " + atan(1) + " radians");
}
```



### atan2

Returns the arc tangent of y/x, where y and x are the coordinates of a point.

double atan2(double y, double x);

#### Arguments:

* double y: The ordinate coordinate.

* double x: The abscissa coordinate.

#### Returns:

double: the arc tangent of y/x.

#### Example:

```NVGT
void main() {
    alert("Example", "The arc tangent of (1, 2) is " + atan2(1, 2) + " radians");
}
```



### ceil

Returns the smallest integer greater than or equal to a value.

double ceil(double x);

#### Arguments:

* double x: The value whose ceiling is to be calculated.

#### Returns:

double: the smallest integer greater than or equal to x.

#### Example:

```NVGT
void main() {
	alert("Example", "The ceiling of 3.14 is " + ceil(3.14));
}
```



### cos

Returns the cosine of an angle given in radians.

double cos(double x);

#### Arguments:

* double x: The angle (in radians) to get the cosine of.

#### Returns:

double: the cosine of the angle.

#### Example:

```NVGT
void main() {
	alert("Example", "The cosine of 45 is " + cos(45 * 3.14159 / 180) + " radians");
}
```



### cosh

Returns the hyperbolic cosine of a value.

double cosh(double x);

#### Arguments:

* double x: The value whose hyperbolic cosine is to be calculated.

#### Returns:

double: the hyperbolic cosine of the given value.

#### Example:

```NVGT
void main() {
    alert("Example", "The hyperbolic cosine of 2 is " + cosh(2));
}
```



### floor

Returns the largest integer less than or equal to a value.

double floor(double x);

#### Arguments:

* double x: The value whose floor is to be calculated.

#### Returns:

double: the largest integer less than or equal to x.

#### Example:

```NVGT
void main() {
	alert("Example", "The floor of 3.14 is " + floor(3.14));
}
```



### fraction

Returns the fractional part of a value.

double fraction(double x);

#### Arguments:

* double x: The value whose fractional part is to be extracted.

#### Returns:

double: the fractional part of the given value.

#### Example:

```NVGT
void main() {
	alert("Example", "The fractional part of 3.75 is " + fraction(3.75));
}
```



### log

Returns the natural logarithm (base e) of a value.

double log(double x);

#### Arguments:

* double x: The value whose natural logarithm is to be calculated.

#### Returns:

double: the natural logarithm of the given value.

#### Example:

```NVGT
void main() {
    alert("Example", "The natural logarithm of 10 is " + log(10));
}
```



### log10

Returns the base 10 logarithm of a value.

double log10(double x);

#### Arguments:

* double x: The value whose base 10 logarithm is to be calculated.

#### Returns:

double: the base 10 logarithm of the given value.

#### Example:

```NVGT
void main() {
    alert("Example", "The base 10 logarithm of 100 is " + log10(100));
}
```



### pow

Returns x raised to the power of y.

double pow(double x, double y);

#### Arguments:

* double x: The base.

* double y: The exponent.

#### Returns:

double: x raised to the power of y.

#### Example:

```NVGT
void main() {
    alert("Example", "2 raised to the power of 3 is " + pow(2, 3));
}
```



### round

Returns the value of a number rounded to the nearest integer.

double round(double n, int p);

#### Arguments:

* double n: The number to be rounded.

* int p: The number of decimal places to round to.

#### Returns:

double: The value of the number rounded to the nearest integer.

#### Example:

```NVGT
void main() {
	alert("Example", "Rounding 3.14159 to 2 decimal places gives " + round(3.14159, 2));
}
```



### sin

Returns the sine of an angle given in radians.

double sin(double x);

#### Arguments:

* double x: The angle (in radians) to get the sine of.

#### Returns:

double: the sine of the angle.

#### Example:

```NVGT
void main() {
	alert("Example", "The sine of 45 is " + sin(45 * 3.14159 / 180) + " radians");
}
```



### sinh

Returns the hyperbolic sine of a value.

double sinh(double x);

#### Arguments:

* double x: The value whose hyperbolic sine is to be calculated.

#### Returns:

double: the hyperbolic sine of the given value.

#### Example:

```NVGT
void main() {
    alert("Example", "The hyperbolic sine of 2 is " + sinh(2));
}
```



### sqrt

Returns the square root of a value.

double sqrt(double x);

#### Arguments:

* double x: The value whose square root is to be calculated.

#### Returns:

double: the square root of the given value.

#### Example:

```NVGT
void main() {
	alert("Example", "The square root of 16 is " + sqrt(16));
}
```



### tan

Returns the tangent of an angle given in radians.

double tan(double x);

#### Arguments:

* double x: The angle (in radians) to get the tangent of.

#### Returns:

double: the tangent of the angle.

#### Example:

```NVGT
void main() {
	alert("Example", "The tangent of 45 is " + tan(45 * 3.14159 / 180) + " radians");
}
```



### tanh

Returns the hyperbolic tangent of a value.

double tanh(double x);

#### Arguments:

* double x: The value whose hyperbolic tangent is to be calculated.

#### Returns:

double: the hyperbolic tangent of the given value.

#### Example:

```NVGT
void main() {
    alert("Example", "The hyperbolic tangent of 2 is " + tanh(2));
}
```



### tinyexpr

Evaluate a mathematical expression using the tinyexpr library.

double tinyexpr(const string&in expression);

#### Arguments:

* const string&in expression: the expression to evaluate.

#### Returns:

double: the result of the expression.

#### Example:

```NVGT
void main() {
	string expression = input_box("Expression", "Enter expression to evaluate");
	if (expression.is_empty()) exit();
	alert("Result", expression + "= " + tinyexpr(expression));
}
```





