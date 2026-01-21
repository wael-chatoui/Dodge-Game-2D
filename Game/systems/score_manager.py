"""
Score tracking and high score persistence.
"""
import json
import os
import pygame
from typing import List, Dict
from ..config import constants as C


class ScoreManager:
    """Manages scoring and high scores."""

    def __init__(self):
        self.current_score = 0
        self.score_multiplier = 1.0
        self.multiplier_end_time = 0
        self.time_elapsed = 0.0
        self.meteorites_dodged = 0
        self.high_scores: List[Dict] = []

        self._load_high_scores()

    def reset(self):
        """Reset current game score."""
        self.current_score = 0
        self.score_multiplier = 1.0
        self.multiplier_end_time = 0
        self.time_elapsed = 0.0
        self.meteorites_dodged = 0

    def update(self, dt: float):
        """
        Update score based on time survived.

        Args:
            dt: Delta time in seconds
        """
        self.time_elapsed += dt

        # Base score from time
        score_gain = int(C.SCORE_PER_SECOND * dt * self.score_multiplier)
        self.current_score += score_gain

    def add_meteorite_dodge(self):
        """Add bonus for dodging a meteorite."""
        bonus = int(C.METEORITE_DODGE_BONUS * self.score_multiplier)
        self.current_score += bonus
        self.meteorites_dodged += 1

    def set_multiplier(self, multiplier: float, duration_ms: int):
        """
        Set score multiplier for power-up.

        Args:
            multiplier: Score multiplier value
            duration_ms: Duration in milliseconds
        """
        self.score_multiplier = multiplier
        self.multiplier_end_time = pygame.time.get_ticks() + duration_ms

    def check_multiplier_expiry(self):
        """Check if multiplier has expired."""
        if self.multiplier_end_time > 0 and pygame.time.get_ticks() >= self.multiplier_end_time:
            self.score_multiplier = 1.0
            self.multiplier_end_time = 0

    def _load_high_scores(self):
        """Load high scores from JSON file."""
        try:
            if os.path.exists(C.HIGHSCORE_FILE):
                with open(C.HIGHSCORE_FILE, 'r') as f:
                    data = json.load(f)
                    self.high_scores = data.get('scores', [])
        except Exception as e:
            print(f"WARNING: Could not load high scores: {e}")
            self.high_scores = []

    def save_high_score(self, player_name: str = "Player"):
        """
        Save current score if it's a high score.

        Args:
            player_name: Name of the player
        """
        score_entry = {
            'name': player_name,
            'score': self.current_score,
            'time': int(self.time_elapsed),
            'meteorites_dodged': self.meteorites_dodged
        }

        self.high_scores.append(score_entry)
        self.high_scores.sort(key=lambda x: x['score'], reverse=True)
        self.high_scores = self.high_scores[:10]  # Keep top 10

        # Save to file
        try:
            os.makedirs(os.path.dirname(C.HIGHSCORE_FILE), exist_ok=True)
            with open(C.HIGHSCORE_FILE, 'w') as f:
                json.dump({'scores': self.high_scores}, f, indent=2)
        except Exception as e:
            print(f"ERROR: Could not save high scores: {e}")

    def is_high_score(self) -> bool:
        """
        Check if current score is a high score.

        Returns:
            True if current score makes the top 10
        """
        if len(self.high_scores) < 10:
            return True
        return self.current_score > self.high_scores[-1]['score']

    def get_rank(self) -> int:
        """
        Get rank of current score (1-10, or 0 if not in top 10).

        Returns:
            Rank number or 0 if not in top 10
        """
        for i, entry in enumerate(self.high_scores):
            if self.current_score >= entry['score']:
                return i + 1
        if len(self.high_scores) < 10:
            return len(self.high_scores) + 1
        return 0
