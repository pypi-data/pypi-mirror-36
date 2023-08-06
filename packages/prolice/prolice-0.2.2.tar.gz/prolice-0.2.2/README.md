[![pipeline status](https://gitlab.com/stefan.mavrodiev/prolice/badges/master/pipeline.svg)](https://gitlab.com/stefan.mavrodiev/prolice/commits/master)

## Description

This tool can be used for uploading generated bit-stream to ether
[iCE40HX1K-EVB] or [iCE40HX8K-EVB]. The tool currently supports only
[ARM-USB-OCD-H] as flashing tool.

## Hardware connection

Connect the flashing tool with the target board as shown:

| Name         | ARM-USB-OCD-H | UEXT | Description  |
| ------------ |:------------: | :--: | ------------ |
| **VCC**      | 1             | 1    | Power supply (*see Note*)|
| **GND**      | 4             | 2    | Ground       |
| **CDONE**    | 11            | 5    | iCE40 status indication |
| **CRESET**   | 3             | 6    | iCE40 reset signal |
| **MISO**     | 13            | 7    | Serial data from the board to the PC |
| **MOSI**     | 5             | 8    | Serial data from the PC to the board |
| **SCK**      | 9             | 9    | Serial clock |
| **CS**       | 7             | 10   | Chip select |

**Note** : In order to work properly ARM-USB-OCD-H must have target voltage
feedback. One simple way is to solder **3.3V_E1** jumper, found on the bottom
of the board. If you're getting the voltage from somewhere else make sure
it's **3.3V**!

## Installation

The recommended way is:

```sh
pip3 install prolice
```

If you chose building from sources:

```sh
git clone https://gitlab.com/stefan.mavrodiev/prolice.git
cd prolice
python3 setup.py install
```

## Usage

Assuming you have bit-stream file called hardware.bin:

```sh
prolice /path/to/file/hardware.bin
```

[iCE40HX1K-EVB]: https://www.olimex.com/Products/FPGA/iCE40/iCE40HX1K-EVB/
[iCE40HX8K-EVB]: https://www.olimex.com/Products/FPGA/iCE40/iCE40HX8K-EVB/
[ARM-USB-OCD-H]: https://www.olimex.com/Products/ARM/JTAG/ARM-USB-OCD-H/
