from marshmallow import post_dump

from api.models.Schemas.MonitorSchema import monitor_summary
from api.models.Schemas.PaginationSchema import PaginationSchema


class MonitoringSchema(PaginationSchema):
    @post_dump()
    def process_dump(self, data, **kwargs):
        data['items'] = monitor_summary.dump(data.get('items', []), many=True)
        return data


monitoring_summary = MonitoringSchema()
