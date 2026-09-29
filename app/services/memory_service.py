return f"bookroom-live-v1-customer-{int(customer_id)}"import os

from hindsight_client import Hindsight


def get_memory_client():
    return Hindsight(
        base_url=os.environ["HINDSIGHT_API_URL"],
        api_key=os.environ["HINDSIGHT_API_KEY"],
    )


def customer_bank_id(customer_id):
    return f"bookroom-live-v1-customer-{int(customer_id)}"


def save_customer_memory(customer_id, text, event_id):
    bank_id = customer_bank_id(customer_id)

    with get_memory_client() as client:
        client.create_bank(
            bank_id=bank_id,
            name=f"Book Room Customer {int(customer_id)}",
        )

        client.retain(
            bank_id=bank_id,
            content=text,
            document_id=f"event-{event_id}",
        )


def recall_customer_memory(customer_id, query):
    with get_memory_client() as client:
        result = client.reflect(
            bank_id=customer_bank_id(customer_id),
            query=(
                f"{query}\n\n"
                "Summarize the customer's saved preferences. "
                "Combine repeated facts, even when worded differently. "
                "State each distinct preference only once. "
                "Write one short paragraph in plain text. "
"Do not use Markdown, asterisks, headings, or bullet points. "
"Only include preferences the customer actually stated. "
"Do not list missing or unknown preferences. "
                "Preserve exact budget limits and other constraints. "
                "Do not invent details. "
                "If no preferences are known, say so."
            ),
            budget="low",
        )

    text = result.text.strip()
    return [text] if text else []
