class Strategy:
    ON_EACH_STEP = "ON_EACH_STEP"
    ON_EACH_SCENARIO = "ON_EACH_SCENARIO"
    ON_FAILURE = "ON_FAILURE"
    DISABLED = "DISABLED"

    @staticmethod
    def get_value(strategy):
        if strategy in [Strategy.ON_EACH_STEP, Strategy.ON_EACH_SCENARIO, Strategy.ON_FAILURE, Strategy.DISABLED]:
            return strategy
