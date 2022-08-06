from marshmallow import post_dump, post_load, ValidationError, pre_load

from api.models.Schemas.MonitorSchema import monitor_summary
from api.models.Schemas.PaginationSchema import PaginationSchema


class MonitoringSchema(PaginationSchema):
    @post_load()
    def process_input_data(self, data, **kwargs):
        self.validate_sort_parameters(data, monitor_summary)
        return data

    @post_dump()
    def process_dump(self, data, **kwargs):
        data['items'] = monitor_summary.dump(data.get('items', []), many=True)
        return data


monitoring_summary = MonitoringSchema()
