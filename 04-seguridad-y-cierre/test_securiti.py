
from domain import ActivityFull, ActivityNotFound, AlreadyRegistered, ActivityService
from security import (
    ConfirmationExpired, ConfirmationInvalid, ConfirmationMismatch,
    ConfirmationRequired, ConfirmationStore, ValidationError,
    confirmation_store, is_host_confirmation_valid,
    validate_activity_id, validate_email,
)


def raises(exc, fn, *args):
    try:
        fn(*args)
    except exc:
        return
    raise AssertionError(f"no lanzó {exc.__name__}")


def test_activity_id():
    assert validate_activity_id(" 007 ") == "7"
    for bad in ["abc", "", "0", "-1", None, "1" * 11]:
        raises(ValidationError, validate_activity_id, bad)


def test_email():
    assert validate_email(" Alumno@UNTDF.edu.ar ") == "alumno@untdf.edu.ar"
    for bad in ["", "no-es-email", "a@b", "a..b@x.com", "@x.com", "a@@x.com", None]:
        raises(ValidationError, validate_email, bad)


def test_confirmacion():
    store = ConfirmationStore()
    t = store.issue("2", "a@x.com")
    assert store.failure_reason(t, "2", "a@x.com") is None
    assert isinstance(store.failure_reason(t, "3", "a@x.com"), ConfirmationMismatch)
    assert isinstance(store.failure_reason(t, "2", "b@x.com"), ConfirmationMismatch)
    assert isinstance(store.failure_reason("inventado", "2", "a@x.com"), ConfirmationInvalid)
    assert type(store.failure_reason(None, "2", "a@x.com")) is ConfirmationRequired
    store.consume(t, "2", "a@x.com")
    raises(ConfirmationInvalid, store.consume, t, "2", "a@x.com")  # un solo uso


def test_vencimiento():
    store = ConfirmationStore(ttl_seconds=-1)
    t = store.issue("2", "a@x.com")
    assert isinstance(store.failure_reason(t, "2", "a@x.com"), ConfirmationExpired)


def test_gate_del_host():
    t = confirmation_store.issue("1", "a@x.com")
    assert is_host_confirmation_valid(t, "1", "a@x.com") is True
    assert is_host_confirmation_valid("true", "1", "a@x.com") is False
    assert is_host_confirmation_valid(None, "1", "a@x.com") is False


def test_dominio():
    svc = ActivityService()
    assert svc.register("1", "nuevo@untdf.edu.ar")["status"] == "registered"
    raises(AlreadyRegistered, svc.register, "1", "nuevo@untdf.edu.ar")
    raises(ActivityFull, svc.register, "3", "x@untdf.edu.ar")
    raises(ActivityNotFound, svc.register, "999", "x@untdf.edu.ar")


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("OK", name)