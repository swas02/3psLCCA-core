from ..road_user_cost.carriage_width_info.carriagewayStandards import CarriagewayStandards
from .. import standard_keys as c


def a():
    print(CarriagewayStandards.list_types_with_names())


available_lanes = [{'code': 'SL', 'description': 'Single Lane'}, {'code': 'IL', 'description': 'Intermediate Lane'}, {'code': '2L', 'description': 'Two Lane'}, {
    'code': '4L', 'description': 'Four Lane'}, {'code': '6L', 'description': 'Six Lane'}, {'code': '8L', 'description': 'Eight Lane'}, {'code': 'EW', 'description': 'Expressway'}]

capacity_lane_wise = {'data': [{'carriageway': c.L2,
                                'lanes_total': 2,
                                'lanewise': {'one_way': {'lanes_per_direction': 2,
                                                         'name': 'One-Way Carriageway',
                                                         'urban_arterial': 1200,
                                                         'urban_collector': 700,
                                                         'urban_sub_arterial': 950},
                                             'two_way': {'lanes_per_direction': 1,
                                                         'name': 'Two-Way Undivided '
                                                         'Carriageway',
                                                         'urban_arterial': 750,
                                                         'urban_collector': 450,
                                                         'urban_sub_arterial': 600}}},
                               {'carriageway': c.L6,
                                'lanes_total': 3,
                                'lanewise': {'one_way': {'lanes_per_direction': 3,
                                                         'name': 'One-Way Carriageway',
                                                         'urban_arterial': 1200,
                                                         'urban_collector': 733,
                                                         'urban_sub_arterial': 967}}},
                               {'carriageway': c.L4,
                                'lanes_total': 4,
                                'lanewise': {'two_way_divided': {'lanes_per_direction': 2,
                                                                 'name': 'Two-Way Divided '
                                                                 'Carriageway',
                                                                 'urban_arterial': 900,
                                                                 'urban_sub_arterial': 725},
                                             'two_way_undivided': {'lanes_per_direction': 2,
                                                                   'name': 'Two-Way Undivided '
                                                                   'Carriageway',
                                                                   'urban_arterial': 750,
                                                                   'urban_collector': 450,
                                                                   'urban_sub_arterial': 600}}},
                               {'carriageway': '6-Lane',
                                'lanes_total': 6,
                                'lanewise': {'two_way_divided': {'lanes_per_direction': 3,
                                                                 'name': 'Two-Way Divided '
                                                                 'Carriageway',
                                                                 'urban_arterial': 900,
                                                                 'urban_sub_arterial': 717},
                                             'two_way_undivided': {'lanes_per_direction': 3,
                                                                   'name': 'Two-Way Undivided '
                                                                   'Carriageway',
                                                                   'urban_arterial': 800,
                                                                   'urban_sub_arterial': 633}}},
                               {'carriageway': '8-Lane',
                                'lanes_total': 8,
                                'lanewise': {'two_way_divided': {'lanes_per_direction': 4,
                                                                 'name': 'Two-Way Divided '
                                                                 'Carriageway',
                                                                 'urban_arterial': 900}}}],
                      'design_LOS': 'C',
                      'source_table': 'Table 2',
                      'standard': 'IRC 106:1990',
                      'unit': 'PCU_per_hour_per_lane'}
