FONT_NAME="JetBrainsMono"

echo "Instalando fontes..."

mkdir -p ~/.local/share/fonts \
  && curl -fLo "${HOME}/.local/share/fonts/${FONT_NAME}.zip" "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/${FONT_NAME}.zip" \
  && unzip $HOME/.local/share/fonts/$FONT_NAME.zip -d $HOME/.local/share/fonts \
  && find $HOME/.local/share/fonts/* -not -name "*.ttf" -delete

echo "instalando temas..."

git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
