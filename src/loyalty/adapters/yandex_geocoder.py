from loyalty.application.common.geo_finder import GeoFinder


class YandexGeocoder(GeoFinder):
    def find_city(self, city: str) -> str:
        # stub
        return city
