# Guardrail Policy

## 1. Purpose

The Hospital Policy RAG Assistant is designed as a reference and retrieval system for a synthetic hospital policy corpus. To reduce hallucinations and unsupported answers, the system applies grounding and provenance guardrails during answer generation.

## 2. Citation-Required Policy

Every non-abstained answer must contain at least one clause-level citation.

Each citation identifies:

* Document ID
* Clause ID

The system enforces provenance programmatically. If an answer is generated without supporting citations, the response is converted into an abstention response rather than returning an unsupported answer.

## 3. Grounding Policy

The language model is instructed to answer using only the policy context retrieved from the corpus.

The system must not:

* Use external medical knowledge.
* Invent policy requirements.
* Invent responsible roles.
* Invent procedural steps.
* Infer unsupported details from general knowledge.

Only information supported by the retrieved policy context should appear in the answer.

## 4. Abstention Policy

The system abstains when the requested information cannot be supported by the available policy context.

The standard abstention response is:

> "I could not find this information in the provided hospital policies."

When abstaining:

* No unsupported answer is generated.
* No fabricated citation is provided.
* The `abstained` field is set to `true`.
* The citations list is empty.

Additionally, if a generated answer is not marked as abstained but contains no supporting citations, the system programmatically converts the response into an abstention.

## 5. Reference-Only Policy

The assistant is intended only as a policy reference tool.

Responses should be interpreted as references to the synthetic corpus and not as:

* Clinical advice
* Medical diagnosis
* Treatment recommendations
* Legal advice
* Autonomous decision-making

The system does not replace professional judgement or official hospital policy systems.

## 6. Out-of-Scope Handling

Questions are considered out of scope when they request information that is not contained in the synthetic hospital policy corpus.

Examples include:

* General medical knowledge not covered by the policies.
* Patient-specific diagnosis or treatment recommendations.
* Information from external hospital policies.
* Legal or regulatory interpretation beyond the provided corpus.

For out-of-scope questions, the system should abstain rather than answer using external knowledge.

## 7. Provenance Enforcement

Before returning a response, the system validates the following condition:

* Supported answer → at least one clause-level citation required.
* No supporting citation → abstain.

This ensures that answers returned by the system maintain traceability to the underlying policy corpus.

## 8. Guardrail Summary

| Guardrail              | Behavior                                                        |
| ---------------------- | --------------------------------------------------------------- |
| Citation Required      | Every supported answer requires clause-level provenance         |
| Grounding              | Answers use retrieved corpus context only                       |
| Abstention             | Unsupported questions return a safe abstention                  |
| Reference Only         | System is not a clinical or decision-making authority           |
| Out of Scope           | External or unsupported questions are abstained                 |
| Provenance Enforcement | Answers without citations are not returned as supported answers |
