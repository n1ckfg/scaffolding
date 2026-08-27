# https://github.com/NousResearch/hermes-agent/issues/87093

curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash 
cd ~/.hermes/hermes-agent/
npm install 
cd ~/.hermes/hermes-agent/hermes_cli
uv run hermes doctor --fix 
hermes setup 

