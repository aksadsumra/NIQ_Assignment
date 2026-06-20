# NIQ Innovation Enablement - Object Counter Challenge

## Overview

This project demonstrates the application of Hexagonal Architecture (Ports & Adapters) in a Machine Learning-based object detection system.

The application exposes a Flask API that accepts an image and a confidence threshold, performs object detection, and returns either:

* Object counts grouped by class (`/object-count`)
* Individual predictions above a threshold (`/predictions`)

## Architecture

The application is composed of three layers:

### Entrypoints

Responsible for:

* Exposing HTTP APIs
* Receiving requests
* Validating input
* Returning responses

### Adapters

Responsible for communication with external services:

* TensorFlow Serving
* MongoDB
* PostgreSQL
* In-memory repositories

Adapters translate domain objects to external service representations and vice versa.

### Domain

Contains:

* Business logic
* Use cases
* Domain models
* Ports (interfaces)

The domain layer remains independent of infrastructure concerns.

## Assignment Deliverables

The following tasks were completed:

### Task 1 – Predictions Endpoint

Added a new endpoint:

```text
POST /predictions
```

Returns a list of predictions above the specified threshold including:

* Class name
* Confidence score
* Bounding box

### Task 2 – PostgreSQL Adapter

Implemented a new relational database adapter:

```text
CountPostgresRepo
```

following the existing Hexagonal Architecture pattern.

### Task 3 – Improvements Proposal

Added:

```text
IMPROVEMENTS.md
```

containing recommendations for:

* Validation
* Logging
* Error handling
* Testing
* Configuration management
* Database migrations

### Task 4 – Implemented Improvement

Implemented request validation:

* Threshold must be numeric
* Threshold must be between 0 and 1
* File upload is required
* Invalid requests return HTTP 400

### Task 5 – Multi-Model Design

Added:

```text
MULTI_MODEL_DESIGN.md
```

describing support for multiple internally trained models using:

* Model Registry
* Detector Factory
* Dynamic model selection

### Task 6 – Testing Enhancements

Added tests covering:

* Predictions endpoint
* Invalid threshold values
* Threshold range validation
* Missing file handling

## Model Setup

### Unix

```bash
mkdir -p tmp/model/ssd_mobilenet_v2/1

curl -L -o tmp/model.tar.gz \
http://download.tensorflow.org/models/object_detection/ssd_mobilenet_v2_coco_2018_03_29.tar.gz

tar -xzvf tmp/model.tar.gz -C tmp/model

mv \
tmp/model/ssd_mobilenet_v2_coco_2018_03_29/saved_model/saved_model.pb \
tmp/model/ssd_mobilenet_v2/1

chmod -R 777 tmp/model

rm tmp/model.tar.gz

rm -rf tmp/model/ssd_mobilenet_v2_coco_2018_03_29
```

Expected structure:

```text
tmp/
└── model/
    └── ssd_mobilenet_v2/
        └── 1/
            └── saved_model.pb
```

## TensorFlow Serving

### Unix

```bash
num_physical_cores=$(lscpu --all --parse=SOCKET,CORE | grep -v '^#' | uniq | wc -l)

docker run --rm -d \
--name=tfserving \
-p 8501:8501 \
--mount type=bind,source=$(pwd)/tmp/model,target=/models \
-e OMP_NUM_THREADS=$num_physical_cores \
-e TENSORFLOW_INTRA_OP_PARALLELISM=$num_physical_cores \
-e MODEL_NAME=ssd_mobilenet_v2 \
tensorflow/serving
```

### Windows PowerShell

```powershell
$num_physical_cores=(Get-WmiObject Win32_Processor | Select-Object NumberOfCores).NumberOfCores

docker run --rm -d `
--name=tfserving `
-p 8501:8501 `
-v "$pwd\tmp\model:/models" `
-e OMP_NUM_THREADS=$num_physical_cores `
-e TENSORFLOW_INTRA_OP_PARALLELISM=$num_physical_cores `
-e MODEL_NAME=ssd_mobilenet_v2 `
tensorflow/serving
```

## MongoDB Setup

```bash
docker run --rm --name test-mongo -p 27017:27017 -d mongo:latest
```

## Python Environment Setup

### Requirements

* Python 3.10+
* Docker

### Unix

```bash
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

export PYTHONPATH=.
```

### Windows PowerShell

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1

pip install -r requirements.txt

$Env:PYTHONPATH="."
```

## Running the Application

### Using Fake Services (Development)

```bash
python -m counter.entrypoints.webapp
```

### Using Real Services

#### Unix

```bash
ENV=prod python -m counter.entrypoints.webapp
```

#### Windows PowerShell

```powershell
$env:ENV="prod"

python -m counter.entrypoints.webapp
```

Application runs on:

```text
http://127.0.0.1:5000
```

## API Usage

### Object Count Endpoint

```http
POST /object-count
```

Example:

```bash
curl -F "threshold=0.9" \
     -F "file=@resources/images/boy.jpg" \
     http://localhost:5000/object-count
```

### Predictions Endpoint

```http
POST /predictions
```

Example:

```bash
curl -F "threshold=0.5" \
     -F "file=@resources/images/boy.jpg" \
     http://localhost:5000/predictions
```

Response Example:

```json
[
  {
    "class_name": "cat",
    "score": 0.999,
    "box": {
      "xmin": 0.36,
      "ymin": 0.27,
      "xmax": 0.73,
      "ymax": 0.69
    }
  }
]
```

## Validation Rules

The API validates:

### Threshold

* Must be numeric
* Must be between 0 and 1

Examples:

```text
0.5   ✓
0.9   ✓
abc   ✗
1.5   ✗
```

### File Upload

A file must be provided in the request.

Invalid requests return:

```http
400 Bad Request
```

## Running Tests

Run all tests:

```bash
pytest
```

or

```bash
py -m pytest
```

Expected result:

```text
10 passed
```

## Documentation

Additional documentation included:

```text
IMPROVEMENTS.md
MULTI_MODEL_DESIGN.md
```

## Notes

If you experience connectivity issues on Windows, replace:

```text
localhost
```

with:

```text
127.0.0.1
```

for all API requests.
