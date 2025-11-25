from allauth.account.adapter import DefaultAccountAdapter

class NoPhoneAccountAdapter(DefaultAccountAdapter):
    def _has_phone_field(self, form):
        # Always disable phone number logic
        return False
