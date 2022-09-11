import contextlib
import multiprocessing
import threading
import typing

T = typing.TypeVar('T')
SelfT = typing.TypeVar('SelfT')

_attr_name_template = '_lazyfield_{name}_'

Synchronizer = typing.Callable[[], typing.ContextManager[typing.Any]]


class ValueShield(typing.Generic[T]):
    def __init__(self, synchronizer: Synchronizer, value: T) -> None:
        self._sync = synchronizer()
        self._value = value

    def get(self):
        with self._sync:
            return self._value

    def set(self, value: T):
        with self._sync:
            self._value = value

    def delete(self):
        with self._sync:
            del self._value


class LazyPropertyDescriptor(typing.Generic[SelfT, T]):
    lock_class = threading.Lock

    def __init__(
        self,
        func: typing.Callable[[SelfT], T],
        synchronizer: Synchronizer,
    ) -> None:
        self._func = func
        self._name = _attr_name_template.format(name=func.__name__)
        self._synchronizer = synchronizer

    def __get__(
        self, instance: SelfT | None, owner: type[SelfT] | None = None
    ):
        if instance is None:
            assert owner is not None
            raise AttributeError(
                f'{owner.__name__!r} has no'
                f'attribute {self._func.__name__!r}'
            )
        try:
            shield = self._get_shield(instance)
            result = shield.get()
        except AttributeError:
            result = self._try_build_attr(instance)
            self._set_shield(instance, result)
        return result

    def _set_shield(self, instance: SelfT, result: T):
        object.__setattr__(
            instance, self._name, ValueShield(self._synchronizer, result)
        )

    def _get_shield(self, instance: SelfT) -> ValueShield[T]:
        return typing.cast(
            ValueShield[T], object.__getattribute__(instance, self._name)
        )

    def _try_build_attr(self, instance: SelfT) -> T:
        try:
            val = self._func(instance)
        except Exception as e:
            raise e from None
        else:
            return val

    def __set__(self, instance: SelfT, value: T) -> None:
        try:
            shield = self._get_shield(instance)
        except AttributeError:
            self._set_shield(instance, value)
        else:
            shield.set(value)

    def __delete__(self, instance: SelfT) -> None:
        with contextlib.suppress(AttributeError):
            self._get_shield(instance).delete()


@typing.overload
def lazy_property(
    func: typing.Callable[[SelfT], T]
) -> LazyPropertyDescriptor[SelfT, T]:
    ...


@typing.overload
def lazy_property(
    func: None = None, /, *, process_safe: bool = False
) -> typing.Callable[
    [typing.Callable[[SelfT], T]], LazyPropertyDescriptor[SelfT, T]
]:
    ...


def lazy_property(
    func: typing.Callable | None = None,
    /,
    *,
    process_safe: bool = False,
) -> typing.Callable | LazyPropertyDescriptor:
    synchronizer: Synchronizer = (
        multiprocessing.Lock if process_safe else threading.Lock
    )

    def outer(func: typing.Callable) -> LazyPropertyDescriptor:
        return LazyPropertyDescriptor(func, synchronizer)

    return outer if func is None else outer(func)
