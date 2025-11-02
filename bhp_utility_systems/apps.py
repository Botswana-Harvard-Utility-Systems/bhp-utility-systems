from django.apps import AppConfig as DjangoAppConfig
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from edc_base.apps import AppConfig as BaseEdcBaseAppConfig
from edc_device.apps import AppConfig as BaseEdcDeviceAppConfig
from edc_device.constants import CENTRAL_SERVER
from edc_facility.apps import AppConfig as BaseEdcFacilityAppConfig
from edc_identifier.apps import AppConfig as BaseEdcIdentifierAppConfig
from edc_navbar.apps import AppConfig as BaseEdcNavbarAppConfig
from edc_protocol.apps import AppConfig as BaseEdcProtocolAppConfig


class AppConfig(DjangoAppConfig):
    name = 'bhp_utility_systems'
    verbose_name = 'BHP Utility Systems'
    identifier_pattern = None


class EdcBaseAppConfig(BaseEdcBaseAppConfig):
    project_name = 'BHP Utility Systems'
    institution = 'Botswana Harvard Health Partnership'
    disclaimer = 'For internal personnel management'


class EdcProtocolAppConfig(BaseEdcProtocolAppConfig):
    protocol = 'BHP199'
    protocol_name = 'BHP Utility Systems'
    protocol_number = '199'
    protocol_title = ''


class EdcDeviceAppConfig(BaseEdcDeviceAppConfig):
    device_role = CENTRAL_SERVER
    device_id = '99'


class EdcFacilityAppConfig(BaseEdcFacilityAppConfig):
    country = 'botswana'
    definitions = {
        '7-day clinic': dict(days=[MO, TU, WE, TH, FR, SA, SU],
                             slots=[100, 100, 100, 100, 100, 100, 100]),
        '5-day clinic': dict(days=[MO, TU, WE, TH, FR],
                             slots=[100, 100, 100, 100, 100])}


class EdcIdentifierAppConfig(BaseEdcIdentifierAppConfig):
    identifier_prefix = '199'


class EdcNavBarAppConfig(BaseEdcNavbarAppConfig):
    default_navbar_name = 'default'
