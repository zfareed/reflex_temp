import reflex as rx
from typing import List, Dict, Any

class State(rx.State):
    """The app state."""
    name: str = ""
    email: str = ""
    message: str = ""
    submitted: bool = False

    def handle_submit(self):
        """Handle the form submission."""
        self.submitted = True

    def reset_form(self):
        """Reset the form after submission."""
        self.name = ""
        self.email = ""
        self.message = ""
        self.submitted = False

def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.heading("UserForm", size="8"),
            rx.cond(
                State.submitted,
                rx.vstack(
                    rx.text("Thank you for your submission!", size="6", color="green"),
                    rx.text(f"We received your message, {State.name}!"),
                    rx.button("Submit another response", on_click=State.reset_form),
                    spacing="4",
                ),
                rx.vstack(
                    rx.form(
                        rx.vstack(
                            rx.input(placeholder="Name", value=State.name, on_change=State.set_name, required=True),
                            rx.input(placeholder="Email", value=State.email, on_change=State.set_email, required=True),
                            rx.text_area(placeholder="Message", value=State.message, on_change=State.set_message, required=True),
                            rx.button("Submit", type_="submit"),
                            spacing="4",
                        ),
                        on_submit=State.handle_submit,
                    ),
                    width="100%",
                    max_width="500px",
                ),
            ),
            spacing="5",
            justify="center",
            align_items="center",
            min_height="85vh",
            padding="5",
        ),
    )

def users_api() -> List[Dict[str, Any]]:
    """API endpoint that returns dummy users data."""
    return [
        {"id": 1, "name": "John Doe", "email": "john@example.com", "role": "Admin"},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "role": "User"}
    ]

# Create the app and add pages
app = rx.App()
app.add_page(index)

# Add API route
app.api.add_api_route("/api/users", users_api, methods=["GET"])