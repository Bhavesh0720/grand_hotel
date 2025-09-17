from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import pymysql
from pymysql import MySQLError
from datetime import datetime, timedelta
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = 'dhaval123'  # Set your secret key for sessions
app.permanent_session_lifetime = timedelta(minutes=10)

@app.before_request
def make_session_permanent():
    session.permanent = True  # This will make the session expire based on `PERMANENT_SESSION_LIFETIME`
    session.modified = True   # Refresh session timeout on every request

def create_connection():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("dpg-d35bfc2li9vc739ll81g-a"),
            user=os.environ.get("hotel_user"),
            password=os.environ.get("sR7FO3JRyOj2ZqgLbYAin5p7PDT3efQu"),
            dbname=os.environ.get("grand_hotel_db"),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# # Database connection function
# def create_connection():
#     try:
#         connection = pymysql.connect(
#             host='localhost',
#             user='root',
#             password='',
#             database='hotel',
#             cursorclass=pymysql.cursors.DictCursor
#         )
#         return connection
#     except MySQLError as e:
#         print(f"Database Connection Error: {e}")
#         return None


@app.route('/')
def index():
    # Assuming you're using PyMySQL for database connection
    conn = create_connection()

    try:
        with conn.cursor() as cursor:
            # Fetch only the desired room types
            query = """
                SELECT room_type, rate
                FROM room
                WHERE room_type IN ('Business Class', 'Deluxe Suite', 'Family Room')
                GROUP BY room_type
            """
            cursor.execute(query)
            rooms = cursor.fetchall()
            conn.close()
    finally:
        # Pass the room data to the template
        return render_template('index.html', rooms=rooms)


@app.route('/signup')
def signup():
    return render_template('signUp.html')  # Render the signup form


@app.route('/handle_signup', methods=['POST'])
def handle_signup():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    password = request.form.get('password')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    address = request.form.get('address')
    terms = request.form.get('terms')

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO users (first_name, last_name, password, email, phone_number, address, terms)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, password, email, phone_number, address, terms)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
            return redirect(url_for('login'))
        except MySQLError as e:
            print(f"Database Error: {e}")
            return f"Error occurred while inserting data: {e}", 500
    return "Failed to connect to database", 500


@app.route('/login')
def login():
    return render_template('login.html')  # Render the login form


@app.route('/handle_login', methods=['POST'])
def handle_login():
    email = request.form.get('email')
    password = request.form.get('password')

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user:
                # Check if the user is blocked
                if user['is_blocked']:
                    error_message = 'Your account has been blocked. Please contact support.'
                    return render_template('login.html', error_message=error_message)

                # Check if the password matches (you should hash the password in production)
                if user['password'] == password:
                    session['user_id'] = user['user_id']
                    session['first_name'] = user.get('first_name', 'Guest')
                    session['is_admin'] = user.get('is_admin', False)
                    session['email'] = user['email']

                    # Redirect to admin dashboard if the user is an admin
                    if session['is_admin']:
                        return redirect(url_for('admin_dashboard'))
                    else:
                        return redirect(url_for('index'))
                else:
                    error_message = 'Invalid email or password. Please try again.'
                    return render_template('login.html', error_message=error_message)
            else:
                error_message = 'Invalid email or password. Please try again.'
                return render_template('login.html', error_message=error_message)
        except MySQLError as e:
            print(f"Database Error: {e}")
            return f"Error occurred while logging in: {e}", 500
    return "Failed to connect to database", 500


@app.route('/rooms')
def rooms():
    conn = create_connection()

    try:
        with conn.cursor() as cursor:
            # Fetch only the desired room types
            query = """
                    SELECT room_type, rate
                    FROM room
                    GROUP BY room_type
                """
            cursor.execute(query)
            rooms = cursor.fetchall()
    finally:
        conn.close()

    # Pass the room data to the template
    return render_template('rooms.html', rooms=rooms)


@app.route('/get_rooms/<room_type>', methods=['GET'])
def get_rooms(room_type):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Query to get all room_ids of the selected room_type that are not already booked
            query = """
                SELECT r.room_id
                FROM room r
                LEFT JOIN reservations res ON r.room_id = res.room_id
                AND (
                    res.check_in_date <= CURDATE() AND res.check_out_date >= CURDATE()
                )
                WHERE r.room_type = %s
                AND res.room_id IS NULL;  # Only select rooms that are not reserved
            """
            cursor.execute(query, (room_type,))
            available_rooms = cursor.fetchall()

            # Extract room_ids from the result
            room_ids = [room['room_id'] for room in available_rooms]

            return jsonify(room_ids)
    except Exception as e:
        print(f"Error retrieving available rooms: {e}")
        return jsonify([])  # Return empty list on error
    finally:
        connection.close()


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    today_date = datetime.today().strftime('%Y-%m-%d')

    # Initialize room_type to empty string or default value
    room_type = request.args.get('room_type', '')  # Can be from the URL if passed in

    if request.method == 'POST':
        room_type = request.form.get('room_type')
        room_id = request.form.get('room_no')  # Ensure this matches the form field name
        reservation_date = request.form.get('reservation_date')
        check_in_date = request.form.get('check_in_date')
        check_out_date = request.form.get('check_out_date')
        notes = request.form.get('message')  # Match this to the form field name

        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = """
                INSERT INTO reservations (user_id, reservation_date, room_id, room_type, check_in_date, check_out_date, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                values = (user_id, reservation_date, room_id, room_type, check_in_date, check_out_date, notes)
                cursor.execute(query, values)
                connection.commit()
                # Flash success message
                flash("Reservation successful!")
                # return redirect(url_for('index'))  # Or a success page
            except Exception as e:
                print(f"Error during reservation: {e}")
                flash('An error occurred while processing your reservation.', 'danger')
                return redirect(url_for('reservation'))
            finally:
                cursor.close()
                connection.close()

    return render_template('reservation.html', user_id=user_id, today_date=today_date, room_type=room_type)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/profile')
def profile():
    if 'user_id' not in session:  # Updated to user_id
        return redirect(url_for('login'))

    user_id = session['user_id']  # Updated to user_id
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Fetch user details
            user_query = "SELECT first_name, last_name, email, phone_number, address FROM users WHERE user_id = %s"  # Updated to user_id
            cursor.execute(user_query, (user_id,))
            user = cursor.fetchone()

            # Fetch user's past reservations
            reservations_query = """
            SELECT reservation_id, room_id, room_type, check_in_date, check_out_date, reservation_date, notes
            FROM reservations WHERE user_id = %s  # Updated to user_id
            ORDER BY reservation_date DESC
            """
            cursor.execute(reservations_query, (user_id,))
            reservations = cursor.fetchall()

            cursor.close()
            connection.close()
            return render_template('profile.html', user=user, reservations=reservations)
        except MySQLError as e:
            print(f"Database Error: {e}")
            return f"Error occurred while fetching profile data: {e}", 500
    return "Failed to connect to database", 500


@app.route('/events')
def events():
    return render_template('events.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/handle_contact', methods=['GET', 'POST'])
def handle_contact():

    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        message = request.form.get('message')

        # Check if all required fields are filled
        if not name or not email or not message:
            flash('Please fill out all required fields.')
            return redirect(url_for('contact'))

        # Insert data into the database
        try:
            connection = create_connection()
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO contact_form (name, phone, email, message)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (name, phone, email, message))
                connection.commit()
                flash('Your message has been sent successfully!')
        except Exception as e:
            connection.rollback()
            return f'Error: {str(e)}'
        finally:
            connection.close()

        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/terms_and_conditions')
def terms_and_conditions():
    return render_template('terms_and_conditions.html')


@app.route('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')


@app.route('/our_location')
def our_location():
    return render_template('our_location.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Updated to user_id
    session.pop('first_name', None)
    session.pop('is_admin', None)
    session.pop('email', None)
    return redirect(url_for('index'))


# ADMIN SIDE PEANAL
@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    else:
        return render_template('admin_dashboard.html')


@app.route('/api/dashboard-stats', methods=['GET'])
def get_dashboard_stats():
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch total users
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]

            # Fetch total admins
            cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
            total_admins = cursor.fetchone()[0]

            # Fetch available rooms
            cursor.execute("SELECT COUNT(*) FROM rooms WHERE room_id NOT IN (SELECT room_id FROM reservations WHERE check_in_date <= CURDATE() AND check_out_date >= CURDATE())")
            available_rooms = cursor.fetchone()[0]

        return jsonify({
            'totalUsers': total_users,
            'totalAdmins': total_admins,
            'availableRooms': available_rooms
        })
    except Exception as e:
        print(f"Error fetching dashboard stats: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        connection.close()


@app.route('/api/recent-reservations', methods=['GET'])
def get_recent_reservations():
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch recent reservations (example query, adjust as needed)
            cursor.execute("""
                SELECT reservation_id, user_id, room_id, check_in_date, check_out_date
                FROM reservations
                ORDER BY reservation_date DESC
                LIMIT 10
            """)
            reservations = cursor.fetchall()

        return jsonify({'reservations': reservations})
    except Exception as e:
        print(f"Error fetching recent reservations: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
    finally:
        connection.close()


# Route to get all reservations
@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM reservations"
            cursor.execute(sql)
            reservations = cursor.fetchall()
            return jsonify(reservations)
    finally:
        connection.close()


# Route to delete a reservation by ID
@app.route('/api/reservations/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM reservations WHERE reservation_id = %s"
            cursor.execute(sql, (reservation_id,))
            connection.commit()
            return jsonify({'message': 'Reservation deleted successfully'}), 200
    finally:
        connection.close()


@app.route('/manage_booking')
def manage_booking():
    if 'user_id' not in session or not session.get('is_admin', False):
        return redirect(url_for('login'))
    else:
        return render_template('manage_reservations.html')


@app.route('/admin/manage_rooms', methods=['GET', 'POST'])
def manage_rooms():
    if 'user_id' not in session or not session.get('is_admin', False):
        return redirect(url_for('login'))

    connection = create_connection()
    cursor = connection.cursor()
    if request.method == 'POST':
        room_id = request.form.get('room-id')  # Get room_id from the form
        room_type = request.form.get('room-type')
        room_rate = request.form.get('room-rate')
        action = request.form.get('action')

        if action == 'add':
            # Add room with room_id specified
            cursor.execute("INSERT INTO room (room_id, room_type, rate) VALUES (%s, %s, %s)", (room_id, room_type, room_rate))
            connection.commit()

        elif action == 'edit':
            # Update room details
            cursor.execute("UPDATE room SET room_type = %s, rate = %s WHERE room_id = %s", (room_type, room_rate, room_id))
            connection.commit()

        elif action == 'delete':
            # Delete the room
            cursor.execute("DELETE FROM room WHERE room_id = %s", (room_id,))
            connection.commit()

    # Fetch the list of rooms to display
    cursor.execute("SELECT room_id, room_type, rate FROM room")
    rooms = cursor.fetchall()

    # Categorize rooms
    categorized_rooms = {}
    for room in rooms:
        room_type = room['room_type']
        if room_type not in categorized_rooms:
            categorized_rooms[room_type] = []
        categorized_rooms[room_type].append(room)

    return render_template('manage_rooms.html', rooms=rooms, categorized_rooms=categorized_rooms)


# Fetch all users (GET)
@app.route('/api/users', methods=['GET'])
def get_users():
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT user_id, first_name, last_name, email, phone_number, address, terms, is_admin, is_blocked FROM users"
            cursor.execute(sql)
            users = cursor.fetchall()
        return jsonify(users)
    finally:
        connection.close()


# Add a new user (POST)
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.form
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')  # Make sure to hash this in a real app
    phone_number = data.get('phone_number')
    address = data.get('address')
    terms = data.get('terms') == '1'
    is_admin = data.get('is_admin') == '1'

    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO users (first_name, last_name, email, password, phone_number, address, terms, is_admin)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (first_name, last_name, email, password, phone_number, address, terms, is_admin))
            connection.commit()
        return redirect(url_for('manage_users'))
    finally:
        connection.close()


# Delete a user (DELETE)
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM users WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            connection.commit()
        return jsonify({"message": "User deleted successfully!"})
    finally:
        connection.close()


# Route for the manage users page
@app.route('/manage_users')
def manage_users():
    if 'user_id' not in session or not session.get('is_admin', False):
        return redirect(url_for('login'))
    else:
        return render_template('manage_users.html')


@app.route('/api/users/<int:user_id>/toggle_admin', methods=['PATCH'])
def toggle_admin(user_id):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch the current role
            sql = "SELECT is_admin FROM users WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            current_role = cursor.fetchone()

            if current_role is None:
                return jsonify({"message": "User not found!"}), 404

            new_role = not current_role['is_admin']

            # Update the user's admin status
            sql = "UPDATE users SET is_admin = %s WHERE user_id = %s"
            cursor.execute(sql, (new_role, user_id))
            connection.commit()

        return jsonify({"message": "User role updated successfully!"})
    finally:
        connection.close()


@app.route('/api/users/<int:user_id>/toggle_block', methods=['PATCH'])
def toggle_block(user_id):
    connection = create_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch the current block status
            sql = "SELECT is_blocked FROM users WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            current_status = cursor.fetchone()

            if current_status is None:
                return jsonify({"message": "User not found!"}), 404

            new_status = not current_status['is_blocked']

            # Update the user's block status
            sql = "UPDATE users SET is_blocked = %s WHERE user_id = %s"
            cursor.execute(sql, (new_status, user_id))
            connection.commit()

        return jsonify({"message": "User status updated successfully!"})
    finally:
        connection.close()

# ADMIN SIDE PENAL


if __name__ == '__main__':
    app.run(debug=True)
