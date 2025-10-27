# HWC-TEST-1-MINUTE

HWC-TEST-1-MINUTE is an egocentric video dataset offering 69.2 seconds of domestic-task video spanning 1 scenario (desk tidying) captured by 1 participant across 1 session.

Each session includes a high-quality collection of time-synchronized sensor data and annotations.

Sensor streams:
- Trifocal world cameras (left/center/right monochrome, 1016x1016 @ ~15 Hz)
- Active depth sensor (544x480 @ ~11 Hz, encoded as 32FC1 floats)
- Photo camera stills (RGB JPEG, 640x480 @ ~15 Hz)
- Headset pose (6-DoF, ML2 inside-out tracking @ ~30 Hz)
- Inertial measurement unit (3-axis accel + gyro @ ~46 Hz)
- Hand tracking skeletons (26-joint left/right hands per frame @ ~13 Hz)
- On-device microphone (mono PCM16, 16 kHz)

Annotations:
- Hand pose and joint positions (26-joint left/right hands per frame @ ~13 Hz)
- Semantic narrations describing the actions being performed

## Download

The full dataset of 2.22 GBs is available for download via Google Drive at the following link:

https://drive.google.com/drive/folders/1ximWvWcSNrdd8wgIWlejRUGVxIN6VndL

For access, please contact will@tracelabs.ai. 

## Dataset Structure

The dataset is organized as follows:

```text
.
├── README.md
├── metadata.json
├── ontology.json
└── recordings
    └── participant-001
        └── session-001
            ├── metadata.json
            └── session.mcap
```

### `README.md`

Overview of the dataset and detailed description of file structure.

### `metadata.json`

Metadata file containing information about the dataset. It contains the following fields:

| name | type | description |
| --- | --- | --- |
| `dataset_id` | `string` | Canonical dataset identifier used across tooling and release artifacts. |
| `dataset_version` | `string` | Semantic version of the dataset release captured by this manifest. |
| `dataset_description` | `string` | Human-readable summary of modalities, duration, and scenario coverage. |
| `homepage` | `string` (URL) | Repository or landing page for documentation, updates, and support. |
| `releases` | `array<object>` | Release history for the dataset; see table below. |
| `participants` | `array<object>` | Participant roster with demographics and nested session manifests; see table below. |
| `sessions` | `array<object>` | Dataset-wide session index duplicating the session schema described below. |
| `ontology` | `object` | Ontology descriptor; see table below. |

Each `releases` array entry contains the following fields:

| name | type | description |
| --- | --- | --- |
| `dataset_version` | `string` | Version tag associated with the release entry. |
| `created_at_timestamp` | `string` (ISO-8601) | UTC timestamp when the release was generated. |
| `notes` | `string` | Free-form release notes describing changes or provenance. |

Each `participants` array entry contains the following fields:

| name | type | description |
| --- | --- | --- |
| `participant_id` | `string` | Unique identifier for the participant. |
| `demographics` | `object` | Participant attributes; see table below. |
| `sessions` | `array<object>` | Capture sessions recorded by the participant; follows the session schema below. |

Each `participants[].demographics` object contains the following fields:

| name | type | description |
| --- | --- | --- |
| `dominant_hand` | `string` or `null` | Self-reported dominant hand (`left`, `right`, `ambidextrous`, or `null`) useful for handedness-aware analysis. |
| `height_cm` | `integer` or `null` | Participant height in centimeters for pose and reach normalization. Use null when the information is unavailable. |

Session entry schema used by both `participants[].sessions[]` and top-level `sessions[]` arrays:

| name | type | description |
| --- | --- | --- |
| `session_id` | `string` | Unique session slug matching the folder under `recordings/`. |
| `participant_id` | `string` | Identifier of the participant who generated this session. |
| `capture_start_timestamp` | `string` (ISO-8601) | UTC timestamp when capture began. |
| `capture_end_timestamp` | `string` (ISO-8601) | UTC timestamp when capture ended. |
| `duration_s` | `number` | Session duration expressed in seconds to millisecond precision. |
| `duration_ns` | `integer` | Session duration expressed in nanoseconds for precise alignment. |
| `files` | `object` | File manifest for session assets; see table below. |
| `calibration` | `object` | Calibration payload for sensors and devices; empty when calibration is not published. |
| `coverage` | `object` | Coverage summary or quality metrics; empty when unavailable. |

Each session `files` object contains the following fields:

| name | type | description |
| --- | --- | --- |
| `session_root_path` | `string` | Relative directory root for the session contents. |
| `metadata` | `object` | Session metadata manifest descriptor; see table below. |
| `mcap` | `object` | Main MCAP recording descriptor; see table below. |

Each session `files.metadata` object contains the following fields:

| name | type | description |
| --- | --- | --- |
| `path` | `string` | Relative path to the session metadata JSON within the dataset. |
| `sha256` | `string` | Lowercase SHA-256 checksum for integrity verification. |
| `bytes` | `integer` | File size in bytes. |

Each session `files.mcap` object contains the following fields:

| name | type | description |
| --- | --- | --- |
| `path` | `string` | Relative path to the MCAP file containing the sensor streams. |
| `sha256` | `string` | Lowercase SHA-256 checksum for verifying the MCAP payload. |
| `bytes` | `integer` | File size in bytes. |

Each `ontology` object contains the following fields:

| name | type | description |
| --- | --- | --- |
| `path` | `string` | Relative path to the ontology JSON within the dataset. |
| `sha256` | `string` | Lowercase SHA-256 checksum for verifying the ontology payload. |
| `bytes` | `integer` | File size in bytes. |


### `ontology.json`

Ontology file containing information about the dataset.

### `/recordings`

Folder containing all the recordings, organized by participant.

### `/recordings/participant-...`

Folder containing all sessions for a participant.

### `/recordings/participant-.../session-...`

Folder containing all the files for a session.

### `/recordings/participant-.../session-.../session.mcap`

The MCAP session file, containing the following time-synchronized topics:

Sensors:
`/ml2/audio/mic`: Microphone audio
`/ml2/depth`: Depth image
`/ml2/head/pose`: Head pose
`/ml2/imu`: Inertial measurement unit
`/ml2/rgb/left`: Wide-FOV left RGB monochrome image
`/ml2/rgb/center`: Wide-FOV center RGB monochrome image
`/ml2/rgb/right`: Wide-FOV right RGB monochrome image
`/ml2/rgb/picture`: Picture RGB image

Annotations:
`/ml2/annotations/narrations`: Semantic narrations describing the actions being performed
`/ml2/hands/left`: Left hand 26-joint pose
`/ml2/hands/right`: Right hand 26-joint pose

### `/recordings/participant-.../session-.../metadata.json`

Metadata file containing information about the session. It contains the following fields:

| name | type | description |
| --- | --- | --- |
| `session_id` | `string` | Unique session identifier aligning with folder name and dataset manifest. |
| `capture_start_timestamp` | `string` (ISO-8601) | UTC timestamp when recording started. |
| `capture_end_timestamp` | `string` (ISO-8601) | UTC timestamp when recording finished. |
| `duration_s` | `number` | Session duration in seconds to millisecond precision. |
| `duration_ns` | `integer` | Session duration in nanoseconds for deterministic replay. |
| `files` | `object` | Session-local file manifest; see tables below. |
| `participant` | `object` | Embedded participant record for this capture; see table below. |
| `calibration` | `object` | Device calibration payload; see table below. |
| `coverage` | `object` | Reserved coverage or annotation summary; empty if not provided. |

The session `files` object contains the following fields:

| name | type | description |
| --- | --- | --- |
| `metadata` | `object` | Descriptor for the session metadata JSON; see table below. |
| `mcap` | `object` | Descriptor for the MCAP payload; see table below. |

The session `files.metadata` object contains the following fields:

| name | type | description |
| --- | --- | --- |
| `path` | `string` | Relative path to this metadata file within the session folder. |

The session `files.mcap` object contains the following fields:

| name | type | description |
| --- | --- | --- |
| `path` | `string` | Relative path to the MCAP file containing time-synchronized sensor streams. |
| `sha256` | `string` | Lowercase SHA-256 checksum for verifying the MCAP payload. |
| `bytes` | `integer` | File size in bytes. |

The session `participant` object contains the following fields:

| name | type | description |
| --- | --- | --- |
| `id` | `string` | Participant identifier repeated for convenience within the session manifest. |
| `demographics` | `object` | Participant attributes captured at recording time; see table below. |

The session `participant.demographics` object contains the following fields:

| name | type | description |
| --- | --- | --- |
| `dominant_hand` | `string` or `null` | Self-reported dominant hand (`left`, `right`, `ambidextrous`, or `null`) useful for handedness-aware analysis. |
| `height_cm` | `integer` or `null` | Participant height in centimeters for pose and reach normalization. Use null when the information is unavailable. |

The session `calibration` object contains the following fields:

| name | type | description |
| --- | --- | --- |
| `device` | `object` | Capture device descriptor; see table below. |

The session `calibration.device` object contains the following fields:

| name | type | description |
| --- | --- | --- |
| `name` | `string` | Device model name reported by capture hardware. |
| `id` | `string` | Device identifier or asset tag for traceability. |

