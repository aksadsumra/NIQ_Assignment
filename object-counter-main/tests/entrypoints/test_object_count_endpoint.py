def test_object_count_invalid_threshold(client):

    image = io.BytesIO(b"fake image")

    response = client.post(
        "/object-count",
        data={
            "threshold": "abc",
            "file": (image, "test.jpg")
        },
        content_type="multipart/form-data"
    )

    assert response.status_code == 400
