from typing import List
import numpy as np

class TrendAnalysis:
    @staticmethod
    def calculate_moving_average(data: List[float], window_size: int) -> List[float]:
        """
        Calculate the moving average of a dataset.
        """
        return np.convolve(data, np.ones(window_size), "valid") / window_size

    @staticmethod
    def calculate_percentage_change(data: List[float]) -> List[float]:
        """
        Calculate the percentage change of a dataset.
        """
        return np.diff(data) / data[:-1] * 100

    @staticmethod
    def detect_trend(data: List[float]) -> str:
        """
        Detect the trend of a dataset (increasing, decreasing, or stable).
        """
        if all(data[i] <= data[i + 1] for i in range(len(data) - 1)):
            return "Increasing"
        elif all(data[i] >= data[i + 1] for i in range(len(data) - 1)):
            return "Decreasing"
        else:
            return "Stable"