import psycopg2

from counter.domain.ports import ObjectCountRepo
from counter.domain.models import ObjectCount


class CountPostgresRepo(ObjectCountRepo):

    def __init__(
            self,
            host,
            port,
            database,
            user,
            password):

        self.conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password
        )

    def read_values(self, object_classes=None):

        cursor = self.conn.cursor()

        if object_classes:

            cursor.execute(
                """
                SELECT object_class, count
                FROM object_counts
                WHERE object_class = ANY(%s)
                """,
                (object_classes,)
            )

        else:

            cursor.execute(
                """
                SELECT object_class, count
                FROM object_counts
                """
            )

        rows = cursor.fetchall()

        return [
            ObjectCount(
                object_class=row[0],
                count=row[1]
            )
            for row in rows
        ]

    def update_values(self, values):

        cursor = self.conn.cursor()

        for value in values:

            cursor.execute(
                """
                INSERT INTO object_counts
                (object_class, count)
                VALUES (%s, %s)

                ON CONFLICT (object_class)
                DO UPDATE SET
                count = object_counts.count + EXCLUDED.count
                """,
                (
                    value.object_class,
                    value.count
                )
            )

        self.conn.commit()
