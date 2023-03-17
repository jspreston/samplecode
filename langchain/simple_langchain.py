# COMMAND ----------
# python imports
import os
from typing import List, Optional

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import AzureOpenAI
import openai

from azure.identity import ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient

# COMMAND ----------
# settings
CLIENT_ID = "dd59d477-fe69-4637-8724-7fcfc30fcc8f"
KEY_VAULT_URL = "https://openai-casper-kv.vault.azure.net"
OPENAI_URL = "https://openai-casper.openai.azure.com/"
OPENAI_VERSION = "2022-06-01-preview"
OPENAI_KEY_NAME = "openai-key"
SERPAPI_KEY_NAME = "serpapi-key"
DEPLOYMENT_NAME = "gpt-35-turbo"
# DEPLOYMENT_NAME = "text-davinci-003"


# COMMAND ----------

class NewAzureOpenAI(AzureOpenAI):
    stop: Optional[List[str]] = None

    @property
    def _invocation_params(self):
        params = super()._invocation_params
        # fix InvalidRequestError: logprobs, best_of and echo parameters are not available on gpt-35-turbo model.
        unsupported_params_and_defaults = {
            "logprobs": None, "best_of": 1, "echo": False
        }
        if self.deployment_name == "gpt-35-turbo":
            for param, default in unsupported_params_and_defaults.items():
                if params.get(param, default) is not default:
                    raise ValueError(f"{param} is not available on gpt-35-turbo model.")
                params.pop(param, None)
        return params
    
# COMMAND ----------
credential = ManagedIdentityCredential(client_id=CLIENT_ID)
secret_client = SecretClient(
    vault_url=KEY_VAULT_URL, credential=credential
)
openai_key = secret_client.get_secret(OPENAI_KEY_NAME).value
serpapi_key = secret_client.get_secret(SERPAPI_KEY_NAME).value

openai.api_type = "azure"
openai.api_key = openai_key
openai.api_base = OPENAI_URL
openai.api_version = OPENAI_VERSION
# set the expected environment variables
os.environ["OPENAI_API_KEY"] = openai_key
os.environ["SERPAPI_API_KEY"] = serpapi_key

# COMMAND ----------
llm = NewAzureOpenAI(deployment_name=DEPLOYMENT_NAME, temperature=0)
tools = load_tools(["serpapi", "llm-math"], llm=llm)

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# COMMAND ----------
agent.run("Who is Leo DiCaprio's girlfriend? What is her current age raised to the 0.43 power?")
# COMMAND ----------
