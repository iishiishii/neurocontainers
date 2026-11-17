from __future__ import annotations

import pytest

from tools.validate_domains import check_labels


REGISTRY = {
    "neuroimaging": {
        "source_repositories": ["NeuroDesk/neurocontainers"],
    },
    "microscopy": {
        "source_repositories": ["Example/microcontainers"],
    },
}


def test_domain_registry_rejects_typos_and_missing_repository_mapping() -> None:
    check_labels(
        ["neuroimaging"],
        "recipes/tool/build.yaml",
        "NeuroDesk/neurocontainers",
        REGISTRY,
    )
    with pytest.raises(ValueError, match="not in neuroimaging.source_repositories"):
        check_labels(
            ["neuroimaging"],
            "recipes/tool/build.yaml",
            "neurodesk/neurocontainers",
            REGISTRY,
        )
    with pytest.raises(ValueError, match="unknown domain microsopy"):
        check_labels(
            ["microsopy"],
            "recipes/tool/build.yaml",
            "NeuroDesk/neurocontainers",
            REGISTRY,
        )
    with pytest.raises(ValueError, match="not in microscopy.source_repositories"):
        check_labels(
            ["microscopy"],
            "recipes/tool/build.yaml",
            "NeuroDesk/neurocontainers",
            REGISTRY,
        )


def test_domain_id_length_and_slug_boundaries() -> None:
    registry = {"a" * 64: REGISTRY["neuroimaging"]}
    check_labels(["a" * 64], "recipe", "NeuroDesk/neurocontainers", registry)
    for invalid in ("a" * 65, "a--b", "a-"):
        with pytest.raises(ValueError, match="invalid domain ID"):
            check_labels([invalid], "recipe", "NeuroDesk/neurocontainers", registry)
