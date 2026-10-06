import streamlit as st
from database import SessionLocal, Event, Registration
from datetime import date


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="College Event Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 College Event Management System")


# =========================================================
# SIDEBAR MENU
# =========================================================

st.sidebar.title("Menu")

choice = st.sidebar.selectbox(
    "Choose an option",
    [
        "Dashboard",
        "Home",
        "Add Event",
        "View Events",
        "Register for Event",
        "My Registrations"
    ]
)


# =========================================================
# DASHBOARD
# =========================================================

if choice == "Dashboard":

    st.header("📊 Admin Dashboard")

    db = SessionLocal()

    # Get all events first
    events = db.query(Event).order_by(
        Event.date,
        Event.time
    ).all()

    # Total events
    total_events = len(events)

    # Remove registrations belonging to deleted events
    event_ids = [event.id for event in events]

    if event_ids:
        db.query(Registration).filter(
            ~Registration.event_id.in_(event_ids)
        ).delete(synchronize_session=False)
    else:
        db.query(Registration).delete()

    db.commit()

    # Total registrations
    total_registrations = db.query(Registration).count()

    # Total available seats
    total_available_seats = 0

    for event in events:

        registration_count = (
            db.query(Registration)
            .filter(
                Registration.event_id == event.id
            )
            .count()
        )

        available_seats = (
            event.capacity - registration_count
        )

        total_available_seats += available_seats

    # Dashboard metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📅 Total Events",
            total_events
        )

    with col2:
        st.metric(
            "👥 Total Registrations",
            total_registrations
        )

    with col3:
        st.metric(
            "🪑 Available Seats",
            total_available_seats
        )

    # =====================================================
    # UPCOMING EVENTS
    # =====================================================

    st.subheader("🔜 Upcoming Events")

    today = date.today()

    upcoming_events = [
        event
        for event in events
        if event.date >= today
    ]

    if len(upcoming_events) == 0:

        st.info("No upcoming events.")

    else:

        for event in upcoming_events:

            st.write(
                f"📅 **{event.name}** — "
                f"{event.date} at {event.time}"
            )

    # =====================================================
    # REGISTRATION CHART
    # =====================================================

    st.subheader("📊 Registration Chart")

    chart_data = {}

    for event in events:

        count = (
            db.query(Registration)
            .filter(
                Registration.event_id == event.id
            )
            .count()
        )

        chart_data[event.name] = count

    if chart_data:

        st.bar_chart(chart_data)

    else:

        st.info(
            "No registration data available."
        )

    # =====================================================
    # EVENT SUMMARY
    # =====================================================

    st.subheader("📋 Event Summary")

    if len(events) == 0:

        st.info("No events available.")

    else:

        for event in events:

            count = (
                db.query(Registration)
                .filter(
                    Registration.event_id == event.id
                )
                .count()
            )

            available = (
                event.capacity - count
            )

            st.write(
                f"**{event.name}** — "
                f"👥 {count} registration(s) | "
                f"🪑 {available} seat(s) available"
            )

    db.close()


# =========================================================
# HOME
# =========================================================

elif choice == "Home":

    st.header("🏠 Home")

    st.write(
        "Manage college events easily from one place."
    )

    st.write("### Features")

    st.write("📅 Add and manage college events")
    st.write("👥 Register students for events")
    st.write("🪑 Manage event capacity")
    st.write("📊 View registration statistics")
    st.write("🔍 Search events")
    st.write("✏️ Edit events")
    st.write("🗑️ Delete events")


# =========================================================
# ADD EVENT
# =========================================================

elif choice == "Add Event":

    st.header("➕ Add New Event")

    event_name = st.text_input(
        "Event Name"
    )

    event_date = st.date_input(
        "Event Date"
    )

    event_time = st.time_input(
        "Event Time"
    )

    venue = st.text_input(
        "Venue"
    )

    organizer = st.text_input(
        "Organizer Name"
    )

    description = st.text_area(
        "Event Description"
    )

    capacity = st.number_input(
        "Maximum Capacity",
        min_value=1,
        value=50,
        step=1
    )

    if st.button("Add Event"):

        if (
            event_name.strip()
            and venue.strip()
            and organizer.strip()
        ):

            db = SessionLocal()

            new_event = Event(
                name=event_name.strip(),
                date=event_date,
                time=event_time,
                venue=venue.strip(),
                organizer=organizer.strip(),
                description=description.strip(),
                capacity=capacity
            )

            db.add(new_event)
            db.commit()
            db.close()

            st.success(
                "✅ Event added successfully!"
            )

            st.rerun()

        else:

            st.error(
                "Please fill Event Name, Venue and Organizer Name."
            )


# =========================================================
# VIEW EVENTS
# =========================================================

elif choice == "View Events":

    st.header("📅 View Events")

    db = SessionLocal()

    events = db.query(Event).order_by(
        Event.date,
        Event.time
    ).all()

    if len(events) == 0:

        st.info("No events available.")

    else:

        search = st.text_input(
            "🔍 Search Event"
        )

        filtered_events = [
            event
            for event in events
            if search.lower() in event.name.lower()
        ]

        if len(filtered_events) == 0:

            st.warning(
                "No matching events found."
            )

        else:

            for event in filtered_events:

                st.subheader(event.name)

                st.write(
                    "📅 Date:",
                    event.date
                )

                st.write(
                    "⏰ Time:",
                    event.time
                )

                st.write(
                    "📍 Venue:",
                    event.venue
                )

                st.write(
                    "👤 Organizer:",
                    event.organizer
                )

                st.write(
                    "📝 Description:",
                    event.description
                )

                # Registration count
                registration_count = (
                    db.query(Registration)
                    .filter(
                        Registration.event_id == event.id
                    )
                    .count()
                )

                st.write(
                    "👥 Registrations:",
                    registration_count
                )

                # Capacity
                st.write(
                    "🪑 Maximum Capacity:",
                    event.capacity
                )

                # Available seats
                available_seats = (
                    event.capacity -
                    registration_count
                )

                st.write(
                    "✅ Available Seats:",
                    available_seats
                )

                # =================================================
                # EDIT EVENT
                # =================================================

                if st.button(
                    "✏️ Edit Event",
                    key=f"edit_{event.id}"
                ):

                    st.session_state[
                        f"editing_{event.id}"
                    ] = True

                if st.session_state.get(
                    f"editing_{event.id}",
                    False
                ):

                    st.write(
                        "### ✏️ Edit Event"
                    )

                    new_name = st.text_input(
                        "Event Name",
                        value=event.name,
                        key=f"name_{event.id}"
                    )

                    new_date = st.date_input(
                        "Event Date",
                        value=event.date,
                        key=f"date_{event.id}"
                    )

                    new_time = st.time_input(
                        "Event Time",
                        value=event.time,
                        key=f"time_{event.id}"
                    )

                    new_venue = st.text_input(
                        "Venue",
                        value=event.venue,
                        key=f"venue_{event.id}"
                    )

                    new_organizer = st.text_input(
                        "Organizer Name",
                        value=event.organizer,
                        key=f"organizer_{event.id}"
                    )

                    new_description = st.text_area(
                        "Event Description",
                        value=event.description,
                        key=f"description_{event.id}"
                    )

                    new_capacity = st.number_input(
                        "Maximum Capacity",
                        min_value=1,
                        value=event.capacity,
                        step=1,
                        key=f"capacity_{event.id}"
                    )

                    if st.button(
                        "💾 Save Changes",
                        key=f"save_{event.id}"
                    ):

                        event.name = new_name.strip()
                        event.date = new_date
                        event.time = new_time
                        event.venue = new_venue.strip()
                        event.organizer = new_organizer.strip()
                        event.description = new_description.strip()
                        event.capacity = new_capacity

                        db.commit()

                        st.success(
                            "✅ Event updated successfully!"
                        )

                        st.session_state[
                            f"editing_{event.id}"
                        ] = False

                        st.rerun()

                # =================================================
                # DELETE EVENT
                # =================================================

                if st.button(
                    "🗑️ Delete Event",
                    key=f"delete_{event.id}"
                ):

                    # Delete registrations first
                    db.query(Registration).filter(
                        Registration.event_id == event.id
                    ).delete(
                        synchronize_session=False
                    )

                    # Delete event
                    db.delete(event)

                    db.commit()

                    st.success(
                        "✅ Event and its registrations deleted successfully!"
                    )

                    st.rerun()

                st.divider()

    db.close()


# =========================================================
# REGISTER FOR EVENT
# =========================================================

elif choice == "Register for Event":

    st.header("📝 Register for Event")

    db = SessionLocal()

    events = db.query(Event).order_by(
        Event.date,
        Event.time
    ).all()

    if len(events) == 0:

        st.info(
            "No events are available for registration."
        )

    else:

        event_options = {
            f"{event.name} — "
            f"{event.date} {event.time}": event
            for event in events
        }

        selected_event_label = st.selectbox(
            "Select Event",
            list(event_options.keys())
        )

        selected_event = event_options[
            selected_event_label
        ]

        student_name = st.text_input(
            "Student Name"
        )

        student_id = st.text_input(
            "Student ID"
        )

        if st.button("Register"):

            if (
                student_name.strip()
                and student_id.strip()
            ):

                registration_count = (
                    db.query(Registration)
                    .filter(
                        Registration.event_id ==
                        selected_event.id
                    )
                    .count()
                )

                # Check capacity
                if (
                    registration_count
                    >= selected_event.capacity
                ):

                    st.error(
                        "❌ This event is full. "
                        "No more registrations are allowed."
                    )

                else:

                    # Check duplicate registration
                    existing_registration = (
                        db.query(Registration)
                        .filter(
                            Registration.student_id ==
                            student_id.strip(),
                            Registration.event_id ==
                            selected_event.id
                        )
                        .first()
                    )

                    if existing_registration:

                        st.warning(
                            "⚠️ You are already registered "
                            "for this event."
                        )

                    else:

                        registration = Registration(
                            student_name=
                            student_name.strip(),

                            student_id=
                            student_id.strip(),

                            event_id=
                            selected_event.id
                        )

                        db.add(registration)
                        db.commit()

                        st.success(
                            f"✅ {student_name} "
                            "registered successfully!"
                        )

                        st.rerun()

            else:

                st.error(
                    "Please enter Student Name and Student ID."
                )

    db.close()


# =========================================================
# MY REGISTRATIONS
# =========================================================

elif choice == "My Registrations":

    st.header("👤 My Registrations")

    db = SessionLocal()

    registrations = (
        db.query(Registration, Event)
        .join(
            Event,
            Registration.event_id == Event.id
        )
        .order_by(
            Registration.id.desc()
        )
        .all()
    )

    if len(registrations) == 0:

        st.info(
            "No registrations yet."
        )

    else:

        for registration, event in registrations:

            st.subheader(
                event.name
            )

            st.write(
                "👤 Student Name:",
                registration.student_name
            )

            st.write(
                "🆔 Student ID:",
                registration.student_id
            )

            st.write(
                "📅 Event Date:",
                event.date
            )

            st.write(
                "⏰ Event Time:",
                event.time
            )

            st.write(
                "📍 Venue:",
                event.venue
            )

            st.divider()

    db.close()