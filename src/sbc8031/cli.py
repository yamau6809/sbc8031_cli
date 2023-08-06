"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = sbc8031.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import logging
import logging.config
from io import FileIO

import click
import serial
import yaml
from serial.tools import list_ports

_logger = logging.getLogger(__name__)


@click.group()
@click.version_option()
@click.option(
    "--logger-config",
    "-l",
    type=click.File(mode="r", encoding="utf_8_sig"),
    required=False,
    default=None,
    help="Specify Logger Configuration File.",
)
def sbc8031_cli(logger_config: FileIO):
    """Calls :func:`cli` passing the CLI arguments.

    This function can be used as entry point to create console scripts with setuptools.
    """
    if logger_config is not None:
        logging.config.dictConfig(yaml.full_load(logger_config))


def send_code(ser: serial.Serial, code_line: str) -> None:
    ser.write((code_line.strip() + "\r\n").encode(encoding="ascii"))
    echoed_line = str(object=ser.readline(), encoding="ascii")
    _logger.info(echoed_line)
    while not echoed_line.startswith(">"):
        echoed_line = str(object=ser.readline(), encoding="ascii")
        _logger.info(echoed_line)


def get_usb_port_name():
    ports = find_usb_serial_body()
    for p in ports:
        port = p[0]
        break
    _logger.info(port)
    return port


@sbc8031_cli.command()
@click.option(
    "--port",
    "-p",
    type=click.STRING,
    required=False,
    default=None,
    help="Specify Port to be used.",
)
@click.argument("output_file", type=click.File(mode="w", encoding="utf_8_sig"))
def save(port: str, output_file: FileIO) -> None:
    """Save the current code from SBC8031."""
    _logger.info("Save")
    _logger.info(port)

    if port is None:
        port = get_usb_port_name()

    with serial.Serial(port) as ser:
        _logger.info(ser.name)
        ser.write(b"list\r\n")
        echoed_line = str(object=ser.readline(), encoding="ascii")
        _logger.info(echoed_line)
        while not echoed_line.startswith("list"):
            echoed_line = str(object=ser.readline(), encoding="ascii")
            _logger.info(echoed_line)

        echoed_line = str(object=ser.readline(), encoding="ascii")
        if len(echoed_line.strip()) > 0:
            _logger.info(echoed_line.strip())
            output_file.write(echoed_line.strip() + "\n")
        while not echoed_line.startswith("READY"):
            echoed_line = str(object=ser.readline(), encoding="ascii")
            if len(echoed_line.strip()) > 0 and not echoed_line.startswith("READY"):
                _logger.info(echoed_line.strip())
                output_file.write(echoed_line.strip() + "\n")


@sbc8031_cli.command()
@click.option(
    "--port",
    "-p",
    type=click.STRING,
    required=False,
    default=None,
    help="Specify Port to be used.",
)
@click.argument("input_file", type=click.File(mode="r", encoding="utf_8_sig"))
def load(port: str, input_file: FileIO) -> None:
    """Load Specified File to SBC8031."""
    _logger.info("Load")
    _logger.info(port)

    if port is None:
        port = get_usb_port_name()

    _logger.info(port)
    with serial.Serial(port=port) as ser:
        _logger.info(ser.name)
        send_code(ser=ser, code_line="new")
        for code_line in input_file:
            _logger.info(code_line)
            send_code(ser=ser, code_line=code_line)


def find_usb_serial_body():
    return list_ports.grep(regexp="VID:PID=1A86:7523")


@sbc8031_cli.command()
def list() -> None:
    """List available serial ports."""
    port_info = list_ports.comports()
    click.secho(message=yaml.dump(data=port_info), fg="green")


@sbc8031_cli.command()
def find_usb_serial() -> None:
    """Find USB Serial COM Port."""
    ports = find_usb_serial_body()
    for port in ports:
        click.secho(message=port, fg="green")


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m sbc8031.cli 42
    #
    sbc8031_cli()
