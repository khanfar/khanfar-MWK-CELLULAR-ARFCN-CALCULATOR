# MWK Cellular Network ARFCN Calculator

A powerful GUI application for calculating cellular network frequencies and providing detailed network information based on ARFCN (Absolute Radio Frequency Channel Number).

![Screenshot 2024-12-29 080433](https://github.com/user-attachments/assets/6f4b80f1-7b7c-41cf-adaa-8c7df5a62b87)


## Features

### 1. Frequency Calculations
- Uplink and Downlink frequencies
- Center frequency calculation
- Channel spacing information
- Supports multiple network types:
  - GSM 900 (2G)
  - GSM 1800 (2G)
  - UMTS 2100 (3G)
  - LTE 1800 (4G)

### 2. Network Information
#### Supported ARFCN Ranges
- GSM 900: 1-124, 128-251
- GSM 1800: 512-885, 1024-1885
- UMTS 2100: 10562-10687
- LTE 1800: 300-379

#### Network Capabilities
- **GSM (2G)**
  - Max Data Rate: 115 Kbps (GPRS), 384 Kbps (EDGE)
  - Features: Voice calls, SMS, Basic data
  - Modulation: GMSK, 8PSK (EDGE)

- **UMTS (3G)**
  - Max Data Rate: 42 Mbps (DC-HSPA+)
  - Features: Video calls, High-speed data, Enhanced security
  - Modulation: QPSK, 16QAM

- **LTE (4G)**
  - Max Data Rate: Up to 150 Mbps
  - Features: High-speed data, VoLTE, Low latency
  - Modulation: QPSK, 16QAM, 64QAM

### 3. Channel Spacing
- GSM 900: 0.2 MHz
- GSM 1800: 0.2 MHz
- UMTS 2100: 5.0 MHz
- LTE 1800: 0.1 MHz

### 4. Additional Features
- Network Info Dialer Codes
  - Android: *#*#4636#*#*
  - iPhone: *3001#12345#*
- Dynamic GUI with auto-adjusting scrollbar
- Error handling for invalid ARFCN inputs
- Centered frequency calculations

## How to Use

1. Launch the application
2. Enter an ARFCN number in the input field
3. Click "Calculate" to see:
   - Uplink and Downlink frequencies
   - Center frequency
   - Channel spacing
   - Network type and capabilities
   - Modulation schemes
   - Maximum data rates

## Technical Requirements
- Python 3.x
- tkinter (included in standard Python distribution)
- No additional dependencies required

## Error Handling
- Validates ARFCN input
- Displays error messages for:
  - Invalid ARFCN numbers
  - Out-of-range values
  - Non-numeric inputs

## GUI Features
- Resizable window (minimum 400x500 pixels)
- Automatic scrollbar for small window sizes
- Clear section organization
- Modern styling with Ttk widgets

## Developer Notes
- Modular code structure with separate calculation and GUI classes
- Type hints for better code maintainability
- Documented methods and functions
- Extensible design for adding new network types
