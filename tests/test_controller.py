import pytest

from app.controller import RIPGuardController


def test_initial_route_selection():
    controller = RIPGuardController("R1", "R6")
    result = controller.update_route()

    assert result["path"] is not None
    assert result["status"] == "Initial route selected"


def test_failed_link_triggers_route_switch():
    controller = RIPGuardController("R1", "R6")
    controller.update_route()

    result = controller.fail_link("R1", "R4")

    assert result["path"] is not None
    assert result["status"] == "Switched after link failure"


def test_link_restoration():
    controller = RIPGuardController("R1", "R6")
    controller.update_route()
    controller.fail_link("R1", "R4")

    result = controller.restore_link("R1", "R4")

    assert result["path"] is not None


def test_route_change_counter():
    controller = RIPGuardController("R1", "R6")
    controller.update_route()
    controller.fail_link("R1", "R4")

    assert controller.route_changes >= 1


def test_controller_uses_configured_threshold():
    controller = RIPGuardController("R1", "R6", threshold_pct=10)
    controller.update_route()

    controller.active_path = ["R1", "R4", "R5", "R6"]
    controller.active_cost = controller._path_cost(controller.active_path)

    # Increase the cost of the alternative route.
    for link in controller.links:
        if {link["source"], link["target"]} == {"R1", "R2"}:
            link["latency_ms"] = 20.1

    result = controller.update_route()

    assert result["route_changed"] is False
    assert result["status"] in (
        "Kept current route for stability",
        "Current route retained",
    )


def test_controller_reports_unavailable_route():
    controller = RIPGuardController("R1", "R6")
    controller.update_route()
    previous_path = controller.active_path.copy()

    for link in controller.links:
        controller.failed_links.add(
            frozenset((link["source"], link["target"]))
        )

    result = controller.update_route()

    assert result["path"] is None
    assert result["status"] == "No route available"
    assert controller.active_path == previous_path


def test_link_metrics_can_be_updated():
    controller = RIPGuardController("R1", "R6")

    result = controller.update_link_metrics(
        "R1", "R2", latency_ms=100
    )

    updated_link = next(
        link for link in controller.links
        if {link["source"], link["target"]} == {"R1", "R2"}
    )

    assert updated_link["latency_ms"] == 100
    assert result["path"] is not None


def test_invalid_packet_loss_is_rejected():
    controller = RIPGuardController("R1", "R6")

    with pytest.raises(ValueError):
        controller.update_link_metrics(
            "R1", "R2", packet_loss_pct=150
        )


def test_invalid_latency_is_rejected():
    controller = RIPGuardController("R1", "R6")

    with pytest.raises(ValueError):
        controller.update_link_metrics(
            "R1", "R2", latency_ms=-5
        )


def test_invalid_threshold_is_rejected():
    with pytest.raises(ValueError):
        RIPGuardController("R1", "R6", threshold_pct=150)


def test_failed_route_is_not_used():
    controller = RIPGuardController("R1", "R6")
    controller.update_route()

    result = controller.fail_link("R1", "R4")

    assert result["path"] is not None

    route_links = {
        frozenset((a, b))
        for a, b in zip(result["path"], result["path"][1:])
    }

    assert frozenset(("R1", "R4")) not in route_links