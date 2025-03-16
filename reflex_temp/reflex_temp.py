"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from typing import List, Dict, Any

from rxconfig import config


class User(rx.Base):
    """User model."""
    id: int
    name: str
    email: str
    role: str


class State(rx.State):
    """The app state."""
    
    # Form fields
    name: str = ""
    email: str = ""
    message: str = ""
    
    # Submission status
    submitted: bool = False
    
    # Users data
    users: List[User] = []
    
    def handle_submit(self):
        """Handle the form submission."""
        # In a real app, you might save to a database or send an email here
        self.submitted = True
        
    def reset_form(self):
        """Reset the form after submission."""
        self.name = ""
        self.email = ""
        self.message = ""
        self.submitted = False
    
    @rx.var
    def get_dummy_users(self) -> List[Dict[str, Any]]:
        """Get dummy users data."""
        return [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "role": "Admin"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "role": "User"}
        ]


def index() -> rx.Component:
    # Welcome Page with Form
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Simple Form Example", size="8"),
            rx.text("Please fill out the form below", size="4"),
            
            # Show form if not submitted, otherwise show success message
            rx.cond(
                State.submitted,
                # Success message after submission
                rx.vstack(
                    rx.text("Thank you for your submission!", size="6", color="green"),
                    rx.text(f"We received your message, {State.name}!"),
                    rx.button("Submit another response", on_click=State.reset_form),
                    spacing="4",
                ),
                # Form
                rx.vstack(
                    rx.form(
                        rx.vstack(
                            rx.vstack(
                                rx.text("Name"),
                                rx.input(
                                    placeholder="Enter your name",
                                    value=State.name,
                                    on_change=State.set_name,
                                    required=True,
                                ),
                            ),
                            rx.vstack(
                                rx.text("Email"),
                                rx.input(
                                    type_="email",
                                    placeholder="Enter your email",
                                    value=State.email,
                                    on_change=State.set_email,
                                    required=True,
                                ),
                            ),
                            rx.vstack(
                                rx.text("Message"),
                                rx.text_area(
                                    placeholder="Enter your message",
                                    value=State.message,
                                    on_change=State.set_message,
                                    required=True,
                                ),
                            ),
                            rx.button("Submit", type_="submit"),
                            spacing="4",
                            width="100%",
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
        rx.logo(),
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
app.api.add_api_route("/users", users_api, methods=["GET"])
