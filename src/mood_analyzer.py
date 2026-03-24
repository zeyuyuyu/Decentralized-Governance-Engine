import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from typing import Dict, List, Tuple
import logging

class MoodAnalyzer:
    def __init__(self):
        try:
            nltk.download('vader_lexicon', quiet=True)
            self.sia = SentimentIntensityAnalyzer()
        except Exception as e:
            logging.error(f'Failed to initialize NLTK: {str(e)}')
            raise

    def analyze_mood(self, text: str) -> Dict[str, float]:
        """
        Analyze the mood/sentiment of input text
        Returns dictionary of sentiment scores
        """
        return self.sia.polarity_scores(text)

    def get_music_parameters(self, sentiment: Dict[str, float]) -> Dict[str, float]:
        """
        Convert sentiment scores to music parameters
        """
        params = {
            'valence': self._normalize_score(sentiment['compound']),
            'energy': self._normalize_score(sentiment['pos']),
            'danceability': self._normalize_score((sentiment['pos'] + sentiment['compound'])/2),
            'tempo': self._map_tempo(sentiment)
        }
        return params

    def _normalize_score(self, score: float) -> float:
        """
        Normalize scores to 0-1 range for music API compatibility
        """
        return (score + 1) / 2

    def _map_tempo(self, sentiment: Dict[str, float]) -> float:
        """
        Map sentiment to appropriate tempo range (60-180 BPM)
        """
        base_tempo = 120
        tempo_range = 60
        modifier = sentiment['compound'] * sentiment['pos'] - sentiment['neg']
        return base_tempo + (modifier * tempo_range)

    def generate_playlist_parameters(self, journal_entries: List[str]) -> List[Tuple[Dict[str, float], float]]:
        """
        Generate music parameters from multiple journal entries with time decay
        Returns list of (parameters, weight) tuples
        """
        playlist_params = []
        decay_factor = 0.85

        for i, entry in enumerate(journal_entries):
            sentiment = self.analyze_mood(entry)
            params = self.get_music_parameters(sentiment)
            weight = decay_factor ** i  # More recent entries have higher weight
            playlist_params.append((params, weight))

        return playlist_params

    def get_mood_description(self, sentiment: Dict[str, float]) -> str:
        """
        Convert sentiment scores to human-readable mood description
        """
        compound = sentiment['compound']
        if compound >= 0.5:
            return 'very positive'
        elif compound >= 0.1:
            return 'positive'
        elif compound <= -0.5:
            return 'very negative'
        elif compound <= -0.1:
            return 'negative'
        return 'neutral'