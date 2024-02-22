from src.main.pytest.ltm.PropertyManager import PropertyManager
from src.main.pytest.ltm.screenshots.Strategy import Strategy


class SSConfig:
    def __init__(self, strategy):
        self.strategy = strategy

    @staticmethod
    def load():
        strategy = Strategy.DISABLED
        if PropertyManager.is_properties_file_present():
            strategy_str = PropertyManager.get_property("test-manager.ltm.screenshots")
            strategy = Strategy.get_value(strategy_str)

        return SSConfig(strategy)

    def contains(self, strategy):
        return self.strategy == strategy

    def is_not_contains(self, strategy):
        return not self.contains(strategy)