from __future__ import annotations

"""Abstract base class for diarization adapters."""

from abc import ABC, abstractmethod


class DiarizationAdapter(ABC):
    """Base class for all diarization model adapters.

    Subclasses must implement ``diarize(audio_path)`` and set the class
    attributes ``name``, ``version``, and ``provider``.
    """

    name: str = ""
    version: str = ""
    provider: str = ""

    @abstractmethod
    def diarize(self, audio_path: str) -> dict:
        """Run speaker diarization on the given audio file.

        Args:
            audio_path: Absolute path to the audio file (WAV recommended).

        Returns:
            A dict with the following keys:

            - ``recording_id`` (str): Identifier for the recording.
            - ``segments`` (list[dict]): Each dict has ``start`` (float),
              ``end`` (float), ``speaker`` (str).
            - ``model`` (str): Model name.
            - ``version`` (str): Model version.
            - ``status`` (str): ``"completed"`` or ``"failed"``.
            - ``error`` (str | None): Error message if status is ``"failed"``.
        """
        raise NotImplementedError
