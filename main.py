from llm_velocity import LLMLookUpStore
from llm_velocity.models import models
from typing import Any
import time


####################### Init ##################################
def validate_account_id(value: Any) -> str | None:
    if value is None or not str(value).strip():
        return "Please provide your account ID."

    return None


def validate_amount(value: Any) -> str | None:
    if value is None or not str(value).strip():
        return "Please enter the amount you want to transfer."

    try:
        amount = float(value)
    except (TypeError, ValueError):
        return "Please enter a valid amount, such as 500."

    if amount <= 0:
        return "The transfer amount must be greater than 0."

    if amount > 20_000:
        return "The maximum transfer amount is ₹20,000."

    return None


def validate_limit(value: Any) -> str | None:
    if value is None or not str(value).strip():
        return "Please provide a limit between 1 and 30."

    try:
        limit = int(value)
    except (TypeError, ValueError):
        return "Please enter a whole number for the limit."

    if limit <= 0:
        return "The limit must be greater than 0."

    if limit > 30:
        return "The maximum limit is 30."

    return None


tools_definition: dict[str, models.ToolInfo] =  {
    "get_account_balance": models.ToolInfo(
        name="get_account_balance",
        description="Get the current balance of a bank account.",
        parameters=[
            models.ToolParameters(
                name="account_id",
                description="The unique ID of the bank account.",
                validationCallback=validate_account_id,
            ),
        ],
    ),

    "transfer_money": models.ToolInfo(
        name="transfer_money",
        description="Transfer money from one bank account to another.",
        parameters=[
            models.ToolParameters(
                name="from_account",
                description="The account to transfer money from.",
                validationCallback=validate_account_id,
            ),
            models.ToolParameters(
                name="to_account",
                description="The account to transfer money to.",
                validationCallback=validate_account_id,
            ),
            models.ToolParameters(
                name="amount",
                description="The amount to transfer. Maximum allowed is 20,000.",
                validationCallback=validate_amount,
            ),
        ],
    ),

    "get_transaction_history": models.ToolInfo(
        name="get_transaction_history",
        description="Get transaction history for a bank account.",
        parameters=[
            models.ToolParameters(
                name="account_id",
                description="The unique ID of the bank account.",
                validationCallback=validate_account_id,
            ),
            models.ToolParameters(
                name="limit",
                description="Number of transactions to return. Maximum is 30.",
                validationCallback=validate_limit,
            ),
        ],
    ),
}

luStore = LLMLookUpStore("gemma2:2b","http://localhost:11434", tools_definition)

luStore.init_setup()

########################### Input ##################################
userContext: list[models.UserChatReq] =  [
    models.UserChatReq(user_message="check my bank balance", llm_response="Please provide your account id"),
    models.UserChatReq(user_message="123456abc"),
    models.UserChatReq(user_message="I want to transfer money", llm_response="Please provide your account ID.\nPlease provide your account ID.\nPlease enter the amount you want to transfer."),
    models.UserChatReq(user_message="transfer money from xya to 123 ", llm_response="Please enter the amount you want to transfer."),
    models.UserChatReq(user_message="2201"),
    models.UserChatReq(user_message="give me my transactions list"),
    models.UserChatReq(user_message="hahah")
]
 


start_time = int(time.time())
res = luStore.call(userContext, True)
end_time = int(time.time())
print("response", res)
print("total time taken", end_time -  start_time)