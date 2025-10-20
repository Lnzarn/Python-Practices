from PyQt6.QtWidgets import (QApplication, QMainWindow, QHeaderView,
                             QTableWidgetItem, QDialog, QVBoxLayout,
                             QLabel, QTimeEdit, QDialogButtonBox, QMessageBox)
from PyQt6.QtCore import QDate, Qt, QTime
from PyQt6.QtGui import QColor
from calcu import Ui_MainWindow
import sys
from datetime import datetime, timedelta
import calendar
import json
import os


class EventDialog(QDialog):
    """Dialog for adding events with time range"""

    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Add Event - {date.toString('MMM d, yyyy')}")
        self.selected_date = date

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Start Time:"))
        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setTime(QTime(9, 0))
        self.start_time_edit.setDisplayFormat("hh:mm AP")
        layout.addWidget(self.start_time_edit)

        layout.addWidget(QLabel("End Time:"))
        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setTime(QTime(17, 0))
        self.end_time_edit.setDisplayFormat("hh:mm AP")
        layout.addWidget(self.end_time_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok |
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_event_data(self):
        return {
            'date': self.selected_date,
            'start_time': self.start_time_edit.time(),
            'end_time': self.end_time_edit.time()
        }


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("TimeZone Calendar")

        # Calendar state
        self.current_date = QDate.currentDate()

        # Timezone names
        self.timezones = ['PHT', 'EDT']
        self.current_tz_index = 0  # Start with PHT

        # Events storage: {QDate: [{'start_time': QTime, 'end_time': QTime, 'timezone': str}, ...]}
        self.events = {}

        # Database file path
        self.db_file = "calendar_events.json"

        # Load existing events
        self.load_events()

        # Setup table
        self.setup_table()
        self.update_calendar()

        # Connect buttons
        self.pushButton.clicked.connect(self.prev_month)
        self.pushButton_2.clicked.connect(self.next_month)

        # Make timezone label clickable with hover effects
        self.label_2.mousePressEvent = self.change_timezone
        self.label_2.setCursor(Qt.CursorShape.PointingHandCursor)
        self.label_2.setProperty("hovered", False)
        self.label_2.enterEvent = lambda e: self.on_tz_label_hover(True)
        self.label_2.leaveEvent = lambda e: self.on_tz_label_hover(False)
        self.update_timezone_colors()

        # Connect table cell clicks
        self.tableWidget.cellClicked.connect(self.cell_clicked)

        # Add button for adding events to selected cells
        from PyQt6.QtWidgets import QPushButton
        from PyQt6.QtGui import QShortcut, QKeySequence

        # Create a floating button or use keyboard shortcut
        self.add_shortcut = QShortcut(QKeySequence("Return"), self)
        self.add_shortcut.activated.connect(self.handle_selection)

    def setup_table(self):
        """Initialize the table as a calendar grid"""
        self.tableWidget.setRowCount(
            6)  # Max 6 weeks in a month (will adjust dynamically)
        self.tableWidget.setColumnCount(7)  # 7 days in a week

        # Set headers - Sunday first
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        self.tableWidget.setHorizontalHeaderLabels(days)

        # Style the table
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.tableWidget.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch)
        self.tableWidget.verticalHeader().setVisible(False)

        # Make cells non-editable but allow multi-selection
        self.tableWidget.setEditTriggers(
            self.tableWidget.EditTrigger.NoEditTriggers)
        self.tableWidget.setSelectionMode(
            self.tableWidget.SelectionMode.MultiSelection)

        # Show grid lines
        self.tableWidget.setShowGrid(True)

        # Enable mouse tracking for hover effects
        self.tableWidget.setMouseTracking(True)
        self.tableWidget.viewport().setMouseTracking(True)
        self.tableWidget.cellEntered.connect(self.on_cell_hover)

        # Will be updated by update_timezone_colors()
        self.update_table_style()

    def update_table_style(self):
        """Update table stylesheet based on current timezone"""
        current_tz = self.get_current_timezone()

        if current_tz == 'PHT':
            header_color = '#5170ff'  # Blue
        else:  # EDT
            header_color = '#ff69b4'  # Pink

        self.tableWidget.setStyleSheet(f"""
            QHeaderView::section {{
                background-color: {header_color};
                color: white;
                font-weight: bold;
                padding: 4px;
            }}
            QTableWidget {{
                gridline-color: #808080;
            }}
        """)

    def get_current_timezone(self):
        """Get the currently selected timezone"""
        return self.timezones[self.current_tz_index]

    def update_timezone_colors(self):
        """Update colors based on current timezone"""
        current_tz = self.get_current_timezone()

        if current_tz == 'PHT':
            header_bg = '#5170ff'  # Blue
            button_bg = '#5170ff'
        else:  # EDT
            header_bg = '#ff69b4'  # Pink
            button_bg = '#ff69b4'

        # Update header widget (contains timezone, month, year)
        self.horizontalWidget.setStyleSheet(f"""
            background-color: {header_bg};
            border-radius: 25px;
        """)

        # Update month navigation buttons
        self.pushButton.setStyleSheet(f"""
            background-color: {button_bg};
            color: white;
            font-weight: bold;
            border: none;
            font-size: 16px;
        """)
        self.pushButton_2.setStyleSheet(f"""
            background-color: {button_bg};
            color: white;
            font-weight: bold;
            border: none;
            font-size: 16px;
        """)

        # Update timezone label styling
        base_style = """
            color: white;
            font-weight: bold;
        """
        self.label_2.setStyleSheet(base_style)

        # Update table header colors
        self.update_table_style()

    def on_tz_label_hover(self, is_hovering):
        """Handle hover effect on timezone label"""
        if is_hovering:
            # Scale up slightly and change cursor
            font = self.label_2.font()
            font.setPointSize(16)  # Slightly larger
            self.label_2.setFont(font)
        else:
            # Return to normal size
            font = self.label_2.font()
            font.setPointSize(14)
            self.label_2.setFont(font)

    def on_cell_hover(self, row, col):
        """Handle hover effect on table cells"""
        # Darken the hovered cell
        item = self.tableWidget.item(row, col)
        if item and item.data(Qt.ItemDataRole.UserRole):
            # Store original color if not already stored
            if not item.data(Qt.ItemDataRole.UserRole + 1):
                original_color = item.background().color()
                item.setData(Qt.ItemDataRole.UserRole + 1, original_color)

            # Darken the color
            original = item.data(Qt.ItemDataRole.UserRole + 1)
            darker = original.darker(110)
            item.setBackground(darker)

        # Reset all other cells to their original color
        for r in range(self.tableWidget.rowCount()):
            for c in range(self.tableWidget.columnCount()):
                if r != row or c != col:
                    cell_item = self.tableWidget.item(r, c)
                    if cell_item:
                        original_color = cell_item.data(
                            Qt.ItemDataRole.UserRole + 1)
                        if original_color:
                            cell_item.setBackground(original_color)

    def load_events(self):
        """Load events from JSON file"""
        if not os.path.exists(self.db_file):
            return

        try:
            with open(self.db_file, 'r') as f:
                data = json.load(f)

            # Convert JSON data back to QDate and QTime objects
            for date_str, event_list in data.items():
                date = QDate.fromString(date_str, "yyyy-MM-dd")
                self.events[date] = []

                for event in event_list:
                    start_time = QTime.fromString(
                        event['start_time'], "hh:mm:ss")
                    end_time = QTime.fromString(event['end_time'], "hh:mm:ss")

                    self.events[date].append({
                        'start_time': start_time,
                        'end_time': end_time,
                        'timezone': event['timezone']
                    })

            print(
                f"Loaded {len(self.events)} date(s) with events from database")
        except Exception as e:
            print(f"Error loading events: {e}")
            QMessageBox.warning(self, "Load Error",
                                f"Could not load saved events: {e}")

    def save_events(self):
        """Save events to JSON file"""
        try:
            # Convert QDate and QTime objects to strings for JSON
            data = {}
            for date, event_list in self.events.items():
                date_str = date.toString("yyyy-MM-dd")
                data[date_str] = []

                for event in event_list:
                    data[date_str].append({
                        'start_time': event['start_time'].toString("hh:mm:ss"),
                        'end_time': event['end_time'].toString("hh:mm:ss"),
                        'timezone': event['timezone']
                    })

            with open(self.db_file, 'w') as f:
                json.dump(data, f, indent=2)

            print(f"Saved {len(self.events)} date(s) with events to database")
        except Exception as e:
            print(f"Error saving events: {e}")
            QMessageBox.warning(self, "Save Error",
                                f"Could not save events: {e}")

    def update_calendar(self):
        """Populate the calendar with dates"""
        year = self.current_date.year()
        month = self.current_date.month()

        # Update header labels
        self.label_3.setText(self.current_date.toString('MMMM'))
        self.label.setText(str(year))
        self.label_2.setText(self.get_current_timezone())

        # Get calendar data with Sunday as first day (firstweekday=6)
        calendar.setfirstweekday(6)  # 6 = Sunday
        cal = calendar.monthcalendar(year, month)

        # Set row count based on actual weeks needed
        self.tableWidget.setRowCount(len(cal))

        # Clear table
        self.tableWidget.clearContents()

        # Fill calendar
        for row_idx, week in enumerate(cal):
            for col_idx, day in enumerate(week):
                if day == 0:
                    # Empty cell for days outside current month
                    item = QTableWidgetItem("")
                    item.setFlags(Qt.ItemFlag.NoItemFlags)
                    item.setBackground(QColor("#D3D3D3"))
                    item.setForeground(QColor("#000000"))
                else:
                    date = QDate(year, month, day)

                    # Get events that should appear on this date
                    display_events = self.get_events_for_date(date)

                    # Create cell text with events
                    cell_text = str(day)
                    for event in display_events[:3]:  # Show max 3 events
                        time_str = f"{event['start'].toString('h:mm AP')}-{event['end'].toString('h:mm AP')}"
                        cell_text += f"\n{time_str}"
                    if len(display_events) > 3:
                        cell_text += f"\n+{len(display_events) - 3} more"

                    item = QTableWidgetItem(cell_text)
                    item.setData(Qt.ItemDataRole.UserRole, date)

                    # Default styling for all cells - IMPORTANT: Set background!
                    base_color = QColor("#E7E7E7")
                    item.setBackground(base_color)
                    item.setForeground(QColor("#000000"))

                    # Store original color for hover effects
                    item.setData(Qt.ItemDataRole.UserRole + 1, base_color)

                    # Highlight if has events
                    if display_events:
                        item.setForeground(QColor("#0066cc"))

                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

                self.tableWidget.setItem(row_idx, col_idx, item)

    def convert_time(self, time, from_tz, to_tz):
        """Convert time between timezones with simple 12-hour rule"""
        if from_tz == to_tz:
            return time, 0  # No conversion needed, no day shift

        # Simple rule: flip AM/PM and shift day
        hour = time.hour()
        minute = time.minute()

        # Convert to 12-hour format, flip AM/PM
        if hour == 0:
            new_hour = 12  # Midnight becomes noon
        elif hour == 12:
            new_hour = 0  # Noon becomes midnight
        elif hour < 12:
            new_hour = hour + 12  # AM becomes PM
        else:
            new_hour = hour - 12  # PM becomes AM

        # Determine day shift
        # PHT to EDT: if PM in PHT, it's AM same day in EDT; if AM in PHT, it's PM previous day
        # EDT to PHT: if PM in EDT, it's AM next day in PHT; if AM in EDT, it's PM same day
        day_shift = 0
        if from_tz == 'PHT' and to_tz == 'EDT':
            # PHT to EDT
            if hour < 12:  # AM in PHT
                day_shift = -1  # Previous day in EDT
        elif from_tz == 'EDT' and to_tz == 'PHT':
            # EDT to PHT
            if hour >= 12:  # PM in EDT
                day_shift = 1  # Next day in PHT

        return QTime(new_hour, minute), day_shift

    def get_events_for_date(self, date):
        """Get all events that should display on this date in current timezone"""
        current_tz = self.get_current_timezone()
        events_to_display = []

        # Check all stored events
        for stored_date, event_list in self.events.items():
            for event in event_list:
                # Convert the event to current timezone
                converted_start, start_day_shift = self.convert_time(
                    event['start_time'], event['timezone'], current_tz
                )
                converted_end, end_day_shift = self.convert_time(
                    event['end_time'], event['timezone'], current_tz
                )

                # Calculate what date this event appears on
                display_date = stored_date.addDays(start_day_shift)

                # If it matches the date we're looking at, add it
                if display_date == date:
                    events_to_display.append({
                        'start': converted_start,
                        'end': converted_end,
                        'original_date': stored_date,
                        'original_start': event['start_time'],
                        'original_end': event['end_time'],
                        'original_tz': event['timezone']
                    })

        return sorted(events_to_display, key=lambda x: x['start'].toString())

    def cell_clicked(self, row, col):
        """Handle clicking on a calendar cell - for single selection"""
        # Check if multiple cells are already selected
        selected_dates = self.get_selected_dates()

        if len(selected_dates) <= 1:
            # Only handle single date if one or none selected
            item = self.tableWidget.item(row, col)
            if not item or not item.data(Qt.ItemDataRole.UserRole):
                return

            date = item.data(Qt.ItemDataRole.UserRole)
            self.handle_single_date(date)

    def handle_selection(self):
        """Handle the current selection (triggered by Enter key or button)"""
        selected_dates = self.get_selected_dates()

        if len(selected_dates) == 0:
            return
        elif len(selected_dates) == 1:
            self.handle_single_date(selected_dates[0])
        else:
            # Multiple dates selected
            msg = QMessageBox()
            msg.setWindowTitle("Multiple Days Selected")
            msg.setText(f"You have {len(selected_dates)} days selected.")
            msg.setInformativeText("What would you like to do?")
            add_multi_btn = msg.addButton(
                "Add Event to All", QMessageBox.ButtonRole.ActionRole)
            cancel_btn = msg.addButton(
                "Cancel", QMessageBox.ButtonRole.RejectRole)

            msg.exec()

            if msg.clickedButton() == add_multi_btn:
                self.add_to_multiple_dates(selected_dates)

    def get_selected_dates(self):
        """Get all valid dates from selected cells"""
        dates = []
        for item in self.tableWidget.selectedItems():
            date = item.data(Qt.ItemDataRole.UserRole)
            if date and date not in dates:
                dates.append(date)
        return dates

    def handle_single_date(self, date):
        """Handle operations for a single date"""
        # Check if there are events on this date
        display_events = self.get_events_for_date(date)

        if display_events:
            # Ask user what they want to do
            msg = QMessageBox()
            msg.setWindowTitle("Event Options")
            msg.setText(f"This date has {len(display_events)} event(s).")
            msg.setInformativeText("What would you like to do?")
            add_btn = msg.addButton(
                "Add New Event", QMessageBox.ButtonRole.ActionRole)
            delete_btn = msg.addButton(
                "Delete Event", QMessageBox.ButtonRole.DestructiveRole)
            cancel_btn = msg.addButton(
                "Cancel", QMessageBox.ButtonRole.RejectRole)

            msg.exec()

            if msg.clickedButton() == add_btn:
                self.add_event(date)
            elif msg.clickedButton() == delete_btn:
                self.delete_event(date, display_events)
        else:
            # No events, just add new one
            self.add_event(date)

    def add_to_selected(self):
        """Add event to all selected dates (deprecated - kept for compatibility)"""
        self.handle_selection()

    def add_to_multiple_dates(self, dates):
        """Add the same event to multiple dates"""
        if not dates:
            return

        # Show dialog with first date as reference
        dialog = EventDialog(dates[0], self)
        dialog.setWindowTitle(f"Add Event to {len(dates)} Days")

        if dialog.exec() == QDialog.DialogCode.Accepted:
            event_data = dialog.get_event_data()
            current_tz = self.get_current_timezone()

            # Add the same event to all selected dates
            for date in dates:
                if date not in self.events:
                    self.events[date] = []

                self.events[date].append({
                    'start_time': event_data['start_time'],
                    'end_time': event_data['end_time'],
                    'timezone': current_tz
                })

            self.save_events()  # Save after adding to multiple dates
            self.update_calendar()

            # Show confirmation
            QMessageBox.information(
                self,
                "Success",
                f"Event added to {len(dates)} day(s)!"
            )

    def add_event(self, date):
        """Add a new event"""
        dialog = EventDialog(date, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            event_data = dialog.get_event_data()

            # Store event with current timezone
            if date not in self.events:
                self.events[date] = []

            self.events[date].append({
                'start_time': event_data['start_time'],
                'end_time': event_data['end_time'],
                'timezone': self.get_current_timezone()
            })

            self.save_events()  # Save after adding
            self.update_calendar()

    def delete_event(self, date, display_events):
        """Delete an event from a date"""
        if not display_events:
            return

        # Create a selection dialog
        msg = QMessageBox()
        msg.setWindowTitle("Delete Event")
        msg.setText("Select event to delete:")

        event_text = ""
        for i, event in enumerate(display_events):
            time_str = f"{event['start'].toString('h:mm AP')}-{event['end'].toString('h:mm AP')}"
            event_text += f"{i+1}. {time_str}\n"

        msg.setInformativeText(event_text)

        # Create buttons for each event
        buttons = []
        for i in range(len(display_events)):
            btn = msg.addButton(
                f"Delete #{i+1}", QMessageBox.ButtonRole.ActionRole)
            buttons.append(btn)
        cancel_btn = msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)

        msg.exec()

        # Find which button was clicked
        for i, btn in enumerate(buttons):
            if msg.clickedButton() == btn:
                event_to_delete = display_events[i]
                original_date = event_to_delete['original_date']

                # Remove from storage using original values
                if original_date in self.events:
                    self.events[original_date] = [
                        e for e in self.events[original_date]
                        if not (e['start_time'] == event_to_delete['original_start'] and
                                e['end_time'] == event_to_delete['original_end'] and
                                e['timezone'] == event_to_delete['original_tz'])
                    ]

                    # Clean up empty date entries
                    if not self.events[original_date]:
                        del self.events[original_date]

                self.save_events()  # Save after deleting
                self.update_calendar()
                break

    def change_timezone(self, event):
        """Switch between timezones"""
        # Make text slightly darker on click
        self.label_2.setStyleSheet("""
            color: #cccccc;
            font-weight: bold;
        """)

        # Switch timezone
        self.current_tz_index = (
            self.current_tz_index + 1) % len(self.timezones)

        # Update all colors
        self.update_timezone_colors()
        self.update_calendar()

        # Reset text color after a brief moment
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, lambda: self.update_timezone_colors())

    def prev_month(self):
        """Navigate to previous month"""
        self.current_date = self.current_date.addMonths(-1)
        self.update_calendar()

    def next_month(self):
        """Navigate to next month"""
        self.current_date = self.current_date.addMonths(1)
        self.update_calendar()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
