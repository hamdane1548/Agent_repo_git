import time
import random
from loguru import logger
def invoke_with_retry(model, message, max_attempts=5):
    for attempt in range(max_attempts):
        try:
            return model.invoke(message)

        except Exception as e:
            if "429" not in str(e):
                raise

            if attempt == max_attempts - 1:
                raise

            wait_time = (2 ** attempt) + random.uniform(0, 1)

            logger.warning(
                f"Mistral rate limit (429). "
                f"Retry {attempt + 1}/{max_attempts} "
                f"in {wait_time:.2f}s"
            )

            time.sleep(wait_time)