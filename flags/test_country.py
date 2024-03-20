from src.country import Country
import pytest
import os
from paths import (json_path,images_path)

@pytest.fixture
def country():
    return Country(json_path,images_path)

def test_remove_accents(country):
    assert "Afganistan" == country.remove_accents("Afganistán")
    assert "Emiratos Arabes Unidos" == country.remove_accents("Emiratos Árabes Unidos")
    assert "Etiopia" == country.remove_accents("Etiopía")
    assert "Islas Virgenes Britanicas" == country.remove_accents("Islas Vírgenes Británicas")

def test_search(country):
    assert "Argentina" in country.search_function("Argent") 
    assert "Bélgica" in country.search_function("Belgi")
    assert "Bosnia y Herzegovina Bosnia-Herzegovina" in country.search_function("Bosnia")
    assert "Islas Vírgenes de los Estados Unidos" in country.search_function("Islas")

def test_fuzzy_search(country):
    assert "Belice" in country.search_function_levenshetein("belize")
    assert "Azerbaiyán" in country.search_function_levenshetein("acerbaillan")
    assert "Botsuana" in country.search_function_levenshetein("botswana")
    assert "Zimbabue" in country.search_function_levenshetein("cimbawe")
    pass
