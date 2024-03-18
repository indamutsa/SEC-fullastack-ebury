import re

class Sanitizer:
    def __init__(self, input_string):
        # Initial sanitization to remove some SQL and XSS injection risks
        sanitized = re.sub(r"[;']", "", input_string)  # Remove semicolons and single quotes
        sanitized = re.sub(r"<script.*?>.*?</script>", "", sanitized, flags=re.DOTALL | re.IGNORECASE)  # Remove script tags
        self.sanitized = sanitized

    def get_valid_name(self):
        """Validate names."""
        if re.match(r"^[A-Za-z\s\-']+$", self.sanitized):
            return self.sanitized
        else:
            return None

    def get_valid_username(self):
        """Validate usernames."""
        if re.match(r"^[A-Za-z0-9_\-]+$", self.sanitized):
            return self.sanitized
        else:
            return None

    def get_valid_email(self):
        """Validate emails."""
        if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", self.sanitized):
            return self.sanitized
        else:
            return None

    def get_valid_phone(self):
        """Validate phone numbers."""
        if re.match(r"^\+?[0-9\s\-]+$", self.sanitized):
            return self.sanitized
        else:
            return None

    def get_valid_location(self):
        """Validate city and country names."""
        if re.match(r"^[A-Za-z\s\-']+$", self.sanitized):
            return self.sanitized
        else:
            return None
