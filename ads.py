import json
import requests

FB = 'https://graph.facebook.com'


"""Python client library for the Facebook ads API."""


class AdsAPI(object):
    """A client for the Facebook Ads API."""

    def __init__(self, ad_account_id, access_token=None, expires=None):
        self.ad_account_id = ad_account_id
        self.access_token = access_token
        self.expires = expires
        self.payload = {'access_token': access_token}

    def get_ad_account_info(self, fields):
        url = '%s/%s' % (FB, self.ad_account_id)
        r = requests.get(url, params=self.payload)
        return r.json()

    def get_ad_account_users(self):
        url = '%s/%s/users' % (FB, self.ad_account_id)
        r = requests.get(url, params=self.payload)
        return r.json()

    def get_broad_targeting_categories(self):
        url = '%s/%s/broadtargetingcategories' % (FB, self.ad_account_id)
        r = requests.get(url, params=self.payload)
        return r.json()

    def get_connection_objects(self):
        url = '%s/%s/connectionobjects' % (FB, self.ad_account_id)
        r = requests.get(url, params=self.payload)
        return r.json()

    def get_ad_stats(self):
        url = '%s/%s/stats' % (FB, self.ad_account_id)
        r = requests.get(url, params=self.payload)
        return r.json()

    def get_ad_campaign_stats(self, campaign_ids=None):
        """Return campaign stats for the given list of campaign ids."""

        payload = {'campaign_ids': json.dumps(campaign_ids)}
        payload.update(self.payload)
        url = '%s/%s/adcampaignstats' % (FB, self.ad_account_id)
        r = requests.get(url, params=payload)
        return r.json()

    def get_ad_group_stats(self, adgroup_ids=None, stats_mode=None):
        payload = {'adgroup_ids': json.dumps(adgroup_ids),
                   'stats_mode': stats_mode}
        payload.update(self.payload)
        url = '%s/%s/adgroupstats' % (FB, self.ad_account_id)
        r = requests.get(url, params=payload)
        return r.json()

    def get_keyword_stats(self, adgroup_id):
        url = '%s/%s/keywordstats' % (FB, adgroup_id)
        r = requests.get(url, params=self.payload)
        return r.json()

    def get_reach_estimate(self, currency, targeting_spec):
        payload = {'currency': currency,
                   'targeting_spec': json.dumps(targeting_spec)}
        payload.update(self.payload)
        url = '%s/%s/reachestimate' % (FB, self.ad_account_id)
        r = requests.get(url, params=payload)
        return r.json()

    def get_targeting_description(self, adgroup_id):
        url = '%s/%s/targetingsentencelines' % (FB, adgroup_id)
        r = requests.get(url, params=self.payload)
        return r.json()

    def search(self, query, type, want_localized_name):
        payload = {'q': query, 'type': type,
                   'want_localized_name': want_localized_name}
        payload.update(self.payload)
        url = '%s/search' % FB
        r = requests.get(url, params=payload)
        return r.json()

    def create_ad_creative(self):
        url = '%s/%s/adcreatives' % (FB, self.ad_account_id)
        r = requests.post(url, params=self.payload)
        return r.json()
