from twitter_ads.client import Client
from twitter_ads.http import Request


class TargetingSuggestions():
    TARGETING_SUGGEST = '/1/accounts/{}/targeting_suggestions'

    def update_params(self):
        params=self._params
        params.update(self._params)
        return params


    def request(self):
        response = Request(self._account, 'get', self.TARGETING_SUGGEST.format(self._account_id),
                       params= self.update_params()).perform()
        return response.bodyp['data']
