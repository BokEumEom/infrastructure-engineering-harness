"""Provider-neutral evidence adapter contracts."""

from .base import normalize_adapter_result
from .prometheus import PrometheusEvidenceAdapter, PrometheusQuery

__all__ = ["PrometheusEvidenceAdapter", "PrometheusQuery", "normalize_adapter_result"]
