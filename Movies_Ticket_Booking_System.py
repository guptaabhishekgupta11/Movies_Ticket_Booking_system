import sqlite3
import random

class MovieTicketBookingSystem:
    def __init__(self):
        self.conn = sqlite3.connect('movie_ticket_system.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                movie_id INTEGER PRIMARY KEY,
                movie_name TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                username TEXT,
                movie_id INTEGER,
                num_tickets INTEGER,
                total_cost INTEGER,
                FOREIGN KEY (username) REFERENCES users (username),
                FOREIGN KEY (movie_id) REFERENCES movies (movie_id)
            )
        ''')
        self.conn.commit()

    def register_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO users VALUES (?, ?)', (username, password))
        self.conn.commit()
        print("Registration successful.")

    def login_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()
        if result:
            print("Login successful.")
            return True
        else:
            print("Invalid username or password. Please try again.")
            return False

    def display_movies(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM movies')
        movies = cursor.fetchall()
        print("\nAvailable Movies:")
        for movie_id, movie_name in movies:
            print(f"{movie_id}. {movie_name}")

    def add_movie(self, movie_name):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO movies (movie_name) VALUES (?)', (movie_name,))
        self.conn.commit()
        print(f"\nMovie '{movie_name}' added successfully.")

    def add_movies_bulk(self, movies):
        cursor = self.conn.cursor()
        for movie_name in movies:
            cursor.execute('INSERT INTO movies (movie_name) VALUES (?)', (movie_name,))
        self.conn.commit()
        print(f"\n{len(movies)} movies added successfully.")

    def book_ticket(self, username, movie_id, num_tickets):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM movies WHERE movie_id=?', (movie_id,))
        movie = cursor.fetchone()

        if movie:
            cost_per_ticket = random.randint(8, 15)
            total_cost = cost_per_ticket * num_tickets

            cursor.execute('INSERT INTO bookings VALUES (?, ?, ?, ?)', (username, movie_id, num_tickets, total_cost))
            self.conn.commit()
            print(f"\nBooking successful for {num_tickets} tickets for {movie[1]}.")
            print(f"Total Cost: ${total_cost}")
        else:
            print("Invalid movie selection.")

    def cancel_booking(self, username):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM bookings WHERE username=?', (username,))
        booking = cursor.fetchone()

        if booking:
            cursor.execute('DELETE FROM bookings WHERE username=?', (username,))
            self.conn.commit()
            print(f"\nBooking canceled for {booking[2]} tickets for movie ID {booking[1]}.")
        else:
            print("No active booking found.")

def main():
    movie_system = MovieTicketBookingSystem()

    while True:
        print("\nMovie Ticket Booking System:")
        print("1. Register")
        print("2. Login")
        print("3. Display Movies")
        print("4. Add Movie")
        print("5. Add Movies (Bulk)")
        print("6. Book Ticket")
        print("7. Cancel Booking")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            movie_system.register_user(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if movie_system.login_user(username, password):
                while True:
                    inner_choice = input("\n1. Display Movies\n2. Add Movie\n3. Add Movies (Bulk)\n4. Book Ticket\n5. Cancel Booking\n6. Logout\nEnter your choice (1-6): ")
                    if inner_choice == '1':
                        movie_system.display_movies()
                    elif inner_choice == '2':
                        movie_name = input("Enter the name of the movie: ")
                        movie_system.add_movie(movie_name)
                    elif inner_choice == '3':
                        movies_input = input("Enter multiple movie names separated by commas: ")
                        movies = [movie.strip() for movie in movies_input.split(',')]
                        movie_system.add_movies_bulk(movies)
                    elif inner_choice == '4':
                        movie_system.display_movies()
                        movie_id = int(input("Enter the movie ID: "))
                        num_tickets = int(input("Enter the number of tickets: "))
                        movie_system.book_ticket(username, movie_id, num_tickets)
                    elif inner_choice == '5':
                        movie_system.cancel_booking(username)
                    elif inner_choice == '6':
                        print("Logging out.")
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 6.")
        elif choice == '3':
            movie_system.display_movies()
        elif choice == '4':
            movie_name = input("Enter the name of the movie: ")
            movie_system.add_movie(movie_name)
        elif choice == '5':
            movies_input = input("Enter multiple movie names separated by commas: ")
            movies = [movie.strip() for movie in movies_input.split(',')]
            movie_system.add_movies_bulk(movies)
        elif choice == '6':
            print("Login required to book a ticket.")
        elif choice == '7':
            print("Login required to cancel a booking.")
        elif choice == '8':
            print("Exiting Movie Ticket Booking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
