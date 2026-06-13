theater_capacity = 350
max_allowed_tickets_per_booking = 15
allowed_age = 12

accepted_bookings = 0
tickets_booked = 0
rejected_bookings = 0
open_tickets = 350

while theater_capacity > 0:
    no_of_tickets = int(input("How Many Tickets"))
    if(no_of_tickets > max_allowed_tickets_per_booking):
        print(f"Max Allowed tickets per booking are: {max_allowed_tickets_per_booking}")
    elif(no_of_tickets > open_tickets):
        print(f"Final Report: Total Bookings: {accepted_bookings}, Total Tickets Sold: {tickets_booked}, Rejected Bookings: {rejected_bookings}, Remaining Seats: {open_tickets}")
    else:
        ages = []
        for i in range(no_of_tickets):
            age = int(input(f"Enter the person {i} Age: "))
            ages.append(age)
        if any (age < allowed_age for age in ages):
            print(f"Minimum Allowed age is {allowed_age}: BOOKING REJECTED -- Age Restriction")
            rejected_bookings += 1
        else:
            print(f"BOOKING CONIRMED - {len(ages)} Tickets")
            accepted_bookings +=1
            tickets_booked += len(ages)
            open_tickets -= tickets_booked
    print(f"Final Report: Total Bookings: {accepted_bookings}, Total Tickets Sold: {tickets_booked}, Rejected Bookings: {rejected_bookings}, Remaining Seats: {open_tickets}")

