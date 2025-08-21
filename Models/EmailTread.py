from Models.Email import Email


class EmailThread:
    """
    Represents an email thread, containing a hierarchical structure of Email objects.
    It is designed to be source-agnostic, tracking its origin via a 'source' attribute.
    """

    def __init__(self, raw_thread_messages: list, dao_instance: object,
                 source: str = "unknown"):  # dao_instance type changed to 'object' for generality
        """
        Initializes a Thread object from a list of raw API message dictionaries.

        Args:
            raw_thread_messages (list): A list of raw message dictionaries from an API thread.
            dao_instance (object): An instance of the relevant Data Access Object (e.g., GmailDAO).
            source (str): A string indicating the origin of this thread (e.g., "gmail", "icloud").
        """
        self._dao = dao_instance
        self.source = source  # NEW: Store the source of this thread
        self.thread_id = None
        if raw_thread_messages:
            self.thread_id = raw_thread_messages[0].get('threadId')  # Use .get() for robustness

        self.messages = self._build_hierarchy(raw_thread_messages)

    def _build_hierarchy(self, raw_messages: list) -> list[Email]:
        """
        Builds a hierarchical structure of Email objects within this thread
        based on In-Reply-To and References headers.
        """
        if not raw_messages:
            return []

        # Instantiate Email objects, passing the source to each
        email_objects = [Email(raw_msg, self._dao, self.source) for raw_msg in raw_messages]
        
        # Correctly create a map with stripped Message-IDs for reliable lookups
        message_map = {}
        for email in email_objects:
            msg_id = email.headers.get('Message-ID')
            if msg_id:
                message_map[msg_id.strip('<>')] = email

        root_messages = []

        for email_obj in email_objects:
            in_reply_to_id = email_obj.headers.get('In-Reply-To')
            if in_reply_to_id:
                in_reply_to_id = in_reply_to_id.strip('<>')

            parent_email = None
            if in_reply_to_id and in_reply_to_id in message_map:
                parent_email = message_map[in_reply_to_id]

            if parent_email:
                parent_email.replies.append(email_obj)
            else:
                root_messages.append(email_obj)

        for email_obj in email_objects:  # Sort replies for consistent ordering
            if email_obj.replies:
                email_obj.replies.sort(key=lambda x: int(x.internal_date or 0))

        # Sort root messages chronologically (oldest first)
        root_messages.sort(key=lambda x: int(x.internal_date or 0))

        return root_messages

    def get_flattened_thread(self) -> list[Email]:
        """
        Returns a flat list of all emails in the thread, with an added 'indent_level' 
        attribute to indicate the reply depth.
        """
        flattened_list = []

        def _flatten(messages, level):
            for msg in messages:
                msg.indent_level = level  # Set the indent level
                flattened_list.append(msg)
                if msg.replies:
                    _flatten(msg.replies, level + 1)

        _flatten(self.messages, 0)  # Start with the root messages at level 0
        return flattened_list

    def display(self, indent=0, emails_list=None):
        """
        Recursively prints the email hierarchy of the thread.
        """
        if emails_list is None:
            emails_list = self.messages  # Start with top-level messages
            print(f"\n--- Displaying Thread ID: {self.thread_id} (Source: {self.source}) ---")

        for email in emails_list:
            print("  " * indent + f"[{email.id}] Subject: {email.headers.get('Subject', 'N/A')}")
            print("  " * indent + f"  From: {email.headers.get('From', 'N/A')}")
            print("  " * indent + f"  To: {email.headers.get('To', 'N/A')}")
            print("  " * indent + f"  Date: {email.headers.get('Date', 'N/A')}")
            if email.headers.get('Message-ID'):
                print("  " * indent + f"  Message-ID: {email.headers['Message-ID']}")
            if email.headers.get('In-Reply-To'):
                print("  " * indent + f"  In-Reply-To: {email.headers['In-Reply-To']}")
            print("  " * indent + f"  Source: {email.source}")  # Display email source

            if email.body_plain_text:
                snippet = email.body_plain_text[:100].replace('\n', ' ') + '...' if len(
                    email.body_plain_text) > 100 else email.body_plain_text
                print("  " * indent + f"  Body Snippet: {snippet}")
            if email.replies:
                print("  " * indent + "  Replies:")
                self.display(indent + 1, email.replies)  # Recursive call

    def find_emails_by_string(self, search_term: str, case_sensitive: bool = False) -> list[Email]:
        """
        Recursively searches for a string in email bodies within the thread's hierarchy
        and returns a list of matching Email objects.
        """
        matching_emails = []

        def _recursive_search(emails_list):
            for email_obj in emails_list:
                if email_obj.search_string(search_term, case_sensitive):
                    matching_emails.append(email_obj)
                if email_obj.replies:
                    _recursive_search(email_obj.replies)

        _recursive_search(self.messages)
        return matching_emails
