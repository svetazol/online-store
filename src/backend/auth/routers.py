from backend.auth.views import LoginView, LogoutView, SignupView

ROUTES = [
    ("POST", '/signup', SignupView),
    ("POST", '/login', LoginView),
    ("GET", '/logout', LogoutView)
]
