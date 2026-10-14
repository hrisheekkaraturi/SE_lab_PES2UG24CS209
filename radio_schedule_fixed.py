"""Manage a simple radio-show schedule using SQLite."""

import sqlite3


def add_slot(connection, show, host, start_hour, minutes):
    """Add a radio show to the schedule."""
    if not show.strip() or not host.strip():
        raise ValueError("Show and host names must not be empty.")
    if not 0 <= start_hour <= 23:
        raise ValueError("Start hour must be between 0 and 23.")
    if minutes <= 0:
        raise ValueError("Duration must be a positive number of minutes.")

    connection.execute(
        """
        INSERT INTO slots (show, host, start_hour, minutes)
        VALUES (?, ?, ?, ?)
        """,
        (show, host, start_hour, minutes),
    )


def slot_label(show, host):
    """Return a readable label for a radio show."""
    return f"{show} hosted by {host}"


def overlap_free(start_hour, minutes, next_start_hour):
    """Return True if a show ends before or when the next one starts."""
    if minutes < 0 or not 0 <= start_hour <= 23:
        raise ValueError("Invalid start hour or duration.")
    return start_hour + minutes / 60 <= next_start_hour


def morning_shows(connection):
    """Return the names of shows scheduled before noon."""
    rows = connection.execute(
        "SELECT show FROM slots WHERE start_hour < ? ORDER BY start_hour",
        (12,),
    )
    return [row[0] for row in rows]


def remove_slot(connection, slot_id):
    """Remove a scheduled show by its ID."""
    connection.execute("DELETE FROM slots WHERE id = ?", (slot_id,))


def main():
    """Create a sample schedule and demonstrate the functions."""
    with sqlite3.connect(":memory:") as connection:
        connection.execute(
            """
            CREATE TABLE slots (
                id INTEGER PRIMARY KEY,
                show TEXT NOT NULL,
                host TEXT NOT NULL,
                start_hour INTEGER NOT NULL,
                minutes INTEGER NOT NULL
            )
            """
        )

        add_slot(connection, "Sunrise Beats", "Vik", 7, 60)
        add_slot(connection, "Midday Talk", "Anu", 13, 45)

        print(slot_label("Sunrise Beats", "Vik"))
        print(overlap_free(7, 60, 13), morning_shows(connection))
        remove_slot(connection, 2)


if __name__ == "__main__":
    main()
