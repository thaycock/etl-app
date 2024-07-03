from flask import Blueprint, jsonify, request

from apihealth.src.health.api.services.handlers.etl_migration_handler import \
    ETLMigrationHandler

status_checks_bp = Blueprint("job_controller", __name__)


@status_checks_bp.route("/start-etl-job", methods=["GET"])
def start_etl_job() -> jsonify:
    """
    starts a etl job

    Returns:
        jsonify: job status
    """
    _etl_handler: object = ETLMigrationHandler()
    _etl_handler.start_data_migration_service()
    # TODO better handling can be done here, response can be generated based on the extraction and transformation
    # notifing the user if there was a failure to process the data
    return jsonify(
        {
            "success": True,
            "message": "Job has started",
        }
    )


@status_checks_bp.route("/latest-event-data", methods=["GET"])
def get_event_data() -> jsonify:
    """
    obtains all records in the db

    Returns:
        jsonify: result set
    """
    _etl_handler: object = ETLMigrationHandler()
    event_data = _etl_handler.get_latest_event_data()
    return jsonify(
        {
            "success": True,
            "data": event_data,
        }
    )
