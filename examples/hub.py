import os

from fastapi import FastAPI
from forge import *


app = FastAPI()

# Database connection setup
db_client = DbClient(
    config=DbConfig(
        db_type=os.getenv("DB_TYPE", "postgresql"),
        driver_type=os.getenv("DRIVER_TYPE", "sync"),
        database=os.getenv("DB_NAME", "a_hub"),
        user=os.environ.get("DB_OWNER_ADMIN") or "a_hub_admin",
        password=os.environ.get("DB_OWNER_PWORD") or "password",
        host=os.environ.get("DB_HOST") or "localhost",
        port=int(os.getenv("DB_PORT", 5432)),
        echo=False,
        pool_config=PoolConfig(
            pool_size=5, max_overflow=10, pool_timeout=30, pool_pre_ping=True
        ),
    )
)
db_client.test_connection()
db_client.log_metadata_stats()

# Create the model manager to organize database objects
model_manager = ModelManager(
    db_client=db_client,
    include_schemas=[
        # Default schemas
        "public",
        "account",
        "auth",
        # A-Hub schemas
        "agnostic",
        "infrastruct",
        "hr",
        "academic",
        "course_offer",
        "student",
        "library",
    ],
)

# Display database statistics
model_manager.log_metadata_stats()

# Initialize API generator
api_forge = ApiForge(
    config=ForgeConfig(
        project_name="API Test",
        version="0.1.0",
    ),
    app=app,
)

# Generate metadata routes
api_forge.gen_metadata_routes(model_manager)
# api_forge.gen_health_routes(model_manager)
api_forge.gen_table_routes(model_manager)
api_forge.gen_view_routes(model_manager)
api_forge.gen_fn_routes(model_manager)
