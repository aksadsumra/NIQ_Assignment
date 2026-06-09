# Multi-Model Support Design

## Overview

The current implementation supports a single object detection model configured through the `MODEL_NAME` environment variable and served through TensorFlow Serving.

While this approach works well for a single model, future business requirements may require supporting multiple object detection models simultaneously. Examples include using different models for accuracy, performance, or domain-specific use cases.

This document describes the architectural changes required to support multiple internal models while preserving the existing Hexagonal Architecture.

---

# Current Architecture

The current architecture uses a single detector implementation:

```text
Client Request
      │
      ▼
CountDetectedObjects
      │
      ▼
ObjectDetector
      │
      ▼
TFSObjectDetector
      │
      ▼
TensorFlow Serving
      │
      ▼
SSD MobileNet V2
```

The model is selected through configuration and cannot be changed dynamically.

---

# Proposed Architecture

Introduce a detector factory responsible for selecting the appropriate model implementation.

```text
Client Request
      │
      ▼
CountDetectedObjects
      │
      ▼
ObjectDetector
      │
      ▼
DetectorFactory
      │
 ┌────┼─────────┐
 ▼    ▼         ▼

SSD  YOLO   RetinaNet
```

Each model implementation continues to satisfy the existing `ObjectDetector` interface.

This allows the domain layer to remain unchanged.

---

# Model Selection

The model can be selected using either:

## Option 1: Request Parameter

Example:

```http
POST /object-count?model=yolo
```

or

```http
POST /predictions?model=retinanet
```

The API layer extracts the model name and requests the appropriate detector from the factory.

---

## Option 2: Environment Configuration

Example:

```text
MODEL_NAME=ssd
```

This approach maintains current behavior while allowing easy model switching.

---

# Detector Factory

A detector factory would be responsible for constructing the correct detector implementation.

Example:

```python
class DetectorFactory:

    @staticmethod
    def create(model_name):

        if model_name == "ssd":
            return SSDDetector()

        if model_name == "yolo":
            return YOLODetector()

        if model_name == "retinanet":
            return RetinaNetDetector()

        raise ValueError("Unsupported model")
```

This keeps model-selection logic isolated from business logic.

---

# Supporting Multiple Serving Frameworks

Different models may be deployed using different serving technologies.

Examples:

| Model         | Serving Framework   |
| ------------- | ------------------- |
| SSD MobileNet | TensorFlow Serving  |
| YOLO          | TorchServe          |
| RetinaNet     | TensorFlow Serving  |
| Custom Model  | Custom REST Service |

The factory can select both the model and the appropriate serving adapter.

---

# Model Registry

To avoid hardcoding model endpoints, a model registry can be introduced.

Example:

```python
MODEL_REGISTRY = {
    "ssd": "http://tf-serving:8501",
    "yolo": "http://torchserve:8080",
    "retinanet": "http://tf-serving:8501"
}
```

The detector retrieves the correct endpoint from the registry.

---

# Benefits

The proposed design provides several advantages:

* Supports multiple object detection models
* Preserves existing Hexagonal Architecture
* Keeps domain logic unchanged
* Simplifies model experimentation
* Enables gradual model migration
* Supports different serving technologies
* Improves scalability for future requirements

---

# Conclusion

The current architecture already provides a strong foundation through the `ObjectDetector` abstraction. By introducing a detector factory and model registry, the system can support multiple internal object detection models without modifying the domain layer. This approach maintains clean architectural boundaries while allowing future expansion of the object detection platform.
