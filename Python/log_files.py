def log_event(message):
    with open("activity_log.txt", "a") as log:
        log.write(message + "\n")

def read_log():
    with open("activity_log.txt", "r") as log:
        for line in log:
            print(line)

log_event("Session started")
log_event("User submitted a form")
log_event("Data saved successfully")

print("--- Activity Log ---")
read_log()
