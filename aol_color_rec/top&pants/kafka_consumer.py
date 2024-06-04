from kafka import KafkaConsumer
import json
import sqlite3

def consume_from_kafka(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    conn = sqlite3.connect('/local/workspace/tappas/apps/h8/gstreamer/general/instance_segmentation/detections.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT,
            confidence REAL,
            x_min INTEGER,
            y_min INTEGER,
            x_max INTEGER,
            y_max INTEGER,
            mask_shape INTEGER,
            color TEXT
        )
    ''')
    conn.commit()

    for message in consumer:
        data = message.value
        cursor.execute('''
            INSERT INTO detections (label, confidence, x_min, y_min, x_max, y_max, mask_shape, color)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['label'], data['confidence'], data['bbox']['x_min'], data['bbox']['y_min'], data['bbox']['x_max'], data['bbox']['y_max'], (data['mask_shape']), data['color']))
        conn.commit()

    conn.close()


