function loadHome(){
  window.location = "/";
}
function fixFormatting()
{
  languages = document.getElementsByClassName("languages");
  for (i = 0; i < languages.length; i++){
    userLangs = languages[i];
    langs = userLangs.innerHTML
    userLangs.innerHTML = langs.replace(/'|'/gi, '').replace('[', '').replace(']', '');
  }
}
function getUser(row)
{
  cell = row.cells;
  name = cell[0].innerHTML;
  console.log(name);
  window.location = "/userinfo/" + name +"/"+row.rowIndex;
}
