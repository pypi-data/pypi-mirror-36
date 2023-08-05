﻿# Copyright (c) 2013, Pullenti. All rights reserved. Non-Commercial Freeware.
# This class is generated using the converter UniSharping from Pullenti C#.NET project.
# See www.pullenti.ru/downloadpage.aspx.
# 
# 

from pullenti.unisharp.Utils import Utils
from pullenti.ner.ReferentClass import ReferentClass
from pullenti.ner.address.AddressHouseType import AddressHouseType
from pullenti.ner.address.AddressBuildingType import AddressBuildingType
from pullenti.ner.address.AddressDetailType import AddressDetailType


class MetaAddress(ReferentClass):
    
    def __init__(self) -> None:
        from pullenti.ner.address.AddressReferent import AddressReferent
        self.detail_feature = None
        self.house_type_feature = None
        self.building_type_feature = None
        super().__init__()
        self.add_feature(AddressReferent.ATTR_STREET, "Улица", 0, 2)
        self.add_feature(AddressReferent.ATTR_HOUSE, "Дом", 0, 1)
        self.house_type_feature = self.add_feature(AddressReferent.ATTR_HOUSETYPE, "Тип дома", 0, 1)
        self.house_type_feature.add_value(Utils.enumToString(AddressHouseType.ESTATE), "Владение", None, None)
        self.house_type_feature.add_value(Utils.enumToString(AddressHouseType.HOUSE), "Дом", None, None)
        self.house_type_feature.add_value(Utils.enumToString(AddressHouseType.HOUSEESTATE), "Домовладение", None, None)
        self.add_feature(AddressReferent.ATTR_BUILDING, "Строение", 0, 1)
        self.building_type_feature = self.add_feature(AddressReferent.ATTR_BUILDINGTYPE, "Тип строения", 0, 1)
        self.building_type_feature.add_value(Utils.enumToString(AddressBuildingType.BUILDING), "Строение", None, None)
        self.building_type_feature.add_value(Utils.enumToString(AddressBuildingType.CONSTRUCTION), "Сооружение", None, None)
        self.building_type_feature.add_value(Utils.enumToString(AddressBuildingType.LITER), "Литера", None, None)
        self.add_feature(AddressReferent.ATTR_CORPUS, "Корпус", 0, 1)
        self.add_feature(AddressReferent.ATTR_PORCH, "Подъезд", 0, 1)
        self.add_feature(AddressReferent.ATTR_FLOOR, "Этаж", 0, 1)
        self.add_feature(AddressReferent.ATTR_FLAT, "Квартира", 0, 1)
        self.add_feature(AddressReferent.ATTR_CORPUSORFLAT, "Корпус или квартира", 0, 1)
        self.add_feature(AddressReferent.ATTR_OFFICE, "Офис", 0, 1)
        self.add_feature(AddressReferent.ATTR_PLOT, "Участок", 0, 1)
        self.add_feature(AddressReferent.ATTR_BLOCK, "Блок", 0, 1)
        self.add_feature(AddressReferent.ATTR_BOX, "Бокс", 0, 1)
        self.add_feature(AddressReferent.ATTR_KILOMETER, "Километр", 0, 1)
        self.add_feature(AddressReferent.ATTR_GEO, "Город\\Регион\\Страна", 0, 1)
        self.add_feature(AddressReferent.ATTR_ZIP, "Индекс", 0, 1)
        self.add_feature(AddressReferent.ATTR_POSTOFFICEBOX, "Абоненский ящик", 0, 1)
        self.add_feature(AddressReferent.ATTR_CSP, "ГСП", 0, 1)
        self.add_feature(AddressReferent.ATTR_METRO, "Метро", 0, 1)
        detail = self.add_feature(AddressReferent.ATTR_DETAIL, "Дополнительный указатель", 0, 1)
        self.detail_feature = detail
        detail.add_value(Utils.enumToString(AddressDetailType.CROSS), "На пересечении", None, None)
        detail.add_value(Utils.enumToString(AddressDetailType.NEAR), "Вблизи", None, None)
        detail.add_value(Utils.enumToString(AddressDetailType.HOSTEL), "Общежитие", None, None)
        detail.add_value(Utils.enumToString(AddressDetailType.NORTH), "Севернее", None, None)
        detail.add_value(Utils.enumToString(AddressDetailType.SOUTH), "Южнее", None, None)
        detail.add_value(Utils.enumToString(AddressDetailType.EAST), "Восточнее", None, None)
        detail.add_value(Utils.enumToString(AddressDetailType.WEST), "Западнее", None, None)
        detail.add_value(Utils.enumToString(AddressDetailType.NORTHEAST), "Северо-восточнее", None, None)
        detail.add_value(Utils.enumToString(AddressDetailType.NORTHWEST), "Северо-западнее", None, None)
        detail.add_value(Utils.enumToString(AddressDetailType.SOUTHEAST), "Юго-восточнее", None, None)
        detail.add_value(Utils.enumToString(AddressDetailType.SOUTHWEST), "Юго-западнее", None, None)
        self.add_feature(AddressReferent.ATTR_MISC, "Разное", 0, 0)
        self.add_feature(AddressReferent.ATTR_DETAILPARAM, "Параметр детализации", 0, 1)
        self.add_feature(AddressReferent.ATTR_FIAS, "Объект ФИАС", 0, 1)
        self.add_feature(AddressReferent.ATTR_BTI, "Объект БТИ", 0, 1)
    
    @property
    def name(self) -> str:
        from pullenti.ner.address.AddressReferent import AddressReferent
        return AddressReferent.OBJ_TYPENAME
    
    @property
    def caption(self) -> str:
        return "Адрес"
    
    ADDRESS_IMAGE_ID = "address"
    
    def get_image_id(self, obj : 'Referent'=None) -> str:
        return MetaAddress.ADDRESS_IMAGE_ID
    
    _global_meta = None
    
    # static constructor for class MetaAddress
    @staticmethod
    def _static_ctor():
        MetaAddress._global_meta = MetaAddress()

MetaAddress._static_ctor()