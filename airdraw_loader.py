"""
AIRDRAW AUTO-GENERATED FILE
This file dynamically loads DAGs created with Airdraw.
"""
import json
from pathlib import Path
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

import logging

# Enable debugging
logging.basicConfig(level=logging.INFO)

logging.info("Starting airdraw_loader.py")

# Path to airdraw's DAG definitions
AIRDRAW_DAGS_PATH = Path.home() / "airflow" / ".airdraw" / "dags"
logging.info(f"Looking for DAGs in: {AIRDRAW_DAGS_PATH}")

# Create path if it doesn't exist
# if not AIRDRAW_DAGS_PATH.exists():
#     logging.info(f"Creating directory: {AIRDRAW_DAGS_PATH}")
#     AIRDRAW_DAGS_PATH.mkdir(parents=True, exist_ok=True)

# Read all DAG definition files
json_files = list(AIRDRAW_DAGS_PATH.glob("*.json"))
logging.info(f"Found {len(json_files)} JSON file(s)")


# This logic should go in the Airdraw library eventually
for dag_file in json_files:
    logging.info(f"Processing: {dag_file.name}")

    try:
        with open(dag_file) as f:
            dag_config = json.load(f)

        logging.info(f"Loaded config for DAG: {dag_config.get('dag_id', 'UNKNOWN')}")
        
        # Create DAG from config
        with DAG(
            dag_id=dag_config['dag_id'],
            description=dag_config.get('description', 'Created by Airdraw'),
            schedule=dag_config.get('schedule'),
            start_date=datetime.strptime(dag_config['start_date'], '%Y-%m-%d'),
            catchup=dag_config.get('catchup', False),
            default_args=dag_config.get('default_args', {}),
            tags=dag_config.get('tags', ['airdraw']),
        ) as dag:
            
            # Create tasks from config
            tasks = {}
            for task_config in dag_config.get('tasks', []):
                if task_config['type'] == 'python':
                    task = PythonOperator(
                        task_id=task_config['task_id'],
                        python_callable=lambda: print(task_config.get('message', 'Hello from Airdraw')),
                    )
                elif task_config['type'] == 'bash':
                    task = BashOperator(
                        task_id=task_config['task_id'],
                        bash_command=task_config.get('command', 'echo "Hello from Airdraw"'),
                    )
                else:
                    continue
                
                tasks[task_config['task_id']] = task
            
            # Set up task dependencies
            for task_config in dag_config.get('tasks', []):
                if 'downstream' in task_config:
                    for downstream_id in task_config['downstream']:
                        tasks[task_config['task_id']] >> tasks[downstream_id]
        
        # Register DAG in globals
        globals()[dag_config['dag_id']] = dag
        logging.info(f"Successfully registered DAG: {dag_config['dag_id']}")
    except Exception as e:
        logging.error(f"ERROR processing {dag_file.name}: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())

logging.info("Finished loading Airdraw DAGs")