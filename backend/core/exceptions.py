#for custom rules
'''
so make sure the exception raised in service layer are not http tied
they should be only exception from python, and we handle with translating to http response in handler.py OR wherever
'''
class ResourceNotFoundError(Exception):
    def __init__(self, resource: str, identifier):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} not found: {identifier}")
        # raise NotFoundError("Account", account_id)

class ResourceExistedError(Exception):
    def __init__(self, resource: str, identifier):
        self.resource = resource
        self.identifier = identifier
        super().__init__(f"{resource} already existed: {identifier}")

class AuthFailedCredential(Exception): #
    def __init__(self):
        super().__init__("Invalid Credential")
