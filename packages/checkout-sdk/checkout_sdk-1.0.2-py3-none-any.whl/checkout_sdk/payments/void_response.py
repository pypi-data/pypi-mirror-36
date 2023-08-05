from checkout_sdk.payments import PaymentResponse


class VoidResponse(PaymentResponse):
    def __init__(self, api_response):
        super().__init__(api_response)

    @property
    def original_id(self):
        return self._response.body['originalId']
