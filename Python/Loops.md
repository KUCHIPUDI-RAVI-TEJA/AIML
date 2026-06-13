Python: Automation & Loops - Subjective

Problem: Build a booking system for a 350-seat theatre that validates age restrictions (12+ only) and seat availability.

Rules:

Theatre capacity: 350 seats (fixed)
Each booking: 1-15 tickets only
Age restriction: 12 years or above
Stop when: Theatre full OR user enters 0
Input: Repeatedly ask for the number of tickets (0 to exit), then the age of each person for valid bookings.

Output: Print booking status for each attempt, then final report showing total bookings, tickets sold, rejected bookings, and remaining seats.

Sample:

Input: 5, then ages: 15, 14, 13, 12, 11 → Output: BOOKING REJECTED - Age restriction

Input: 3, then ages: 20, 18, 16 → Output: BOOKING CONFIRMED - 3 tickets

Input: 0 → Final Report: Total Bookings: 1, Total Tickets Sold: 3, Rejected Bookings: 1, Remaining Seats: 347

Requirements: Use a while loop (main booking), continue statement (skip invalid tickets), for loop (check ages), and break statements (exit loops when needed).