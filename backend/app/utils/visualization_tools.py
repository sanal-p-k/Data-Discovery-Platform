from typing import List, Dict
import matplotlib.pyplot as plt
import pandas as pd

class VisualizationTools:
    @staticmethod
    def create_bar_chart(data: Dict[str, int], title: str, xlabel: str, ylabel: str):
        """
        Create a bar chart.
        """
        plt.bar(data.keys(), data.values())
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def create_line_chart(data: Dict[str, int], title: str, xlabel: str, ylabel: str):
        """
        Create a line chart.
        """
        plt.plot(data.keys(), data.values())
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()

    @staticmethod
    def create_pie_chart(data: Dict[str, int], title: str):
        """
        Create a pie chart.
        """
        plt.pie(data.values(), labels=data.keys(), autopct="%1.1f%%")
        plt.title(title)
        plt.show()