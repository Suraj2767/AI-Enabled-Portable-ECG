# AI-Enabled Portable ECG Monitoring System for Early Cardiac Risk Detection

📌 Project Overview

The **AI-Enabled Portable ECG Monitoring System for Early Cardiac Risk Detection** is a compact, low-cost and portable healthcare monitoring System designed to acquire ECG signals and provide real-time cardiac status information.

The system combines **ECG signal acquisition, digital signal processing, machine learning, physiological sensing, ESP32-based embedded processing, MQTT communication, and a Flutter mobile dashboard** into a single monitoring platform.

The primary objective is to develop an affordable portable system that can monitor ECG signals, extract useful features, classify the detected heartbeat pattern, and provide an understandable status to the user.


## 🎯 Objectives

* Acquire ECG signals using the **AD8232 ECG sensor**.
* Process and filter ECG signals using the ESP32.
* Detect important ECG waveform characteristics such as R-peaks.
* Calculate heart rate from the ECG signal.
* Extract numerical features from ECG heartbeat segments.
* Use a **Machine Learning model** for heartbeat classification.
* Display ECG and physiological information on an OLED display.
* Measure pulse rate and SpO₂ using the **MAX30102** sensor.
* Transmit processed data wirelessly using Wi-Fi and MQTT.
* Display monitoring information through a **Flutter mobile application**.
* Develop a portable and expandable embedded healthcare platform.


# 🔧 Hardware Components

| Component          | Purpose                                         |
| ------------------ | ----------------------------------------------- |
| ESP32 Dev Module   | Main microcontroller and wireless communication |
| AD8232             | ECG signal acquisition                          |
| MAX30102           | Heart rate and SpO₂ measurement                 |
| OLED Display       | Local real-time information display             |
| LEDs               | System/status indication                        |
| TP4056             | Li-ion/Li-Po battery charging                   |
| Battery            | Portable power supply                           |
| Push Button/Switch | Power/control                                   |
| Pref-Board         | Circuit assembly                                |

# ⚙️ Working Principle

## 1. ECG Signal Acquisition

The **AD8232** is used as the ECG analog front-end.

Electrodes attached to the body detect the electrical activity of the heart. The AD8232 amplifies and conditions the weak ECG signal and provides an analog output to the ESP32 ADC.

```text
Electrodes
    ↓
AD8232
    ↓
Analog ECG Signal
    ↓
ESP32 ADC
```

# 2. ECG Signal Processing

The raw ECG signal can contain:

* Baseline wandering
* Power-line interference
* High-frequency noise
* Motion artifacts

Digital filtering is therefore applied before feature extraction.

The project uses filtering concepts such as a **Butterworth filter** to reduce unwanted frequency components while preserving important ECG waveform characteristics.


# 3. R-Peak Detection

The processed ECG waveform is analyzed to identify **R-peaks**.

The time difference between consecutive R-peaks can be used to estimate heart rate.

The basic relationship is:

```text
Heart Rate (BPM) = 60 / RR interval (seconds)
```

For example, if:

```text
RR interval = 1 second
```

then:

```text
Heart Rate = 60 BPM
```

# 4. Heartbeat Segmentation

After identifying an R-peak, a fixed window around the peak is extracted to represent an individual heartbeat.

For the current dataset processing:

```text
90 samples before R-peak
+
162 samples after R-peak
=
252 samples per heartbeat
```

The MIT-BIH ECG data used in the initial model uses a sampling frequency of:

```text
360 Hz
```
# 🤖 Artificial Intelligence / Machine Learning

The project uses Machine Learning to classify ECG heartbeat patterns.

Initially, a **Random Forest classifier** is used for classification.

Instead of directly feeding the entire ECG waveform into the classifier, numerical features are extracted from each heartbeat.

### Features used
The final embedded model uses 84 ECG features.

The feature set includes:

Record-normalized amplitude characteristics
Maximum and minimum amplitude
Peak-to-peak amplitude
Standard deviation
RMS
Median
IQR
ECG waveform shape characteristics
Maximum and mean slope
Peak positions
Zero-crossing information
QRS-width related information
Downsampled waveform characteristics
RR-interval ratios

These features form the input vector for the Random Forest model.

Example:

```text
ECG Beat
   ↓
Feature Extraction
   ↓
[Mean, Std, Max, Min, P2P, RMS,..]
   ↓
Random Forest
   ↓
Classification
```
# 📊 Dataset

The initial model development used ECG data from the **MIT-BIH Arrhythmia Database**.

The ECG recordings were processed into individual heartbeat segments.

The initial prototype used:

```text
500 Normal beats
+
500 Abnormal beats
```
for model development and training.

The initial model achieved approximately:

```text
Accuracy: 87.71%
```
with the available   dataset.

# 🧩 ESP32 AI Integration
After training and evaluation, the trained model can be converted into a format suitable for embedded deployment.
Example:

```text
ecg_model_v3_3.h
```
The model is then integrated into the ESP32 firmware.
The intended embedded workflow is:
```text
ECG Acquisition
      ↓
Filtering
      ↓
R-Peak Detection
      ↓
Heartbeat Segmentation
      ↓
Feature Extraction
      ↓
Random Forest Model
      ↓
Normal / Abnormal
```
This allows the ESP32 to perform the main processing locally rather than sending raw ECG data to the mobile application for AI processing.
---
# ❤️ MAX30102 Integration
The **MAX30102** is used as an additional physiological sensing module.
It can provide:
* Heart rate
* SpO₂ estimation

The sensor communicates with the ESP32 using the **I²C interface**.

The MAX30102 is intended to complement ECG monitoring rather than replace ECG analysis.

# 🖥️ OLED Display
An OLED display provides local feedback without requiring a smartphone.
The display can show information such as:

```text
SMART ECG

HR: 72 BPM
SpO2: 98%

STATUS:
NORMAL
```
For an abnormal classification, the system can provide an alert through the display, LED and buzzer.

# 📡 IoT Communication
The ESP32 provides Wi-Fi connectivity and communicates with the Flutter application using the **MQTT protocol**.
System flow:

```text
ESP32
  ↓
Wi-Fi
  ↓
MQTT Broker
  ↓
Flutter Application
```
The project uses MQTT for lightweight publish/subscribe communication.

Example topic:

```text
smart_ecg/demo_esp32_01/data
```
The mobile application receives processed monitoring information rather than performing the primary ECG AI processing.
---
# 📱 Flutter Mobile Application

A Flutter-based mobile application is used as the monitoring dashboard.

The application can display:

* ECG monitoring information
* Heart rate
* SpO₂
* Classification status
* Device connection status
* Real-time monitoring information

The application communicates with the ESP32 through the MQTT broker.

### Technology Stack

```text
Flutter
Dart
MQTT
ESP32
Wi-Fi
```

# 🛠️ Software & Tools

### Embedded

* Arduino IDE / ESP32 development environment
* C/C++
* ESP32 framework

### AI / Data Processing

* Python
* NumPy
* Matplotlib
* Scikit-learn
* WFDB
* Random Forest

### Mobile Application

* Flutter
* Dart
* MQTT Client

### Hardware Design

* EasyEDA / KiCad
* PCB prototyping
---
# 📁 Project Structure

```text
AI-Enabled-Portable-ECG/
│
├── README.md
│
├── ESP32/
│   └── smart_ecg.ino
│
├── AI_Model/
│   ├── training_code/
│   ├── dataset_processing/
│   └── ecg_model_v3_3.h
│
├── Flutter_App/
│   └── smart_ecg/
│
├── Hardware/
│   ├── circuit_diagram/
│   ├── wiring/
│   └── PCB/
│
├── Dataset/
│   └── README.md
│
├── Images/
│   ├── prototype.jpg
│   ├── circuit.jpg
│   └── app_dashboard.jpg
│
└── LICENSE
```

---

# 🔮 Future Scope

Future improvements may include:

* Larger and more diverse ECG datasets
* Multi-class arrhythmia classification
* Improved ECG feature extraction
* Lightweight deep-learning models for embedded devices
* Better motion-artifact rejection
* Custom PCB and compact enclosure
* Cloud-based historical monitoring
* Secure patient-data storage
* Additional physiological sensors
* Clinical validation under appropriate medical supervision
---

<img width="611" height="374" alt="image" src="https://github.com/user-attachments/assets/23dfba6d-bb32-45e9-9211-6e66aeca45f4" />
<img width="205" height="384" alt="image" src="https://github.com/user-attachments/assets/bf4edc53-36d4-45c9-9861-bd59287e0805" />



