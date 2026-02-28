"""Unit tests for interaction filtering logic."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int) -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind="attempt")


def test_filter_returns_all_when_item_id_is_none() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, None)
    assert result == interactions


def test_filter_returns_empty_for_empty_input() -> None:
    result = _filter_by_item_id([], 1)
    assert result == []


def test_filter_returns_interaction_with_matching_ids() -> None:
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 1
    assert result[0].id == 1


def test_filter_excludes_interaction_with_different_learner_id() -> None:
    """Test that filtering by item_id includes interactions with different learner_id."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 2
    assert all(i.item_id == 1 for i in result)


def test_filter_with_multiple_items_returns_correct_matches() -> None:
    """Test filtering with multiple different items returns only matching item_id."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 1),
        _make_log(3, 3, 2),
        _make_log(4, 1, 3),
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 2
    assert all(i.item_id == 1 for i in result)
    assert result[0].id == 1
    assert result[1].id == 2


def test_filter_preserves_interaction_order() -> None:
    """Test that filter preserves the order of interactions."""
    interactions = [_make_log(5, 1, 2), _make_log(3, 2, 2), _make_log(1, 3, 2)]
    result = _filter_by_item_id(interactions, 2)
    assert len(result) == 3
    assert result[0].id == 5
    assert result[1].id == 3
    assert result[2].id == 1


def test_filter_no_matches_returns_empty_list() -> None:
    """Test that filtering with no matches returns empty list."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, 99)
    assert result == []
