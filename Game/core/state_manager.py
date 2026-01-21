"""
Finite State Machine for game states.
"""
from enum import Enum, auto
from typing import Optional


class GameState(Enum):
    """All possible game states."""
    MENU = auto()
    DIFFICULTY_SELECT = auto()
    TUTORIAL = auto()
    COUNTDOWN = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


class StateManager:
    """Manages game state transitions."""

    def __init__(self):
        self._current_state = GameState.MENU
        self._previous_state: Optional[GameState] = None

    @property
    def current_state(self) -> GameState:
        """Get the current game state."""
        return self._current_state

    def transition_to(self, new_state: GameState):
        """
        Transition to a new state.

        Args:
            new_state: The state to transition to
        """
        if new_state != self._current_state:
            self._previous_state = self._current_state
            self._current_state = new_state
            print(f"State: {self._previous_state.name} -> {new_state.name}")

    def is_state(self, state: GameState) -> bool:
        """
        Check if current state matches.

        Args:
            state: The state to check

        Returns:
            True if current state matches
        """
        return self._current_state == state

    def return_to_previous(self):
        """Return to previous state (useful for pause/resume)."""
        if self._previous_state:
            self.transition_to(self._previous_state)
