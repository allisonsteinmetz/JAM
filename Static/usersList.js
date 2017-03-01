function loadHome(){
  window.location = "/";
}
function fixFormatting()
{
  scores = document.getElementsByClassName("contributionScore");
  for (i = 0; i < scores.length; i++){
    scores[i].innerHTML = (((scores[i].innerHTML) * 100).toFixed(2)) + '%';
  }
  languages = document.getElementsByClassName("languages");
  for (i = 0; i < languages.length; i++){
    userLangs = languages[i];
    langs = userLangs.innerHTML
    userLangs.innerHTML = langs.replace(/'|'/gi, '').replace('[', '').replace(']', '');
  }
}
function getUser(row)
{
  console.log(row);
  cell = row.cells;
  name = cell[0].innerHTML;
  console.log(name);
  window.location = "/userinfo/" + name;
}
