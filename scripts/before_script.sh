touch ~/.ssh/id_rsa
echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa
echo -e "Host *\nStrictHostKeyChecking no\n" > ~/.ssh/config
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
chmod 700 ~/.ssh

