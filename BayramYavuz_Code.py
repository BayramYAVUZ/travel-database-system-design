import streamlit as st
import sqlite3
import pandas as pd
import time
import os
from datetime import datetime, timedelta

#=============================================================================================
#============               Bayram YAVUZ  ID : 122200058              ========================
#=============================================================================================

st.set_page_config(
    page_title="Travel Booking System",
    page_icon="logo-1.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

#=============================================================================================

DB_FILE = "travel_system_final.db"
BG_IMAGE = "deneme-1.png"  

#=============================================================================================

def add_bg():
    """Apply full app background (including sidebar)."""
    if os.path.exists(BG_IMAGE):
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url('{BG_IMAGE}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            /* sidebar */
            [data-testid="stSidebar"] {{
                background-image: url('{BG_IMAGE}');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            /* Make content backgrounds slightly opaque so text is readable */
            .css-18e3th9 {{ background-color: rgba(255,255,255,0.85); border-radius: 8px; padding: 1rem; }}
            .stDataFrame > div {{ background-color: rgba(255,255,255,0.85) !important; }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning(f"Background image '{BG_IMAGE}' not found in app folder. Put it next to the .py file to see background.")

def db_connect():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

#=============================================================================================

def table_has_column(table, column):
    with db_connect() as conn:
        cur = conn.cursor()
        cur.execute(f"PRAGMA table_info({table})")
        cols = [r[1] for r in cur.fetchall()]
        return column in cols

#=============================================================================================

def run_query(query, params=(), fetch=True):
    with db_connect() as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        if fetch:
            return cur.fetchall()
        return None

#=============================================================================================

def get_dataframe(query, params=()):
    with db_connect() as conn:
        return pd.read_sql(query, conn, params=params)

#=============================================================================================

def init_db():
    """Create tables and insert sample data if empty. Also perform safe migrations."""
    with db_connect() as conn:
        cursor = conn.cursor()

#=============================================================================================

        cursor.execute("""CREATE TABLE IF NOT EXISTS Customers (
            cust_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Destinations (
            dest_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            country TEXT NOT NULL
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Services (
            service_id INTEGER PRIMARY KEY AUTOINCREMENT,
            service_name TEXT NOT NULL,
            base_price REAL NOT NULL
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Hotels (
            hotel_id INTEGER PRIMARY KEY,
            stars INTEGER,
            FOREIGN KEY (hotel_id) REFERENCES Services(service_id) ON DELETE CASCADE
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Flights (
            flight_id INTEGER PRIMARY KEY,
            airline TEXT,
            FOREIGN KEY (flight_id) REFERENCES Services(service_id) ON DELETE CASCADE
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Rooms (
            room_id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_id INTEGER,
            room_no TEXT,
            FOREIGN KEY (hotel_id) REFERENCES Hotels(hotel_id) ON DELETE CASCADE
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Seats (
            seat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_id INTEGER,
            seat_no TEXT,
            FOREIGN KEY (flight_id) REFERENCES Flights(flight_id) ON DELETE CASCADE
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS TravelPackages (
            pkg_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dest_id INTEGER,
            pkg_name TEXT,
            price REAL,
            FOREIGN KEY (dest_id) REFERENCES Destinations(dest_id)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS PackageContents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pkg_id INTEGER,
            service_id INTEGER,
            FOREIGN KEY (pkg_id) REFERENCES TravelPackages(pkg_id) ON DELETE CASCADE,
            FOREIGN KEY (service_id) REFERENCES Services(service_id) ON DELETE CASCADE
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Bookings (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            cust_id INTEGER,
            pkg_id INTEGER,
            booking_date DATE DEFAULT CURRENT_DATE,
            is_paid INTEGER DEFAULT 0,
            FOREIGN KEY (cust_id) REFERENCES Customers(cust_id) ON DELETE CASCADE,
            FOREIGN KEY (pkg_id) REFERENCES TravelPackages(pkg_id)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Payments (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER,
            amount REAL,
            payment_date DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Reservations (
            res_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER,
            service_id INTEGER,
            room_id INTEGER,
            check_in DATE,
            check_out DATE,
            FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE,
            FOREIGN KEY (service_id) REFERENCES Services(service_id),
            FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS Tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            booking_id INTEGER,
            seat_id INTEGER,
            issue_date DATE DEFAULT CURRENT_DATE,
            FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE,
            FOREIGN KEY (seat_id) REFERENCES Seats(seat_id)
        )""")

        if not table_has_column("Bookings", "is_paid"):
            try:
                cursor.execute("ALTER TABLE Bookings ADD COLUMN is_paid INTEGER DEFAULT 0")
            except Exception:
                pass

        if not table_has_column("Reservations", "check_out"):
            try:
                cursor.execute("ALTER TABLE Reservations ADD COLUMN check_out DATE")
            except Exception:
                pass

        conn.commit()

        cursor.execute("SELECT COUNT(*) FROM Customers")
        if cursor.fetchone()[0] == 0:

#=============================================================================================

            customers = [
                ("Ali Yilmaz", "ali@mail.com"),
                ("Ayse Demir", "ayse@mail.com"),
                ("Mehmet Kara", "mehmet@mail.com"),
                ("Zeynep Aydin", "zeynep@mail.com"),
                ("Burak Aslan", "burak@mail.com")
            ]
            cursor.executemany("INSERT INTO Customers (name, email) VALUES (?, ?)", customers)

#=============================================================================================

            destinations = [
                ("Paris", "France"),
                ("Tokyo", "Japan"),
                ("Rome", "Italy"),
                ("New York", "USA"),
                ("Dubai", "UAE"),
                ("Istanbul", "Turkey"),
                ("Barcelona", "Spain"),
                ("Cairo", "Egypt"),
                ("Nice", "France (Nice)") 
            ]
            cursor.executemany("INSERT INTO Destinations (city, country) VALUES (?, ?)", destinations)

            services = [
                ("TK101 Flight", 1500), ("LH404 Flight", 2000), ("BA505 Flight", 2500), ("AA100 Flight", 1800), ("JL777 Flight", 2200),
                ("Hilton Paris", 3000), ("Rixos Antalya", 4500), ("Marriott Rome", 2800), ("Plaza NYC", 5000), ("Burj Al Arab", 8000)
            ]
            for i, (name, price) in enumerate(services):
                cursor.execute("INSERT INTO Services (service_name, base_price) VALUES (?, ?)", (name, price))
                service_id = cursor.lastrowid
                if i < 5:
                    cursor.execute("INSERT INTO Flights (flight_id, airline) VALUES (?, ?)", (service_id, name.split()[0]))
                    for seat_no in ["1A", "1B", "2A", "2B"]:
                        cursor.execute("INSERT INTO Seats (flight_id, seat_no) VALUES (?, ?)", (service_id, seat_no))
                else: 
                    cursor.execute("INSERT INTO Hotels (hotel_id, stars) VALUES (?, ?)", (service_id, 5))
                    for room_no in ["101", "102", "201", "202"]:
                        cursor.execute("INSERT INTO Rooms (hotel_id, room_no) VALUES (?, ?)", (service_id, room_no))

#=============================================================================================

            cursor.execute("SELECT dest_id FROM Destinations WHERE city='Paris' LIMIT 1")
            paris_id = cursor.fetchone()[0]
            cursor.execute("SELECT dest_id FROM Destinations WHERE city='Tokyo' LIMIT 1")
            tokyo_id = cursor.fetchone()[0]
            cursor.execute("SELECT dest_id FROM Destinations WHERE city='Rome' LIMIT 1")
            rome_id = cursor.fetchone()[0]
            cursor.execute("SELECT dest_id FROM Destinations WHERE city='New York' LIMIT 1")
            ny_id = cursor.fetchone()[0]
            cursor.execute("SELECT dest_id FROM Destinations WHERE city='Dubai' LIMIT 1")
            dubai_id = cursor.fetchone()[0]
            cursor.execute("SELECT dest_id FROM Destinations WHERE city='Istanbul' LIMIT 1")
            ist_id = cursor.fetchone()[0]
            cursor.execute("SELECT dest_id FROM Destinations WHERE city='Barcelona' LIMIT 1")
            bar_id = cursor.fetchone()[0]
            cursor.execute("SELECT dest_id FROM Destinations WHERE city='Cairo' LIMIT 1")
            cai_id = cursor.fetchone()[0]

#=============================================================================================

            packages = [
                (paris_id, "Romantic Escape", 5000),
                (tokyo_id, "Sakura Tour", 7000),
                (rome_id, "Ancient Rome", 4000),
                (ny_id, "NYC Lights", 6000),
                (dubai_id, "Dubai Luxury", 9000),

                (ist_id, "Türkiye Delight", 3500),
                (bar_id, "Spain Fiesta", 3800),
                (rome_id, "Italy Cultural Package", 5500),
                (paris_id, "France Tour Deluxe", 6200),
                (cai_id, "Egypt Nile Experience", 4800)
            ]
            cursor.executemany("INSERT INTO TravelPackages (dest_id, pkg_name, price) VALUES (?, ?, ?)", packages)

            cursor.execute("SELECT service_id FROM Services LIMIT 10")
            sids = [r[0] for r in cursor.fetchall()]
            if len(sids) >= 10:
                package_contents = [
                    (1, sids[5]), (1, sids[0]),
                    (2, sids[6]), (2, sids[1]),
                    (3, sids[7]), (3, sids[2]),
                    (4, sids[8]), (4, sids[3]),
                    (5, sids[9]), (5, sids[4]),
                    (6, sids[5]), (7, sids[6]),
                    (8, sids[7]), (9, sids[5]),
                    (10, sids[9])
                ]
                cursor.executemany("INSERT INTO PackageContents (pkg_id, service_id) VALUES (?, ?)", package_contents)

#=============================================================================================
  
            bookings = [
                (1, 1, "2025-01-10", 0),
                (2, 2, "2025-02-15", 0),
                (3, 3, "2025-03-20", 0),
                (4, 4, "2025-04-05", 0),
                (1, 5, "2025-05-12", 0)
            ]
            cursor.executemany("INSERT INTO Bookings (cust_id, pkg_id, booking_date, is_paid) VALUES (?, ?, ?, ?)", bookings)

#=============================================================================================

            payments = [
                (1, 5000), 
                (2, 4000), 
                (3, 4000), (4, 3000), (5, 9000)
            ]
            cursor.executemany("INSERT INTO Payments (booking_id, amount) VALUES (?, ?)", payments)

            cursor.execute("INSERT INTO Reservations (booking_id, service_id, room_id, check_in, check_out) VALUES (1, ?, 1, '2025-01-10', '2025-01-15')", (sids[5],))
            cursor.execute("INSERT INTO Tickets (booking_id, seat_id, issue_date) VALUES (1, 1, '2025-01-10')")

            conn.commit()

    update_all_booking_payment_statuses()

#=============================================================================================

def sum_payments_for_booking(booking_id):
    res = run_query("SELECT COALESCE(SUM(amount),0) FROM Payments WHERE booking_id=?", (booking_id,))
    return res[0][0] if res else 0

#=============================================================================================

def get_package_price(pkg_id):
    res = run_query("SELECT price FROM TravelPackages WHERE pkg_id=?", (pkg_id,))
    return res[0][0] if res else 0

#=============================================================================================

def update_booking_payment_status(booking_id):
    """Set Bookings.is_paid depending on payments vs package price"""
    total_paid = sum_payments_for_booking(booking_id)
    res = run_query("SELECT pkg_id FROM Bookings WHERE booking_id=?", (booking_id,))
    if not res:
        return
    pkg_id = res[0][0]
    price = get_package_price(pkg_id)
    status = 0
    if total_paid <= 0:
        status = 0
    elif total_paid < price:
        status = 1
    else:
        status = 2
    run_query("UPDATE Bookings SET is_paid=? WHERE booking_id=?", (status, booking_id), fetch=False)

#=============================================================================================

def update_all_booking_payment_statuses():
    rows = run_query("SELECT booking_id FROM Bookings")
    for r in rows:
        update_booking_payment_status(r[0])

# ===========================
# FRONTEND 
# ===========================

def main():
    add_bg() 
    st.title("ᯓ ✈︎ Travel Booking & Reservation System")
    st.markdown("### CMPE 351 Term Project | ID 122200058")
    init_db()

    menu = st.sidebar.radio("Navigation", [" • Dashboard", " • Data Entry (CRUD)", " • Manage Bookings", " • Reports & SQL"])

    if menu == " • Dashboard":
        show_dashboard()
    elif menu == " • Data Entry (CRUD)":
        show_data_entry()
    elif menu == " • Manage Bookings":
        show_bookings()
    elif menu == " • Reports & SQL":
        show_reports()

#=============================================================================================

def show_dashboard():
    st.subheader("System Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        count = run_query("SELECT COUNT(*) FROM Customers")[0][0]
        st.metric("Total Customers", count)
    with col2:
        count = run_query("SELECT COUNT(*) FROM Bookings")[0][0]
        st.metric("Total Bookings", count)
    with col3:
        count = run_query("SELECT COUNT(*) FROM TravelPackages")[0][0]
        st.metric("Packages Available", count)
    with col4:
        revenue_row = run_query("SELECT COALESCE(SUM(amount),0) FROM Payments")[0][0]
        st.metric("Total Revenue", f"${revenue_row:,.2f}")

    if os.path.exists(BG_IMAGE):
        st.image(BG_IMAGE, use_column_width=True, caption="Travel the World")
    else:
        st.image("C:\TravelBookingProject\deneme-1.png", use_column_width=True, caption="Travel the World")

    df = get_dataframe("""
        SELECT b.booking_id, b.booking_date, c.name as customer, tp.pkg_name as package,
               b.is_paid
        FROM Bookings b
        JOIN Customers c ON b.cust_id = c.cust_id
        JOIN TravelPackages tp ON b.pkg_id = tp.pkg_id
        ORDER BY b.booking_date DESC
        LIMIT 10
    """)
    if not df.empty:
        df['Payment Status'] = df['is_paid'].map({0: 'Unpaid', 1: 'Partial', 2: 'Paid'})
        st.dataframe(df.drop(columns=['is_paid']), use_container_width=True)
    else:
        st.info("No recent bookings to show.")

#=============================================================================================

def show_data_entry():
    st.header("📂 Data Management")
    tab1, tab2, tab3, tab4 = st.tabs(["Customers", "Destinations", "Services", "Packages"])
    with tab1:
        st.subheader("Manage Customers")
        with st.form("add_cust", clear_on_submit=True):
            c1, c2 = st.columns(2)
            name = c1.text_input("Full Name")
            email = c2.text_input("Email")
            if st.form_submit_button(" Add Customer"):
                if name and email:
                    try:
                        run_query("INSERT INTO Customers (name, email) VALUES (?, ?)", (name, email), fetch=False)
                        st.success(f"Customer {name} added!")
                        time.sleep(0.5)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("Please provide both name and email.")

        cust_df = get_dataframe("SELECT * FROM Customers")
        st.dataframe(cust_df, use_container_width=True)

        if not cust_df.empty:
            c1, c2 = st.columns(2)
            with c1:
                del_id = st.selectbox("Select Customer to Delete", cust_df['cust_id'], key="del_c")
                if st.button(" Delete Customer"):
                    run_query("DELETE FROM Customers WHERE cust_id=?", (del_id,), fetch=False)
                    st.warning("Customer deleted.")
                    st.rerun()

            with c2:
                upd_id = st.selectbox("Select Customer to Update", cust_df['cust_id'], key="upd_c")
                new_name = st.text_input("New Name", key="new_name")
                new_email = st.text_input("New Email", key="new_email")
                if st.button(" Update Customer"):
                    if new_name or new_email:
                        if new_name:
                            run_query("UPDATE Customers SET name=? WHERE cust_id=?", (new_name, upd_id), fetch=False)
                        if new_email:
                            run_query("UPDATE Customers SET email=? WHERE cust_id=?", (new_email, upd_id), fetch=False)
                        st.success("Customer updated.")
                        st.rerun()
                    else:
                        st.error("Provide a new name or email to update.")

    with tab2:
        st.subheader("Manage Destinations")
        with st.form("add_dest", clear_on_submit=True):
            c1, c2 = st.columns(2)
            city = c1.text_input("City")
            country = c2.text_input("Country")
            if st.form_submit_button(" Add Destination"):
                if city and country:
                    run_query("INSERT INTO Destinations (city, country) VALUES (?, ?)", (city, country), fetch=False)
                    st.success("Destination added!")
                    st.rerun()
                else:
                    st.error("Provide both city and country.")

        st.dataframe(get_dataframe("SELECT * FROM Destinations"), use_container_width=True)

        dests = get_dataframe("SELECT * FROM Destinations")
        if not dests.empty:
            c1, c2 = st.columns(2)
            with c1:
                del_id = st.selectbox("Select Destination to Delete", dests['dest_id'], key="del_dest")
                if st.button(" Delete Destination"):
                    run_query("DELETE FROM Destinations WHERE dest_id=?", (del_id,), fetch=False)
                    st.warning("Destination deleted.")
                    st.rerun()

            with c2:
                upd_id = st.selectbox("Select Destination to Update", dests['dest_id'], key="upd_dest")
                new_city = st.text_input("New City", key="new_city")
                new_country = st.text_input("New Country", key="new_country")
                if st.button(" Update Destination"):
                    if new_city:
                        run_query("UPDATE Destinations SET city=? WHERE dest_id=?", (new_city, upd_id), fetch=False)
                    if new_country:
                        run_query("UPDATE Destinations SET country=? WHERE dest_id=?", (new_country, upd_id), fetch=False)
                    st.success("Destination updated.")
                    st.rerun()

    with tab3:
        st.subheader("Manage Services (Flights & Hotels)")

        type_choice = st.radio("Service Type", ["Flight", "Hotel"], horizontal=True)

        with st.form("add_service", clear_on_submit=True):
            name = st.text_input("Service Name (e.g. TK101 or Hilton)")
            price = st.number_input("Base Price", min_value=0.0, step=10.0)

            extra = ""
            if type_choice == "Flight":
                extra = st.text_input("Airline Code")
            else:
                extra = st.number_input("Stars", min_value=1, max_value=5)

            if st.form_submit_button(" Add Service"):
                if not name:
                    st.error("Service name required.")
                else:
                    conn = db_connect()
                    cur = conn.cursor()

                    cur.execute("INSERT INTO Services (service_name, base_price) VALUES (?, ?)", (name, price))
                    new_id = cur.lastrowid

                    if type_choice == "Flight":
                        cur.execute("INSERT INTO Flights (flight_id, airline) VALUES (?, ?)", (new_id, extra))
                        for seat_no in ["1A","1B","2A","2B"]:
                            cur.execute("INSERT INTO Seats (flight_id, seat_no) VALUES (?, ?)", (new_id, seat_no))
                    else:
                        cur.execute("INSERT INTO Hotels (hotel_id, stars) VALUES (?, ?)", (new_id, extra))
                        for room_no in ["101","102","201","202"]:
                            cur.execute("INSERT INTO Rooms (hotel_id, room_no) VALUES (?, ?)", (new_id, room_no))

                    conn.commit()
                    conn.close()
                    st.success(f"{type_choice} Added with ID {new_id}")
                    st.rerun()

        st.markdown("#### All Services")
        services_df = get_dataframe("""
            SELECT s.service_id, s.service_name, s.base_price,
                   f.airline AS 'Airline (If Flight)',
                   h.stars AS 'Stars (If Hotel)'
            FROM Services s
            LEFT JOIN Flights f ON s.service_id = f.flight_id
            LEFT JOIN Hotels h ON s.service_id = h.hotel_id
        """)
        st.dataframe(services_df, use_container_width=True)
        st.markdown("###  Delete Service")

        if not services_df.empty:
            del_service = st.selectbox(
                "Select Service to Delete",
                services_df["service_id"],
                format_func=lambda x: services_df[services_df["service_id"] == x]["service_name"].values[0]
            )

            if st.button(" Delete Service"):
                run_query("DELETE FROM Services WHERE service_id=?", (del_service,), fetch=False)
                st.warning("Service deleted.")
                st.rerun()
        else:
            st.info("No services available to delete.")

    with tab4:
        st.subheader("Manage Travel Packages")

        with st.form("add_pkg", clear_on_submit=True):
            dests = get_dataframe("SELECT dest_id, city, country FROM Destinations")
            if dests.empty:
                st.info("Add destinations first.")
            else:
                dest_map = {row['dest_id']: f"{row['city']}, {row['country']}" for _, row in dests.iterrows()}
                pkg_name = st.text_input("Package Name")
                pkg_price = st.number_input("Package Price", min_value=0.0, step=10.0)
                dest_choice = st.selectbox("Destination", options=list(dest_map.keys()), 
                                           format_func=lambda x: dest_map[x])

                if st.form_submit_button("Add Package"):
                    if pkg_name:
                        run_query("INSERT INTO TravelPackages (dest_id, pkg_name, price) VALUES (?, ?, ?)",
                                  (dest_choice, pkg_name, pkg_price), fetch=False)
                        st.success("Package added.")
                        st.rerun()
                    else:
                        st.error("Package name required.")

        st.markdown("#### All Packages")
        st.dataframe(
            get_dataframe("""
                SELECT tp.pkg_id, tp.pkg_name, tp.price,
                       d.city || ', ' || d.country AS destination
                FROM TravelPackages tp
                JOIN Destinations d ON tp.dest_id = d.dest_id
            """),
            use_container_width=True,
        )

        pkgs = get_dataframe("SELECT pkg_id, pkg_name, price FROM TravelPackages")

        if not pkgs.empty:
            c1, c2 = st.columns(2)
            with c1:
                del_id = st.selectbox("Select Package to Delete", pkgs['pkg_id'], key="del_pkg")
                if st.button("Delete Package"):
                    run_query("DELETE FROM TravelPackages WHERE pkg_id=?", (del_id,), fetch=False)
                    st.warning("Package deleted.")
                    st.rerun()

            with c2:
                upd_id = st.selectbox("Select Package to Update", pkgs['pkg_id'], key="upd_pkg")
                new_name = st.text_input("New Package Name", key="new_pkg_name")
                new_price = st.number_input("New Package Price", min_value=0.0, step=10.0, key="new_pkg_price")
                if st.button("Update Package"):
                    if new_name:
                        run_query("UPDATE TravelPackages SET pkg_name=? WHERE pkg_id=?", (new_name, upd_id), fetch=False)
                    if new_price:
                        run_query("UPDATE TravelPackages SET price=? WHERE pkg_id=?", (new_price, upd_id), fetch=False)
                    st.success("Package updated.")
                    st.rerun()

        st.markdown("#### Manage Package Contents (Which services a package contains)")

        pkgs = get_dataframe("SELECT pkg_id, pkg_name FROM TravelPackages")
        services = get_dataframe("SELECT service_id, service_name FROM Services")

        if pkgs.empty or services.empty:
            st.info("Add packages and services to manage contents.")
        else:
            pcol1, pcol2 = st.columns(2)

            with pcol1:
                chosen_pkg = st.selectbox("Choose Package", pkgs['pkg_id'], 
                                          format_func=lambda x: pkgs[pkgs['pkg_id']==x]['pkg_name'].values[0])
                chosen_service = st.selectbox("Choose Service to Add", services['service_id'],
                                              format_func=lambda x: services[services['service_id']==x]['service_name'].values[0])

                if st.button(" Add Service to Package"):
                    run_query("INSERT INTO PackageContents (pkg_id, service_id) VALUES (?, ?)",
                              (chosen_pkg, chosen_service), fetch=False)
                    st.success("Service added to package.")
                    st.rerun()

            with pcol2:
                dfpc = get_dataframe("""
                    SELECT pc.id, tp.pkg_name, s.service_name
                    FROM PackageContents pc
                    JOIN TravelPackages tp ON pc.pkg_id = tp.pkg_id
                    JOIN Services s ON pc.service_id = s.service_id
                    ORDER BY pc.id DESC
                """)
                st.dataframe(dfpc, use_container_width=True)

                if not dfpc.empty:
                    del_row = st.selectbox("Select PackageContent ID to delete", dfpc['id'])
                    if st.button("Remove selected content"):
                        run_query("DELETE FROM PackageContents WHERE id=?", (del_row,), fetch=False)
                        st.success("Removed.")
                        st.rerun()


#=============================================================================================

def show_bookings():
    st.header("📅 Manage Bookings")
    st.subheader("Create New Booking")

    customers = get_dataframe("SELECT cust_id, name FROM Customers")
    packages = get_dataframe("SELECT pkg_id, pkg_name, price FROM TravelPackages")

    if customers.empty or packages.empty:
        st.warning("Please add Customers and Packages first.")
    else:
        with st.form("new_booking"):
            c1, c2, c3 = st.columns(3)
            cust_idx = c1.selectbox("Customer", customers['cust_id'], format_func=lambda x: customers[customers['cust_id']==x]['name'].values[0])
            pkg_idx = c2.selectbox("Package", packages['pkg_id'], format_func=lambda x: f"{packages[packages['pkg_id']==x]['pkg_name'].values[0]} (${packages[packages['pkg_id']==x]['price'].values[0]})")
            date = c3.date_input("Booking Date")
            if st.form_submit_button("Confirm Booking"):
                run_query("INSERT INTO Bookings (cust_id, pkg_id, booking_date) VALUES (?, ?, ?)", (cust_idx, pkg_idx, date), fetch=False)
                st.success("Booking Created Successfully!")
                time.sleep(1)
                st.rerun()

    st.divider()
    st.subheader("Manage Existing Bookings (Update / Delete)")
    bookings = get_dataframe("SELECT b.booking_id, b.booking_date, c.name, tp.pkg_name, b.is_paid FROM Bookings b JOIN Customers c ON b.cust_id = c.cust_id JOIN TravelPackages tp ON b.pkg_id = tp.pkg_id")
    if bookings.empty:
        st.info("No bookings yet.")
    else:
        st.dataframe(bookings, use_container_width=True)
        b1, b2 = st.columns(2)
        with b1:
            sel_booking = st.selectbox("Choose Booking to Update", bookings['booking_id'], format_func=lambda x: f"ID {x}")
            new_pkg = st.selectbox("New Package", packages['pkg_id'], format_func=lambda x: f"{packages[packages['pkg_id']==x]['pkg_name'].values[0]}")
            new_date = st.date_input("New Booking Date")
            if st.button("Update Booking"):
                run_query("UPDATE Bookings SET pkg_id=?, booking_date=? WHERE booking_id=?", (new_pkg, new_date, sel_booking), fetch=False)
                update_booking_payment_status(sel_booking)
                st.success("Booking updated.")
                st.rerun()
        with b2:
            del_booking = st.selectbox("Choose Booking to Delete", bookings['booking_id'], format_func=lambda x: f"ID {x}", key="del_booking")
            if st.button(" Delete Booking"):
                run_query("DELETE FROM Bookings WHERE booking_id=?", (del_booking,), fetch=False)
                st.warning("Booking deleted (and related payments/tickets/reservations cascaded).")
                st.rerun()

    st.divider()
    st.subheader("Process Payment")
    booking_list = get_dataframe("SELECT b.booking_id, c.name, tp.pkg_name, tp.price FROM Bookings b JOIN Customers c ON b.cust_id=c.cust_id JOIN TravelPackages tp ON b.pkg_id = tp.pkg_id")
    if booking_list.empty:
        st.info("No bookings to process payment.")
    else:
        with st.form("new_payment"):
            bsel = st.selectbox("Select Booking", booking_list['booking_id'], format_func=lambda x: f"ID {x}: {booking_list[booking_list['booking_id']==x]['name'].values[0]} - {booking_list[booking_list['booking_id']==x]['pkg_name'].values[0]}")
            amt = st.number_input("Amount ($)", min_value=0.0)
            if st.form_submit_button("Add Payment"):
                run_query("INSERT INTO Payments (booking_id, amount) VALUES (?, ?)", (bsel, amt), fetch=False)
                update_booking_payment_status(bsel)
                st.success("Payment Recorded!")
                st.rerun()

#=============================================================================================

def show_reports():
    st.header("📊 Reports & JOIN Queries")

    st.markdown("### 1. Comprehensive Booking Report (Complex JOIN)")
    st.markdown("Displays who booked what, where they are going, and total payments.")
    sql = """
    SELECT
        b.booking_id AS ID,
        b.booking_date AS Date,
        c.name AS Customer,
        c.email AS Contact,
        tp.pkg_name AS Package,
        tp.price AS Package_Price,
        d.city || ', ' || d.country AS Destination,
        COALESCE(SUM(pay.amount), 0) AS Total_Paid,
        CASE b.is_paid WHEN 0 THEN 'Unpaid' WHEN 1 THEN 'Partial' WHEN 2 THEN 'Paid' ELSE 'Unknown' END AS Payment_Status
    FROM Bookings b
    JOIN Customers c ON b.cust_id = c.cust_id
    JOIN TravelPackages tp ON b.pkg_id = tp.pkg_id
    JOIN Destinations d ON tp.dest_id = d.dest_id
    LEFT JOIN Payments pay ON b.booking_id = pay.booking_id
    GROUP BY b.booking_id
    ORDER BY b.booking_date DESC
    """
    df = get_dataframe(sql)
    st.dataframe(df, use_container_width=True)

    st.divider()

    st.markdown("### 2. Service Inventory Status")
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Hotel Rooms")
        st.dataframe(get_dataframe("""
            SELECT h.hotel_id, s.service_name, COUNT(r.room_id) as Total_Rooms
            FROM Hotels h
            JOIN Services s ON h.hotel_id = s.service_id
            LEFT JOIN Rooms r ON h.hotel_id = r.hotel_id
            GROUP BY h.hotel_id
        """), use_container_width=True)
    with col2:
        st.caption("Flight Seats")
        st.dataframe(get_dataframe("""
            SELECT f.flight_id, s.service_name, f.airline, COUNT(st.seat_id) as Total_Seats
            FROM Flights f
            JOIN Services s ON f.flight_id = s.service_id
            LEFT JOIN Seats st ON f.flight_id = st.flight_id
            GROUP BY f.flight_id
        """), use_container_width=True)

    st.divider()
    st.markdown("### 3. Customer Spending Report")
    st.markdown("Total paid per customer")
    rpt = get_dataframe("""
        SELECT c.cust_id, c.name, c.email, COALESCE(SUM(p.amount),0) AS total_paid
        FROM Customers c
        LEFT JOIN Bookings b ON c.cust_id = b.cust_id
        LEFT JOIN Payments p ON b.booking_id = p.booking_id
        GROUP BY c.cust_id
        ORDER BY total_paid DESC
    """)
    st.dataframe(rpt, use_container_width=True)


#=============================================================================================


if __name__ == "__main__":
    main()

#=============================================================================================
#============               Bayram YAVUZ  ID : 122200058              ========================
#=============================================================================================