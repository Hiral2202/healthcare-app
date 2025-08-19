from . import models, database
  # adjust if needed

# Drop all tables
models.Base.metadata.drop_all(bind=database.engine)
print("All tables dropped.")

# Recreate tables with updated schema (including patient_phone)
models.Base.metadata.create_all(bind=database.engine)
print("All tables created with updated schema.")
