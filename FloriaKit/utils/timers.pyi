import typing as t

from .calculated_value import CalculatedValue, gcv

class VariableTimer:
    """Repeating timer with configurable interval

    Triggers at fixed intervals but does not accumulate missed ticks
    Ideal for non-critical periodic tasks like UI updates

    For example:

    ```python

        timer = VariableTimer(1/120)
        while running:
            if timer.attempt():
                ...

    ```
    """

    def __init__(self, interval: CalculatedValue[float] | float = 0) -> None:
        """Initialize VariableTimer instance

        Args:
            interval (float, optional): Time between triggers in seconds (must be >= 0). Defaults to 0.

        Raises:
            ValueError: If interval is negative
        """

    def attempt(self) -> bool:
        """Attempt triggering based on elapsed time

        Updates trigger timestamp when activated

        Returns:
            True if timer triggered, False otherwise
        """

    def get_interval(self) -> float: ...
    @property
    def interval(self) -> float:
        """Current interval duration in seconds"""

    @property
    def last_time(self) -> float: ...
    def get_progress(self) -> float: ...
    @property
    def progress(self) -> float: ...

class FixedTimer:
    """Fixed-interval timer

    Tracks ideal tick progression based on elapsed time and triggers discrete ticks when the ideal count exceeds processed ticks

    For example:

    ```python

        timer = FixedTimer(1/20)
        while running:
            if timer.Try():
                ...

    ```
    """

    def __init__(
        self,
        interval: float,
        max_lag: int = 10,
    ) -> None:
        """Initialize FixedTimer instance

        Args:
            interval (float): Time between ticks in seconds (must be > 0)
            max_lag (int): Максимальное количество отстающих тиков

        Raises:
            ValueError: If interval is not positive
        """

    def attempt(self) -> bool:
        """Attempt to process next tick

        Advances internal counter if sufficient time has elapsed since last processed tick

        Returns:
            True if tick was processed, False otherwise
        """

    @property
    def interval(self) -> float:
        """Fixed duration between ticks (seconds)"""

    @property
    def tick(self) -> int:
        """Number of ticks processed"""

    def get_ideal_ticks(self) -> float: ...
    @property
    def ideal_ticks(self) -> float:
        """Theoretical tick count based on elapsed time

        Represents how many ticks should have occurred since timer start, calculated as: (current_time - start_time) / interval
        """

    def get_progress_by_tick(self, tick: t.Optional[int]) -> float: ...
    @property
    def progress(self) -> float: ...

__all__ = [
    'VariableTimer',
    'FixedTimer',
]
