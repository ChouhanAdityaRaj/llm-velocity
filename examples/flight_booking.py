from llm_velocity import VelocityEngine
from llm_velocity.models import models
from typing import Any
import time

####################### Init ##################################

# Validation callbacks
def validate_from_location(value: Any) -> str | None:
    if value is None or not str(value).strip():
        return "Please provide your where you flying from."

    availableFlightLocation = ["USA", "India", "japan"]
    if value not in availableFlightLocation:
        return f"Please provide valid departure location, we only provide flight from {', '.join(availableFlightLocation)}."

    return None


def validate_to_location(value: Any) -> str | None:
    if value is None or not str(value).strip():
        return "Please provide your where you flying to."

    availableFlightLocation = ["China", "Africa"]
    if value not in availableFlightLocation:
        return f"Please provide valid destination location, we only provide flight to {', '.join(availableFlightLocation)}."

    return None


def validate_data(value: Any) -> str | None:
    if value is None or not str(value).strip():
        return "Please provide booking date."

    return None


def validate_flight_id(value: Any) -> str | None:
    if value is None or not str(value).strip():
        return "Please provide flight id."

    return None


def validate_passenger_name(value: Any) -> str | None:
    if value is None or not str(value).strip():
        return "Please provide your name."

    return None


def validate_booking_id(value: Any) -> str | None:
    if value is None or not str(value).strip():
        return "Please provide your booking id."

    return None


# 
tools_definition: dict[str, models.ToolInfo] = {
    "search_flights": models.ToolInfo(
        name="search_flights",
        description="Search for available flights.",
        parameters=[
            models.ToolParameters(
                name="from_location",
                description="The departure city or airport.",
                validationCallback=validate_from_location,
            ),
            models.ToolParameters(
                name="to_location",
                description="The destination city or airport",
                validationCallback=validate_to_location
            ),
            models.ToolParameters(
                name="date",
                description="The date of travel.",
                validationCallback=validate_data,
            ),
        ],
    ),
    "get_flight_details": models.ToolInfo(
        name="get_flight_details",
        description="Get detailed information about a specific flight.",
        parameters=[
            models.ToolParameters(
                name="flight_id",
                description="A unique identifier of flight",
                validationCallback=validate_flight_id,
            ),
        ],

    ),
    "book_flight": models.ToolInfo(
        name="book_flight",
        description="Book a specific flight for a passenger.",
        parameters=[
            models.ToolParameters(
                name="flight_id",
                description="The unique ID of the flight to book.",
                validationCallback=validate_flight_id,
            ),
            models.ToolParameters(
                name="passenger_name",
                description="The full name of the passenger.",
                validationCallback=validate_passenger_name,
            ),
        ],
    ),
    "get_booking_details": models.ToolInfo(
        name="get_booking_details",
        description="Retrieve the details of an existing flight booking.",
        parameters=[
            models.ToolParameters(
                name="booking_id",
                description="The unique ID of the flight booking.",
                validationCallback=validate_booking_id,
            ),
        ],
    ),
}

luStore = VelocityEngine(
    llm_provider=models.LLMProvider.GEMINI.value,
    llm_model="gemini-3.6-flash",
    endpoint_url="",
    tools_definition=tools_definition,
    api_key=""
)

try:
    luStore.init_setup()
except Exception as e:
    print(e)

########################### Input ##################################
# list flight
# userContext: list[models.UserChatReq] =  [
#     models.UserChatReq(
#         user_message="give me available flight options from japan to canada",
#         llm_response="Please provide valid destination location, we only provide flight to China, Africa.\nPlease provide booking date."
#     ),
#     models.UserChatReq(
#         user_message="my destination is Africa",
#         llm_response="Please provide booking date."
#     ),
#     models.UserChatReq(
#         user_message="2 dec 2026",
#     ),
# ]

# userContext: list[models.UserChatReq] = [
#     models.UserChatReq(
#         user_message="find flights from UK to Africa",
#         llm_response=(
#             "Please provide valid departure location, we only provide flight from USA, India, japan.\nPlease provide booking date."
#         )
#     ),
#     models.UserChatReq(
#         user_message="I am flying from japan",
#         llm_response="Please provide booking date."
#     ),
#     models.UserChatReq(
#         user_message="December 2nd 2026",
#         llm_response="{from_location': 'japan', 'to_location': 'Africa', 'date': '2026-12-02'}"
#     ),
# ]

# userContext: list[models.UserChatReq] = [
#     models.UserChatReq(
#         user_message="find flights to Africa",
#         llm_response=(
#             "Please provide your where you flying from.\nPlease provide booking date."
#         )
#     ),
#     models.UserChatReq(
#         user_message="from USA",
#         llm_response="Please provide booking date."
#     ),
#     models.UserChatReq(
#         user_message="December 10 2026",
#         llm_response="{from_location': 'USA', 'to_location': 'Africa', 'date': '2026-12-10'}"
#     ),
#         models.UserChatReq(
#         user_message="I want to see the flight details",
#         llm_response="Please provide flight id."
#     ),
#     models.UserChatReq(
#         user_message="The flight id is AI203",
#         llm_response="{'flight_id': 'AI203'}"
#     ),
#     models.UserChatReq(
#         user_message="book flight AI203",
#         llm_response="Please provide your name."
#     ),
#     models.UserChatReq(
#         user_message="My name is Aditya Raj Singh Chouhan"
#     ),
# ]

userContext: list[models.UserChatReq] = [
    models.UserChatReq(
        user_message="book a flight for Aditya Sharma",
        # llm_response="Please provide flight id."
    ),
    # models.UserChatReq(
    #     user_message="Book flight AI203"
    # ),
]


try:
    start_time = int(time.time())
    res = luStore.call(userContext, True)
    end_time = int(time.time())
    print("response", res)
    print("total time taken", end_time -  start_time)
except Exception as e:
    print(e)



