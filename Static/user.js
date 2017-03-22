function fixFormatting()
{
  languages = document.getElementsByClassName("languages");
  for (i = 0; i < languages.length; i++){
    userLangs = languages[i];
    langs = userLangs.innerHTML
    userLangs.innerHTML = langs.replace(/'|'/gi, '').replace('[', '').replace(']', '');
  }
}
