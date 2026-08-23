from langchain_aws import ChatBedrockConverse

from app.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_SESSION_TOKEN,
    AWS_REGION,
    BEDROCK_MODEL_ID,
)


llm = ChatBedrockConverse(
    model_id=BEDROCK_MODEL_ID,
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    temperature=0,
)
