#include <cmath>
#include <iomanip>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

class Ride {
private:
    std::string rideID_, pickupLocation_, dropoffLocation_;
    double distance_;
    mutable double fare_ = 0.0;

protected:
    double distance() const { return distance_; }
    double recordFare(double amount) const { return fare_ = amount; }

public:
    Ride(std::string id, std::string pickup, std::string dropoff, double miles)
        : rideID_(std::move(id)), pickupLocation_(std::move(pickup)),
          dropoffLocation_(std::move(dropoff)), distance_(miles) {
        if (!std::isfinite(miles) || miles < 0)
            throw std::invalid_argument("Distance must be finite and nonnegative.");
    }
    virtual ~Ride() = default;
    virtual double fare() const { return recordFare(distance() * 1.50); }
    virtual std::string type() const { return "Ride"; }
    virtual void rideDetails(std::ostream& out = std::cout) const {
        out << type() << " " << rideID_ << ": " << pickupLocation_ << " -> "
            << dropoffLocation_ << ", " << std::fixed << std::setprecision(2)
            << distance_ << " miles, fare $" << fare() << '\n';
    }
};

class StandardRide : public Ride {
public:
    using Ride::Ride;
    double fare() const override { return recordFare(distance() * 1.50); }
    std::string type() const override { return "Standard"; }
};

class PremiumRide : public Ride {
public:
    using Ride::Ride;
    double fare() const override { return recordFare(distance() * 2.75); }
    std::string type() const override { return "Premium"; }
};

class Driver {
private:
    std::string driverID_, name_;
    double rating_;
    std::vector<std::shared_ptr<Ride>> assignedRides_;

public:
    Driver(std::string id, std::string name, double rating)
        : driverID_(std::move(id)), name_(std::move(name)), rating_(rating) {
        if (!std::isfinite(rating) || rating < 0 || rating > 5)
            throw std::invalid_argument("Rating must be between 0 and 5.");
    }
    // In this demonstration, adding a ride records its completion.
    void addRide(const std::shared_ptr<Ride>& ride) {
        if (!ride) throw std::invalid_argument("A ride is required.");
        assignedRides_.push_back(ride);
    }
    void getDriverInfo(std::ostream& out = std::cout) const {
        double earnings = 0;
        for (const auto& ride : assignedRides_) earnings += ride->fare();
        out << "Driver " << driverID_ << ": " << name_ << ", rating "
            << std::fixed << std::setprecision(2) << rating_ << "/5, completed rides: "
            << assignedRides_.size() << ", gross fares: $" << earnings << '\n';
    }
};

class Rider {
private:
    std::string riderID_, name_;
    std::vector<std::shared_ptr<Ride>> requestedRides_;

public:
    Rider(std::string id, std::string name)
        : riderID_(std::move(id)), name_(std::move(name)) {}
    void requestRide(const std::shared_ptr<Ride>& ride) {
        if (!ride) throw std::invalid_argument("A ride is required.");
        requestedRides_.push_back(ride);
    }
    void viewRides(std::ostream& out = std::cout) const {
        out << "Ride history for " << name_ << " (" << riderID_ << "):\n";
        if (requestedRides_.empty()) out << "No rides requested.\n";
        for (const auto& ride : requestedRides_) ride->rideDetails(out);
    }
};

int main() {
    try {
        Driver driver("D001", "Morgan Lee", 4.9);
        Rider rider("U001", "Alex Chen");
        // Base-class pointers preserve dynamic dispatch and avoid object slicing.
        std::vector<std::shared_ptr<Ride>> rides{
            std::make_shared<StandardRide>("R001", "Campus", "Library", 4.0),
            std::make_shared<PremiumRide>("R002", "Library", "Airport", 12.0),
            std::make_shared<StandardRide>("R003", "Airport", "Downtown", 8.0)
        };
        std::cout << "Mixed ride collection (polymorphic calls):\n";
        double total = 0;
        for (const auto& ride : rides) {
            total += ride->fare();
            ride->rideDetails();
            rider.requestRide(ride);
            driver.addRide(ride);
        }
        std::cout << "Total fares: $" << std::fixed << std::setprecision(2) << total << "\n\n";
        driver.getDriverInfo();
        rider.viewRides();
    } catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << '\n';
        return 1;
    }
}
