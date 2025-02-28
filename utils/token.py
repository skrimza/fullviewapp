from utils.base_form import BaseValidation


class TokenData(BaseValidation):
    access_token: str
    token_type: str = 'Bearer'
    
