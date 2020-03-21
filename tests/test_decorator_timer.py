from unittest.mock import MagicMock

from decorator_timer import DecoratorConfig, DecoratedCallable


def test_decorator_config_copy():
    config = DecoratorConfig()

    config_copy = config.copy_config()

    assert config is not config_copy

    assert config.normalization == config_copy.normalization
    assert config.triggers == config_copy.triggers
    assert config.log_level == config_copy.log_level


def test_decorated_callable_triggers_and_normalizer_called():
    norm_value = 1

    trigger_1 = MagicMock()
    trigger_2 = MagicMock()
    normalizer = MagicMock(return_value=norm_value)

    def test_function():
        pass

    config = DecoratorConfig(normalization=normalizer, triggers=[trigger_1, trigger_2])
    dc = DecoratedCallable(callable_object=test_function, config=config)

    dc()

    trigger_1.assert_called_once_with(norm_value)
    trigger_2.assert_called_once_with(norm_value)
    normalizer.assert_called_once()
    assert len(normalizer.call_args[0]) == 1
    assert type(normalizer.call_args[0][0]) is float


