class CapiClientError(Exception):
    """Eccezione personalizzata per errori del client CAPI."""
    pass

class CapiClinetAuthError(CapiClientError):
    """This means that the user is not authenticated or the token is invalid"""
    pass

class CapiClinetRequestError(CapiClientError):
    """This means that the request to the CAPI endpoint failed"""
    pass

class JournalNoContentError(CapiClinetRequestError):
    """This means that the player has not (yet) played this day"""
    pass

class JournalPartialContentError(CapiClinetRequestError):
    """The request did not get the entire journal, best solution is to keep trying until you get 200 - OK"""
    pass

class FleetCarrierNotOwnedError(CapiClinetRequestError):
    """Eccezione sollevata quando l'utente non possiede una Fleet Carrier."""
    pass