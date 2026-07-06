import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import load_events, search_events


def test_load_events_reads_xml_file():
    events = load_events('raw_xml/registry_persistance.xml')
    assert len(events) > 0


def test_search_events_by_event_id():
    events = load_events('raw_xml/registry_persistance.xml')
    results = search_events(events, 'event_id == 13')
    assert len(results) > 0
    assert results[0]['event_id'] == 13


def test_invalid_query_returns_empty_results():
    events = load_events('raw_xml/registry_persistance.xml')
    results = search_events(events, 'event_id >>> 13')
    assert results == []
