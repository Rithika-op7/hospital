from src.generator import RAGGenerator

generator = RAGGenerator()

response = generator.generate(
    "What are the mandatory disposal protocols?"
)

print("\nANSWER:")
print(response.answer)

print("\nCITATIONS:")
for citation in response.citations:
    print(
        f"{citation.document_id} | "
        f"Clause: {citation.clause_id}"
    )

print("\nAPPLICABLE POLICY:")
print(response.applicable_policy)

print("\nSTEP SEQUENCE:")
if response.step_sequence:
    for i, step in enumerate(response.step_sequence, start=1):
        print(f"{i}. {step}")
else:
    print("None")

print("\nRESPONSIBLE ROLE:")
print(response.responsible_role)

print("\nCONFIDENCE:")
print(response.confidence)

print("\nABSTAINED:")
print(response.abstained)