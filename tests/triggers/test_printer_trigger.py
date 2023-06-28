from pytimers.triggers.printer_trigger import PrinterTrigger


def test_basic_call() -> None:
    pt = PrinterTrigger()
    pt(1.0, False)
