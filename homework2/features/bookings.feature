Feature: Seat Booking
  As a user
  I want to book a seat for a movie
  So that I can watch it

  Scenario: Book an available seat
    Given there is a movie and an available seat
    And I am a logged-in user
    When I book the seat for the movie
    Then I should receive a 201 status code
    And the seat should be marked as booked

  Scenario: View booking history
    Given I have an existing booking
    When I request my booking history
    Then I should see my past bookings