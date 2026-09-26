from datetime import datetime
import math
import os


# ============================================================
# KZN SMART MALL PARKING MANAGEMENT SYSTEM


#           PROGRAMMING 511 ASSIGNMENT 
# ============================================================

USERS_FILE = "users.txt"
PARKING_FILE = "parking.txt"
PAYMENTS_FILE = "payments.txt"
MALLS_FILE = "malls.txt"


# ============================================================
# PRICING CLASSES
# ============================================================

class FlatRate:

    def __init__(self, rate):
        self.rate = rate

    def calculate(self, hours):
        return self.rate


class HourlyRate:

    def __init__(self, rate):
        self.rate = rate

    def calculate(self, hours):
        return self.rate * math.ceil(hours)


class CappedRate:

    def __init__(self, rate, cap):
        self.rate = rate
        self.cap = cap

    def calculate(self, hours):
        fee = self.rate * math.ceil(hours)
        return min(fee, self.cap)


# ============================================================
# MALL CLASS
# ============================================================

class Mall:


#this stores information about a shopping mall such as its capacity , pricing model , name and location 
    def __init__(
        self,
        mall_id,
        name,
        location,
        capacity,
        pricing_type,
        rate,
        cap=0
    ):

        self.id = mall_id
        self.name = name
        self.location = location
        self.capacity = capacity
        self.pricing_type = pricing_type
        self.rate = rate
        self.cap = cap

    def calculate_fee(self, hours):

        if self.pricing_type == "flat":

            return FlatRate(self.rate).calculate(hours)

        elif self.pricing_type == "hourly":

            return HourlyRate(self.rate).calculate(hours)

        elif self.pricing_type == "capped":

            return CappedRate(
                self.rate,
                self.cap
            ).calculate(hours)

        return 0.00

    def pricing_name(self):

        if self.pricing_type == "flat":

            return "R15.00 flat fee per visit"

        elif self.pricing_type == "hourly":

            return "R10.00 per hour or part thereof"

        elif self.pricing_type == "capped":

            return "R12.00 per hour or part thereof, capped at R60.00"

        return "Unknown"


# ============================================================
# CREATE DEFAULT MALL FILE
# ============================================================

def create_mall_file():

    # this creates mall data file , if no data file exists 
    
    default_malls = [
        "1|Gateway Theatre of Shopping|Umhlanga, Durban|250|flat|15|0\n",
        "2|Pavilion Shopping Centre|Westville, Durban|180|hourly|10|0\n",
        "3|La Lucia Mall|La Lucia, Durban|150|capped|12|60\n"
    ] 



    # Check whether the file exists
    if not os.path.exists(MALLS_FILE):

        with open(MALLS_FILE, "w") as file:

            for mall in default_malls:
                file.write(mall)

        return

    # this checks whether the existing file contains the required malls
    valid_ids = set()

    with open(MALLS_FILE, "r") as file:

        for line in file:

            line = line.strip()

            if line == "":
                continue

            parts = line.split("|")

            if len(parts) >= 7:

                valid_ids.add(parts[0])

    
    required_ids = {"1", "2", "3"}

    if not required_ids.issubset(valid_ids):

        with open(MALLS_FILE, "w") as file:

            for mall in default_malls:
                file.write(mall)

# ============================================================
# LOAD MALLS FROM FILE
# ============================================================

def load_malls():

    malls = {}

    with open(MALLS_FILE, "r") as file:

        for line in file:

            line = line.strip()

            if line == "":
                continue

            parts = line.split("|")

            if len(parts) >= 7:

                mall_id = parts[0]
                name = parts[1]
                location = parts[2]
                capacity = int(parts[3])
                pricing_type = parts[4]
                rate = float(parts[5])
                cap = float(parts[6])

                malls[mall_id] = Mall(
                    mall_id,
                    name,
                    location,
                    capacity,
                    pricing_type,
                    rate,
                    cap
                )

    return malls


# ============================================================
# FILE CREATION
# ============================================================

def create_files():

    create_mall_file()

    # Create users file if it does not exist
    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, "w").close()

    # Required system accounts
    #shows the password of each mall and user 
    required_accounts = [
        ("admin_gateway", "admin123", "admin", "1"),
        ("admin_pavilion", "admin123", "admin", "2"),
        ("admin_lalucia", "admin123", "admin", "3"),
        ("owner", "owner123", "owner", "")
    ]

    # Get existing users
    users = get_users()

    existing_usernames = []

    for user in users:
        existing_usernames.append(
            user["username"].lower()
        )

    # Add missing system accounts
    for account in required_accounts:

        username = account[0]
        password = account[1]
        role = account[2]
        mall_id = account[3]

        if username.lower() not in existing_usernames:

            save_user(
                username,
                password,
                role,
                mall_id
            )

    # Create parking file
    if not os.path.exists(PARKING_FILE):
        open(PARKING_FILE, "w").close()

    # Create payments file
    if not os.path.exists(PAYMENTS_FILE):
        open(PAYMENTS_FILE, "w").close()


# ============================================================
# GENERAL FUNCTIONS
# ============================================================

def money(amount):

    return "R{:.2f}".format(amount)


def pause():

    input("\nPress Enter to continue...")


# ============================================================
# USER FILE FUNCTIONS
# ============================================================

def get_users():

    users = []

    with open(USERS_FILE, "r") as file:

        for line in file:

            line = line.strip()

            if line == "":
                continue

            parts = line.split("|")

            if len(parts) >= 4:

                users.append({
                    "username": parts[0],
                    "password": parts[1],
                    "role": parts[2],
                    "mall_id": parts[3]
                })

    return users


def save_user(username, password, role, mall_id):

    with open(USERS_FILE, "a") as file:

        file.write(
            username + "|" +
            password + "|" +
            role + "|" +
            mall_id + "\n"
        )


def find_user(username):

    users = get_users()

    for user in users:

        if user["username"].lower() == username.lower():

            return user

    return None


# ============================================================
# PARKING FILE FUNCTIONS
# ============================================================

def get_parking_records():

    records = []

    with open(PARKING_FILE, "r") as file:

        for line in file:

            line = line.strip()

            if line == "":
                continue

            parts = line.split("|")

            if len(parts) >= 8:

                try:

                    records.append({

                        "plate": parts[0],

                        "username": parts[1],

                        "mall_id": parts[2],

                        "entry_time": parts[3],

                        "exit_time": parts[4],

                        "duration": int(parts[5]),

                        "fee": float(parts[6]),

                        "paid": parts[7] == "True"

                    })

                except ValueError:

                    continue

    return records


def save_parking_records(records):

    with open(PARKING_FILE, "w") as file:

        for record in records:

            file.write(

                record["plate"] + "|" +

                record["username"] + "|" +

                record["mall_id"] + "|" +

                record["entry_time"] + "|" +

                record["exit_time"] + "|" +

                str(record["duration"]) + "|" +

                str(record["fee"]) + "|" +

                str(record["paid"]) +

                "\n"

            )


# ============================================================
# PAYMENT FILE FUNCTIONS
# ============================================================

def get_payments():

    payments = []

    with open(PAYMENTS_FILE, "r") as file:

        for line in file:

            line = line.strip()

            if line == "":
                continue

            parts = line.split("|")

            if len(parts) >= 5:

                try:

                    payments.append({

                        "username": parts[0],

                        "plate": parts[1],

                        "mall_id": parts[2],

                        "amount": float(parts[3]),

                        "timestamp": parts[4]

                    })

                except ValueError:

                    continue

    return payments


def save_payment(
    username,
    plate,
    mall_id,
    amount,
    timestamp
):

    with open(PAYMENTS_FILE, "a") as file:

        file.write(

            username + "|" +

            plate + "|" +

            mall_id + "|" +

            str(amount) + "|" +

            timestamp +

            "\n"

        )


# ============================================================
# DISPLAY MALLS
# ============================================================

def show_malls(malls):

    print("\n")
    print("=" * 90)
    print("AVAILABLE SHOPPING MALLS")
    print("=" * 90)

    for mall in malls.values():

        print("ID:", mall.id)

        print("Mall:", mall.name)

        print("Location:", mall.location)

        print("Capacity:", mall.capacity)

        print("Pricing:", mall.pricing_name())

        print("-" * 90)


# ============================================================
# DISPLAY MALL FILE
# ============================================================

def display_mall_file():

    print("\n")
    print("=" * 90)
    print("MALL DETAILS STORED IN malls.txt")
    print("=" * 90)

    with open(MALLS_FILE, "r") as file:

        for line in file:

            print(line.strip())

    print("=" * 90)


# ============================================================
# CHOOSE MALL
# ============================================================

def choose_mall(malls):

    show_malls(malls)

    while True:

        choice = input(
            "\nSelect mall: "
        ).strip()

        if choice in malls:

            return malls[choice]

        print("Invalid mall selection.")


# ============================================================
# ACTIVE PARKING RECORDS
# ============================================================

def active_records(
    mall_id=None,
    username=None
):

    records = get_parking_records()

    active = []

    for record in records:

        if record["exit_time"] != "":
            continue

        if mall_id is not None:

            if record["mall_id"] != mall_id:
                continue

        if username is not None:

            if (
                record["username"].lower()
                != username.lower()
            ):

                continue

        active.append(record)

    return active


# ============================================================
# CALCULATE PARKING HOURS
# ============================================================

def get_hours(entry_time, exit_time):

    entry = datetime.fromisoformat(
        entry_time
    )

    exit = datetime.fromisoformat(
        exit_time
    )

    seconds = (
        exit - entry
    ).total_seconds()

    hours = math.ceil(
        seconds / 3600
    )

    if hours < 1:

        hours = 1

    return hours


# ============================================================
# CUSTOMER REGISTRATION
# ============================================================

def register():

    print("\n")
    print("=" * 60)
    print("CUSTOMER REGISTRATION")
    print("=" * 60)

    username = input(
        "Choose username: "
    ).strip()

    if username == "":

        print("Username cannot be empty.")

        return

    if "|" in username:

        print("Username cannot contain |.")

        return

    if find_user(username) is not None:

        print("Username already exists.")

        return

    password = input(
        "Choose password: "
    ).strip()

    if len(password) < 4:

        print(
            "Password must contain at least 4 characters."
        )

        return

    if "|" in password:

        print("Password cannot contain |.")

        return

    save_user(
        username,
        password,
        "customer",
        ""
    )

    print("\nCustomer account created successfully.")


# ============================================================
# LOGIN
# ============================================================

def login(required_role=None):

    print("\n")
    print("=" * 60)
    print("LOGIN")
    print("=" * 60)

    username = input(
        "Username: "
    ).strip()

    password = input(
        "Password: "
    ).strip()

    user = find_user(username)

    if user is None:

        print("\nInvalid username or password.")

        return None

    if user["password"] != password:

        print("\nInvalid username or password.")

        return None

    if (
        required_role is not None
        and user["role"] != required_role
    ):

        print(
            "\nThis account does not belong to this role."
        )

        return None

    print("\nLogin successful.")

    print(
        "Welcome,",
        user["username"]
    )

    return user


# ============================================================
# CUSTOMER VEHICLE ENTRY
# ============================================================

def customer_entry(user, malls):

    print("\n")
    print("=" * 60)
    print("VEHICLE ENTRY")
    print("=" * 60)

    mall = choose_mall(malls)

    current_vehicles = active_records(
        mall_id=mall.id
    )

    if len(current_vehicles) >= mall.capacity:

        print("\nSORRY , THIS MALL IS FULL.")

        print(
            "Capacity:",
            mall.capacity
        )

        print(
            "Vehicle entry is not allowed."
        )

        return

    plate = input(
        "\nVehicle registration number: "
    ).strip().upper()

    if plate == "":

        print(
            "Vehicle registration cannot be empty."
        )

        return

    if "|" in plate:

        print("Invalid vehicle registration.")

        return

    all_active = active_records()

    for record in all_active:

        if (
            record["plate"].upper()
            == plate
        ):

            print(
                "This vehicle is already parked."
            )

            return

    entry_time = datetime.now().isoformat(
        timespec="seconds"
    )

    records = get_parking_records()

    records.append({

        "plate": plate,

        "username": user["username"],

        "mall_id": mall.id,

        "entry_time": entry_time,

        "exit_time": "",

        "duration": 0,

        "fee": 0.00,

        "paid": False

    })

    save_parking_records(records)

    print("\nVehicle entered successfully.")

    print(
        "Mall:",
        mall.name
    )

    print(
        "Vehicle:",
        plate
    )

    print(
        "Entry time:",
        entry_time
    )


# ============================================================
# CUSTOMER CURRENT PARKING
# ============================================================

def customer_current_parking(user, malls):

    print("\n")
    print("=" * 70)
    print("CURRENT PARKING STATUS")
    print("=" * 70)

    records = active_records(
        username=user["username"]
    )

    if not records:

        print(
            "You currently have no vehicle parked."
        )

        return

    for record in records:

        mall = malls[record["mall_id"]]

        print(
            "Vehicle:",
            record["plate"]
        )

        print(
            "Mall:",
            mall.name
        )

        print(
            "Entry time:",
            record["entry_time"]
        )

        print(
            "Status: CURRENTLY PARKED"
        )

        print("-" * 70)


# ============================================================
# CUSTOMER VEHICLE EXIT AND PAYMENT
# ============================================================

def customer_exit(user, malls):

    print("\n")
    print("=" * 70)
    print("VEHICLE EXIT")
    print("=" * 70)

    records = get_parking_records()

    active = []

    for record in records:

        if (
            record["username"].lower()
            == user["username"].lower()
            and record["exit_time"] == ""
        ):

            active.append(record)

    if not active:

        print(
            "You have no currently parked vehicle."
        )

        return

    print("\nYour parked vehicles:")

    for i, record in enumerate(active, 1):

        mall = malls[record["mall_id"]]

        print(
            str(i) + ". " +
            record["plate"] +
            " - " +
            mall.name
        )

    try:

        choice = int(
            input("\nSelect vehicle: ")
        )

        if (
            choice < 1
            or choice > len(active)
        ):

            print("Invalid selection.")

            return

    except ValueError:

        print(
            "Please enter a valid number."
        )

        return

    record = active[choice - 1]

    mall = malls[record["mall_id"]]

    exit_time = datetime.now().isoformat(
        timespec="seconds"
    )

    hours = get_hours(
        record["entry_time"],
        exit_time
    )

    fee = mall.calculate_fee(hours)

    print("\n")
    print("=" * 70)
    print("PARKING CHARGE")
    print("=" * 70)

    print(
        "Mall:",
        mall.name
    )

    print(
        "Pricing:",
        mall.pricing_name()
    )

    print(
        "Vehicle:",
        record["plate"]
    )

    print(
        "Entry time:",
        record["entry_time"]
    )

    print(
        "Exit time:",
        exit_time
    )

    print(
        "Parking duration:",
        hours,
        "hour(s)"
    )

    print(
        "Amount payable:",
        money(fee)
    )

    print(
        "\nThe amount above is displayed before payment."
    )

    answer = input(
        "\nMake payment now? (Y/N): "
    ).strip().lower()

    if answer != "y":

        print(
            "\nPayment cancelled."
        )

        print(
            "The vehicle remains parked."
        )

        return

    record["exit_time"] = exit_time

    record["duration"] = hours

    record["fee"] = fee

    record["paid"] = True

    save_parking_records(records)

    save_payment(
        user["username"],
        record["plate"],
        mall.id,
        fee,
        exit_time
    )

    print("\n")
    print("=" * 70)
    print("PAYMENT CONFIRMED")
    print("=" * 70)

    print(
        "Vehicle:",
        record["plate"]
    )

    print(
        "Mall:",
        mall.name
    )

    print(
        "Amount paid:",
        money(fee)
    )

    print(
        "Payment date:",
        exit_time
    )

    print(
        "Status: PAYMENT SUCCESSFUL"
    )

    print(
        "Vehicle exit recorded successfully."
    )


# ============================================================
# CUSTOMER PARKING HISTORY
# ============================================================

def customer_history(user, malls):

    print("\n")
    print("=" * 90)
    print("MY PARKING HISTORY")
    print("=" * 90)

    records = get_parking_records()

    found = False

    for record in records:

        if (
            record["username"].lower()
            != user["username"].lower()
        ):

            continue

        found = True

        mall = malls[record["mall_id"]]

        print(
            "Vehicle:",
            record["plate"]
        )

        print(
            "Mall:",
            mall.name
        )

        print(
            "Entry:",
            record["entry_time"]
        )

        if record["exit_time"] == "":

            print(
                "Exit: Not exited"
            )

            print(
                "Status: CURRENTLY PARKED"
            )

        else:

            print(
                "Exit:",
                record["exit_time"]
            )

            print(
                "Status: COMPLETED"
            )

        print(
            "Duration:",
            record["duration"],
            "hour(s)"
        )

        print(
            "Fee:",
            money(record["fee"])
        )

        print(
            "Paid:",
            "Yes" if record["paid"]
            else "No"
        )

        print("-" * 90)

    if not found:

        print(
            "No parking history found."
        )


# ============================================================
# CUSTOMER PAYMENT HISTORY
# ============================================================

def customer_payment_history(user, malls):

    print("\n")
    print("=" * 90)
    print("MY PAYMENT HISTORY")
    print("=" * 90)

    payments = get_payments()

    found = False

    for payment in payments:

        if (
            payment["username"].lower()
            != user["username"].lower()
        ):

            continue

        found = True

        mall = malls[payment["mall_id"]]

        print(
            "Date/time:",
            payment["timestamp"]
        )

        print(
            "Mall:",
            mall.name
        )

        print(
            "Vehicle:",
            payment["plate"]
        )

        print(
            "Amount:",
            money(payment["amount"])
        )

        print("-" * 90)

    if not found:

        print(
            "No payments found."
        )


# ============================================================
# ADMIN : PARKED VEHICLES
# ============================================================

def admin_parked_vehicles(user, malls):

    mall = malls[user["mall_id"]]

    print("\n")
    print("=" * 90)

    print(
        "CURRENTLY PARKED VEHICLES -",
        mall.name
    )

    print("=" * 90)

    records = active_records(
        mall_id=mall.id
    )

    if not records:

        print(
            "No vehicles currently parked."
        )

        return

    for record in records:

        print(
            "Vehicle:",
            record["plate"]
        )

        print(
            "Customer:",
            record["username"]
        )

        print(
            "Entry time:",
            record["entry_time"]
        )

        print("-" * 90)


# ============================================================
# ADMIN : CAPACITY
# ============================================================

def admin_capacity(user, malls):

    mall = malls[user["mall_id"]]

    current = len(
        active_records(
            mall_id=mall.id
        )
    )

    available = (
        mall.capacity - current
    )

    occupancy = (
        current / mall.capacity
    ) * 100

    print("\n")
    print("=" * 70)

    print(
        "PARKING CAPACITY MONITOR"
    )

    print(
        mall.name
    )

    print("=" * 70)

    print(
        "Maximum capacity:",
        mall.capacity
    )

    print(
        "Currently parked:",
        current
    )

    print(
        "Available spaces:",
        available
    )

    print(
        "Occupancy:",
        "{:.1f}%".format(occupancy)
    )

    if available == 0:

        print(
            "STATUS: FULL"
        )

    else:

        print(
            "STATUS: SPACES AVAILABLE"
        )


# ============================================================
# ADMIN : DAILY ACTIVITY
# ============================================================

def admin_daily_activity(user, malls):

    mall = malls[user["mall_id"]]

    today = datetime.now().date()

    records = get_parking_records()

    daily_records = []

    for record in records:

        if record["mall_id"] != mall.id:

            continue

        entry_date = datetime.fromisoformat(
            record["entry_time"]
        ).date()

        if entry_date == today:

            daily_records.append(record)

    print("\n")
    print("=" * 100)

    print(
        "DAILY PARKING ACTIVITY -",
        mall.name
    )

    print("=" * 100)

    print(
        "Date:",
        today
    )

    if not daily_records:

        print(
            "No parking activity recorded today."
        )

        return

    total_revenue = 0.00

    total_duration = 0

    completed = 0

    for record in daily_records:

        print(
            "Vehicle:",
            record["plate"]
        )

        print(
            "Customer:",
            record["username"]
        )

        print(
            "Entry:",
            record["entry_time"]
        )

        if record["exit_time"] == "":

            print(
                "Exit: Still parked"
            )

        else:

            print(
                "Exit:",
                record["exit_time"]
            )

        print(
            "Fee:",
            money(record["fee"])
        )

        print("-" * 100)

        if record["paid"]:

            total_revenue += record["fee"]

            total_duration += record["duration"]

            completed += 1

    print(
        "Vehicles recorded today:",
        len(daily_records)
    )

    print(
        "Completed visits:",
        completed
    )

    print(
        "Revenue today:",
        money(total_revenue)
    )

    if completed > 0:

        average = (
            total_duration / completed
        )

        print(
            "Average parking duration:",
            "{:.2f}".format(average),
            "hour(s)"
        )

    else:

        print(
            "Average parking duration:",
            "0.00 hour(s)"
        )


# ============================================================
# OWNER :  MALL REPORT
# ============================================================

def mall_report(mall):

    records = get_parking_records()

    mall_records = []

    completed = []

    parked = []

    for record in records:

        if record["mall_id"] != mall.id:

            continue

        mall_records.append(record)

        if record["exit_time"] == "":

            parked.append(record)

        if record["paid"]:

            completed.append(record)

    revenue = 0.00

    duration = 0

    for record in completed:

        revenue += record["fee"]

        duration += record["duration"]

    if len(completed) > 0:

        average = (
            duration / len(completed)
        )

        average_fee = (
            revenue / len(completed)
        )

    else:

        average = 0

        average_fee = 0

    return (
        mall_records,
        completed,
        parked,
        revenue,
        average,
        average_fee
    )


# ============================================================
# OWNER : CROSS MALL REPORT
# ============================================================

def owner_reports(malls):

    print("\n")
    print("=" * 110)
    print("CROSS-MALL MANAGEMENT REPORT")
    print("=" * 110)

    total_revenue = 0.00

    for mall in malls.values():

        (
            mall_records,
            completed,
            parked,
            revenue,
            average,
            average_fee
        ) = mall_report(mall)

        total_revenue += revenue

        print("\n")

        print(
            "MALL:",
            mall.name
        )

        print(
            "Location:",
            mall.location
        )

        print(
            "Capacity:",
            mall.capacity
        )

        print(
            "Pricing:",
            mall.pricing_name()
        )

        print(
            "Currently parked:",
            len(parked)
        )

        print(
            "Total parking records:",
            len(mall_records)
        )

        print(
            "Completed visits:",
            len(completed)
        )

        print(
            "Total revenue:",
            money(revenue)
        )

        print(
            "Average parking duration:",
            "{:.2f}".format(average),
            "hour(s)"
        )

        print(
            "Average fee per visit:",
            money(average_fee)
        )

        print("-" * 110)

    print("\n")

    print(
        "TOTAL REVENUE ACROSS ALL MALLS:",
        money(total_revenue)
    )

    print("\n")
    print("=" * 110)
    print("PRICING RULE COMPARISON")
    print("=" * 110)

    print("\nGateway Theatre of Shopping:")

    print(
        "R15.00 flat fee per visit."
    )

    print("\nPavilion Shopping Centre:")

    print(
        "R10.00 per hour or part thereof."
    )

    print("\nLa Lucia Mall:")

    print(
        "R12.00 per hour or part thereof,"
    )

    print(
        "with a maximum charge of R60.00."
    )

    print("\n")

    print(
        "The pricing rules are different, so"
    )

    print(
        "customers with similar parking durations"
    )

    print(
        "may pay different amounts."
    )


# ============================================================
# OWNER : MALL DETAILS
# ============================================================

def owner_mall_details(malls):

    print("\n")
    print("=" * 100)
    print("ALL MALL DETAILS")
    print("=" * 100)

    for mall in malls.values():

        print(
            "Mall:",
            mall.name
        )

        print(
            "Location:",
            mall.location
        )

        print(
            "Capacity:",
            mall.capacity
        )

        print(
            "Pricing:",
            mall.pricing_name()
        )

        print("-" * 100)


# ============================================================
# CUSTOMER MENU
# ============================================================

def customer_menu(user, malls):

    while True:

        print("\n")
        print("=" * 70)

        print("CUSTOMER MENU")

        print("=" * 70)

        print(
            "Logged in as:",
            user["username"]
        )

        print()

        print(
            "1. Register vehicle entry"
        )

        print(
            "2. View current parking status"
        )

        print(
            "3. Register vehicle exit and pay"
        )

        print(
            "4. View parking history"
        )

        print(
            "5. View payment history"
        )

        print(
            "6. Logout"
        )

        choice = input(
            "\nChoose option: "
        ).strip()

        if choice == "1":

            customer_entry(
                user,
                malls
            )

            pause()

        elif choice == "2":

            customer_current_parking(
                user,
                malls
            )

            pause()

        elif choice == "3":

            customer_exit(
                user,
                malls
            )

            pause()

        elif choice == "4":

            customer_history(
                user,
                malls
            )

            pause()

        elif choice == "5":

            customer_payment_history(
                user,
                malls
            )

            pause()

        elif choice == "6":

            print(
                "Logged out."
            )

            break

        else:

            print(
                "Invalid option."
            )


# ============================================================
# ADMIN MENU
# ============================================================

def admin_menu(user, malls):

    mall = malls[user["mall_id"]]

    while True:

        print("\n")
        print("=" * 80)

        print(
            "PARKING ADMINISTRATOR MENU"
        )

        print(
            "Mall:",
            mall.name
        )

        print("=" * 80)

        print(
            "1. View currently parked vehicles"
        )

        print(
            "2. Monitor parking capacity"
        )

        print(
            "3. View daily parking activity"
        )

        print(
            "4. Logout"
        )

        choice = input(
            "\nChoose option: "
        ).strip()

        if choice == "1":

            admin_parked_vehicles(
                user,
                malls
            )

            pause()

        elif choice == "2":

            admin_capacity(
                user,
                malls
            )

            pause()

        elif choice == "3":

            admin_daily_activity(
                user,
                malls
            )

            pause()

        elif choice == "4":

            print(
                "Logged out."
            )

            break

        else:

            print(
                "Invalid option."
            )


# ============================================================
# OWNER MENU
# ============================================================

def owner_menu(malls):

    while True:

        print("\n")
        print("=" * 80)

        print(
            "OWNER / SHAREHOLDER MENU"
        )

        print("=" * 80)

        print(
            "1. View all mall details"
        )

        print(
            "2. Generate cross-mall report"
        )

        print(
            "3. View mall information file"
        )

        print(
            "4. Logout"
        )

        choice = input(
            "\nChoose option: "
        ).strip()

        if choice == "1":

            owner_mall_details(
                malls
            )

            pause()

        elif choice == "2":

            owner_reports(
                malls
            )

            pause()

        elif choice == "3":

            display_mall_file()

            pause()

        elif choice == "4":

            print(
                "Logged out."
            )

            break

        else:

            print(
                "Invalid option."
            )


# ============================================================
# CUSTOMER ROLE
# ============================================================

def customer_role(malls):

    while True:

        print("\n")
        print("=" * 70)

        print(
            "CUSTOMER"
        )

        print("=" * 70)

        print(
            "1. Register"
        )

        print(
            "2. Login"
        )

        print(
            "3. Back"
        )

        choice = input(
            "\nChoose option: "
        ).strip()

        if choice == "1":

            register()

            pause()

        elif choice == "2":

            user = login(
                "customer"
            )

            if user is not None:

                customer_menu(
                    user,
                    malls
                )

        elif choice == "3":

            break

        else:

            print(
                "Invalid option."
            )


# ============================================================
# ADMIN ROLE
# ============================================================

def administrator_role(malls):

    while True:

        print("\n")
        print("=" * 70)

        print(
            "PARKING ADMINISTRATOR"
        )

        print("=" * 70)

        print(
            "1. Login"
        )

        print(
            "2. Back"
        )

        choice = input(
            "\nChoose option: "
        ).strip()

        if choice == "1":

            user = login(
                "admin"
            )

            if user is not None:

                admin_menu(
                    user,
                    malls
                )

        elif choice == "2":

            break

        else:

            print(
                "Invalid option."
            )


# ============================================================
# OWNER ROLE
# ============================================================

def owner_role(malls):

    while True:

        print("\n")
        print("=" * 70)

        print(
            "OWNER / SHAREHOLDER"
        )

        print("=" * 70)

        print(
            "1. Login"
        )

        print(
            "2. Back"
        )

        choice = input(
            "\nChoose option: "
        ).strip()

        if choice == "1":

            user = login(
                "owner"
            )

            if user is not None:

                owner_menu(
                    malls
                )

        elif choice == "2":

            break

        else:

            print(
                "Invalid option."
            )


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    create_files()

    malls = load_malls()

    while True:

        print("\n")
        print("=" * 80)

        print(
            "KZN SMART MALL PARKING MANAGEMENT SYSTEM"
        )

        print("=" * 80)

        print(
            "1. Customer"
        )

        print(
            "2. Parking Administrator"
        )

        print(
            "3. Owner / Shareholder"
        )

        print(
            "4. View Malls"
        )

        print(
            "5. Exit"
        )

        print("=" * 80)

        choice = input(
            "\nChoose your role: "
        ).strip()

        # ----------------------------------------------------
        # CUSTOMER
        # ----------------------------------------------------

        if choice == "1":

            customer_role(
                malls
            )

        # ----------------------------------------------------
        # ADMINISTRATOR
        # ----------------------------------------------------

        elif choice == "2":

            administrator_role(
                malls
            )

        # ----------------------------------------------------
        # OWNER
        # ----------------------------------------------------

        elif choice == "3":

            owner_role(
                malls
            )

        # ----------------------------------------------------
        # VIEW MALLS
        # ----------------------------------------------------

        elif choice == "4":

            show_malls(
                malls
            )

            pause()

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        elif choice == "5":

            print("\n")

            print(
                "Thank you for using the"
            )

            print(
                "KZN Smart Mall Parking Management System."
            )

            break

        else:

            print(
                "Invalid option."
            )


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    main()