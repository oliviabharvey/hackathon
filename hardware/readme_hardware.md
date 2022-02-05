# Hardward Readme
This readme covers the hardware installation and connections.

## Overview
The hardware is composed of the components described below. Schematics is available below.
- **LEDs**: All LEDs are the generic 5mm, ≈15mA LED. They are all in serie with a 220Ω[^1] resistance to limit current to 15mA from the Raspberry Pi 3.3V source.
   - Tray light: LED near the food tray delivery system that turns on when food is available to give a visual indicator. Yellow-colored LED.
   - Experiment light: LED on the outside of the experiment box that turns on as a visual indicator that an experiment is currently ongoing. Red-colored LED.
   - Box light: LED on the top of the experiment box that act as a flood light. As of February 2022, this is currently unused in the code or experiment, but can be used when doing maintenance, etc. White-colored LED.
- **Motor**: A motor is used to push a syringe that provides <span style="color:red">sugar-based liquid</span> reward, usually to a mouse when a good answer is given. The motor is a basic 28BYJ-48 stepper motor using 5V DC voltage. It can be run from the 5V output of the Raspberry Pi directly for our application of pushing slighly on a syring. Otherwise, a 2nd 5V source should be used.
- **Buzzer**: A passive piezoeletric buzzer that can be driven by a 3.3V pulse-width modulated signal is used to play a sound (default at 3kHz), generally when the food is delivered.
- **Infrared Beam (IRB)**: An 5mm infrared (IR) LED using a wavelenght of 940nm is placed in front of a matched receiver. The LED is in serie with a 220Ω resistance to limit current to 15mA. The receiver is in serie with a 220Ω resistance to limit current and a pull-down resistor of 1MΩ. Currently, we are using Gikfun EK8443 LED (clear LED head) & Receivers (dark LED head) combo[^2]. Note that infrared is used to prevent any interaction with other lighting indicators (such as the tray light).

Overview of the connections & Schematics:
![Overview of the hardware](./hardware/hardware_diagram.png)

## LEDs

## Motor

## Buzzer

## Infrared Beam

[^1]: We were lacking some 220Ω when soldering the boards. 330Ω resistances were used as a replacement.
[^2]: Any IR LED/Receiver that can be driven by 3.3V would work. Just make sure that the receiver is a IR receiver that is at its high voltage state when being illumitated by the IR LED and its low voltage state when the infrared beam is broken.