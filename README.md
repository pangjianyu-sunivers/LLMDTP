# LLMDTP
*** Because we need two python version for the environment, so we should build the environment from the scratch ***
Follow steps 1 to 4 below to set up the Python environment on a server. The server must have at least one GPU with 40GB GPU memory to run the example model Baichuan2-13B-chat. The framework and knowledge base used in this solution are consistent with our RCT, but the model used is not the one we have trained with LoRA. (Due to Chinese regulations, we cannot provide the trained LoRA weights.)


# model download
# Please download the distiluse-base-multilingual-cased-v1 model from https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v1 and put it in the same folder of Readme.md

# step 1
# Please install the environment first with conda by running the following code in the terminal, and enter the environment

conda create -n glm4 python=3.9.13 -y 

conda activate glm4 

pip install zhipuai requests flask 

conda create -n embedding python=3.10 -y 

conda activate embedding 

# step 2
# And install the following packets

pip install chromadb streamlit flask sentence_transformers requests fastapi uvicorn transformers gtts pydub pygtrans pydantic-settings

# step 3
# We use the glm4 as an example of our demo, start the api service fisrt
# Move to the same location of README.md, run the following code

conda activate glm4

cd to_NBE

nohup python CHATZOC_glm4_jump_api.py &

# step 4
# Now we gonna open our system, run the following code

conda activate embedding

cd demo_NBE

nohup python teaching_api.py &

nohup streamlit run SP_choose.py &
