class User:
    def __init__(self, user_id, name, username, password, role):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = password
        self.role = role

    def login(self, username, password):
        if self.username == username and self.password == password:
            print("Login successful! Welcome", self.name)
            return True
        else:
            print("Invalid username or password")
            return False

    def display_info(self):
        print("User ID:", self.user_id)
        print("Name:", self.name)
        print("Role:", self.role)


class Admin(User):
    def __init__(self, user_id, name, username, password):
        super().__init__(user_id, name, username, password, "admin")

    def manage_system(self):
        print("Admin is managing the hotel system")


class Staff(User):
    def __init__(self, user_id, name, username, password, position):
        super().__init__(user_id, name, username, password, "staff")
        self.position = position

    def work(self):
        print(self.name, "is working as", self.position)


class Customer(User):
    def __init__(self, user_id, name, username, password):
        super().__init__(user_id, name, username, password, "customer")
        self.room_number = None

    def book_room(self, room_number):
        self.room_number = room_number
        print("Room", room_number, "booked successfully")

    def view_booking(self):
        if self.room_number is not None:
            print("Booked Room:", self.room_number)
        else:
            print("No room booked")


# Test (this will run only if file is executed directly)
if __name__ == "__main__":
    admin = Admin(1, "Admin", "admin", "1234")
    staff = Staff(2, "John", "john", "1234", "Receptionist")
    customer = Customer(3, "Alice", "alice", "1234")

    print("\n--- Login Test ---")
    admin.login("admin", "1234")

    print("\n--- Staff Work ---")
    staff.work()

    print("\n--- Booking ---")
    customer.book_room(101)
    customer.view_booking()
