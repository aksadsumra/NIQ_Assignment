import os

from counter.adapters.count_repo import CountMongoDBRepo, CountInMemoryRepo
from counter.adapters.object_detector import TFSObjectDetector, FakeObjectDetector
from counter.domain.actions import CountDetectedObjects
from counter.domain.actions import GetPredictions
from counter.adapters.postgres_repo import CountPostgresRepo

def dev_count_action() -> CountDetectedObjects:
    return CountDetectedObjects(FakeObjectDetector(), CountInMemoryRepo())


def prod_count_action() -> CountDetectedObjects:

    tfs_host = os.environ.get('TFS_HOST', 'localhost')
    tfs_port = os.environ.get('TFS_PORT', 8501)
    model_name = os.environ.get('MODEL_NAME', 'ssd_mobilenet_v2')

    repo_type = os.environ.get("REPO_TYPE", "mongo")

    if repo_type == "postgres":

        repo = CountPostgresRepo(
            host=os.environ.get("POSTGRES_HOST", "localhost"),
            port=os.environ.get("POSTGRES_PORT", 5432),
            database=os.environ.get("POSTGRES_DB", "counter"),
            user=os.environ.get("POSTGRES_USER", "postgres"),
            password=os.environ.get("POSTGRES_PASSWORD", "postgres")
        )

    else:

        mongo_host = os.environ.get('MONGO_HOST', 'localhost')
        mongo_port = os.environ.get('MONGO_PORT', 27017)
        mongo_db = os.environ.get('MONGO_DB', 'prod_counter')

        repo = CountMongoDBRepo(
            host=mongo_host,
            port=mongo_port,
            database=mongo_db
        )

    return CountDetectedObjects(
        TFSObjectDetector(
            tfs_host,
            tfs_port,
            model_name
        ),
        repo
    )


def get_count_action() -> CountDetectedObjects:
    env = os.environ.get('ENV', 'dev')
    count_action_fn = f"{env}_count_action"
    return globals()[count_action_fn]()


def get_prediction_action():

    env = os.environ.get("ENV", "dev")

    if env == "prod":

        tfs_host = os.environ.get("TFS_HOST", "localhost")
        tfs_port = os.environ.get("TFS_PORT", 8501)
        model_name = os.environ.get("MODEL_NAME", "ssd_mobilenet_v2")

        detector = TFSObjectDetector(
            tfs_host,
            tfs_port,
            model_name
        )

    else:

        detector = FakeObjectDetector()

    return GetPredictions(detector)
