# Synthetic Data and PII Policy

## Data Source

All documents used in this project are synthetic and were created solely for the purpose of evaluating the Hospital Policy RAG Assistant.

The corpus includes synthetic:

* Hospital operational policies
* Infection control SOPs
* Patient safety protocols
* Consent procedures
* Healthcare compliance manuals

## Personally Identifiable Information (PII)

No real patient data, employee data, or personally identifiable information is included in the project dataset.

Any names, roles, identifiers, phone extensions, or scenarios appearing in the synthetic policies are fictional and used only to simulate realistic hospital documentation.

## Logging Policy

The system implements basic logging for development and evaluation purposes.

The dataset and evaluation queries are synthetic. In a real-world deployment, patient information, personally identifiable information, or protected health information must not be written to logs in plaintext.

## Data Handling

* All committed data is synthetic.
* No real hospital records are used.
* No API keys or secrets are committed.
* Environment variables are used for sensitive configuration.
* Logs are excluded from version control.

This policy ensures that the project can be safely shared and evaluated without exposing real patient or organizational data.
