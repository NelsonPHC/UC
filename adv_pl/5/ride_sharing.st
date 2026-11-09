"GNU Smalltalk script. Distances are miles; fares are US dollars."

Object subclass: Ride [
    | rideID pickupLocation dropoffLocation distance fareAmount |

    Ride class >> id: anID pickup: pickup dropoff: dropoff distance: miles [
        ^self new initializeID: anID pickup: pickup dropoff: dropoff distance: miles
    ]

    initializeID: anID pickup: pickup dropoff: dropoff distance: miles [
        (miles isNumber and: [miles >= 0])
            ifFalse: [self error: 'Distance must be nonnegative'].
        rideID := anID.
        pickupLocation := pickup.
        dropoffLocation := dropoff.
        distance := miles.
        fareAmount := 0.
        ^self
    ]

    fare [
        fareAmount := distance * 1.50.
        ^fareAmount
    ]

    rideType [ ^'Ride' ]

    rideDetails [
        Transcript nextPutAll: self rideType; nextPutAll: ' ';
            nextPutAll: rideID; nextPutAll: ': ';
            nextPutAll: pickupLocation; nextPutAll: ' -> ';
            nextPutAll: dropoffLocation; nextPutAll: ', ';
            nextPutAll: distance printString; nextPutAll: ' miles, fare $';
            nextPutAll: self fare printString; nl
    ]
]

Ride subclass: StandardRide [
    fare [
        fareAmount := distance * 1.50.
        ^fareAmount
    ]
    rideType [ ^'Standard' ]
]

Ride subclass: PremiumRide [
    fare [
        fareAmount := distance * 2.75.
        ^fareAmount
    ]
    rideType [ ^'Premium' ]
]

Object subclass: Driver [
    | driverID name rating assignedRides |

    Driver class >> id: anID name: aName rating: aRating [
        ^self new initializeID: anID name: aName rating: aRating
    ]

    initializeID: anID name: aName rating: aRating [
        (aRating isNumber and: [aRating >= 0 and: [aRating <= 5]])
            ifFalse: [self error: 'Rating must be between 0 and 5'].
        driverID := anID.
        name := aName.
        rating := aRating.
        assignedRides := OrderedCollection new.
        ^self
    ]

    "Adding a ride records its completion; the collection is never exposed."
    addRide: aRide [
        (aRide isKindOf: Ride) ifFalse: [self error: 'A Ride is required'].
        assignedRides add: aRide
    ]

    getDriverInfo [
        | earnings |
        earnings := 0.
        assignedRides do: [:ride | earnings := earnings + ride fare].
        Transcript nextPutAll: 'Driver '; nextPutAll: driverID;
            nextPutAll: ': '; nextPutAll: name; nextPutAll: ', rating ';
            nextPutAll: ((rating asScaledDecimal: 2) printString copyUpTo: $s);
            nextPutAll: '/5, completed rides: ';
            nextPutAll: assignedRides size printString;
            nextPutAll: ', gross fares: $'; nextPutAll: earnings printString; nl
    ]
]

Object subclass: Rider [
    | riderID name requestedRides |

    Rider class >> id: anID name: aName [
        ^self new initializeID: anID name: aName
    ]

    initializeID: anID name: aName [
        riderID := anID.
        name := aName.
        requestedRides := OrderedCollection new.
        ^self
    ]

    requestRide: aRide [
        (aRide isKindOf: Ride) ifFalse: [self error: 'A Ride is required'].
        requestedRides add: aRide
    ]

    viewRides [
        Transcript nextPutAll: 'Ride history for '; nextPutAll: name;
            nextPutAll: ' ('; nextPutAll: riderID; nextPutAll: '):'; nl.
        requestedRides isEmpty ifTrue: [Transcript nextPutAll: 'No rides requested.'; nl].
        requestedRides do: [:ride | ride rideDetails]
    ]
]

| driver rider rides total |
driver := Driver id: 'D001' name: 'Morgan Lee' rating: 4.9.
rider := Rider id: 'U001' name: 'Alex Chen'.
rides := OrderedCollection new.
rides add: (StandardRide id: 'R001' pickup: 'Campus' dropoff: 'Library' distance: 4.0).
rides add: (PremiumRide id: 'R002' pickup: 'Library' dropoff: 'Airport' distance: 12.0).
rides add: (StandardRide id: 'R003' pickup: 'Airport' dropoff: 'Downtown' distance: 8.0).
Transcript nextPutAll: 'Mixed ride collection (polymorphic calls):'; nl.
total := 0.
rides do: [:ride |
    total := total + ride fare.
    ride rideDetails.
    rider requestRide: ride.
    driver addRide: ride
].
Transcript nextPutAll: 'Total fares: $'; nextPutAll: total printString; nl; nl.
driver getDriverInfo.
rider viewRides.
