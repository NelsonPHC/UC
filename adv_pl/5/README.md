# Ride Sharing System

Two implementations of the same class-based application: C++ and GNU Smalltalk.
Distances are miles and fares are US dollars. Standard rides cost $1.50 per mile;
premium rides cost $2.75 per mile. The base Ride implementation uses $1.50 per mile.

## Run C++

```sh
g++ main.cpp -o ride_sharing
./ride_sharing
```

## Run Smalltalk

Install GNU Smalltalk (on macOS: `brew install gnu-smalltalk`), then run:

```sh
gst ride_sharing.st
```

The `.st` file uses GNU Smalltalk's bracket syntax.

## Object-oriented design

- **Encapsulation:** C++ data members are private. `Driver::addRide` controls
  insertion into the private ride collection; no mutable collection is exposed.
  Smalltalk instance variables are accessed through an object's methods, and the
  driver likewise never returns its internal collection. Both versions validate
  distances and driver ratings and reject invalid ride objects.
- **Inheritance:** StandardRide and PremiumRide inherit core ride data,
  initialization, and ride-detail behavior from Ride.
- **Polymorphism:** Both subclasses override `fare`. The demonstration iterates
  over a mixed collection, calling `fare` and `rideDetails` on each ride. C++ uses
  virtual methods and shared pointers to Ride; Smalltalk dispatches messages
  dynamically. The inherited `rideDetails` method also calls the overridden
  fare and ride-type methods.

Each demo creates one rider, one driver, and three rides. Requesting a ride adds
it to the rider's history. For this simulation, adding it to the driver records
completion immediately. The driver reports the completed count and gross fares;
no commission, payment processing, or asynchronous trip lifecycle is modeled.
C++ shared pointers allow the same ride to appear safely in all three collections.

## Expected results

The rides cost $6.00 (4-mile standard), $33.00 (12-mile premium), and $12.00
(8-mile standard), for a total of **$51.00**. The driver has three completed
rides, and the rider's history displays all three. Smalltalk's numeric display
may omit trailing zeroes.

Verified with GNU Smalltalk 3.2.5 on Apple Silicon macOS. Driver ratings use
scaled-decimal formatting to avoid a floating-point printing error in this runtime.
