from tap_campaign_monitor.streams.base import ChildStream


class CampaignEmailClientUsageStream(ChildStream):
    KEY_PROPERTIES = ['CampaignID', 'Client', 'Version']
    TABLE = 'campaign_email_client_usage'
    REQUIRES = ['campaigns']

    def get_parent_id(self, parent):
        return parent.get('CampaignID')

    def incorporate_parent_id(self, obj, parent):
        obj['CampaignID'] = self.get_parent_id(parent)
        return obj

    def get_api_path_for_child(self, parent):
        return (
            '/campaigns/{}/emailclientusage.json'
            .format(self.get_parent_id(parent)))

    def get_stream_data(self, result):
        return [self.transform_record(item)
                for item in result]
