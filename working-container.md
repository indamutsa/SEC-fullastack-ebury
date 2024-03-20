Let us start by provisioning a working container so that we don't have to install any software on our local machine.

```bash

# Run a working container
docker run -it --rm --net host --name working-container \
-v /var/run/docker.sock:/var/run/docker.sock \
-v ${PWD}:/work \
-w /work alpine:3.19.1 sh

```

```bash
mkdir -p /cmd
```

Install common utilities

```bash
# Install common utilities and beautify the terminal
apk update
apk add --no-cache docker curl wget python3 py3-pip python3-dev libffi-dev openssl-dev gcc libc-dev make  zip bash openssl git mongodb-tools openssl git docker-compose zsh vim nano bash unzip npm openjdk17 openssh
# Install zsh for a cool looking terminal with plugins auto-suggestions and syntax-highlighting
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

## Clone the zsh-autosuggestions repository into $ZSH_CUSTOM/plugins
git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
sed -i.bak 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting)/' ~/.zshrc

# Install kubectl
curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/arm64/kubectl
chmod +x ./kubectl
mv ./kubectl /usr/local/bin/kubectl

# Install helm
curl -LO https://get.helm.sh/helm-v3.7.2-linux-arm64.tar.gz
tar -C /tmp/ -zxvf helm-v3.7.2-linux-arm64.tar.gz
rm helm-v3.7.2-linux-arm64.tar.gz
mv /tmp/linux-arm64/helm /usr/local/bin/helm
chmod +x /usr/local/bin/helm

# Get Terraform
wget https://releases.hashicorp.com/terraform/1.6.1/terraform_1.6.1_linux_arm64.zip
unzip terraform_1.6.1_linux_arm64.zip
mv terraform /usr/local/bin/
chmod +x /usr/local/bin/terraform
rm terraform_1.6.1_linux_arm64.zip
terraform version


# Install kind to access the cluster
wget https://github.com/kubernetes-sigs/kind/releases/download/v0.11.1/kind-linux-arm64
chmod +x kind-linux-arm64
mv kind-linux-arm64 /usr/local/bin/kind
kind version

# 4. Install ArgoCD CLI

wget argocd-linux-arm64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-arm64
install -m 555 argocd-linux-arm64 /usr/bin/argocd
rm argocd-linux-arm64

# 5. Install AWS CLI
python -m venv pyenv
source pyenv/bin/activate
pip install awscli==1.32.63

# Install nvm
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

Deleting in linux is a dangerous operation, let us create a script to confirm before deleting

```bash
cat << 'EOF' > /cmd/confirm_rm_rf.sh
#!/bin/sh
printf "Do you really wanna delete (yes/no) \n===>: "
# Reading the input from terminal
read answer
if [ $answer == "yes" ]
then
  rm -rf $@
elif [ "$answer" !=  "yes" ]
then
  printf "You didn't confirm!\nExiting, no action taken!"
fi
EOF
chmod +x /cmd/confirm_rm_rf.sh
cat /cmd/confirm_rm_rf.sh


# ---
cat << 'EOF' >> ~/.zshrc
source $ZSH/oh-my-zsh.sh
source $ZSH_CUSTOM/plugins/zsh-autosuggestions
source $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
export PATH="$PATH:/cmd"
alias rm="confirm_rm_rf.sh"
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
EOF
cat ~/.zshrc

# To apply the changes, the auto-suggestions and syntax-highlighting plugins must be sourced:
source ~/.zshrc
chown -R 1000:1000 .
chown -R 1000:1000 /opt
zsh
```
