import io


def test_predictions_endpoint(client):

    image = io.BytesIO(b"fake image")

    response = client.post(
        "/predictions",
        data={
            "threshold": "0.5",
            "file": (image, "test.jpg")
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 200


def test_invalid_threshold(client):

    image = io.BytesIO(b"fake image")

    response = client.post(
        "/predictions",
        data={
            "threshold": "abc",
            "file": (image, "test.jpg")
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400


def test_threshold_out_of_range(client):

    image = io.BytesIO(b"fake image")

    response = client.post(
        "/predictions",
        data={
            "threshold": "1.5",
            "file": (image, "test.jpg")
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400


def test_missing_file(client):

    response = client.post(
        "/predictions",
        data={
            "threshold": "0.5"
        }
    )

    assert response.status_code == 400
